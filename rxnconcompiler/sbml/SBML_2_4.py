from rxnconcompiler.SBGN.PD import ReducedProcessDescription
from rxnconcompiler.rxncon import Rxncon
from rxnconcompiler.util.rxncon_errors import RxnconRateError
import os
from libsbml import *
# libsbml import always marked as unused and (some of) the depending methods as unresolved but work as intended when run
#TODO import only needed packages (when its clear which are needed)


# for each rxncon model there has to be another instance of SBMLBuilder, otherwise all information of the first model will be stored in the second sbml
class SBMLBuilder(object):

    def __init__(self, level = 2, version = 4):
        # creates a SBML document of given level and version, default is 2.4 because of Celldesigner specs
        try:
            self.namespace = SBMLNamespaces(level, version)
            self.document = SBMLDocument(self.namespace)
        except ValueError:
            raise SystemExit("SBML Document creation failed")
        self.model = self.document.createModel()

    def process_complex_id(self, complex):
        # generates the species id for complexes with one or more molecules consisting of "s_m[id of molecule]_m..."
        compId = "s"
        for mol in complex.molecules:
             compId = compId + "_m" + str(mol._id)

        return compId

    def species_set_SBML_defaults(self, species):
        #optional set species.setSpeciesType()      # optional attribute
        species.setCompartment('cell')                # Compartment is set to default comp cell, has to be changed if compartments are added to rxncon
        species.setInitialAmount(100)               # Default set to 100
        #species.setInitialConcentration()
        #species.setSubstanceUnits('mole')          #there are no units in rxncon
        #species.setHasOnlySubstanceUnits(False)
        #species.setBoundaryCondition(False)
        #species.setConstant(False)

    def process_node(self, visitId):
        # takes an unvisited node and creates species out of it
        # optional values are commented out until an according rxncon variable is found
        # TODO only minimal necessary information is set, mostly defaults

        species = self.model.createSpecies()
        node = self.tree.get_node(visitId)

        species.setId( self.process_complex_id(node.node_object) )
        species.setName(str(node.name))
        self.species_set_SBML_defaults(species)

    def process_reaction(self, rxnconReactions):
        # gets a list of tuple (reaction, edge.id)  and processes stored information

        reaction = self.model.createReaction()
        id = 'r' + str(rxnconReactions[0][0].rid)   # id is a string "r[rid]" where rid is the number from the rxncon-reaction
        reaction.setId(id)

        #creates a name out of the unique reaction names that are part of this reaction
        names = set()
        for reactionTuple in rxnconReactions:
            names.add(reactionTuple[0].name)
        names = list(names)
        reaction.setName(";".join(names))

        reaction.setReversible(rxnconReactions[0][0].definition["Reversibility"] == "reversible")  # sets a bool according to Reversibility, True for reversible False for irreversible
        #reaction.setFast()
        #reaction.setSBOTerm()
        if(self.namespace.getLevel >=3):
            reaction.setCompartment('cell')                          # Reaction_Compartment exists not before SBML L3V1

        #adds SpeciesReferences to the reaction and gives back a tupel of (reactantList, prodList, rxncon-reaction.rid)
        [self.add_references(id, reactionTuple[1]) for reactionTuple in rxnconReactions]

        self.compute_KineticLaw(id, rxnconReactions)

    def set_reference(self, reaction, reactant, is_substrate):
        # sets the reactant/product/modifier references for the given reaction

        if not reactant._BiologicalComplex__is_modifier:
            if is_substrate:
                reactRef = reaction.createReactant()
                reactRef.setSpecies(self.process_complex_id(reactant))
            else:
                prodRef =  reaction.createProduct()
                prodRef.setSpecies(self.process_complex_id(reactant))
        else:
            modRef = reaction.createModifier()
            modRef.setSpecies(self.process_complex_id(reactant))

    def add_references(self, id, edge_id):
        # adds new reactants to an reaction

        reaction = self.model.getReaction(id)

        substrate = self.tree.get_node(edge_id[0]).node_object
        if reaction.getReactant(self.process_complex_id(substrate)) is None and reaction.getModifier(self.process_complex_id(substrate)) is None:
            reactRefs = (self.set_reference(reaction, substrate, True))

        product = self.tree.get_node(edge_id[1]).node_object
        if reaction.getProduct(self.process_complex_id(product)) is None and reaction.getModifier(self.process_complex_id(product)) is None:
          self.set_reference(reaction, product, False)

    def add_parameter(self, parId):
        par = self.model.createParameter()
        par.setId(parId)

    def compute_KineticLaw(self, reaction_id, rxnconReactions):
        handledReaction=[]
        rule = ""
        for reactions in rxnconReactions:
            if reactions[0].rid not in handledReaction:
                handledReaction.append(reactions[0].rid)
                handledNode = []
                if reactions[0].rate.rate is not None:
                    if rule:
                        rule += " + "
                    rule += reactions[0].rate.rate
                    self.add_parameter(reactions[0].rate.rate)

                    for reactionTuple in rxnconReactions:
                        if reactionTuple[0].rid == reactions[0].rid:
                            if reactionTuple[1][0] not in handledNode:
                                rule += " * " + self.process_complex_id( self.tree.get_node(reactionTuple[1][0]).node_object)
                                handledNode.append(reactionTuple[1][0])

                elif reactions[0].rate.rate is None and reactions[0].rate.rrate is not None and reactions[0].rate.frate is not None:
                    there =" "+ reactions[0].rate.frate
                    self.add_parameter(reactions[0].rate.frate)
                    back =" "+ reactions[0].rate.rrate
                    self.add_parameter(reactions[0].rate.rrate)
                    for reactionTuple in rxnconReactions:
                        if reactionTuple[0].rid == reactions[0].rid:
                            if reactionTuple[1][0] not in handledNode:
                                there += " * " + self.process_complex_id( self.tree.get_node(reactionTuple[1][0]).node_object)
                                handledNode.append(reactionTuple[1][0])
                            if reactionTuple[1][1] not in handledNode:
                                back += " * " + self.process_complex_id( self.tree.get_node(reactionTuple[1][1]).node_object)
                                handledNode.append(reactionTuple[1][1])
                    rule += there + " - " + back
                else:
                    raise RxnconRateError("failed to set Kinetic law for reaction " + str(reactions[0].rid ))

        reaction = self.model.getReaction(reaction_id)
        kineticLaw = reaction.createKineticLaw()
        kineticLaw.setMath(parseL3Formula(rule))

    def save_SBML(self, document, path):
        # writes the SBML Document to a textfile

        #TODO validation of model before writing to file!?
        if writeSBMLToFile(document, path):
            print("file save xuscessful")
        else:
            print('file save failed')

    def build_model(self, rPDTree):
        # build_model takes a reducedPD.tree and calls the functions to build a species for each node and reaction for each edge
        self.tree = rPDTree

        # default compartment until further changes to rxncon
        c = self.model.createCompartment()
        c.setId('cell')
        # example values for compartments
        #c.setConstant(True)
        c.setSize(1)
        #c.setSpatialDimensions(3)
        #c.setUnits('litre')


        visited_nodes = []
        handled_reactions= []

        # for all edges it is checked if the nodes are already visited, if not they are added as species in process_node
        # the same will happen for each edge and their reaction, an reaction can be on two different edges so it has to be checked if this reaction was already added
        for edge in rPDTree.edges:
            # add all nodes as species
            if edge.id[0] not in visited_nodes :
                self.process_node(edge.id[0])
                visited_nodes.append(edge.id[0])
            if edge.id[1] not in visited_nodes :
                self.process_node(edge.id[1])
                visited_nodes.append(edge.id[1])

        for edge in rPDTree.edges:
            #handle edges, so that all reactions with the same product(s) get handled at once
            for reaction in edge.reaction:
                if reaction.rid not in handled_reactions:
                    reactions = [(reaction, edge.id)]
                    handled_reactions.append(reaction.rid)
                    products = []
                    for prod in reaction.product_complexes:
                        if not prod.is_modifier:
                            products.append(edge.id[1])
                    for other_edge in rPDTree.edges:
                        for other_reaction in other_edge.reaction:
                            if other_edge.id != edge.id:
                                if other_edge.id[1] in products:
                                    reactions.append((other_reaction, other_edge.id ))
                                    handled_reactions.append(other_reaction.rid)
                    self.process_reaction(reactions)

        return(self.document)


# TODO everything with Celldesigner should go here so that the basic SBML isn't changed in the process
class CDBuilder(SBMLBuilder):
    def __init__(self, level = 2, version = 4):
        # creates a SBML document of given level and version, default is 2.4 because of Celldesigner specs
        try:
            self.namespace = SBMLNamespaces(level, version)
            self.namespace.addNamespace("http://www.sbml.org/2001/ns/celldesigner", "celldesigner")
            self.document = SBMLDocument(self.namespace)
        except ValueError:
            raise SystemExit("SBML Document creation failed")
        self.model = self.document.createModel()
        self.proteins = set()   # all unique proteins in this model (Id,name) where id == 0 means it is unset to the moment
        self.modRes = set()     # all unique modification Sites in this model, Set of tuple (id, domain)
        self.species_Mod = {}   # key: species, object: List[(modification id, state)]

    #TODO decide weather or not this is needed
    def addlistOfCompartmentAliases(self):
        # TODO might as well go back in model_CdAnnotation as a +=...
        return "<celldesigner:listOfCompartmentAliases/>\n"

    # TODO
    def addlistOfComplexSpeciesAliases(self):
        # as long as it is empty
        return "<celldesigner:listOfComplexSpeciesAliases/>\n"

    # TODO include speciesalias "placeholder" for species inside of a complex
    def addlistOfSpeciesAliases(self):
        # adds for every Species an entry mostly of default information , except id and species, the later is "s"+ species_id
        speciesList = self.model.getListOfSpecies()

        losa = "<celldesigner:listOfSpeciesAliases>\n"
        id = 1
        for species in self.model.getListOfSpecies():
            losa += "<celldesigner:speciesAlias id=\"sa"+ str(id) +"\" species=\""+ str(species.getId()) +"\">\n"
            id +=1
            # block of necessary but uninteresting default informations
            losa += """<celldesigner:activity>inactive</celldesigner:activity>
<celldesigner:bounds x="0.0" y="0.0" w="80.0" h="40.0"/>
<celldesigner:font size="12"/>
<celldesigner:view state="usual"/>
<celldesigner:usualView>
<celldesigner:innerPosition x="0.0" y="0.0"/>
<celldesigner:boxSize width="80.0" height="40.0"/>
<celldesigner:singleLine width="1.0"/>
<celldesigner:paint color="ffccffcc" scheme="Color"/>
</celldesigner:usualView>
<celldesigner:briefView>
<celldesigner:innerPosition x="0.0" y="0.0"/>
<celldesigner:boxSize width="80.0" height="60.0"/>
<celldesigner:singleLine width="0.0"/>
<celldesigner:paint color="3fff0000" scheme="Color"/>
</celldesigner:briefView>
<celldesigner:info state="empty" angle="-1.5707963267948966"/>"""

            losa += "</celldesigner:speciesAlias>\n"

        losa += "</celldesigner:listOfSpeciesAliases>\n"
        return losa

    def addlistOfProtein(self):
    # writes for every unique protein an entry in model.Annotation and replaces it in the proteins list with its new id
        lop = "<celldesigner:listOfProteins>\n"
        pId = 1
        for prot in list(self.proteins):
            lop += "<celldesigner:protein id=\"pr"+ str(pId) +"\" name=\""+ prot[0] +"\" type=\"GENERIC\"/>"
            self.proteins.add((prot[0],"pr" + str(pId)))
            self.proteins.remove(prot)
            pId +=1

        lop +="</celldesigner:listOfProteins>\n"
        return lop

    def addlistOfModificationResidues(self):
        lomr = "<celldesigner:listOfModificationResidues>\n"
        angle = 0
        for residue in self.modRes:
            lomr += "<celldesigner:modificationResidue angle=\"" + str(angle) + "\" id=\""+ residue[0]+"\" name=\""+ residue[1] +"\" side=\"none\"/>\n"
            angle += 1
        lomr += "</celldesigner:listOfModificationResidues>\n"
        return lomr

    # TODO complex species
    def setSpeciesAnnotation(self):
        listOfSpecies = self.model.getListOfSpecies()
        for species in listOfSpecies:
            print("set species annotation")
            id = species.getId()
            annotation = "<celldesigner:extension>\n<celldesigner:positionToCompartment>inside</celldesigner:positionToCompartment>\n<celldesigner:speciesIdentity>"
            annotation += "<celldesigner:class>PROTEIN</celldesigner:class>\n" # TODO handle complexes maybe by checking if in list of Proteins
            annotation += "<celldesigner:proteinReference>"
            for prot in list(self.proteins):
                name = species.getName()
                if prot[0] == name:
                    annotation += str(prot[1]) + "</celldesigner:proteinReference>\n"
                    break
            annotation += "</celldesigner:speciesIdentity>\n"

            #adds listOfReactions to species Annotation
            cat = ""
            for reaction in self.model.getListOfReactions():
                if reaction.getListOfModifiers().get(id) is not None:
                    cat += "<celldesigner:catalyzed reaction=\""+ str(reaction.getId()) +"\"/>\n"
            if cat:
                annotation += "<celldesigner:listOfCatalyzedReactions>\n"+ cat +"</celldesigner:listOfCatalyzedReactions>\n"

            # adds listOfModifications to species Annotaion
            if id in self.species_Mod:
                annotation += "<celldesigner:state>\n<celldesigner:listOfModifications>\n"
                for mod in self.species_Mod[id]:
                    annotation += "<celldesigner:modification residue=\""+ mod[0]  +"\" state=\""+ mod[1] +"\"/>\n"
                annotation += "</celldesigner:listOfModifications>\n</celldesigner:state>\n"


            annotation += "</celldesigner:extension>"
            species.setAnnotation(annotation)

    def model_CdAnnotation(self):
        theAnnotation = "<celldesigner:extension>\n"
        theAnnotation += "<celldesigner:modelVersion>4.0</celldesigner:modelVersion>\n"
        theAnnotation += "<celldesigner:modelDisplay sizeX=\"600\" sizeY=\"400\"/>\n"
        theAnnotation += self.addlistOfCompartmentAliases()
        theAnnotation += self.addlistOfComplexSpeciesAliases()    # TODO will needed for complexes that are formed in ppi
        theAnnotation += self.addlistOfSpeciesAliases()
        theAnnotation += "<celldesigner:listOfGroups/>\n"
        theAnnotation += self.addlistOfProtein()
        theAnnotation += self.addlistOfModificationResidues()
        theAnnotation += "</celldesigner:extension>"

        # TODO handle error codes
        self.model.setAnnotation(theAnnotation)        #currently adding the model annotation makes the file not readable for CD

        self.setSpeciesAnnotation()

    def process_node(self, visitId):
        # takes an unvisited node and creates species out of it
        # optional values are commented out until an according rxncon variable is found

        species = self.model.createSpecies()
        node = self.tree.get_node(visitId)

        species.setId( self.process_complex_id(node.node_object) )
        species.setMetaId( self.process_complex_id(node.node_object) )
        #change for CD
        if len(node.node_object.molecules) >= 2:
            # TODO handle Complex, add to complex list, note which species are in the complex
            species.setName(str(node.name))
        else:
            species.setName(node.node_object.molecules[0].name)
            self.proteins.add((node.node_object.molecules[0].name, 0))

        self.species_set_SBML_defaults(species)

        # for CD handling of Modifications
        for molecule in node.node_object.molecules:
            switcher = {"P" : "phosphorylated"} # TODO different cases for different modifications
            modNum = 1
            mods = []
            for modSite in molecule.modifications:
                self.modRes.add((species.getName() + str(modNum), modSite._State__components[0].domain)) #might there be more _State__components, its a list so there might but what does it mean
                mods.append(((species.getName() + str(modNum)), switcher[modSite.modifier]))
                modNum += 1
            if mods:
                self.species_Mod = {species.getId(): mods}

    def build_model(self, rPDTree):
        # build_model takes a reducedPD.tree and calls the functions to build a species for each node and reaction for each edge
        self.tree = rPDTree

        # default compartment until further changes to rxncon
        c = self.model.createCompartment()
        c.setId('cell')
        # example values for compartments
        #c.setConstant(True)
        c.setSize(1)
        #c.setSpatialDimensions(3)
        #c.setUnits('litre')


        visited_nodes = []
        handled_reactions= []

        # for all edges it is checked if the nodes are already visited, if not they are added as species in process_node
        # the same will happen for each edge and their reaction, an reaction can be on two different edges so it has to be checked if this reaction was already added
        for edge in rPDTree.edges:
            # add all nodes as species
            if edge.id[0] not in visited_nodes :
                self.process_node(edge.id[0])
                visited_nodes.append(edge.id[0])
            if edge.id[1] not in visited_nodes :
                self.process_node(edge.id[1])
                visited_nodes.append(edge.id[1])

        for edge in rPDTree.edges:
            #handle edges, so that all reactions with the same product(s) get handled at once
            for reaction in edge.reaction:
                if reaction.rid not in handled_reactions:
                    reactions = [(reaction, edge.id)]
                    handled_reactions.append(reaction.rid)
                    products = []
                    for prod in reaction.product_complexes:
                        if not prod.is_modifier:
                            products.append(edge.id[1])
                    for other_edge in rPDTree.edges:
                        for other_reaction in other_edge.reaction:
                            if other_edge.id != edge.id:
                                if other_edge.id[1] in products:
                                    reactions.append((other_reaction, other_edge.id ))
                                    handled_reactions.append(other_reaction.rid)
                    self.process_reaction(reactions)

        self.model_CdAnnotation()
        return(self.document)

if __name__ == "__main__":

    simple = """
    a_p+_b_[x]
    """
    simple2 = """
    a_ppi_b
    """

    TOY1 = """
    a_p+_b_[x]; ! b_[y]-{P}
    c_p+_b_[y]
    d_ppi_e
    """

    TOY3 = """
    a_p+_b_[x]
    c_p+_b_[x]
    d_ppi_e
    """
    #d_ppi_e

    TOY2 = """
    C_p+_A_[x]
    A_ppi_B; X A_[x]-{P}
    """
    TOY4 = """
    C_p+_A_[x]
    A_ppi_B; K+ A_[x]-{P}
    """

    #rxncon = Rxncon(TOY3)
    #rxncon = Rxncon(TOY2)
    #rxncon = Rxncon(TOY4)
    #rxncon = Rxncon(TOY1)
    rxncon = Rxncon(simple)
    rxncon.run_process()
    reducedPD = ReducedProcessDescription(rxncon.reaction_pool)
    reducedPD.build_reaction_Tree()

    #useCD = False
    useCD = True

    if useCD:
        #cd = SBMLBuilder(level = 3, version = 1)
        cd = CDBuilder()
        toy1sbml =  cd.build_model(reducedPD.tree)
        cd.save_SBML(toy1sbml, os.path.expanduser("~/Desktop/CDTest/cdtest.xml"))
        #sb.save_SBML(toy1sbml, os.path.expanduser("~/Desktop/cdtest.sbml"))
        print("\n" + writeSBMLToString(toy1sbml) + "\n")

    else:
        #sb = SBMLBuilder(level = 3, version = 1)
        sb = SBMLBuilder()
        toy1sbml =  sb.build_model(reducedPD.tree)
        sb.save_SBML(toy1sbml, os.path.expanduser("~/Desktop/sbmltest.xml"))
        #sb.save_SBML(toy1sbml, os.path.expanduser("~/Desktop/sbmltest.sbml"))
        print("\n" + writeSBMLToString(toy1sbml) + "\n")
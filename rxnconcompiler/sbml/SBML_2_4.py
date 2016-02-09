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

    def process_node_id(self, nodeId):
        return ("s" + str(nodeId))

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

        #species.setId( self.process_complex_id(node.node_object) )
        species.setId( self.process_node_id(node.id))
        species.setName(str(node.name))
        self.species_set_SBML_defaults(species)

    def set_reference(self, reaction, reactant, is_substrate, node_id):
        # sets the reactant/product/modifier references for the given reaction

        if not reactant._BiologicalComplex__is_modifier:
            if is_substrate:
                reactRef = reaction.createReactant()
                reactRef.setSpecies(self.process_node_id(node_id))
            else:
                prodRef =  reaction.createProduct()
                prodRef.setSpecies(self.process_node_id(node_id))
        else:
            modRef = reaction.createModifier()
            modRef.setSpecies(self.process_node_id(node_id))

    def add_references(self, sbmlRId, edge_id):
        # adds new reactants to an reaction

        sbmlReaction = self.model.getReaction(sbmlRId)
        rxnconReaction = None
        for edge in self.tree.edges:
            if edge_id == edge.id:
                rxnconReaction = edge.reaction[0]

        substrate = None
        product = None

        for node in self.tree.nodes:
            if node.id == edge_id[0]:
                if node.node_object.molecules == rxnconReaction.substrat_complexes[0].molecules:
                    substrate = rxnconReaction.substrat_complexes[0]
                elif node.node_object.molecules == rxnconReaction.substrat_complexes[1].molecules:
                    substrate = rxnconReaction.substrat_complexes[1]
                else:
                    print("error in print referenz substrat is neither of the two substrat_complexes")

            elif node.id == edge_id[1]:
                if node.node_object.molecules == rxnconReaction.product_complexes[0].molecules:
                    product = rxnconReaction.product_complexes[0]
                elif node.node_object.molecules == rxnconReaction.product_complexes[1].molecules:
                    product = rxnconReaction.product_complexes[1]
                else:
                    print("error in print reference product is neither of the two product_complexes")


        if sbmlReaction.getReactant(self.process_node_id(edge_id[0])) is None and sbmlReaction.getModifier(self.process_node_id(edge_id[0])) is None:
            self.set_reference(sbmlReaction, substrate, True, edge_id[0])

        if sbmlReaction.getProduct(self.process_node_id(edge_id[1])) is None and sbmlReaction.getModifier(self.process_node_id(edge_id[1])) is None:
            self.set_reference(sbmlReaction, product, False, edge_id[1])

        #substrate = self.tree.get_node(edge_id[0]).node_object # old but incorrect way, information in node ist inccorect, is_modifier is reaction dependand not globaly
        #product = self.tree.get_node(edge_id[1]).node_object the same with substrate

        # if sbmlReaction.getReactant(self.process_complex_id(substrate)) is None and sbmlReaction.getModifier(self.process_complex_id(substrate)) is None:
        #     reactRefs = (self.set_reference(sbmlReaction, substrate, True))
        #
        # if sbmlReaction.getProduct(self.process_complex_id(product)) is None and sbmlReaction.getModifier(self.process_complex_id(product)) is None:
        #     self.set_reference(sbmlReaction, product, False)

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

        #adds SpeciesReferences to the reaction
        [self.add_references(id, reactionTuple[1]) for reactionTuple in rxnconReactions]

        self.compute_KineticLaw(id, rxnconReactions)

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
                                #rule += " * " + self.process_complex_id( self.tree.get_node(reactionTuple[1][0]).node_object)
                                rule += " * " + self.process_node_id(reactionTuple[1][0])
                                handledNode.append(reactionTuple[1][0])

                elif reactions[0].rate.rate is None and reactions[0].rate.rrate is not None and reactions[0].rate.frate is not None:
                    there =" "+ reactions[0].rate.frate
                    self.add_parameter(reactions[0].rate.frate)
                    back =" "+ reactions[0].rate.rrate
                    self.add_parameter(reactions[0].rate.rrate)
                    for reactionTuple in rxnconReactions:
                        if reactionTuple[0].rid == reactions[0].rid:
                            if reactionTuple[1][0] not in handledNode:
                                #there += " * " + self.process_complex_id( self.tree.get_node(reactionTuple[1][0]).node_object)
                                there += " * " + self.process_node_id( reactionTuple[1][0])
                                handledNode.append(reactionTuple[1][0])
                            if reactionTuple[1][1] not in handledNode:
                                #back += " * " + self.process_complex_id( self.tree.get_node(reactionTuple[1][1]).node_object)
                                back += " * " + self.process_node_id(reactionTuple[1][1])
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


# TODO everything for Celldesigner should go here so that the basic SBML isn't changed in the process
# TODO check compartments, the default "cell" compartment gets lost in CD output visualisation
class CDBuilder(SBMLBuilder):
    def __init__(self, level = 2, version = 4):
        # creates a SBML document of given level and version, default is 2.4 because of Celldesigner specs
        # adds Cellldesigner Namespace
        try:
            self.namespace = SBMLNamespaces(level, version)
            self.namespace.addNamespace("http://www.sbml.org/2001/ns/celldesigner", "celldesigner")
            self.document = SBMLDocument(self.namespace)
        except ValueError:
            raise SystemExit("SBML Document creation failed")
        self.model = self.document.createModel()
        self.speciesAliases = {} # dict of key = species id and value alias
        self.complexSpeciesAliases = {} #dict of key = species id and value aliasId
        self.proteins = set()   # all unique proteins in this model (name, id) where id == 0 means it is not set yet
        self.complexes= set()   # all unique complex species (id, parentNode1.id, parentNode2.id)
        self.modRes = set()     # all unique modification Sites in this model, Set of tuple (name, domain)
        self.species_Mod = {}   # key: species, object: List[(modification id, state)]

        self.modSwitcher = {"1.1.1.1" : "phosphorylated"} # TODO add other known modifications

        self.reactionSwitcher = {"1.1.1.1" : "STATE_TRANSITION", "2.1.1.1" : "HETERODIMER_ASSOCIATION"} #TODO add more reaction types

    def addlistOfIncludedSpecies(self):
        annotation = "<celldesigner:listOfIncludedSpecies>\n"

        for comp in self.complexes:
            #print "we look into complex " + str(comp[0])
            for iId in [comp[1], comp[2]]:
                #print "with included species " + str(iId)
                node = self.tree.get_node(iId)
                speciesId = self.model.getSpecies(self.process_node_id(iId)).getId()

                #for molecule in node.molecules:
                # speciesId = self.model.getSpecies(self.process_node_id(iId)).getId()
                #species id += molecule.name
                #indenent everything in the secon for loop, so it will be in this one


                name = "-".join(mol.name for mol in node.node_object.molecules)

                annotation += "<celldesigner:species id=\"i"+ str(iId) +"\" name=\"" + name +"\">\n"
                annotation += "<celldesigner:annotation>\n"
                annotation += "<celldesigner:complexSpecies>"+comp[0]+"</celldesigner:complexSpecies>\n"
                annotation += "<celldesigner:speciesIdentity>\n"

                #TODO at the momentent only proteins as parts of a complex, complex should get represented as one species instead of a real complex with included species (which would be better but might get strange with included species getting displaced, needs tests)

                for prot in self.proteins:
                    #print node.node_object.molecules[0].name
                    #print prot[0]
                    if prot[0] == node.node_object.molecules[0].name:
                        annotation += "<celldesigner:class>PROTEIN</celldesigner:class>\n"
                        annotation += "<celldesigner:proteinReference>"+prot[1]+"</celldesigner:proteinReference>\n"

                if speciesId in self.species_Mod:
                    annotation += "<celldesigner:state>\n<celldesigner:listOfModifications>\n"
                    for mod in self.species_Mod[speciesId]:
                        annotation += "<celldesigner:modification residue=\""+ mod[0]  +"\" state=\""+ mod[1] +"\"/>\n"
                        annotation += "</celldesigner:listOfModifications>\n</celldesigner:state>\n"

                annotation +=   """</celldesigner:speciesIdentity>
                                </celldesigner:annotation>
                                </celldesigner:species>"""

        annotation +="</celldesigner:listOfIncludedSpecies>\n"
        return annotation

    #TODO decide weather or not this is needed
    def addlistOfCompartmentAliases(self):
        # TODO might as well go back in model_CdAnnotation as a +=...
        return "<celldesigner:listOfCompartmentAliases/>\n"

    def addlistOfComplexSpeciesAliases(self):
        annotation = "<celldesigner:listOfComplexSpeciesAliases>\n"
        for comp in self.complexes:
            annotation +=  "<celldesigner:complexSpeciesAlias id=\""+ self.complexSpeciesAliases[comp[0]] + "\" species=\""+comp[0]+"\">\n"
            annotation += """ <celldesigner:activity>inactive</celldesigner:activity>
    <celldesigner:bounds x="0.0" y="0.0" w="100.0" h="120.0"/>
    <celldesigner:font size="12"/>
    <celldesigner:view state="usual"/>
    <celldesigner:backupSize w="0.0" h="0.0"/>
    <celldesigner:backupView state="none"/>
    <celldesigner:usualView>
    <celldesigner:innerPosition x="0.0" y="0.0"/>
    <celldesigner:boxSize width="100.0" height="120.0"/>
    <celldesigner:singleLine width="2.0"/>
    <celldesigner:paint color="fff7f7f7" scheme="Color"/>
    </celldesigner:usualView>
    <celldesigner:briefView>
    <celldesigner:innerPosition x="0.0" y="0.0"/>
    <celldesigner:boxSize width="80.0" height="60.0"/>
    <celldesigner:singleLine width="2.0"/>
    <celldesigner:paint color="fff7f7f7" scheme="Color"/>
    </celldesigner:briefView>
    <celldesigner:info state="empty" angle="-1.5707963267948966"/>
    </celldesigner:complexSpeciesAlias>\n"""

        annotation += "</celldesigner:listOfComplexSpeciesAliases>\n"
        return annotation

    def addlistOfSpeciesAliases(self):
        # adds for every Species an entry mostly of default information , except id and species, the later is "s"+ species_id
        speciesList = self.model.getListOfSpecies()

        losa = "<celldesigner:listOfSpeciesAliases>\n"
        id = 1
        for species in self.model.getListOfSpecies():
            if self.complexSpeciesAliases.has_key(species.getId()):
                continue
            losa += "<celldesigner:speciesAlias id=\"sa"+ str(id) +"\" species=\""+ str(species.getId()) +"\">\n"
            self.speciesAliases[species.getId()] = "sa"+str(id)
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
<celldesigner:info state="empty" angle="-1.5707963267948966"/>\n"""

            losa += "</celldesigner:speciesAlias>\n"

        for comp in self.complexes:
            ypos = 0
            #print "we look into complex " + str(comp[0])
            for iId in [comp[1], comp[2]]:
                losa += "<celldesigner:speciesAlias id=\"isa"+ str(iId) +"\" species=\"i"+ str(iId) +"\" complexSpeciesAlias=\""+ self.complexSpeciesAliases[comp[0]] +"\">\n"
                losa += "<celldesigner:activity>inactive</celldesigner:activity>\n"
                losa += "<celldesigner:bounds x=\"0.0\" y=\""+str(ypos)+"\" w=\"80.0\" h=\"40.0\"/>\n"     #for more then three also x has to be manipulated
                ypos += 40
                losa += """<celldesigner:font size="12"/>
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
                        <celldesigner:singleLine width="1.0"/>
                        <celldesigner:paint color="3fff0000" scheme="Color"/>
                        </celldesigner:briefView>
                        <celldesigner:info state="empty" angle="-1.5707963267948966"/>
                        </celldesigner:speciesAlias>\n"""

        losa += "</celldesigner:listOfSpeciesAliases>\n"
        return losa

    def addlistOfModificationResidues(self, name):
        lomr = "<celldesigner:listOfModificationResidues>\n"
        angle = 1
        num = 1
        for residue in list(self.modRes):
            if name == residue[0]:
                lomr += "<celldesigner:modificationResidue angle=\"" + str(angle) + "\" id=\""+ residue[0] + str(num) +"\" name=\""+ residue[1] +"\" side=\"none\"/>\n"
                angle += 1
                num += 1
        lomr += "</celldesigner:listOfModificationResidues>\n"
        return lomr

    def addlistOfProtein(self):
    # writes for every unique protein an entry in model.Annotation and replaces it in the proteins list with its new id
        lop = "<celldesigner:listOfProteins>\n"
        pId = 1
        for prot in list(self.proteins):
            lop += "<celldesigner:protein id=\"pr"+ str(pId) +"\" name=\""+ prot[0] +"\" type=\"GENERIC\">"
            self.proteins.add((prot[0],"pr" + str(pId)))
            self.proteins.remove(prot)
            lop += self.addlistOfModificationResidues(prot[0])
            lop += "</celldesigner:protein>\n"
            pId +=1

        lop +="</celldesigner:listOfProteins>\n"
        return lop

    def setSpeciesAnnotation(self):
        listOfSpecies = self.model.getListOfSpecies()
        for species in listOfSpecies:
            id = species.getId()
            annotation = "<celldesigner:extension>\n<celldesigner:positionToCompartment>inside</celldesigner:positionToCompartment>\n<celldesigner:speciesIdentity>"
            name = species.getName()

            for prot in list(self.proteins):
                name = species.getName()
                if prot[0] == name:
                    annotation += "<celldesigner:class>PROTEIN</celldesigner:class>\n"
                    annotation += "<celldesigner:proteinReference>"
                    annotation += str(prot[1]) + "</celldesigner:proteinReference>\n"
                    break

            for comp in list(self.complexes):
                if id == comp[0]:
                   annotation +=  "<celldesigner:class>COMPLEX</celldesigner:class>\n"
                   annotation +=  "<celldesigner:name>"+ id +"</celldesigner:name>\n"


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

            annotation += "</celldesigner:speciesIdentity>\n"
            annotation += "</celldesigner:extension>"
            species.setAnnotation(annotation)

    def setReferenzAnnotation(self, reaction, rtype):

        for ref in reaction.getListOfReactants():
            annotation = "<celldesigner:extension>\n"
            annotation += "<celldesigner:alias>"+self.speciesAliases[ref.getSpecies()]+"</celldesigner:alias>\n"
            annotation += "</celldesigner:extension>"
            ref.setAnnotation(annotation)

        for ref in reaction.getListOfProducts():
            annotation = "<celldesigner:extension>\n"
            if rtype == "2.1.1.1":
                annotation += "<celldesigner:alias>"+self.complexSpeciesAliases[ref.getSpecies()]+"</celldesigner:alias>\n"
            else:
                annotation += "<celldesigner:alias>"+self.speciesAliases[ref.getSpecies()]+"</celldesigner:alias>\n"
            annotation += "</celldesigner:extension>"
            ref.setAnnotation(annotation)

        for ref in reaction.getListOfModifiers():
            annotation = "<celldesigner:extension>\n"
            annotation += "<celldesigner:alias>"+self.speciesAliases[ref.getSpecies()]+"</celldesigner:alias>\n"
            annotation += "</celldesigner:extension>"
            ref.setAnnotation(annotation)

    def setReactionAnnotation(self):
        listOfReactions = self.model.getListOfReactions()
        for reaction in listOfReactions:
            id = reaction.getId()
            name = reaction.getName()
            rxnconreaction = None
            for edge in self.tree.edges:
                if str(edge.reaction[0].rid) == id[1:]:
                    rxnconreaction = edge.reaction[0]
                    break

            annotation = "<celldesigner:extension>\n"
            annotation += "<celldesigner:name>"+name+"</celldesigner:name>\n"
            annotation += "<celldesigner:reactionType>"+ self.reactionSwitcher[ rxnconreaction.rtype ] +"</celldesigner:reactionType>\n"

            annotation += "<celldesigner:baseReactants>\n"
            for reactant in reaction.getListOfReactants():
                annotation += "<celldesigner:baseReactant species=\""+ str(reactant.getSpecies()) +"\" alias=\"" + self.speciesAliases[reactant.getSpecies()] + "\">\n"
                annotation += "<celldesigner:linkAnchor position=\"S\"/>\n</celldesigner:baseReactant>\n"
            annotation += "</celldesigner:baseReactants>\n"

            annotation += "<celldesigner:baseProducts>\n"
            for product in reaction.getListOfProducts():
                is_complex = False
                for comp in self.complexes:
                    if product.getSpecies() == comp[0]:
                        is_complex = True
                        break

                if is_complex:
                    annotation += "<celldesigner:baseProduct species=\""+ str(product.getSpecies()) +"\" alias=\""+ self.complexSpeciesAliases[product.getSpecies()] +"\">\n"
                    annotation += "<celldesigner:linkAnchor position=\"WNW\"/>\n</celldesigner:baseProduct>\n"
                else:
                    annotation += "<celldesigner:baseProduct species=\""+ str(product.getSpecies()) +"\" alias=\""+ self.speciesAliases[product.getSpecies()] +"\">\n"
                    annotation += "<celldesigner:linkAnchor position=\"WNW\"/>\n</celldesigner:baseProduct>\n"
            annotation += "</celldesigner:baseProducts>\n"

            if rxnconreaction.rtype == "2.1.1.1":
                annotation += "<celldesigner:editPoints>0.0,0.0</celldesigner:editPoints>\n"

            annotation +="<celldesigner:listOfModification>\n"
            for modifier in reaction.getListOfModifiers():
                annotation += "<celldesigner:modification type=\"CATALYSIS\" modifiers=\""+ modifier.getSpecies() +"\" aliases=\""+ self.speciesAliases[modifier.getSpecies()] +"\">\n"
                annotation += "</celldesigner:modification>\n"
            annotation+= "</celldesigner:listOfModification>\n"

            annotation += "</celldesigner:extension>"

            reaction.setAnnotation(annotation)
            self.setReferenzAnnotation(reaction, rxnconreaction.rtype)

    def model_CdAnnotation(self):

        listOfProtein = self.addlistOfProtein()


        theAnnotation = "<celldesigner:extension>\n"
        theAnnotation += "<celldesigner:modelVersion>4.0</celldesigner:modelVersion>\n"
        theAnnotation += "<celldesigner:modelDisplay sizeX=\"600\" sizeY=\"400\"/>\n"
        theAnnotation += self.addlistOfIncludedSpecies()
        theAnnotation += self.addlistOfCompartmentAliases()
        theAnnotation += self.addlistOfComplexSpeciesAliases()    # TODO will needed for complexes that are formed in ppi
        theAnnotation += self.addlistOfSpeciesAliases()
        theAnnotation += "<celldesigner:listOfGroups/>\n"
        theAnnotation += listOfProtein
        #theAnnotation += self.addlistOfModificationResidues()
        theAnnotation += "</celldesigner:extension>"

        #print theAnnotation
        # TODO handle error codes
        self.model.setAnnotation(theAnnotation)        #currently adding the model annotation makes the file not readable for CD

    def process_node(self, visitId):
        # takes an unvisited node and creates species out of it
        # optional values are commented out until an according rxncon variable is found

        species = self.model.createSpecies()
        node = self.tree.get_node(visitId)

        species.setId( self.process_node_id(node.id))
        species.setMetaId( self.process_node_id(node.id ))

        is_complex = False
        #change for CD
        if len(node.node_object.molecules) >= 2:
            is_complex = True
            species.setName(str(node.name))
            #species.setName("Complex")
            self.complexSpeciesAliases[species.getId()] = "csa" + str(node.id)
        else:
            species.setName(node.node_object.molecules[0].name)
            self.proteins.add((node.node_object.molecules[0].name, 0))

        self.species_set_SBML_defaults(species)

        # for CD handling of Modifications
        if not is_complex :
            modNum = 1
            mods = []
            for modSite in node.node_object.molecules[0].modifications:
                self.modRes.add((species.getName(), modSite._State__components[0].domain))
                #mods.append(((species.getName() + str(modNum)), self.modSwitcher[modSite.modifier]))  #unpractical method due to lacking clearness of .modifier
                visitedReactions = []
                for edge in self.tree.edges:
                    if edge.id[1] == node.id and edge.reaction[0].rid not in visitedReactions:
                        mods.append(((species.getName() + str(modNum)), self.modSwitcher[edge.reaction[0].rtype]))
                        visitedReactions.append(edge.reaction[0].rid)
                modNum += 1
            if mods:
                self.species_Mod[species.getId()] = mods
        else:
            self.complexes.add( (self.process_node_id(node.id), node.parent[0][1], node.parent[1][1] ))
            #print "" +str(visitId) + ", "+ str(node.parent[0][1] )+ ", "+  str(node.parent[1][1])

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
        self.setSpeciesAnnotation()
        self.setReactionAnnotation()

        return(self.document)

if __name__ == "__main__":

    sample1 = """
    a_ppi_b
    """""

    sample2= """
    a_ppi_b
    c_ppi_d
    """

    sample3= """
    c_p+_a
    a_ppi_d; ! a-{P}
    """

    simple = """
    A_ppi_C
    C_ppi_E
    A_p+_B_[x]; ! <comp>
    <comp>; AND A--C
    <comp>; AND C--E
    """
    simple2 = """
    c_p+_a
    a_ppi_b; ! a-{P}
    """

    simple3 = """
    c_p+_a_[x]
    a_ppi_b; ! a_[x]-{P}
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

    rxncon = Rxncon(sample3)

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
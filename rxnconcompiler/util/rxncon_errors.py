class RxnconError(Exception): pass

class RxnconParserError(RxnconError): pass

class RxnconBioNetGenError(RxnconError): pass

class TetramericComplexError(RxnconError): pass

class SbgnBuilderError(RxnconError): pass

class SbgnErError(RxnconError): pass



class BnglError(Exception): pass

class BnglRuleError(BnglError): pass

class BnglSpeciesError(BnglError): pass
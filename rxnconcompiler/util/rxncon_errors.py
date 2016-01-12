class RxnconError(Exception): pass

class RxnconRateError(RxnconError): pass


class RxnconParserError(RxnconError): pass


class RxnconConingencyError(RxnconError): pass


class RxnconBooleanError(RxnconError): pass


class RxnconBioNetGenError(RxnconError): pass


class TetramericComplexError(RxnconError): pass


class SbgnBuilderError(RxnconError): pass


class SbgnErError(RxnconError): pass


class BnglError(Exception): pass


class BnglRuleError(BnglError): pass


class BnglSpeciesError(BnglError): pass

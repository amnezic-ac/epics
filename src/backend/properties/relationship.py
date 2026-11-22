from src.backend.properties.property import *

class Atttendee(Property):
    # un peu plus complexe que ça (3.8.4.1)

    def __init__(self, name: str, cutypeparam: str = None, memberparam: str = None, roleparam: str = None, parstatparam: str = None, rsvpparam: bool = None, deltoparam: str = None, delfromparam: str = None, sentbyparam: str = None, cnparam: str = None, dirparam: str = None, languageparam: str = None):
        if (not name):
            raise Exception(f"Attendee name can't be None")

        self.name = name

        self.cutypeparam = Cutype(cutypeparam) if cutypeparam else None
        self.memberparam = Member(memberparam) if memberparam else None
        self.roleparam = Role(roleparam) if roleparam else None
        self.partstatparam = Partstat(parstatparam) if parstatparam else None
        self.rsvpparam = Rsvp(rsvpparam) if rsvpparam != None else None
        # the following attributes have to be Caladdress
        self.deltoparam = Delto(deltoparam) if deltoparam else None
        self.delfromparam = Delfrom(delfromparam) if delfromparam else None
        self.sentbyparam = Sentby(sentbyparam) if sentbyparam else None
        ########
        self.cnparam = Cn(cnparam) if cnparam else None
        self.dirparam = Dir(dirparam) if dirparam else None
        self.languageparam = Language(languageparam) if languageparam else None

    def __str__(self):
        result = "ATTENDEE"

        if (self.cutypeparam):
            result += f";{str(self.cutypeparam)}"
        if (self.memberparam):
            result += f";{str(self.memberparam)}"
        if (self.roleparam):
            result += f";{str(self.roleparam)}"
        if (self.partstatparam):
            result += f";{str(self.partstatparam)}"
        if (self.rsvpparam):
            result += f";{str(self.rsvpparam).upper()}"
        if (self.deltoparam):
            result += f";{str(self.deltoparam)}"
        if (self.delfromparam):
            result += f";{str(self.delfromparam)}"
        if (self.sentbyparam):
            result += f";{str(self.sentbyparam)}"
        if (self.cnparam):
            result += f";{str(self.cnparam)}"
        if (self.dirparam):
            result += f";{str(self.dirparam)}"
        if (self.languageparam):
            result += f";{str(self.languageparam)}"

        result += f":{self.name}"
        
        return result


class Contact(Property):
    # not displayed on thunderbird
    def __init__(self, value: str, altrep: str = None, language: str = None):
        if (not value):
            raise Exception (f"Contact value can't be None")

        self.value = value
        self.altrep = Altrep(altrep) if altrep else None
        self.language = Language(language) if language else None

    def __str__(self):
        result = "CONTACT"

        if (self.altrep):
            result += f";{str(self.altrep)}"
        if (self.language):
            result += f";{str(self.language)}"

        result += f":{self.value}"
        return result

class Organizer(Property):
    def __init__(self, value: str, cnparam: str = None, dirparam: str = None, sentbyparam: str = None, languageparam: str = None):
        if (not value):
            raise Exception(f"Organizer value can't be None")

        self.value = value
        self.cnparam = Cn(cnparam) if cnparam else None
        self.dirparam = Dir(dirparam) if dirparam else None
        self.sentbyparam = Sentby(sentbyparam) if sentbyparam else None
        self.languageparam = Language(languageparam) if languageparam else None

    def __str__(self):
        result = "Organizer"

        if (self.cnparam):
            result += f";{str(self.cnparam)}"
        if (self.dirparam):
            result += f";{str(self.dirparam)}"
        if (self.sentbyparam):
            result += f";{str(self.sentbyparam)}"
        if (self.languageparam):
            result += f";{str(self.languageparam)}"

        result += f":{self.value}"
        return result

# TODO: check that value complies with RFC 3986
class Url(Property):
    def __init__(self, value: str):
        self.value = value

    def __str__(self):
        return f"URL:{self.value}"

class Uid(Property):
    def __init__(self, value: str):
        self.value = value

    def __str__(self):
        return f"UID:{self.value}"
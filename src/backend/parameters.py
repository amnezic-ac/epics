from src.backend.datatypes import Caladdress, Uri
from src.utils import configuration

class Parameter():
    def __str__(classe: str, value: str, quoted: bool = True):
        result = f"{classe.upper()}="

        if (quoted):
            result += f"\"{value}\""
        else:
            result += f"{value}"

        return result

class Altrep(Parameter):

    def __init__(self, value: str):
        self.value = value.strip()

    def __str__(self):
        return f"ALTREP=\"{self.value}\""

# Does it needs quote ?
# # https://datatracker.ietf.org/doc/html/rfc5545#autoid-13
class Cn(Parameter, Caladdress):
    def __init__(self, value: str):
        if (not value or not value.strip()):
            raise Exception(f"Can't create an empty common name parameter")
        self.value = value.strip()

    def __str__(self):
        return f"CN=\"{self.value}\""

class Cutype(Parameter, Caladdress):
    def __init__(self, value: str = "INDIVIDUAL"):
        if (not value):
            value = "INDIVIDUAL"
            logging.warn(f"User attempted to create a cutype parameter with a value set to None. Automatically set to the default value \"INDIVIDUAL\"")
        self.value = value.upper().strip()

    def __str__(self):
        return f"CUTYPE={self.value}"

class Delfrom(Parameter, Caladdress):
    def __init__(self, addresses: [Caladdress]):
        self.addresses = set(addresses)

    def __str__(self):
        tmp = list(self.addresses)
        result = f"DELEGATED-FROM=\"{tmp[0]}\""
        tmp.pop(0)

        for address in tmp:
            result += f",\"{address}\""

        return result

    def add(self, person: str):
        self.addresses.add(person)

    def remove(self, person: str):
        self.addresses.remove(person)

class Delto(Parameter, Caladdress):
    def __init__(self, addresses: [Caladdress]):
        self.addresses = set(addresses)

    def __str__(self):
        tmp = list(self.addresses)
        result = f"DELEGATED-TO=\"{tmp[0]}\""
        tmp.pop(0)

        for address in tmp:
            result += f",\"{address}\""

        return result

    def add(self, person: str):
        self.addresses.add(person)

    def remove(self, person: str):
        self.addresses.remove(person)

class Dir(Parameter, Caladdress):
    def __init__(self, uri: str):
        self.uri = Uri(uri)

    def __str__(self):
        return f"URI={str(uri)}"

class Encoding(Parameter):
    def __init__(self, name: str):
        self.encoding_name = name

    def __str__(self):
        return f"ENCODING={self.encoding_name}"

class Fmttype(Parameter):
    def __init__(self, typename: str, subtypename: str):
        # refer to RFC 4288 section 4.2 for (sub)typename documentation
        self.typename = typename
        self.subtypename = subtypename

    def __str__(self):
        return f"FMTTYPE={self.typename}/{self.subtypename}"

class Fbtype(Parameter):
    def __init__(self, value: str = "BUSY"):
        self.value = value

    def __str__(self):
        return f"FBTYPE:{self.value}"

class Language(Parameter):
    def __init__(self, key: str):
        # please refer to FC 5646 for compliance
        if (not key in [pair[0] for pair in configuration["language"]["choices"]]):
            raise Exception(f"{key} is not a valid lnaguage key. Please refer to configuration file.")
        self.key = key

    def __str__(self):
        return f"LANGUAGE={self.key}"

class Member(Parameter, Caladdress):
    def __init__(self, members: [str]):
        self.members = set(members)

    def __str__(self):
        tmp = list(self.members)
        result = f"MEMBER=\"{tmp[0]}\""
        tmp.pop(0)

        for member in tmp:
            result += f",\"{member}\""

        return result

    def add(self, person: str):
        self.members.add(person)

    def remove(self, person: str):
        self.members.remove(person)

class Partstat(Parameter, Caladdress):
    def __init__(self, value: str):
        self.value = value

    def __str__(self):
        return f"PARSTAT={self.value}"

class Range(Parameter):
    pass

class Trigrel(Parameter):
    def __init__(self, value: str):
        self.value = value

    def __str__(self):
        return f"RELATED={self.value}"

class Reltype(Parameter):
    def __init__(self, value: str):
        self.value = value

class Role(Parameter, Caladdress):
    def __init__(self, value: str = "REQ-PARTICIPANT"):
        self.value = value

    def __str__(self):
        return f"ROLE:{self.value}"

class Rsvp(Parameter, Caladdress):
    def __init__(self, value: bool = False):
        self.value = value

    def __str__(self):
        return f"RSVP={str(self.value).upper()}"

class Sentby(Parameter, Caladdress):
    def __init__(self, value: Caladdress):
        self.value = value

class Tzid():
    pass
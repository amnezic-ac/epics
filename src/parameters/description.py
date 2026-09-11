# section 3.8.1

class Attachement():
    
    # now (sub)typename is considered always valid, need work on that
    def __init__(value: str, encoding: str = None, typename: str = None, subtypename: str = None):
        self.value = value
        self.encoding = encoding
        self.typename = typename # define at section 4.2 of RFC 4288

        if ((not typename and subtypename) or (typename and not subtypename)):
            raise Exception(f"If given, an attachement should have both a type name ({typename}) and a subtype name ({subtypename}). Please refer to section 3.2.8 of RFC 5545 for further information.")

        self.subtypename = subtypename

    def __str__():
        result = "ATTACH"

        if (self.typename):
            result += f";FMTTYPE={self.typename}/{self.subtypename}"

        if (self.encoding):
            result += f";ENCODING={self.encoding}"

        result += f":{self.value}"

        return result

class Categories():
    # on considère que la langue donnée est correcte
    def __init__(categories: [str], language : str = None):
        self.categories = categories
        self.language = language # needs to comply with RFC 5646

    def __str__():
        result = f"CATEGORIES"

        if (self.language):
            result += f";LANGUAGE={self.language}"

        result += ":"

        for i in range(len(self.categories) - 1):
            result += f"{self.categories[i]},"
        if (len(self.categories) > 1):
            result += f"{self.categories[-1]}"

        return result

class Classification():

    def __init__(value: str = "Public"):
        self.value = str.upper(value)
        # possible values of Class are: Public, Private and Confidential

    def __str__():
        return f"CLASS:{self.value}"

class Comment():

    def __init__(value: str, altrep: str = None, language: str = None):
        self.value = value
        self.altrep = altrep
        self.language = language

    def __str__():
        result = f"COMMENT"

        if (self.altrep):
            result += f";ALTREP=\"{self.altrep}\""

        if (self.language):
            result += f";LANGUAGE={self.language}"

        result += f"{self.value}"
        return result

class Description():
    
    def __init__(value: str, altrep: str = None, language: str = None):
        self.value = value
        self.altrep = altrep
        self.language = language

    def __str__():
        result = "DESCRIPTION"

        if (self.altrep):
            result += f";ALTREP={self.altrep}"

        if (self.language):
            result += f";LANGUAGE={self.language}"

        result += f":{self.value}"
        return result

class Geo():

    def __init__(latitude: str, longitude: str):
        self.latitude = None
        self.longitude = None

        try:
            latitude = float(latitude) 
            longitude = float(longitude) 
        except ValueError as e:
            raise Exception(f"Error: {e}")

        if (not (self.latitude >= -90 and self.latitude <= 90)):
            raise Exception(f"Invalid latitude value ({self.latitude}), should be between -90 and 90")
        if (not (self.longitude >= -180 and self.longitude <= 180)):
            raise Exception(f"Invalid latitude value ({self.latitude}), should be between -90 and 90")

    def __str__():
        return f"GEO{str(self.latitude)};{str(self.longitude)}"
            
class Location():

    def __init__(value: str, altrep: str = None, language: str = None):
        self.value = value
        self.altrep = altrep
        self.language = language

    def __str__():
        result = "LOCATION"

        if (self.altrep):
            result += f";ALTREP={self.altrep}"

        if (self.language):
            result += f";LANGUAGE={self.language}"

        result += f":{self.value}"
        return result

class Percent():

    def __init__(value: str):
        self.value = None
        try:
            self.value = int(value)
        except ValueError as e:
            raise e

        if (not (self.value >= 0 and self.value <= 100)):
            raise Exception(f"Percentage have to be between 0 and 100 (current value: {self.value})")

        def __str__():
            return f"PERCENT-COMPLETE:{self.value}"

class Priority():

    def __init__(value: int = 0):
        if (value < 0 or value > 9):
            raise Exception(f"Priority value have to be include between 0 and 9")

        self.value = value

    def __str__():
        return f"PRIORITY:{self.value}"

class Resources():
    def __init__(value: str, altrep: str = None, language: str = None):
        self.value = value
        self.altrep = altrep
        self.language = language

    def __str__():
        result = "RESOURCES"

        if (self.altrep):
            result += f";ALTREP={self.altrep}"

        if (self.language):
            result += f";LANGUAGE={self.language}"

        result += f":{self.value}"
        return result

class Status():
    def __init__(value: str):
        self.value = value

    def __str__():
        return f"STATUS:{self.value}"

class Summary():
    def __init__(value: str, altrep: str, language: str):
        self.value = value
        self.altrep = altrep
        self.language = language

    def __str__():
        result = "SUMMARY"

        if (self.altrep):
            result += f";ALTREP={self.altrep}"

        if (self.language):
            result += f";LANGUAGE={self.language}"

        result += f":{self.value}"
        return result
 
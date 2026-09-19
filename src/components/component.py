from datetime import datetime

class Component():

    def __init__(self):
        pass

    def display_list(attr_name: str, liste: [any], newline: bool = False) -> str:
        result = f"{attr_name.upper()}"

        return result



    def __str__(self, name: str):
        result = "BEGIN:"

        if (name not in ["VALARM", "VEVENT", "VFEEBUSY", "VJOURNAL", "VTODO"]):
            raise Exception(f"{name} is not a valid component.")

        result += f"{name}\n"

        for attr, value in self.__dict__.items():
            if (not value):
                continue
            elif (type(value) is datetime):
                result += f"{attr.upper()}:{value.strftime("%Y%m%dT%H%M%SZ%z")}\n"
            elif (type(value) is list):
                if (attr.upper() in ["ATTENDEE", "ATTACH"]):
                    for elt in value:
                        result += f"{str(elt)}\n"
            else:
                result += f"{value}\n"

        result += f"END:{name}"
        return result
    
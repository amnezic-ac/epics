from datetime import datetime

class Component():

    uid = 1

    def __init__(self):
        self.uid = Component.uid
        Component.uid += 1


    def __str__(self, name: str):
        result = "BEGIN:"

        if (name not in ["VALARM", "VEVENT", "VFEEBUSY", "VJOURNAL", "VTODO"]):
            raise Exception(f"{name} is not a valid component.")

        result += f"{name}\n"

        for attr, value in self.__dict__.items():
            if (not value):
                continue
            elif (attr in ["recurrid", "relatedto"]):
                if (attr == "recurrid"):
                    result += f"RECURRENCE"
            elif (type(value) is datetime):
                result += f"{attr.upper()}:{value.strftime("%Y%m%dT%H%M%SZ%z")}\n"
            elif (attr == "uid"):
                result += f"UID:{self.uid}\n"
            else:
                result += f"{value}\n"

        result += f"END:{name}"
        return result
    
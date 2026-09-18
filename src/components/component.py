class Component():

    def __init__(self):
        self.uid = None


    def __str__(self, name: str):
        result = "BEGIN:"

        if (name not in ["VALARM", "VEVENT", "VFEEBUSY", "VJOURNAL", "VTODO"]):
            raise Exception(f"{name} is not a valid component.")

        result += f"{name}\n"

        for attr, value in self.__dict__.items():
            if (attr in ["recurrid", "relatedto"]):
                if (attr == "recurrid"):
                    result += f"RECURRENCE"
            elif (type(value) is str):
                result += f"{attr.upper()}:{value}\n"
            else:
                esult += f"{attr.upper()}:{value}\n"

        result += f"END:{name}"
        return result
    
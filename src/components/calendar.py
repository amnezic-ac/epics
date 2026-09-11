class Calendar():

    def __init__(uid: str = "uid"):
        self.componants = []

    def __str__(self):
        result = """
        BEGIN:VCALENDAR
        VERSION:2.0
        PRODID:MyICSCalendar
        """

        # adding the componants

        result += """
        END:VEVENT
        END:VCALENDA
        """

        return result
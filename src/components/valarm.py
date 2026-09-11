class Valarm():
    # for further information, please refer to 3.6.6

    uid = 1

    def __init__():
        self.uid = Valarm.uid
        Valarm.uid += 1

    def __str__(self):
        result = f"""
        BEGIN:VALARM
        UID:{self.uid}
        """

        result += """
        END:VALARM
        """
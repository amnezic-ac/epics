from src.backend.components.calendar import Calendar
from src.gui.imports import *
from src.gui.components import calendar
from src.utils import exportConfigToJSONFile

def main():
    logging.debug(f"New session activated")

    root = tk.Tk()
    root.rowconfigure(0, weight=1)
    root.columnconfigure(0, weight=1)


    dico = {}
    frame = calendar.foo(root, dico)
    frame.grid(row=0, column=0, sticky="nsew")
    root.mainloop()

    exportConfigToJSONFile("default_config.json", configuration)
    logging.debug(f"Session ended")

# def main():
#     myCalendar = Calendar()
#     tmstp = datetime.now()
# 
#     myEvent = Vevent(tmstp, tmstp, tmstp + timedelta(hours=2))
#     myCalendar.add_component(myEvent)
# 
#     print(myCalendar)
# 
# main()
from src.backend.components.calendar import Calendar
from src.gui.imports import *
from src.gui.components import calendar
from src.utils import exportConfigToJSONFile

# for testing only
from src.gui.properties.descriptive import makeResourceFrame
from uuid import uuid4
##################

def main():
    logging.debug(f"New session activated")

    root = tk.Tk()
    root.rowconfigure(0, weight=1)
    root.columnconfigure(0, weight=1)


    dico = {}
    # frame = makeResourceFrame(root, dico, uuid4())
    frame = calendar.makeCalendarFrame(root, dico)
    frame.grid(row=0, column=0, sticky="nsew")
    root.mainloop()

    exportConfigToJSONFile("configuration.json", configuration)
    logging.debug(f"Session ended")

main()
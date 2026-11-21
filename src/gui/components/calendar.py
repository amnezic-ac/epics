import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import filedialog as fd
from src.gui.components.event import makeEventFrame
from src.utils import exportConfigToJSONFile
from src.backend.components.calendar import Calendar
import uuid

from src.utils import configuration, logging

def export(calendar: Calendar, notebook):
    if (not calendar):
        logging.warning(f"User attempted to add an unexisting calendar. Should display (not implemented yet) a warning popup")
        return None

    # Open dialog
    file_path = fd.asksaveasfilename(
        defaultextension=".ics",
        filetypes=[("ICal files", "*.ics"), ("Text files", "*.txt"), ("All files", "*.*")],
        title="Save File"
    )

    # Check if user selected a file (not cancelled)
    if file_path:
        with open(file_path, 'w') as f:
            f.write(str(calendar))
            logging.info(f"Calendar successfully saved with {len(calendar.components)} component(s)")
            notebook.destroy()
    else:
        logging.warning("Save operation cancelled.")


def foo(root: tk.frame, holder: dict) -> tk.Frame:
    id_ = uuid.uuid4()
    logging.debug(f"User opened a calendar creation frame (uuid: {id_})")
    notebook = ttk.Notebook(root)
    # list containing all components of the calendar
    components = []

    # frame that will contain features button
    main = ttk.Frame(notebook)

    # frame for letting the user type the calendar name
    calendarTitleFrame = ttk.LabelFrame(main, text="Calendar name")
    calendarTitle = tk.StringVar()
    calendarTitleEntry = ttk.Entry(calendarTitleFrame, textvariable=calendarTitle)
    calendarTitleEntry.grid()
    calendarTitleFrame.grid()

    # let the user open a new event
    def addEvent():
        logging.debug(f"User began to add an event to {calendarTitle.get()} calendar ({id_})")
        eventHolder = {}
        eventFrame = makeEventFrame(notebook, eventHolder)
        notebook.add(eventFrame, text="New event")
        components.append(eventHolder)
        # redirect automatically the user to the new frame
        notebook.select(eventFrame)
        # let the tab title update in real time
        def updateSummary(event):
            notebook.tab(eventFrame, text=eventHolder["titleEntry"].get())
        eventHolder["titleEntry"].bind('<KeyRelease>', updateSummary)
    addButton = ttk.Button(main, text="Add a new event", command=addEvent)
    addButton.grid()
    notebook.add(main, text="Main")

    # let the user clear the calendar
    def clearCalendar():
        logging.debug(f"User attempt to clear {calendarTitle.get()} calendar ({id_})")
        if (len(components) == 0):
            logging.debug(f"{calendarTitle.get()} can't be clear: no component yet")
            return
        confirmation = messagebox.askyesno(
            message=f"Are you sure to reset {calendarTitle.get()} calendar ?",
            icon="question",
            title="Confirm"
        )
        if (not confirmation):
            logging.debug(f"User cancelled {calendarTitle.get()} clear ({id_})")
            return
        components.clear() 
        tabs = notebook.tabs()
        for i in range(len(tabs)-1, 0, -1):
            notebook.forget(i)
        logging.debug(f"{calendarTitle.get} calendar ({id_}) cleared")
    clearButton = ttk.Button(main, text="Clear the calendar", command=clearCalendar)
    clearButton.grid()

    def exportCalendar():
        if (components == []):
            return None
        calendar = Calendar(id_)
        for holder in components:
            component = holder["getValue"]()
            calendar.add_component(component)
        export(calendar, notebook)
    exportButton = ttk.Button(main, text="Create calendar", command=exportCalendar)
    exportButton.grid()

    return notebook
import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import filedialog as fd
from src.gui.components.event import makeEventFrame
from src.backend.components.calendar import Calendar
import uuid
from src.utils import logging

def export(calendar: Calendar, notebook):
    if (not calendar):
        logging.warning(f"[Calendar {calendar.uid}] User attempted to add a None calendar object")
        return None

    file_path = fd.asksaveasfilename(
        defaultextension=".ics",
        filetypes=[("ICal files", "*.ics"), ("Text files", "*.txt"), ("All files", "*.*")],
        title="Save File"
    )

    # save the calendar only if a file has been selected
    if file_path:
        with open(file_path, 'w') as f:
            # calendar does not have any categories
            f.write(str(calendar))
            logging.info(f"[Calendar {calendar.uid}] Calendar successfully saved with {len(calendar.components)} component(s)")
    else:
        logging.warning(f"[Calendar {calendar.uid}] Save operation cancelled.")


def makeCalendarFrame(root: tk.frame, holder: dict) -> tk.Frame:
    id_ = uuid.uuid4()
    logging.debug(f"[Calendar {id_}] User opened a calendar creation frame")
    notebook = ttk.Notebook(root)
    # list containing all components of the calendar
    components = []

    # frame that will contain feature buttons
    main = ttk.Frame(notebook)

    # frame for letting the user type the calendar name
    calendarTitleFrame = ttk.LabelFrame(main, text="Calendar name")
    calendarTitle = tk.StringVar()
    calendarTitleEntry = ttk.Entry(calendarTitleFrame, textvariable=calendarTitle)
    calendarTitleEntry.grid()
    calendarTitleFrame.grid()

    # let the user open a new event
    def addEvent():
        logging.debug(f"[Calendar {id_}] User began to add an event to {calendarTitle.get()} calendar")
        eventHolder = {}
        eventFrame = makeEventFrame(notebook, eventHolder, id_)
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
        logging.debug(f"[Calendar {id_}] User attempt to clear {calendarTitle.get()} calendar")
        if (len(components) == 0):
            logging.warn(f"[Calendar {id_}] User attempted to clear an empty calendar ({calendarTitle.get()})")
            return
        confirmation = messagebox.askyesno(
            message=f"Are you sure to reset {calendarTitle.get()} calendar ?",
            icon="question",
            title="Confirm"
        )
        if (not confirmation):
            logging.warn(f"[Calendar {id_}] User cancelled {calendarTitle.get()} clear ({id_})")
            return
        components.clear() 
        tabs = notebook.tabs()
        for i in range(len(tabs)-1, 0, -1):
            notebook.forget(i)
        logging.debug(f"[Calendar {id_}] User cleared {calendarTitle.get()} calendar")
    clearButton = ttk.Button(main, text="Clear the calendar", command=clearCalendar)
    clearButton.grid()

    def exportCalendar():
        if (components == []):
            logging.warn(f"[Calendar {id_}] User tried to export an empty calendar")
            return None
        calendar = Calendar(id_)
        for holder in components:
            component = holder["getValue"]()
            # the component does not have any categories
            calendar.add_component(component)
        export(calendar, notebook)
    exportButton = ttk.Button(main, text="Create calendar", command=exportCalendar)
    exportButton.grid()

    return notebook
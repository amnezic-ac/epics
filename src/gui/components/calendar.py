import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import filedialog as fd
from src.gui.components.event import makeEventFrame
from src.utils import exportConfigToJSONFile
from src.backend.components.calendar import Calendar

def export(calendar: Calendar):
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
    else:
        logging.warning("Save operation cancelled.")


def foo(root: tk.frame, holder: dict, configuration: dict) -> tk.Frame:
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
        eventHolder = {}
        eventFrame = makeEventFrame(notebook, eventHolder, configuration)
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
        if (len(components) == 0):
            return
        confirmation = messagebox.askyesno(
            message=f"Are you sure to reset {calendarTitle.get()} calendar ?",
            icon="question",
            title="Confirm"
        )
        if (not confirmation):
            return
        components.clear() 
        tabs = notebook.tabs()
        for i in range(len(tabs)-1, 0, -1):
            notebook.forget(i)
    clearButton = ttk.Button(main, text="Clear the calendar", command=clearCalendar)
    clearButton.grid()

    return notebook


# def create(master):
#     root = tk.Toplevel(master)
#     notebook = ttk.Notebook(root)
#     notebook.pack(expand=True, fill='both')
#     events = []
#     main = tk.Frame(notebook)
#     notebook.add(main, text="Main")
#     logging.debug(f"Calendar notebook created")
# 
#     calendar = None
# 
#     buttonsFrame = tk.Frame(main)
#     def addEvent():
#         title = tk.StringVar(value="New event")
#         eventHolder = {"value": None}
#         eventFrame = makeEventFrame(notebook, eventHolder)
#         notebook.add(eventFrame, text="New event")
#         events.append(eventHolder)
#     eventButton = tk.Button(buttonsFrame, text="Create new event", command=addEvent)
#     eventButton.pack()
# 
#     def submit():
#         calendar = Calendar()
#         for event in events:
#             if (event["value"]):
#                 calendar.add_component(event["value"])
#         export(calendar)
#     submitButton = tk.Button(buttonsFrame, text="Submit", command=submit)
#     submitButton.pack()
#     buttonsFrame.pack()
#     
#     def tab_selected(event):
#         notebook = event.widget
#         tab_id = notebook.select()
#         tab_text = notebook.tab(tab_id, 'text')
#     notebook.bind("<<NotebookTabChanged>>", tab_selected)
# 
#     return root, None
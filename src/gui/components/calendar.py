import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
from src.gui.components.event import makeEventFrame
from src.utils import configuration, exportConfigToJSONFile, logging
from src.backend.components.calendar import Calendar

def export(root: tk.Frame, calendar: Calendar):
    if (not calendar):
        logging.warning(f"User attempted to add an empty calendar. Should display (not implemented yet) a warning popup")
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
            logging.info(f"Calendar successfully saved")
    else:
        logging.warning("Save operation cancelled.")



def create(master):
    root = tk.Toplevel(master)
    notebook = ttk.Notebook(root)
    notebook.pack(expand=True, fill='both')
    events = []
    main = tk.Frame(notebook)
    notebook.add(main, text="Main")
    logging.debug(f"Calendar notebook created")

    calendar = None

    buttonsFrame = tk.Frame(main)
    def addEvent():
        title = tk.StringVar(value="New event")
        eventHolder = {"value": None}
        eventFrame = makeEventFrame(notebook, eventHolder)
        notebook.add(eventFrame, text="New event")
        events.append(eventHolder)
        print("eventHolder added to the list")
    eventButton = tk.Button(buttonsFrame, text="Create new event", command=addEvent)
    eventButton.pack()

    def submit():
        calendar = Calendar()
        for event in events:
            if (event["value"]):
                calendar.add_component(event["value"])
        print(str(calendar))
        export(root, calendar)
    submitButton = tk.Button(buttonsFrame, text="Submit", command=submit)
    submitButton.pack()
    buttonsFrame.pack()
    
    def tab_selected(event):
        notebook = event.widget
        tab_id = notebook.select()
        tab_text = notebook.tab(tab_id, 'text')
    notebook.bind("<<NotebookTabChanged>>", tab_selected)

    return root, None
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
from src.gui.components.event import makeEventFrame
from src.utils import configuration, exportConfigToJSONFile, logging
from src.backend.components.calendar import Calendar


def handleCalendarCreation(master):
    root = tk.Toplevel(master)
    notebook = ttk.Notebook(root)
    notebook.pack(expand=True, fill='both')
    events = []
    main = tk.Frame(notebook)
    notebook.add(main, text="Main")
    logging.debug(f"Calendar notebook created")

    calendar = Calendar()

    buttonsFrame = tk.Frame(main)
    def addEvent():
        title = tk.StringVar(value="New event")
        eventFrame, eventDict = makeEventFrame(notebook, title)
        notebook.add(eventFrame, text=f"{title.get()}")
        events.append(eventDict)
    eventButton = tk.Button(buttonsFrame, text="Create new event", command=addEvent)
    eventButton.pack()
    # taskButton = tk.Button(buttonsFrame, text="Create new task", command=None)
    # taskButton.pack()
    # alarmButton = tk.Button(buttonsFrame, text="Create new alarm", command=None)
    # alarmButton.pack()
    # journalButton = tk.Button(buttonsFrame, text="Create new journal", command=None)
    # journalButton.pack()
    def submit():
        for event in events:
            calendar.add_component(event["value"])
        print(str(calendar))
    submitButton = tk.Button(buttonsFrame, text="Submit", command=submit)
    submitButton.pack()
    buttonsFrame.pack()
    
    def tab_selected(event):
        notebook = event.widget
        tab_id = notebook.select()
        tab_text = notebook.tab(tab_id, 'text')
    notebook.bind("<<NotebookTabChanged>>", tab_selected)

    return root, None
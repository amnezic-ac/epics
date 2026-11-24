from src.gui.imports import *
from datetime import date, datetime
import tkcalendar as tkc
from src.backend.properties.datetime import Transparency, Duration

# TODO
def makeDurationFrame(root):
    frame = tk.Frame(root)

    week = tk.StringVar(value="0")
    weekEntry = tk.Spinbox(frame, textvariable=week, width=3, from_=0, wrap=True, justify=tk.RIGHT)
    weekEntry.pack(side="left")
    tk.Label(frame, text=configuration["duration"]["week-text"]).pack(side="left")
    day = tk.StringVar(value="")
    dayEntry = tk.Spinbox(frame, textvariable=day, width=2, from_=0, to=31, wrap=True, justify=tk.RIGHT)
    dayEntry.pack(side="left")
    tk.Label(frame, text=configuration["duration"]["day-text"]).pack(side="left")
    hour = tk.StringVar(value="")
    hourEntry = tk.Spinbox(frame, textvariable=hour, width=2, from_=0, to=23, wrap=True, justify=tk.RIGHT)
    hourEntry.pack(side="left")
    tk.Label(frame, text=configuration["duration"]["hour-text"]).pack(side="left")
    minute = tk.StringVar(value="")
    minuteEntry = tk.Spinbox(frame, textvariable=minute, width=2, from_=0, to=59, wrap=True, justify=tk.RIGHT)
    minuteEntry.pack(side="left")
    tk.Label(frame, text=configuration["duration"]["minute-text"]).pack(side="left")
    second = tk.StringVar(value="")
    secondEntry = tk.Spinbox(frame, textvariable=second, width=2, from_=0, to=59, wrap=True, justify=tk.RIGHT)
    secondEntry.pack(side="left")
    tk.Label(frame, text=configuration["duration"]["second-text"]).pack(side="left")

    valueHolder = {
        "week": week,
        "day": day,
        "hour": hour,
        "minute": minute,
        "second": second
    }

    return frame, valueHolder

# TODO: put default value for start are now and for end its start + default duration
def makeDtFrame(root, typename: str, valueHolder: dict, componentId) -> tk.Frame:
    frame = tk.Frame(root)
    timestamp = datetime.now()

    if (typename not in ["start", "end"]):
        logging.error(f"[Component {componentId}] {typename} is not a valid typename value for datime frame creation (should be \"start\" or \"end\")")

    labeltext = "From" if typename == "start" else "to"
    label = tk.Label(frame, text=labeltext)
    label.grid(row=0, column=0)

    dateEntry = tkc.DateEntry(
        frame,
        selectmode="day",
        date_pattern="y/mm/dd"
    )
    dateEntry.grid(row=0, column=1)
    # line below is mandatroy: let the calendar be clickable even if there is a widget below it on the z-axis
    dateEntry._top_cal.lift()

    # check that user inpput for spinboxes are valid
    def validateSpinboxInputWhenKey(max, text):
        if (not text):
            return True
        if (text and len(text) > 2):
            return False
        try:
            tmp = int(text)
            return tmp >= 0 and tmp <= max
        except:
            return False

    timelabel = tk.Label(frame, text=" at ")
    hour = tk.StringVar(value="0")
    hourSpinbox = ttk.Spinbox(
        frame,
        from_=0,
        to=23,
        increment=1,
        width=3,
        textvariable=hour,
        wrap=True,
        validate="key", # this line and the one below ensure that what is typed in the keyboard is a valid value
        validatecommand=(frame.register(lambda t: validateSpinboxInputWhenKey(23, t)), "%P")
    )
    hourLabel = tk.Label(frame, text="h ")
    minute = tk.StringVar(value="0")
    minuteSpinbox = ttk.Spinbox(
        frame,
        from_=0,
        to=59,
        increment=1,
        width=3,
        textvariable=minute,
        wrap=True,
        validate="key",
        validatecommand=(frame.register(lambda t: validateSpinboxInputWhenKey(59, t)), "%P")
    )
    minuteLabel = tk.Label(frame, text="m ")
    second = tk.StringVar(value="0")
    secondSpinbox = ttk.Spinbox(
        frame,
        from_=0,
        to=59,
        increment=1,
        width=3,
        textvariable=second,
        wrap=True,
        validate="key",
        validatecommand=(frame.register(lambda t: validateSpinboxInputWhenKey(59, t)), "%P")
    )
    secondLabel = tk.Label(frame, text="s")

    # let a datetime got time or not
    state = tk.BooleanVar(value=configuration["general"]["timestate"])
    def addTime():
        timelabel.grid(row=0, column=2)
        hourSpinbox.grid(row=0, column=3)
        hourLabel.grid(row=0, column=4)
        minuteSpinbox.grid(row=0, column=5)
        minuteLabel.grid(row=0, column=6)
        secondSpinbox.grid(row=0, column=7)
        secondLabel.grid(row=0, column=8)
    valueHolder["addTime"] = addTime
    def removeTime():
        timelabel.grid_remove()
        hourSpinbox.grid_remove()
        hourLabel.grid_remove()
        minuteSpinbox.grid_remove()
        minuteLabel.grid_remove()
        secondSpinbox.grid_remove()
        secondLabel.grid_remove()
    valueHolder["removeTime"] = removeTime


    def getDT():
        try:
            actual = state.get()
            tmp = datetime(
                year = int(dateEntry.get_date().strftime("%Y")),
                month = int(dateEntry.get_date().strftime("%m")),
                day = int(dateEntry.get_date().strftime("%d")),
                hour = int(hour.get()) if actual else None,
                minute = int(minute.get()) if actual else None,
                second = int(second.get()) if actual else None
            )
            # logging.debug(f"Timestamp successfully created ({typename})")
            return tmp
        except:
            logging.error(f"[Component {componentId}] Unable to create the {typename} timestamp")
            return None
    valueHolder["getValue"] = getDT

    return frame

def makeTranspFrame(root: tk.Frame, valueHolder: dict) -> tk.Frame:
    frame = tk.Frame(root)

    value = tk.StringVar(value=configuration["choices"][0])
    transpCombobox = ttk.Combobox(
        frame,
        values=configuration["tranparency"]["choices"],
        state=["readonly"],
        textvariable=value
    )
    # avoid the selected item to be blue highlighted
    combobox.bind('<<ComboboxSelected>>', lambda e: e.widget.selection_clear())
    transpCombobox.grid()

    ToolTip(transpCombobox, msg="Tells if the event should block overlapping events")

    def getTransp():
        if (not value.get()):
            return None
        
        try:
            tmp = Transparency(value.get())
            logging.debug(f"Transp successfully created")
            return tmp
        except:
            logging.error(f"Unable to create transp")
            return None
    valueHolder["getValue"] = getTransp

    return frame

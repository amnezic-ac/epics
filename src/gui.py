from tkinter import *
from tkcalendar import Calendar, DateEntry
from datetime import datetime

from gui_property import *


main_window = Tk()
main_window.title("ICS generator")

attachement_frame = make_attachement_frame(main_window)
attachement_frame.pack()

main_window.mainloop()
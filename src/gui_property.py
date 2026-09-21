from properties import *
from tkinter import *

def make_attachement_frame(master_frame):
    attachement_frame = Frame(master_frame)

    ### Attachment value
    value_frame = Frame(attachement_frame)
    value_label = Label(value_frame, text="value")
    value_entry = Entry(value_frame)
    value_label.pack(side=LEFT)
    value_entry.pack(side=RIGHT)
    value_frame.pack(anchor="w")

    ### If there is an encoding
    encoding_frame = Frame(attachement_frame, padx=1, pady=1)
    isEncodingCheckBoxChecked = BooleanVar(value=False)
    isAlreadyAnEncodingValue = BooleanVar(value = False)
    encodingEntryValue = StringVar(value=None)
    encoding_entry_frame = Frame(encoding_frame)

    def toggle_encoding_entry_frame():
        test_bool = isEncodingCheckBoxChecked.get()
        if isEncodingCheckBoxChecked.get():
            encoding_checkbox.pack(side=LEFT)
            if (not isAlreadyAnEncodingValue.get()):
                entry = Entry(encoding_entry_frame, textvariable=encodingEntryValue)
                entry.pack()
                isAlreadyAnEncodingValue.set(True)
            encoding_entry_frame.pack(side="right")
        else:
            encoding_entry_frame.pack_forget()

    encoding_checkbox = Checkbutton(encoding_frame, text="Encoding ? ", variable=isEncodingCheckBoxChecked, onvalue=True, offvalue=False, command=toggle_encoding_entry_frame)
    encoding_checkbox.pack()
    encoding_frame.pack(anchor="w")
    
    ### If there is (sub)type
    type_frame = Frame(attachement_frame)
    isTypeCheckBoxchecked = BooleanVar(value=False)
    isAlreadyTypeValue = BooleanVar(value = False)
    typeEntryValue = StringVar(value="")
    subtypeEntryValue = StringVar(value="")
    typesEntryFrame = Frame(type_frame)

    def toggle_type_entry_frame():
        if isTypeCheckBoxchecked.get():
            type_checkbox.pack(side="left")
            if (not isAlreadyTypeValue.get()):
                Entry(typesEntryFrame, textvariable=typeEntryValue).pack(side=RIGHT)
                Label(typesEntryFrame, text="/").pack(side=RIGHT)
                Entry(typesEntryFrame, textvariable=subtypeEntryValue).pack(side=RIGHT)
                isAlreadyTypeValue.set(True)
            typesEntryFrame.pack(side="right")
        else:
            typesEntryFrame.pack_forget()

    type_checkbox = Checkbutton(type_frame, text="Type ? ", variable=isTypeCheckBoxchecked, onvalue=True, offvalue=False, command=toggle_type_entry_frame)
    type_checkbox.pack()
    type_frame.pack(anchor="w")

    def submit_attachement():
        value_error_label = Label(value_frame, text="Unable to add an empty value, please put a value or unchecked the encoding checkbox")
        if (value_entry.get() == ""):
            value_error_label.pack(side="right")
            return None

        value_error_label.pack_forget()
        typename = typeEntryValue.get() if typeEntryValue.get() != "" else None
        subtypename = subtypeEntryValue.get() if subtypeEntryValue.get() != "" else None
        encoding = encodingEntryValue.get()
        attachement = Attachement(value_entry.get(), encoding=encoding, typename=typename, subtypename=subtypename)
        print(attachement)

    Button(attachement_frame, text="Submit", command=submit_attachement).pack()

    return attachement_frame

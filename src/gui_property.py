from properties import *
from tkinter import *
from components.component import Component


def make_attachement_frame(master_frame):
    attachement_frame = Frame(master_frame)

    ### Attachment value
    value_frame = Frame(attachement_frame)
    value_label = Label(value_frame, text="value : ")
    value_entry = Entry(value_frame)
    value_label.pack(side="left", anchor="w")
    value_entry.pack(side=RIGHT, anchor="e")
    value_frame.pack()

    ### If there is an encoding
    encoding_frame = Frame(attachement_frame, padx=1, pady=1)
    isEncodingCheckBoxChecked = BooleanVar(value=False)
    isAlreadyAnEncodingValue = BooleanVar(value = False)
    encodingEntryValue = StringVar(value=None)
    encoding_entry_frame = Frame(encoding_frame)

    def toggle_encoding_entry_frame():
        test_bool = isEncodingCheckBoxChecked.get()
        if isEncodingCheckBoxChecked.get():
            encoding_checkbox.pack(side=LEFT, anchor="w")
            if (not isAlreadyAnEncodingValue.get()):
                encoding_checkbox.config(text="Encoding : ")
                entry = Entry(encoding_entry_frame, textvariable=encodingEntryValue)
                entry.pack(side="right", anchor="e")
                isAlreadyAnEncodingValue.set(True)
            encoding_entry_frame.pack()
        else:
            encoding_checkbox.config(text="Encoding ? ")
            encoding_entry_frame.pack_forget()

    encoding_checkbox = Checkbutton(encoding_frame, text="Encoding ? ", variable=isEncodingCheckBoxChecked, onvalue=True, offvalue=False, command=toggle_encoding_entry_frame)
    encoding_checkbox.pack(side="left", anchor="w")
    encoding_frame.pack()
    
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
                type_checkbox.config(text="type/subtype : ")
                Entry(typesEntryFrame, textvariable=typeEntryValue).pack(side=RIGHT, anchor="e")
                Label(typesEntryFrame, text="/").pack(side=RIGHT)
                Entry(typesEntryFrame, textvariable=subtypeEntryValue).pack(side=RIGHT)
                isAlreadyTypeValue.set(True)
            typesEntryFrame.pack()
        else:
            type_checkbox.config(text="Type ? ")
            typesEntryFrame.pack_forget()

    type_checkbox = Checkbutton(type_frame, text="Type ? ", variable=isTypeCheckBoxchecked, onvalue=True, offvalue=False, command=toggle_type_entry_frame)
    type_checkbox.pack(side="left", anchor="w")
    type_frame.pack()

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

    Button(attachement_frame, text="Submit", command=submit_attachement).pack()

    return attachement_frame

def make_categories_frame(master_frame, configuration):
    categoriesFrame = Frame(master_frame)

    hiddableFrame = Frame(categoriesFrame)

    userInputFrame = Frame(hiddableFrame)
    listbox = Listbox(userInputFrame, selectmode=MULTIPLE)
    for i in range (len(configuration["choices"])):
        listbox.insert(i, configuration["choices"][i])
    listbox.config(height=min(len(configuration["choices"]), configuration["categories_view_height"]))
    listbox.pack(side="top")
    entry = Entry(userInputFrame)
    entry.pack(side="bottom")
    userInputFrame.pack(side="left")

    buttonsFrame = Frame(hiddableFrame)
    def add():
        if (entry.get().upper() not in listbox.get(0, listbox.size()-1) and entry.get().strip() != ""):
            listbox.insert(listbox.size(), entry.get().upper())
            entry.delete(0, END)

    addButton = Button(buttonsFrame, text="Add", command=add)
    addButton.pack()

    def addToConfig():
        add()
        if (entry.get().upper() not in configuration["choices"] and entry.get().strip() != ""):
            configuration["choices"].append(entry.get().upper())
    addToConfigButton = Button(buttonsFrame, text="Add to configuration", command=addToConfig)
    addToConfigButton.pack()

    def delete():
        choices = listbox.curselection()
        if (type(choices) is int):
            listbox.delete(choices)
        else:
            for choice in choices[::-1]:
                listbox.delete(choice)
        return choices
    deleteButton = Button(buttonsFrame, text="Delete", command=delete)
    deleteButton.pack()
    
    def deleteFromConfig():
        choices = delete()
        if (type(choices) is int):
            configuration["choices"].pop(choices)
        else:
            for choice in choices[::-1]:
                configuration["choices"].pop(choice)
    deleteFromConfigButton = Button(buttonsFrame, text="Delete from configuration", command=deleteFromConfig)
    deleteFromConfigButton.pack()

    buttonsFrame.pack(side="right")

    checkbuttonState = BooleanVar(value=False)
    def toggleCategoriesMenu():
        if (checkbuttonState.get()):
            checkbutton.config(text="Categories : ")
            hiddableFrame.pack(side="right")
        else:
            hiddableFrame.pack_forget()
            checkbutton.config(text="Categories ? ")
    checkbutton = Checkbutton(categoriesFrame, text="Categories ? ", variable=checkbuttonState, onvalue=True, offvalue=False, command=toggleCategoriesMenu)
    checkbutton.pack(side="left",anchor="w")

    return categoriesFrame

def make_classification_frame(master_frame, configuration):
    classificationFrame = Frame(master_frame)

    hiddableFrame = Frame(classificationFrame)

    userInputFrame = Frame(hiddableFrame)
    listbox = Listbox(userInputFrame)
    for i in range(len(configuration["choices"])):
        listbox.insert(i, configuration["choices"][i])
    listbox.config(height=min(len(configuration["choices"]), configuration["classification_view_height"]))
    listbox.pack(side="top")
    entry = Entry(userInputFrame)
    entry.pack(side="bottom")
    userInputFrame.pack(side="left")

    buttonsFrame = Frame(hiddableFrame)
    def add():
        if (entry.get().upper() not in listbox.get(0, listbox.size()-1) and entry.get().strip() != ""):
            listbox.insert(listbox.size(), entry.get().upper())
            entry.delete(0, END)

    addButton = Button(buttonsFrame, text="Add", command=add)
    addButton.pack()

    def addToConfig():
        add()
        if (entry.get().upper() not in configuration["choices"] and entry.get().strip() != ""):
            configuration["choices"].append(entry.get().upper())
    addToConfigButton = Button(buttonsFrame, text="Add to configuration", command=addToConfig)
    addToConfigButton.pack()

    def delete():
        choice = listbox.curselection()
        listbox.delete(choice)
        return choice
    deleteButton = Button(buttonsFrame, text="Delete", command=delete)
    deleteButton.pack()
    
    def deleteFromConfig():
        choice = delete()
        configuration["choices"].pop(choice[0])
    deleteFromConfigButton = Button(buttonsFrame, text="Delete from configuration", command=deleteFromConfig)
    deleteFromConfigButton.pack()

    def submit():
        choice = None
        try:
            choice = configuration["choices"][listbox.curselection()[0]]
        except Exception as _:
            pass
        else:
            if (choice and choice.strip() != ""):
                classification = Classification(choice)
    submitButton = Button(buttonsFrame, text="Submit", command=submit)
    submitButton.pack()
    buttonsFrame.pack(side="right")

    checkbuttonState = BooleanVar(value=False)
    def toggleClassificationMenu():
        if (checkbuttonState.get()):
            hiddableFrame.pack(side="right")
        else:
            hiddableFrame.pack_forget()

    checkbutton = Checkbutton(classificationFrame, text="Classification ? ", variable=checkbuttonState, onvalue=True, offvalue=False, command=toggleClassificationMenu)
    checkbutton.pack(side="left",anchor="w")

    return classificationFrame
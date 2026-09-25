from properties import *
from tkinter import ttk
import tkinter as tk
from components.component import Component


def make_attachement_frame(master_frame):
    attachement_frame = tk.Frame(master_frame)

    ### Attachment value
    value_frame = tk.Frame(attachement_frame)
    value_label = tk.Label(value_frame, text="value : ")
    value_entry = tk.Entry(value_frame)
    value_label.pack(side="left", anchor="w")
    value_entry.pack(side=RIGHT, anchor="e")
    value_frame.pack()

    ### If there is an encoding
    encoding_frame = tk.Frame(attachement_frame, padx=1, pady=1)
    isEncodingCheckBoxChecked = tk.BooleanVar(value=False)
    isAlreadyAnEncodingValue = tk.BooleanVar(value = False)
    encodingEntryValue = tk.StringVar(value=None)
    encoding_entry_frame = tk.Frame(encoding_frame)

    def toggle_encoding_entry_frame():
        test_bool = isEncodingCheckBoxChecked.get()
        if isEncodingCheckBoxChecked.get():
            encoding_checkbox.pack(side=LEFT, anchor="w")
            if (not isAlreadyAnEncodingValue.get()):
                encoding_checkbox.config(text="Encoding : ")
                entry = tk.Entry(encoding_entry_frame, textvariable=encodingEntryValue)
                entry.pack(side="right", anchor="e")
                isAlreadyAnEncodingValue.set(True)
            encoding_entry_frame.pack()
        else:
            encoding_checkbox.config(text="Encoding ? ")
            encoding_entry_frame.pack_forget()

    encoding_checkbox = tk.Checkbutton(encoding_frame, text="Encoding ? ", variable=isEncodingCheckBoxChecked, onvalue=True, offvalue=False, command=toggle_encoding_entry_frame)
    encoding_checkbox.pack(side="left", anchor="w")
    encoding_frame.pack()
    
    ### If there is (sub)type
    type_frame = tk.Frame(attachement_frame)
    isTypeCheckBoxchecked = tk.BooleanVar(value=False)
    isAlreadyTypeValue = tk.BooleanVar(value = False)
    typeEntryValue = tk.StringVar(value="")
    subtypeEntryValue = tk.StringVar(value="")
    typesEntryFrame = tk.Frame(type_frame)

    def toggle_type_entry_frame():
        if isTypeCheckBoxchecked.get():
            type_checkbox.pack(side="left")
            if (not isAlreadyTypeValue.get()):
                type_checkbox.config(text="type/subtype : ")
                tk.Entry(typesEntryFrame, textvariable=typeEntryValue).pack(side=RIGHT, anchor="e")
                tk.Label(typesEntryFrame, text="/").pack(side=RIGHT)
                tk.Entry(typesEntryFrame, textvariable=subtypeEntryValue).pack(side=RIGHT)
                isAlreadyTypeValue.set(True)
            typesEntryFrame.pack()
        else:
            type_checkbox.config(text="Type ? ")
            typesEntryFrame.pack_forget()

    type_checkbox = tk.Checkbutton(type_frame, text="Type ? ", variable=isTypeCheckBoxchecked, onvalue=True, offvalue=False, command=toggle_type_entry_frame)
    type_checkbox.pack(side="left", anchor="w")
    type_frame.pack()

    def submit_attachement():
        value_error_label = tk.Label(value_frame, text="Unable to add an empty value, please put a value or unchecked the encoding checkbox")
        if (value_entry.get() == ""):
            value_error_label.pack(side="right")
            return None

        value_error_label.pack_forget()
        typename = typeEntryValue.get() if typeEntryValue.get() != "" else None
        subtypename = subtypeEntryValue.get() if subtypeEntryValue.get() != "" else None
        encoding = encodingEntryValue.get()
        attachement = Attachement(value_entry.get(), encoding=encoding, typename=typename, subtypename=subtypename)

    tk.Button(attachement_frame, text="Submit", command=submit_attachement).pack()

    return attachement_frame

def make_categories_frame(master_frame, configuration):
    categoriesFrame = tk.Frame(master_frame)

    hiddableFrame = tk.Frame(categoriesFrame)

    userInputFrame = tk.Frame(hiddableFrame)
    listbox = Listbox(userInputFrame, selectmode=MULTIPLE)
    for i in range (len(configuration["choices"])):
        listbox.insert(i, configuration["choices"][i])
    listbox.config(height=min(len(configuration["choices"]), configuration["categories_view_height"]))
    listbox.pack(side="top")
    entry = tk.Entry(userInputFrame)
    entry.pack(side="bottom")
    userInputFrame.pack(side="left")

    buttonsFrame = tk.Frame(hiddableFrame)
    def add():
        if (entry.get().upper() not in listbox.get(0, listbox.size()-1) and entry.get().strip() != ""):
            listbox.insert(listbox.size(), entry.get().upper())
            entry.delete(0, END)

    addButton = tk.Button(buttonsFrame, text="Add", command=add)
    addButton.pack()

    def addToConfig():
        add()
        if (entry.get().upper() not in configuration["choices"] and entry.get().strip() != ""):
            configuration["choices"].append(entry.get().upper())
    addToConfigButton = tk.Button(buttonsFrame, text="Add to configuration", command=addToConfig)
    addToConfigButton.pack()

    def delete():
        choices = listbox.curselection()
        if (type(choices) is int):
            listbox.delete(choices)
        else:
            for choice in choices[::-1]:
                listbox.delete(choice)
        return choices
    deleteButton = tk.Button(buttonsFrame, text="Delete", command=delete)
    deleteButton.pack()
    
    def deleteFromConfig():
        choices = delete()
        if (type(choices) is int):
            configuration["choices"].pop(choices)
        else:
            for choice in choices[::-1]:
                configuration["choices"].pop(choice)
    deleteFromConfigButton = tk.Button(buttonsFrame, text="Delete from configuration", command=deleteFromConfig)
    deleteFromConfigButton.pack()

    buttonsFrame.pack(side="right")

    checkbuttonState = tk.BooleanVar(value=False)
    def toggleCategoriesMenu():
        if (checkbuttonState.get()):
            checkbutton.config(text="Categories : ")
            hiddableFrame.pack(side="right")
        else:
            hiddableFrame.pack_forget()
            checkbutton.config(text="Categories ? ")
    checkbutton = tk.Checkbutton(categoriesFrame, text="Categories ? ", variable=checkbuttonState, onvalue=True, offvalue=False, command=toggleCategoriesMenu)
    checkbutton.pack(side="left",anchor="w")

    return categoriesFrame

def make_classification_frame(master_frame, configuration):
    classificationFrame = tk.Frame(master_frame)

    hiddableFrame = tk.Frame(classificationFrame)

    userInputFrame = tk.Frame(hiddableFrame)
    listbox = Listbox(userInputFrame)
    for i in range(len(configuration["choices"])):
        listbox.insert(i, configuration["choices"][i])
    listbox.config(height=min(len(configuration["choices"]), configuration["classification_view_height"]))
    listbox.pack(side="top")
    entry = tk.Entry(userInputFrame)
    entry.pack(side="bottom")
    userInputFrame.pack(side="left")

    buttonsFrame = tk.Frame(hiddableFrame)
    def add():
        if (entry.get().upper() not in listbox.get(0, listbox.size()-1) and entry.get().strip() != ""):
            listbox.insert(listbox.size(), entry.get().upper())
            entry.delete(0, END)

    addButton = tk.Button(buttonsFrame, text="Add", command=add)
    addButton.pack()

    def addToConfig():
        add()
        if (entry.get().upper() not in configuration["choices"] and entry.get().strip() != ""):
            configuration["choices"].append(entry.get().upper())
    addToConfigButton = tk.Button(buttonsFrame, text="Add to configuration", command=addToConfig)
    addToConfigButton.pack()

    def delete():
        choice = listbox.curselection()
        listbox.delete(choice)
        return choice
    deleteButton = tk.Button(buttonsFrame, text="Delete", command=delete)
    deleteButton.pack()
    
    def deleteFromConfig():
        choice = delete()
        configuration["choices"].pop(choice[0])
    deleteFromConfigButton = tk.Button(buttonsFrame, text="Delete from configuration", command=deleteFromConfig)
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
    submitButton = tk.Button(buttonsFrame, text="Submit", command=submit)
    submitButton.pack()
    buttonsFrame.pack(side="right")

    checkbuttonState = tk.BooleanVar(value=False)
    def toggleClassificationMenu():
        if (checkbuttonState.get()):
            hiddableFrame.pack(side="right")
        else:
            hiddableFrame.pack_forget()

    checkbutton = tk.Checkbutton(classificationFrame, text="Classification ? ", variable=checkbuttonState, onvalue=True, offvalue=False, command=toggleClassificationMenu)
    checkbutton.pack(side="left",anchor="w")

    return classificationFrame

def make_comment_frame(master_frame, configuration):
    commentFrame = tk.Frame(master_frame)

    hiddableFrame = tk.Frame(commentFrame)

    commentTextFrame = tk.Frame(hiddableFrame)
    commentTextInput = tk.Text(commentTextFrame)
    commentTextInput.config(
        height=configuration["comment"]["comment_view_height"],
        width=configuration["comment"]["comment_view_width"]
    )
    commentTextInput.pack()
    commentTextFrame.pack()

    altrepFrame = tk.Frame(hiddableFrame)
    altrepText = tk.Text(altrepFrame)
    altrepText.config(
        height=configuration["comment"]["comment_view_height"],
        width=configuration["comment"]["comment_view_width"]
    )
    altrepCheckbuttonState = tk.BooleanVar(value=False)
    def toggleAltrepEntry():
        if (altrepCheckbuttonState.get()):
            altrepCheckbutton.config(text="Alternative representation : ")
            altrepText.pack()
        else:
            altrepCheckbutton.config(text="Alternative representation ? ")
            altrepText.pack_forget()
    altrepCheckbutton = tk.Checkbutton(altrepFrame, text="Alternative representation ? ", variable=altrepCheckbuttonState, onvalue=True, offvalue=False, command=toggleAltrepEntry)
    altrepCheckbutton.pack()
    altrepFrame.pack()

    languageFrame = tk.Frame(hiddableFrame)
    languageChoice = tk.StringVar(value="")
    languageComboBox = ttk.Combobox(languageFrame, textvariable=languageChoice)
    languageValues = []
    for language in configuration["languages"]:
        for language_id, description in language.items():
            languageValues.append(f"{language_id} ({description})")
    languageComboBox["values"] = languageValues
    languageComboBox['state'] = 'readonly'
    languageCheckbuttonState = tk.BooleanVar(value=False)
    def toggleLanguageMenu():
        if (languageCheckbuttonState.get()):
            languageCheckbutton.config(text="Language : ")
            languageComboBox.pack(side="right")
        else:
            languageCheckbutton.config(text="Language ? ")
            languageComboBox.pack_forget()
    languageCheckbutton = tk.Checkbutton(languageFrame, text="Language ? ", variable=languageCheckbuttonState, onvalue=True, offvalue=False, command=toggleLanguageMenu)
    languageCheckbutton.pack(side="left")
    languageFrame.pack()

    checkbuttonState = tk.BooleanVar(value=False)
    def toggleCommentText():
        if (checkbuttonState.get()):
            checkbutton.config(text="Comment : ")
            hiddableFrame.pack()
        else:
            checkbutton.config(text="Comment ? ")
            hiddableFrame.pack_forget()
    checkbutton = tk.Checkbutton(commentFrame, text="Comment ? ", variable=checkbuttonState, onvalue=True, offvalue=False, command=toggleCommentText)
    checkbutton.pack(side="top")

    return commentFrame

def make_description_frame(master_frame, configuration): # master_frame is the parent container of the entirely new frame and configuration a JSON object for minimal information
    descriptionFrame = tk.Frame(master_frame)

    hiddableFrame = tk.Frame(descriptionFrame)

    descriptionTextFrame = tk.Frame(hiddableFrame)
    descriptionTextInput = tk.Text(descriptionTextFrame)
    descriptionTextInput.config(
        height=configuration["description"]["description_view_height"],
        width=configuration["description"]["description_view_width"]
    )
    descriptionTextInput.pack()
    descriptionTextFrame.pack()

    altrepFrame = tk.Frame(hiddableFrame)
    altrepText = tk.Text(altrepFrame)
    altrepText.config(
        height=configuration["description"]["description_view_height"],
        width=configuration["description"]["description_view_width"]
    )
    altrepCheckbuttonState = tk.BooleanVar(value=False)
    def toggleAltrepEntry():
        if (altrepCheckbuttonState.get()):
            altrepCheckbutton.config(text="Alternative representation : ")
            altrepText.pack()
        else:
            altrepCheckbutton.config(text="Alternative representation ? ")
            altrepText.pack_forget()
    altrepCheckbutton = tk.Checkbutton(altrepFrame, text="Alternative representation ? ", variable=altrepCheckbuttonState, onvalue=True, offvalue=False, command=toggleAltrepEntry)
    altrepCheckbutton.pack()
    altrepFrame.pack()

    languageFrame = tk.Frame(hiddableFrame)
    languageChoice = tk.StringVar(value="")
    languageComboBox = ttk.Combobox(languageFrame, textvariable=languageChoice)
    languageValues = []
    for language in configuration["languages"]:
        for language_id, description in language.items():
            languageValues.append(f"{language_id} ({description})")
    languageComboBox["values"] = languageValues
    languageComboBox["state"] = "readonly"
    languageCheckbuttonState = tk.BooleanVar(value=False)
    def toggleLanguageMenu():
        if (languageCheckbuttonState.get()):
            languageCheckbutton.config(text="Language : ")
            languageComboBox.pack(side="right")
        else:
            languageCheckbutton.config(text="Language ? ")
            languageComboBox.pack_forget()
    languageCheckbutton = tk.Checkbutton(languageFrame, text="Language ? ", variable=languageCheckbuttonState, onvalue=True, offvalue=False, command=toggleLanguageMenu)
    languageCheckbutton.pack(side="left")
    languageFrame.pack()

    checkbuttonState = tk.BooleanVar(value=False)
    def toggleDescriptionText():
        if (checkbuttonState.get()):
            checkbutton.config(text="Description : ")
            hiddableFrame.pack()
        else:
            checkbutton.config(text="Description ? ")
            hiddableFrame.pack_forget()
    checkbutton = tk.Checkbutton(descriptionFrame, text="Description ? ", variable=checkbuttonState, onvalue=True, offvalue=False, command=toggleDescriptionText)
    checkbutton.pack(side="top")

    return descriptionFrame
from tkinter import ttk
import tkinter as tk

from src.backend.parameters import *
from utils import configuration

"""
Disclaimer
    Except the first two functions, all the other one have been AI generated for convenience purpose
"""

def makeAlternativeRepresentationFrame(masterFrame):
    altrepFrame = tk.Frame(masterFrame)

    hiddableFrame = tk.Frame(altrepFrame)
    altrepInput = tk.Text(hiddableFrame)
    altrepInput.config(
        height=configuration["altrep"]["height"],
        width=configuration["altrep"]["width"]
    )
    altrepInput.pack()

    state = tk.BooleanVar(value=False)
    def toggleHiddableFrame():
        if (state.get()):
            hiddableFrame.pack()
            button.config(text="Alternative representation")
        else:
            hiddableFrame.pack_forget()
            button.config(text="Alternative configuration ? ")
    button = tk.Checkbutton(altrepFrame, text="Alternative representation ? ", variable = state, offvalue=False, onvalue=True, command=toggleHiddableFrame)
    button.pack()

    return  altrepFrame, altrepInput

def makeCommonNameFrame(masterFrame):
    commonNameFrame = tk.Frame(masterFrame)

    hiddableFrame = tk.Frame(commonNameFrame)
    commonNameInput = tk.Entry(hiddableFrame)
    commonNameInput.pack()

    state = tk.BooleanVar(value=False)
    def toggleHiddableFrame():
        if (state.get()):
            hiddableFrame.pack(side="right")
            button.config(text="Common name : ")
        else:
            hiddableFrame.pack_forget()
            button.config(text="Common name ? ")
    button = tk.Checkbutton(commonNameFrame, text="Common name ? ", variable = state, offvalue=False, onvalue=True, command=toggleHiddableFrame)
    button.pack(side="left")

    return  commonNameFrame, commonNameInput

def makeCutypeFrame(masterFrame, configuration):
    cutypeFrame = tk.Frame(masterFrame)

    hiddableFrame = tk.Frame(cutypeFrame)
    userFrame = tk.Frame(hiddableFrame)
    value = tk.StringVar(value="")
    cutypeInput = ttk.Combobox(
        hiddableFrame,
        values=configuration["cutype"]["choices"],
        state="readonly",
        textvariable=value
    )
    cutypeInput.config(
        height=min(configuration["cutype"]["height"], len(configuration["cutype"]["choices"]))
    )
    cutypeInput.pack()

    userInput = tk.Entry(hiddableFrame)
    userInput.pack()
    userFrame.pack(side="left")

    def add():
        value = userInput.get()
        values = list(cutypeInput["values"])
        if value and value not in values:
            values.append(value)
            cutypeInput["values"] = values
            userInput.delete(0, tk.END)
            cutypeInput.set(cutypeInput["values"][-1])

    def addToConfiguration():
        value = userInput.get()
        if value and value not in configuration["cutype"]["choices"]:
            add()
            configuration["cutype"]["choices"].append(value)

    def remove():
        value = cutypeInput.get()
        values = list(cutypeInput["values"])
        if value in values:
            values.remove(value)
            cutypeInput["values"] = values
            userInput.delete(0, tk.END)
            if (len(cutypeInput["values"]) != 0):
                cutypeInput.set(values[0])
            else:
                cutypeInput.set("")

    def removeFromConfiguration():
        value = cutypeInput.get()
        if value in configuration["cutype"]["choices"]:
            remove()
            configuration["cutype"]["choices"].remove(value)

    buttonsFrame = tk.Frame(hiddableFrame)
    tk.Button(buttonsFrame, text="Add", command=add).pack()
    tk.Button(buttonsFrame, text="Add to configuration", command=addToConfiguration).pack()
    tk.Button(buttonsFrame, text="Remove", command=remove).pack()
    tk.Button(buttonsFrame, text="Remove from configuration", command=removeFromConfiguration).pack()
    buttonsFrame.pack(side="right")

    state = tk.BooleanVar(value=False)
    def toggleHiddableFrame():
        if (state.get()):
            hiddableFrame.pack(side="right")
            button.config(text="Calendar user type : ")
        else:
            hiddableFrame.pack_forget()
            button.config(text="Calendar user type ? ")
    button = tk.Checkbutton(cutypeFrame, text="Calendar user type ? ", variable = state, offvalue=False, onvalue=True, command=toggleHiddableFrame)
    button.pack(side="left")

    cutypeDict = {
        "state": state,
        "value": value
    }

    return cutypeFrame, cutypeDict

def makeDelegatedFromFrame(masterFrame):
    delegatedFromFrame = tk.Frame(masterFrame)

    hiddableFrame = tk.Frame(delegatedFromFrame)
    value = tk.StringVar(value="")
    delegatedFromInput = tk.Entry(hiddableFrame, textvariable=value)
    delegatedFromInput.pack()

    state = tk.BooleanVar(value=False)
    def toggleHiddableFrame():
        if (state.get()):
            hiddableFrame.pack(side="right")
            button.config(text="Delegated from : ")
        else:
            hiddableFrame.pack_forget()
            button.config(text="Delegated from ? ")
    button = tk.Checkbutton(delegatedFromFrame, text="Delegated from ? ", variable = state, offvalue=False, onvalue=True, command=toggleHiddableFrame)
    button.pack(side="left")

    delfromDict = {
        "state": state,
        "value": value
    }

    return delegatedFromFrame, delfromDict

def makeDelegatedToFrame(masterFrame):
    delegatedToFrame = tk.Frame(masterFrame)

    hiddableFrame = tk.Frame(delegatedToFrame)
    value = tk.StringVar(value="")
    delegatedToInput = tk.Entry(hiddableFrame, textvariable=value)
    delegatedToInput.pack()

    state = tk.BooleanVar(value=False)
    def toggleHiddableFrame():
        if (state.get()):
            hiddableFrame.pack(side="right")
            button.config(text="Delegated to : ")
        else:
            hiddableFrame.pack_forget()
            button.config(text="Delegated to ? ")
    button = tk.Checkbutton(delegatedToFrame, text="Delegated to ? ", variable = state, offvalue=False, onvalue=True, command=toggleHiddableFrame)
    button.pack(side="left")

    deltoDict = {
        "state": state,
        "value": value
    }

    return delegatedToFrame, deltoDict

def makeDirFrame(masterFrame):
    dirFrame = tk.Frame(masterFrame)

    hiddableFrame = tk.Frame(dirFrame)
    dirInput = tk.Entry(hiddableFrame)
    dirInput.pack()

    state = tk.BooleanVar(value=False)
    def toggleHiddableFrame():
        if (state.get()):
            hiddableFrame.pack(side="right")
            button.config(text="Directory : ")
        else:
            hiddableFrame.pack_forget()
            button.config(text="Directory ? ")
    button = tk.Checkbutton(dirFrame, text="Directory ? ", variable = state, offvalue=False, onvalue=True, command=toggleHiddableFrame)
    button.pack(side="left")

    return dirFrame, dirInput

def makeEncodingFrame(masterFrame, configuration):
    encodingFrame = tk.Frame(masterFrame)

    hiddableFrame = tk.Frame(encodingFrame)
    userFrame = tk.Frame(hiddableFrame)
    encodingInput = ttk.Combobox(
        userFrame,
        values=configuration["encoding"]["choices"],
        state="readonly"
    )
    encodingInput.pack()
    userEntry = tk.Entry(userFrame)
    userEntry.pack()
    userFrame.pack(side="left")

    def addToCombobox():
        values = list(encodingInput["values"])
        value = userEntry.get()
        if value and value not in values:
            values.append(value)
            encodingInput["values"] = values
            userEntry.delete(0, tk.END)
            encodingInput.set(encodingInput["values"][-1])

    def addToConfiguration():
        value = userEntry.get()
        if value and value not in configuration["encoding"]["choices"]:
            addToCombobox()
            configuration["encoding"]["choices"].append(value)

    def removeFromCombobox():
        values = list(encodingInput["values"])
        value = encodingInput.get()
        if value in values:
            values.remove(value)
            encodingInput["values"] = values
            encodingInput.set(values[0])

    def removeFromConfiguration():
        value = encodingInput.get()
        if value in configuration["encoding"]["choices"]:
            removeFromCombobox()
            configuration["encoding"]["choices"].remove(value)

    buttonsFrame = tk.Frame(encodingFrame)
    tk.Button(
        buttonsFrame,
        text="Add",
        command=addToCombobox
    ).pack()

    tk.Button(
        buttonsFrame,
        text="Add to configuration",
        command=addToConfiguration
    ).pack()

    tk.Button(
        buttonsFrame,
        text="Remove",
        command=removeFromCombobox
    ).pack()

    tk.Button(
        buttonsFrame,
        text="Remove from configuration",
        command=removeFromConfiguration
    ).pack()
    buttonsFrame.pack(side="right")

    state = tk.BooleanVar(value=False)
    def toggleHiddableFrame():
        if (state.get()):
            hiddableFrame.pack(side="right")
            button.config(text="Encoding : ")
        else:
            hiddableFrame.pack_forget()
            button.config(text="Encoding ? ")
    button = tk.Checkbutton(encodingFrame, text="Encoding ? ", variable = state, offvalue=False, onvalue=True, command=toggleHiddableFrame)
    button.pack(side="left")

    return encodingFrame, encodingInput

def makeFmtTypeFrame(masterFrame):
    # for more regulation on fmttype input value, please refer to RFC 4288 section 4.2
    fmtTypeFrame = tk.Frame(masterFrame)

    typesFrame = tk.Frame(fmtTypeFrame)
    typeInput = tk.Entry(typesFrame)
    typeInput.pack(side="right")
    tk.Label(typesFrame, text="/").pack(side="right")
    subtypeInput = tk.Entry(typesFrame)
    subtypeInput.pack(side="right")

    userFrame = tk.Frame(fmtTypeFrame)
    buttonState = tk.BooleanVar(value=False)
    def toggleFmttypeEntry():
        if (buttonState.get()):
            button.config(text="type/subtype : ")
            typesFrame.pack(side="right")
        else:
            button.config(text="FMT type ? ")
            typesFrame.pack_forget()

    button = tk.Checkbutton(fmtTypeFrame, text="FMT type ?", variable=buttonState, offvalue=False, onvalue=True, command=toggleFmttypeEntry)
    button.pack(side="left")

    # it's an error here but I don't understand how to put subtypeInput on the right of typeInput
    fmtTypeInput = {
        "type" : subtypeInput,
        "subtype" : typeInput
    }

    return fmtTypeFrame, fmtTypeInput

def makeFreeBusyTimeFrame(masterFrame, configuration):
    freeBusyTimeFrame = tk.Frame(masterFrame)

    hiddableFrame = tk.Frame(freeBusyTimeFrame)

    freeBusyTimeInput = ttk.Combobox(
        hiddableFrame,
        values=configuration["freebusytime"]["choices"],
        state="readonly"
    )
    freeBusyTimeInput.pack()

    state = tk.BooleanVar(value=False)
    def toggleHiddableFrame():
        if (state.get()):
            hiddableFrame.pack(side="right")
        else:
            hiddableFrame.pack_forget()
    button = tk.Checkbutton(freeBusyTimeFrame, text="Free or busy ? ", variable = state, offvalue=False, onvalue=True, command=toggleHiddableFrame)
    button.pack(side="left")

    # maybe useful for later development
    # def add():
    #     value = freeBusyTimeInput.get()
    #     values = list(freeBusyTimeInput["values"])
    #     if value and value not in values:
    #         values.append(value)
    #         freeBusyTimeInput["values"] = values

    # def addToConfiguration():
    #     value = freeBusyTimeInput.get()
    #     if value and value not in configuration["freebusytime"]["choices"]:
    #         configuration["freebusytime"]["choices"].append(value)

    # def remove():
    #     value = freeBusyTimeInput.get()
    #     values = list(freeBusyTimeInput["values"])
    #     if value in values:
    #         values.remove(value)
    #         freeBusyTimeInput["values"] = values

    # def removeFromConfiguration():
    #     value = freeBusyTimeInput.get()
    #     if value in configuration["freebusytime"]["choices"]:
    #         configuration["freebusytime"]["choices"].remove(value)

    # tk.Button(freeBusyTimeFrame, text="Add", command=add).pack()
    # tk.Button(freeBusyTimeFrame, text="Add to configuration", command=addToConfiguration).pack()
    # tk.Button(freeBusyTimeFrame, text="Remove", command=remove).pack()
    # tk.Button(freeBusyTimeFrame, text="Remove from configuration", command=removeFromConfiguration).pack()

    return freeBusyTimeFrame, freeBusyTimeInput

def makeLanguageFrame(masterFrame):
    languageFrame = tk.Frame(masterFrame)

    result = [f"{value}" for item in configuration["language"]["choices"] for _, value in item.items()]
    result.sort()

    hiddableFrame = tk.Frame(languageFrame)
    languageInput = ttk.Combobox(
        hiddableFrame,
        values=result,
        state="readonly"
    )
    languageInput.pack()


    buttonState = tk.BooleanVar(value=False)
    def toggleHiddableFrame():
        if (buttonState.get()):
            hiddableFrame.pack(side="right")
        else:
            hiddableFrame.pack_forget()
    checkbutton = tk.Checkbutton(languageFrame, text="Language ? ", variable=buttonState, offvalue=False, onvalue=True, command=toggleHiddableFrame)
    checkbutton.pack(side="left")

    # could be useful for later
    # def add():
    #     value = languageInput.get()
    #     values = list(languageInput["values"])
    #     if value and value not in values:
    #         values.append(value)
    #         languageInput["values"] = values

    # def addToConfiguration():
    #     value = languageInput.get()
    #     if value and value not in configuration["languages"]["choices"]:
    #         configuration["languages"]["choices"].append(value)

    # def remove():
    #     value = languageInput.get()
    #     values = list(languageInput["values"])
    #     if value in values:
    #         values.remove(value)
    #         languageInput["values"] = values

    # def removeFromConfiguration():
    #     value = languageInput.get()
    #     if value in configuration["languages"]["choices"]:
    #         configuration["languages"]["choices"].remove(value)

    # tk.Button(languageFrame, text="Add", command=add).pack()
    # tk.Button(languageFrame, text="Add to configuration", command=addToConfiguration).pack()
    # tk.Button(languageFrame, text="Remove", command=remove).pack()
    # tk.Button(languageFrame, text="Remove from configuration", command=removeFromConfiguration).pack()

    return languageFrame, languageInput

def makeMemberFrame(masterFrame, configuration):
    memberFrame = tk.Frame(masterFrame)

    hiddableFrame = tk.Frame(memberFrame)
    inputFrame = tk.Frame(hiddableFrame)
    value = tk.StringVar(value="")
    memberInput = ttk.Combobox(
        inputFrame,
        values=configuration["member"]["choices"],
        state="readonly",
        textvariable=value
    )
    memberInput.pack()
    userEntry = tk.Entry(inputFrame)
    userEntry.pack()
    inputFrame.pack(side="left")

    def add():
        value = userEntry.get()
        values = list(memberInput["values"])
        if value and value not in values:
            values.append(value)
            memberInput["values"] = values
            memberInput.set(memberInput["values"][-1])
            userEntry.delete(0, tk.END)

    def addToConfiguration():
        value = userEntry.get()
        if value and value not in configuration["member"]["choices"]:
            add()
            configuration["member"]["choices"].append(value)

    def remove():
        value = memberInput.get()
        values = list(memberInput["values"])
        if value in values:
            values.remove(value)
            memberInput["values"] = values
            if (len(memberInput["values"]) > 0):
                memberInput.set(memberInput["values"][0])
            else:
                memberInput.set("")

    def removeFromConfiguration():
        value = memberInput.get()
        if value in configuration["member"]["choices"]:
            remove()
            configuration["member"]["choices"].remove(value)

    buttonsFrame = tk.Frame(memberFrame)
    tk.Button(buttonsFrame, text="Add", command=add).pack()
    tk.Button(buttonsFrame, text="Add to configuration", command=addToConfiguration).pack()
    tk.Button(buttonsFrame, text="Remove", command=remove).pack()
    tk.Button(buttonsFrame, text="Remove from configuration", command=removeFromConfiguration).pack()
    buttonsFrame.pack(side="right")

    buttonState = tk.BooleanVar(value=False)
    def toggleHiddableFrame():
        if (buttonState.get()):
            hiddableFrame.pack(side="right")
            checkbutton.config(text="Member role : ")
        else:
            hiddableFrame.pack_forget()
            checkbutton.config(text="Member role ? ")
    checkbutton = tk.Checkbutton(memberFrame, text="Member role ? ", variable=buttonState, offvalue=False, onvalue=True, command=toggleHiddableFrame)
    checkbutton.pack(side="left")

    memberDict = {
        "state": buttonState,
        "value": value
    }

    return memberFrame, memberDict

def makePartstatFrame(masterFrame, configuration, eventType: str):
    if (eventType not in ["event", "todo", "journal"]):
        raise Exception(f"Partstat parameter could only be used on an event, a todo or a journal, not a {eventType}")

    partstatFrame = tk.Frame(masterFrame)

    hiddableFrame = tk.Frame(partstatFrame)
    userFrame = tk.Frame(hiddableFrame)
    parstatChoices = configuration["parstat"][f"{eventType}-choices"]
    value = tk.StringVar(value="")
    partstatInput = ttk.Combobox(
        userFrame,
        values=parstatChoices,
        state="readonly",
        textvariable=value
    )
    partstatInput.pack()
    userFrame.pack()

    buttonState = tk.BooleanVar(value=False)
    def toggleHiddableFrame():
        if (buttonState.get()):
            hiddableFrame.pack(side="right")
            checkbutton.config(text="Participation status : ")
        else:
            hiddableFrame.pack_forget()
            checkbutton.config(text="Participation status ? ")
    checkbutton = tk.Checkbutton(partstatFrame, text="Participation status ? ", variable=buttonState, offvalue=False, onvalue=True, command=toggleHiddableFrame)
    checkbutton.pack(side="left")

    # maybe useful for later development
    # def add():
    #     value = partstatInput.get()
    #     values = list(partstatInput["values"])
    #     if value and value not in values:
    #         values.append(value)
    #         partstatInput["values"] = values

    # def addToConfiguration():
    #     value = partstatInput.get()
    #     if value and value not in configuration["partstat"][f"{eventType}-choices"]:
    #         configuration["partstat"][f"{eventType}-choices"].append(value)

    # def remove():
    #     value = partstatInput.get()
    #     values = list(partstatInput["values"])
    #     if value in values:
    #         values.remove(value)
    #         partstatInput["values"] = values

    # def removeFromConfiguration():
    #     value = partstatInput.get()
    #     if value in configuration["partstat"][f"{eventType}-choices"]:
    #         configuration["partstat"][f"{eventType}-choices"].remove(value)

    # buttonsFrame = tk.Frame(partstatFrame)
    # tk.Button(partstatFrame, text="Add", command=add).pack()
    # tk.Button(partstatFrame, text="Add to configuration", command=addToConfiguration).pack()
    # tk.Button(partstatFrame, text="Remove", command=remove).pack()
    # tk.Button(partstatFrame, text="Remove from configuration", command=removeFromConfiguration).pack()
    # buttonsFrame.pack(side="right")

    partstatDict = {
        "state": buttonState,
        "value": value
    }

    return partstatFrame, partstatDict

def makeRoleFrame(masterFrame, configuration):
    roleFrame = tk.Frame(masterFrame)

    hiddableFrame = tk.Frame(roleFrame)
    userFrame = tk.Frame(hiddableFrame)
    roleInput = ttk.Combobox(
        userFrame,
        values=configuration["role"]["choices"],
        state="readonly"
    )
    roleInput.pack()
    userEntry = tk.Entry(userFrame)
    userEntry.pack()
    userFrame.pack(side="left")

    buttonState = tk.BooleanVar(value=False)
    def toggleHiddableFrame():
        if (buttonState.get()):
            hiddableFrame.pack(side="right")
            checkbutton.config(text="Role : ")
        else:
            hiddableFrame.pack_forget()
            checkbutton.config(text="Role ? ")
    checkbutton = tk.Checkbutton(roleFrame, text="Role ? ", variable=buttonState, offvalue=False, onvalue=True, command=toggleHiddableFrame)
    checkbutton.pack(side="left")

    # maybe useful for later development
    # def add():
    #     value = userEntry.get()
    #     values = list(roleInput["values"])
    #     if value and value not in values:
    #         values.append(value)
    #         roleInput["values"] = values
    #         roleInput.set(roleInput["values"][-1])

    # def addToConfiguration():
    #     value = userEntry.get()
    #     if value and value not in configuration["role"]["choices"]:
    #         add()
    #         configuration["role"]["choices"].append(value)

    # def remove():
    #     value = roleInput.get()
    #     values = list(roleInput["values"])
    #     if value in values:
    #         values.remove(value)
    #         roleInput["values"] = values
    #         if (len(values) != 0):
    #             roleInput.set(roleInput["values"][0])
    #         else:
    #             roleInput.set("")

    # def removeFromConfiguration():
    #     value = roleInput.get()
    #     if value in configuration["role"]["choices"]:
    #         remove()
    #         configuration["role"]["choices"].remove(value)

    # buttonsFrame = tk.Frame(roleFrame)
    # tk.Button(buttonsFrame, text="Add", command=add).pack()
    # tk.Button(buttonsFrame, text="Add to configuration", command=addToConfiguration).pack()
    # tk.Button(buttonsFrame, text="Remove", command=remove).pack()
    # tk.Button(buttonsFrame, text="Remove from configuration", command=removeFromConfiguration).pack()
    # buttonsFrame.pack(side="right")

    return roleFrame, roleInput

def makeRelationshipFrame(masterFrame, configuration):
    relationshipFrame = tk.Frame(masterFrame)

    hiddableFrame = tk.Frame(relationshipFrame)
    userFrame = tk.Frame(hiddableFrame)
    relationshipInput = ttk.Combobox(
        userFrame,
        values=configuration["relationship"]["choices"],
        state="readonly"
    )
    relationshipInput.pack()
    userEntry = tk.Entry(userFrame)
    userEntry.pack()
    userFrame.pack(side="left")

    def add():
        value = userEntry.get()
        values = list(roleInput["values"])
        if value and value not in values:
            values.append(value)
            relationshipInput["values"] = values
            relationshipInput.set(relationshipInput["values"][-1])

    def addToConfiguration():
        value = userEntry.get()
        if value and value not in configuration["relationship"]["choices"]:
            add()
            configuration["relationship"]["choices"].append(value)

    def remove():
        value = relationshipInput.get()
        values = list(relationshipInput["values"])
        if value in values:
            values.remove(value)
            relationshipInput["values"] = values
            if (len(values) != 0):
                relationshipInput.set(relationshipInput["values"][0])
            else:
                relationshipInput.set("")

    def removeFromConfiguration():
        value = relationshipInput.get()
        if value in configuration["relationship"]["choices"]:
            remove()
            configuration["relationship"]["choices"].remove(value)

    buttonsFrame = tk.Frame(relationshipFrame)
    tk.Button(buttonsFrame, text="Add", command=add).pack()
    tk.Button(buttonsFrame, text="Add to configuration", command=addToConfiguration).pack()
    tk.Button(buttonsFrame, text="Remove", command=remove).pack()
    tk.Button(buttonsFrame, text="Remove from configuration", command=removeFromConfiguration).pack()
    buttonsFrame.pack(side="right")

    buttonState = tk.BooleanVar(value=False)
    def toggleHiddableFrame():
        if (buttonState.get()):
            hiddableFrame.pack(side="right")
            checkbutton.config(text="Relationship : ")
        else:
            hiddableFrame.pack_forget()
            checkbutton.config(text="Relationship : ")
    checkbutton = tk.Checkbutton(relationshipFrame, text="Relationship ? ", variable=buttonState, offvalue=False, onvalue=True, command=toggleHiddableFrame)
    checkbutton.pack(side="left")

    return relationshipFrame, relationshipInput

def makeRsvpFrame(masterFrame, configuration):
    rsvpFrame = tk.Frame(masterFrame)

    hiddableFrame = tk.Frame(rsvpFrame)
    value = tk.StringVar(value="")
    rsvpInput = ttk.Combobox(
        hiddableFrame,
        values=configuration["rsvp"]["choices"],
        state="readonly",
        textvariable=value
    )
    rsvpInput.pack()

    # maybe useful for later development
    # def add():
    #     value = rsvpInput.get()
    #     values = list(rsvpInput["values"])
    #     if value and value not in values:
    #         values.append(value)
    #         rsvpInput["values"] = values

    # def addToConfiguration():
    #     value = rsvpInput.get()
    #     if value and value not in configuration["rsvp"]["choices"]:
    #         configuration["rsvp"]["choices"].append(value)

    # def remove():
    #     value = rsvpInput.get()
    #     values = list(rsvpInput["values"])
    #     if value in values:
    #         values.remove(value)
    #         rsvpInput["values"] = values

    # def removeFromConfiguration():
    #     value = rsvpInput.get()
    #     if value in configuration["rsvp"]["choices"]:
    #         configuration["rsvp"]["choices"].remove(value)

    # tk.Button(rsvpFrame, text="Add", command=add).pack()
    # tk.Button(rsvpFrame, text="Add to configuration", command=addToConfiguration).pack()
    # tk.Button(rsvpFrame, text="Remove", command=remove).pack()
    # tk.Button(rsvpFrame, text="Remove from configuration", command=removeFromConfiguration).pack()
    
    buttonState = tk.BooleanVar(value=False)
    def toggleHiddableFrame():
        if (buttonState.get()):
            hiddableFrame.pack(side="right")
            checkbutton.config(text="RSVP status : ")
        else:
            hiddableFrame.pack_forget()
            checkbutton.config(text="RSVP status ? ")
    checkbutton = tk.Checkbutton(rsvpFrame, text="RSVP status ? ", variable=buttonState, offvalue=False, onvalue=True, command=toggleHiddableFrame)
    checkbutton.pack(side="left")

    rsvpDict = {
        "state": buttonState,
        "value": value
    }

    return rsvpFrame, rsvpDict

def makeSentByFrame(masterFrame):
    sentByFrame = tk.Frame(masterFrame)

    hiddableFrame = tk.Frame(sentByFrame)
    value = tk.StringVar(value="")
    sentByInput = tk.Entry(hiddableFrame, textvariable=value)
    sentByInput.pack()
    
    buttonState = tk.BooleanVar(value=False)
    def toggleHiddableFrame():
        if (buttonState.get()):
            hiddableFrame.pack(side="right")
            checkbutton.config(text="Sent by : ")
        else:
            hiddableFrame.pack_forget()
            checkbutton.config(text="Sent by ? ")
    checkbutton = tk.Checkbutton(sentByFrame, text="Sent by ? ", variable=buttonState, offvalue=False, onvalue=True, command=toggleHiddableFrame)
    checkbutton.pack(side="left")

    sentbyDict = {
        "state": buttonState,
        "value": value
    }

    return sentByFrame, sentbyDict
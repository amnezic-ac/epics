from tkinter import ttk
import tkinter as tk

from src.backend.parameters import *

"""
Disclaimer
    Except the first two functions, all the other one have been AI generated for convenience purpose
"""

def makeAlternativeRepresentationFrame(masterFrame, configuration):
    altrepFrame = tk.Frame(masterFrame)

    altrepInput = tk.Text(masterFrame)
    altrepInput.config(
        height=configuration["altrep"]["height"],
        width=configuration["altrep"]["width"]
    )
    altrepInput.pack()

    return  altrepFrame, altrepInput

def makeCommonNameFrame(masterFrame):
    commonNameFrame = tk.Frame(masterFrame)

    commonNameInput = tk.Entry(commonNameFrame)
    commonNameInput.pack()

    return  commonNameFrame, commonNameInput

def makeCutypeFrame(masterFrame, configuration):
    cutypeFrame = tk.Frame(masterFrame)

    userFrame = tk.Frame(cutypeFrame)
    cutypeInput = ttk.Combobox(
        userFrame,
        values=configuration["cutype"]["choices"],
        state="readonly"
    )
    cutypeInput.config(
        height=min(configuration["cutype"]["height"], len(configuration["cutype"]["choices"]))
    )
    cutypeInput.pack()

    userInput = tk.Entry(userFrame)
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

    buttonsFrame = tk.Frame(cutypeFrame)
    tk.Button(buttonsFrame, text="Add", command=add).pack()
    tk.Button(buttonsFrame, text="Add to configuration", command=addToConfiguration).pack()
    tk.Button(buttonsFrame, text="Remove", command=remove).pack()
    tk.Button(buttonsFrame, text="Remove from configuration", command=removeFromConfiguration).pack()
    buttonsFrame.pack(side="right")

    return cutypeFrame, cutypeInput

def makeDelegatedFromFrame(masterFrame):
    delegatedFromFrame = tk.Frame(masterFrame)

    delegatedFromInput = tk.Entry(delegatedFromFrame)
    delegatedFromInput.pack()

    return delegatedFromFrame, delegatedFromInput

def makeDelegatedToFrame(masterFrame):
    delegatedToFrame = tk.Frame(masterFrame)

    delegatedToInput = tk.Entry(delegatedToFrame)
    delegatedToInput.pack()

    return delegatedToFrame, delegatedToInput

def makeDirFrame(masterFrame):
    dirFrame = tk.Frame(masterFrame)

    dirInput = tk.Entry(dirFrame)
    dirInput.pack()

    return dirFrame, dirInput

def makeEncodingFrame(masterFrame, configuration):
    encodingFrame = tk.Frame(masterFrame)

    userFrame = tk.Frame(encodingFrame)
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

    return encodingFrame, encodingInput

def makeFmtTypeFrame(masterFrame):
    # for more regulation on fmttype input value, please refer to RFC 4288 section 4.2
    fmtTypeFrame = tk.Frame(masterFrame)

    fmtTypeInput = tk.Entry(fmtTypeFrame)
    fmtTypeInput.pack()

    return fmtTypeFrame, fmtTypeInput

def makeFreeBusyTimeFrame(masterFrame, configuration):
    freeBusyTimeFrame = tk.Frame(masterFrame)

    freeBusyTimeInput = ttk.Combobox(
        freeBusyTimeFrame,
        values=configuration["freebusytime"]["choices"],
        state="readonly"
    )
    freeBusyTimeInput.pack()

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

def makeLanguageFrame(masterFrame, configuration):
    languageFrame = tk.Frame(masterFrame)

    result = [f"{value}" for item in configuration["language"]["choices"] for _, value in item.items()]

    languageInput = ttk.Combobox(
        languageFrame,
        values=result,
        state="readonly"
    )
    languageInput.pack()

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

    inputFrame = tk.Frame(memberFrame)
    memberInput = ttk.Combobox(
        inputFrame,
        values=configuration["member"]["choices"],
        state="readonly"
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

    return memberFrame, memberInput

def makePartstatFrame(masterFrame, configuration, eventType: str):
    if (eventType not in ["event", "todo", "journal"]):
        raise Exception(f"Partstat parameter could only be used on an event, a todo or a journal, not a {eventType}")

    partstatFrame = tk.Frame(masterFrame)

    userFrame = tk.Frame(partstatFrame)
    parstatChoices = configuration["parstat"][f"{eventType}-choices"]
    partstatInput = ttk.Combobox(
        partstatFrame,
        values=parstatChoices,
        state="readonly"
    )
    partstatInput.pack()
    userFrame.pack()

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

    return partstatFrame, partstatInput

def makeRoleFrame(masterFrame, configuration):
    roleFrame = tk.Frame(masterFrame)

    userFrame = tk.Frame(roleFrame)
    roleInput = ttk.Combobox(
        userFrame,
        values=configuration["role"]["choices"],
        state="readonly"
    )
    roleInput.pack()
    userEntry = tk.Entry(userFrame)
    userEntry.pack()
    userFrame.pack(side="left")

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


def makeRsvpFrame(masterFrame):
    rsvpFrame = tk.Frame(masterFrame)

    rsvpInput = ttk.Combobox(
        rsvpFrame,
        values=configuration["rsvp"]["choices"],
        state="readonly"
    )
    rsvpInput.pack()

    def add():
        value = rsvpInput.get()
        values = list(rsvpInput["values"])
        if value and value not in values:
            values.append(value)
            rsvpInput["values"] = values

    def addToConfiguration():
        value = rsvpInput.get()
        if value and value not in configuration["rsvp"]["choices"]:
            configuration["rsvp"]["choices"].append(value)

    def remove():
        value = rsvpInput.get()
        values = list(rsvpInput["values"])
        if value in values:
            values.remove(value)
            rsvpInput["values"] = values

    def removeFromConfiguration():
        value = rsvpInput.get()
        if value in configuration["rsvp"]["choices"]:
            configuration["rsvp"]["choices"].remove(value)

    tk.Button(rsvpFrame, text="Add", command=add).pack()
    tk.Button(rsvpFrame, text="Add to configuration", command=addToConfiguration).pack()
    tk.Button(rsvpFrame, text="Remove", command=remove).pack()
    tk.Button(rsvpFrame, text="Remove from configuration", command=removeFromConfiguration).pack()

    return rsvpFrame, rsvpInput

def makeSentByFrame(masterFrame):
    sentByFrame = tk.Frame(masterFrame)

    sentByInput = tk.Entry(sentByFrame)
    sentByInput.pack()

    return sentByFrame, sentByInput
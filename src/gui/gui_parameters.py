from tkinter import ttk
import tkinter as tk
from parameters import *
from gui import configuration

"""
Disclaimer
    Except the first two functions, all the other one have been AI generated for convenience purpose
"""

def makeAlternativeRepresentationFrame(masterFrame):
    altrepFrame = tk.Frame(masterFrame)

    altrepInput = tk.Text(masterFrame)
    altrepInput.config(
        height=configuration["altrep"]["height"],
        width=configuration["altrep"]["width"]
    )
    altrepInput.pack()

    return {altrepFrame, altrepInput}

def makeCommonNameFrame(masterFrame):
    commonNameFrame = tk.Frame(masterFrame)

    commonNameInput = tk.Entry(commonNameFrame)
    commonNameInput.pack()

    return {masterFrame, commonNameInput}

def makeCutypeFrame(masterFrame):
    cutypeFrame = tk.Frame(masterFrame)

    cutypeInput = ttk.Combobox(
        cutypeFrame,
        values=configuration["cutype"]["choices"],
        state="readonly"
    )
    cutypeInput.pack()

    def add():
        value = cutypeInput.get()
        values = list(cutypeInput["values"])
        if value and value not in values:
            values.append(value)
            cutypeInput["values"] = values

    def addToConfiguration():
        value = cutypeInput.get()
        if value and value not in configuration["cutype"]["choices"]:
            configuration["cutype"]["choices"].append(value)

    def remove():
        value = cutypeInput.get()
        values = list(cutypeInput["values"])
        if value in values:
            values.remove(value)
            cutypeInput["values"] = values

    def removeFromConfiguration():
        value = cutypeInput.get()
        if value in configuration["cutype"]["choices"]:
            configuration["cutype"]["choices"].remove(value)

    tk.Button(cutypeFrame, text="Add", command=add).pack()
    tk.Button(cutypeFrame, text="Add to configuration", command=addToConfiguration).pack()
    tk.Button(cutypeFrame, text="Remove", command=remove).pack()
    tk.Button(cutypeFrame, text="Remove from configuration", command=removeFromConfiguration).pack()

    return {cutypeFrame, cutypeInput}


def makeDelegatedFromFrame(masterFrame):
    delegatedFromFrame = tk.Frame(masterFrame)

    delegatedFromInput = tk.Entry(delegatedFromFrame)
    delegatedFromInput.pack()

    return {delegatedFromFrame, delegatedFromInput}


def makeDelegatedToFrame(masterFrame):
    delegatedToFrame = tk.Frame(masterFrame)

    delegatedToInput = tk.Entry(delegatedToFrame)
    delegatedToInput.pack()

    return {delegatedToFrame, delegatedToInput}

def makeDirFrame(masterFrame):
    dirFrame = tk.Frame(masterFrame)

    dirInput = tk.Entry(dirFrame)
    dirInput.pack()

    return {dirFrame, dirInput}

def makeEncodingFrame(masterFrame):
    encodingFrame = tk.Frame(masterFrame)

    encodingInput = ttk.Combobox(
        encodingFrame,
        values=configuration["encoding"]["choices"],
        state="readonly"
    )
    encodingInput.pack()

    def addToCombobox():
        values = list(encodingInput["values"])
        value = encodingInput.get()
        if value and value not in values:
            values.append(value)
            encodingInput["values"] = values

    def addToConfiguration():
        value = encodingInput.get()
        if value and value not in configuration["encoding"]["choices"]:
            configuration["encoding"]["choices"].append(value)

    def removeFromCombobox():
        values = list(encodingInput["values"])
        value = encodingInput.get()
        if value in values:
            values.remove(value)
            encodingInput["values"] = values

    def removeFromConfiguration():
        value = encodingInput.get()
        if value in configuration["encoding"]["choices"]:
            configuration["encoding"]["choices"].remove(value)

    tk.Button(
        encodingFrame,
        text="Add to combobox",
        command=addToCombobox
    ).pack()

    tk.Button(
        encodingFrame,
        text="Add to configuration",
        command=addToConfiguration
    ).pack()

    tk.Button(
        encodingFrame,
        text="Remove from combobox",
        command=removeFromCombobox
    ).pack()

    tk.Button(
        encodingFrame,
        text="Remove from configuration",
        command=removeFromConfiguration
    ).pack()

    return {encodingFrame, encodingInput}


def makeFmtTypeFrame(masterFrame):
    # for more regulation on fmttype input value, please refer to RFC 4288 section 4.2
    fmtTypeFrame = tk.Frame(masterFrame)

    fmtTypeInput = tk.Entry(fmtTypeFrame)
    fmtTypeInput.pack()

    return {fmtTypeFrame, fmtTypeInput}

def makeFreeBusyTimeFrame(masterFrame):
    freeBusyTimeFrame = tk.Frame(masterFrame)

    freeBusyTimeInput = ttk.Combobox(
        freeBusyTimeFrame,
        values=configuration["freebusytime"]["choices"],
        state="readonly"
    )
    freeBusyTimeInput.pack()

    def add():
        value = freeBusyTimeInput.get()
        values = list(freeBusyTimeInput["values"])
        if value and value not in values:
            values.append(value)
            freeBusyTimeInput["values"] = values

    def addToConfiguration():
        value = freeBusyTimeInput.get()
        if value and value not in configuration["freebusytime"]["choices"]:
            configuration["freebusytime"]["choices"].append(value)

    def remove():
        value = freeBusyTimeInput.get()
        values = list(freeBusyTimeInput["values"])
        if value in values:
            values.remove(value)
            freeBusyTimeInput["values"] = values

    def removeFromConfiguration():
        value = freeBusyTimeInput.get()
        if value in configuration["freebusytime"]["choices"]:
            configuration["freebusytime"]["choices"].remove(value)

    tk.Button(freeBusyTimeFrame, text="Add", command=add).pack()
    tk.Button(freeBusyTimeFrame, text="Add to configuration", command=addToConfiguration).pack()
    tk.Button(freeBusyTimeFrame, text="Remove", command=remove).pack()
    tk.Button(freeBusyTimeFrame, text="Remove from configuration", command=removeFromConfiguration).pack()

    return {freeBusyTimeFrame, freeBusyTimeInput}


def makeLanguageFrame(masterFrame):
    languageFrame = tk.Frame(masterFrame)

    languageInput = ttk.Combobox(
        languageFrame,
        values=configuration["languages"]["choices"],
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

    return {languageFrame, languageInput}

def makeMemberFrame(masterFrame):
    memberFrame = tk.Frame(masterFrame)

    memberInput = ttk.Combobox(
        memberFrame,
        values=configuration["member"]["choices"],
        state="readonly"
    )
    memberInput.pack()

    def add():
        value = memberInput.get()
        values = list(memberInput["values"])
        if value and value not in values:
            values.append(value)
            memberInput["values"] = values

    def addToConfiguration():
        value = memberInput.get()
        if value and value not in configuration["member"]["choices"]:
            configuration["member"]["choices"].append(value)

    def remove():
        value = memberInput.get()
        values = list(memberInput["values"])
        if value in values:
            values.remove(value)
            memberInput["values"] = values

    def removeFromConfiguration():
        value = memberInput.get()
        if value in configuration["member"]["choices"]:
            configuration["member"]["choices"].remove(value)

    tk.Button(memberFrame, text="Add", command=add).pack()
    tk.Button(memberFrame, text="Add to configuration", command=addToConfiguration).pack()
    tk.Button(memberFrame, text="Remove", command=remove).pack()
    tk.Button(memberFrame, text="Remove from configuration", command=removeFromConfiguration).pack()

    return {memberFrame, memberInput}


def makePartstatFrame(masterFrame, eventType: str):
    if (eventType not in ["event", "todo", "journal"]):
        raise Exception(f"Partstat parameter could only be used on an event, a todo or a journal, not a {eventType}")

    partstatFrame = tk.Frame(masterFrame)

    parstatChoices = configuration["parstat"][f"{eventType}-choices"]
    partstatInput = ttk.Combobox(
        partstatFrame,
        values=parstatChoices,
        state="readonly"
    )
    partstatInput.pack()

    def add():
        value = partstatInput.get()
        values = list(partstatInput["values"])
        if value and value not in values:
            values.append(value)
            partstatInput["values"] = values

    def addToConfiguration():
        value = partstatInput.get()
        if value and value not in configuration["partstat"][f"{eventType}-choices"]:
            configuration["partstat"][f"{eventType}-choices"].append(value)

    def remove():
        value = partstatInput.get()
        values = list(partstatInput["values"])
        if value in values:
            values.remove(value)
            partstatInput["values"] = values

    def removeFromConfiguration():
        value = partstatInput.get()
        if value in configuration["partstat"][f"{eventType}-choices"]:
            configuration["partstat"][f"{eventType}-choices"].remove(value)

    tk.Button(partstatFrame, text="Add", command=add).pack()
    tk.Button(partstatFrame, text="Add to configuration", command=addToConfiguration).pack()
    tk.Button(partstatFrame, text="Remove", command=remove).pack()
    tk.Button(partstatFrame, text="Remove from configuration", command=removeFromConfiguration).pack()

    return {partstatFrame, partstatInput}

def makeRoleFrame(masterFrame):
    roleFrame = tk.Frame(masterFrame)

    roleInput = ttk.Combobox(
        roleFrame,
        values=configuration["role"]["choices"],
        state="readonly"
    )
    roleInput.pack()

    def add():
        value = roleInput.get()
        values = list(roleInput["values"])
        if value and value not in values:
            values.append(value)
            roleInput["values"] = values

    def addToConfiguration():
        value = roleInput.get()
        if value and value not in configuration["role"]["choices"]:
            configuration["role"]["choices"].append(value)

    def remove():
        value = roleInput.get()
        values = list(roleInput["values"])
        if value in values:
            values.remove(value)
            roleInput["values"] = values

    def removeFromConfiguration():
        value = roleInput.get()
        if value in configuration["role"]["choices"]:
            configuration["role"]["choices"].remove(value)

    tk.Button(roleFrame, text="Add", command=add).pack()
    tk.Button(roleFrame, text="Add to configuration", command=addToConfiguration).pack()
    tk.Button(roleFrame, text="Remove", command=remove).pack()
    tk.Button(roleFrame, text="Remove from configuration", command=removeFromConfiguration).pack()

    return {roleFrame, roleInput}


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

    return {rsvpFrame, rsvpInput}

def makeSentByFrame(masterFrame):
    sentByFrame = tk.Frame(masterFrame)

    sentByInput = tk.Entry(sentByFrame)
    sentByInput.pack()

    return {sentByFrame, sentByInput}
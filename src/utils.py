import json
import logging
import datetime

def importConfigFromJSONFile(filepath: str) -> dict:
    data = None
    with open(filepath, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data

def launchLogging(logfile):
    logging.basicConfig(
        filename=f"{logfile}",
        encoding='utf-8',
        level=logging.DEBUG,
        format='%(levelname)s [%(asctime)s]: %(message)s',
        datefmt='%m/%d/%Y %I:%M:%S %p'
    )
    return logging

def findLangIdFromLangValue(language: str):
    for language in configuration["language"]:
        for key, value in language.items():
            if (value == language):
                return key
    return None

configuration = importConfigFromJSONFile("configuration.json")
logging = launchLogging(configuration["general"]["log-file"])

def exportConfigToJSONFile(filepath: str, configuration) -> bool:
    with open(filepath, "w", encoding='utf-8') as file:
        json.dump(configuration, file, indent=4)
        logging.debug(f"Configuration successfully saved")
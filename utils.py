import json
import logging

def importConfigFromJSONFile(filepath: str) -> dict:
    data = None
    with open(filepath, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data

def exportConfigToJSONFile(filepath: str) -> bool:
    with open(filepath, "w", encoding='utf-8') as file:
        json.dump(configuration, file, indent=4)

configuration = importConfigFromJSONFile("default_config.json")

logging.basicConfig(
    filename=f"{configuration["general"]["log-file"]}",
    encoding='utf-8',
    level=logging.DEBUG,
    format='%(levelname)s [%(asctime)s]: %(message)s',
    datefmt='%m/%d/%Y %I:%M:%S %p'
)
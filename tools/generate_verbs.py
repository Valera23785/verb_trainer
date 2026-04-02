import csv
import json
from pathlib import Path
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler('generate_verbs.log', encoding='utf-8')
file_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)       


def make_past_form(verb: str) -> str:
    ''' Generates the past form of a verb based on English spelling rules. '''
    if verb:
        verb = verb.lower()
    else:
        logger.error("Input verb cannot be empty")
        raise ValueError("Verb cannot be empty")
    vowels = 'aeiou'

    if verb[-1] == 'e': 
        v2v3 = verb + 'd'
    elif verb[-1] == 'y' and len(verb) > 1 and verb[-2] not in vowels:
        v2v3 = verb[:-1] + 'ied'
    elif verb[-1] == 'c':
        v2v3 = verb + 'ked'
    else:
        vowel_groups = 0
        flag = False
        for symbol in verb:
            if symbol in vowels:
                if not flag:
                    vowel_groups += 1
                    flag = True
            else:
                flag = False
        if (len(verb) > 2 
            and verb[-3] not in vowels 
            and verb[-2] in vowels 
            and verb[-1] in 'bcdfghjklmnpqrstvz' 
            and vowel_groups == 1):
            v2v3 = verb + verb[-1] + 'ed'
        else:
            v2v3 = verb + 'ed'

    return v2v3


def generate_verbs() -> None:
    ''' Reads verbs from a CSV file, generates their past forms, and writes the results to a JSON file. '''
    input_file = Path("data", "verbs.csv")
    output_file = Path("data", "verbs.json")
    if not input_file.exists():
        logger.error(f"Input file {input_file} does not exist.")
        raise FileNotFoundError(f"Input file {input_file} does not exist.")
    verbs = []
    with input_file.open("r", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)

        for id, row in enumerate(reader, start=1):
            verb = row['english'].strip()
            if not verb:
                logger.warning(f"Skipping empty verb at line {id}")
                continue
            past_form = make_past_form(verb)
            
            if row['v2']:
                irregular = past_form != row['v2'].strip()
                verbs.append({
                    "id": id,
                    "english": verb,
                    "v2": row['v2'].strip(),
                    "v3": row['v3'].strip(),
                    "irregular": irregular,
                    "russian": row['russian'].strip(),
                    "example": ''
                })
                
                logger.debug(f"Added {('irregular' if irregular else 'regular')} verb: {verb} (v2v3: {verbs[-1]['v2']}, {verbs[-1]['v3']}) from CSV")
            else:
                verbs.append({
                    "id": id,
                    "english": verb,
                    "v2": past_form,
                    "v3": past_form,
                    "irregular": False,
                    "russian": row['russian'].strip(),
                    "example": ''
                })
                logger.debug(f"Added regular verb: {verb} (v2v3: {past_form}, {past_form}) generated")

    with output_file.open("w", encoding="utf-8") as jsonfile:
        json.dump(verbs, jsonfile, ensure_ascii=False, indent=4)
        logger.info(f"Successfully wrote {len(verbs)} verbs to {output_file}")

if __name__ == "__main__":
    try:
        generate_verbs()
        print("Done! Verbs have been generated and saved to data/verbs.json.")
    except Exception as e:
        logger.exception("An error occurred while generating verbs.")
        print(f"An error occurred: {e}")
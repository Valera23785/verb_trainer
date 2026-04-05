import json
from pathlib import Path
from datetime import date
from core.models import Verb, UserProgress, VerbProgress

def load_verbs() -> list[Verb]:
    ''' Loads verbs from a JSON file and returns a list of Verb objects. '''
    input_file = Path(__file__).parent.parent / "data" / "verbs.json"
    if not input_file.exists():
        raise FileNotFoundError(f"Input file {input_file} does not exist.")
    with input_file.open("r", encoding="utf-8") as jsonfile:
        verbs_data = json.load(jsonfile)
        verbs = [Verb(**verb) for verb in verbs_data]
        return verbs

def load_progress() -> UserProgress:
    ''' Loads user progress from a JSON file and returns a UserProgress object. '''
    progress_file = Path(__file__).parent.parent / "data" / "progress.json"
    if not progress_file.exists():
        return UserProgress()  # Return default progress if file doesn't exist
    with progress_file.open("r", encoding="utf-8") as progressfile:
        progress_data = json.load(progressfile)
        verbs_progress = {
                int(k): VerbProgress(
                    next_review=date.fromisoformat(v["next_review"]), 
                    status=v["status"], 
                    consecutive_errors=v["consecutive_errors"], 
                    consecutive_correct=v["consecutive_correct"]
                    ) 
                for k, v in progress_data.get("verbs", {}).items()
                }
        last_session = progress_data.get("last_session", UserProgress().last_session)
        streak = progress_data.get("streak", UserProgress().streak)
        return UserProgress(verbs=verbs_progress, last_session=last_session, streak=streak)

def save_progress(progress: UserProgress) -> None:
    ''' Saves user progress to a JSON file. '''
    progress_file = Path(__file__).parent.parent / "data" / "progress.json"
    
    progress_data = {"verbs": {
                        k: {
                            "next_review": v.next_review.isoformat(), 
                            "status": v.status, 
                            "consecutive_errors": v.consecutive_errors, 
                            "consecutive_correct": v.consecutive_correct
                            } 
                       for k, v in progress.verbs.items()
                       }, 
                       "last_session": progress.last_session.isoformat(), 
                       "streak": progress.streak
                       }

    with progress_file.open("w", encoding="utf-8") as progressfile:
        json.dump(progress_data, progressfile, ensure_ascii=False, indent=4)
        

def load_config() -> dict:
    ''' Loads configuration from config.json and returns it as a dictionary. '''
    config_file = Path(__file__).parent.parent / "data" / "config.json"
    if not config_file.exists():
        raise FileNotFoundError(f"Config file {config_file} does not exist.")
    with config_file.open("r", encoding="utf-8") as jsonfile:
        return json.load(jsonfile)
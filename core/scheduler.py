from core.models import UserProgress, Verb
from datetime import date

def get_todays_verbs(verbs: list[Verb], progress: UserProgress, config: dict) -> list[Verb]:
    ''' Returns a list of verbs that are due for review today based on the user's progress and the configuration. '''
    
    today_verbs = []
    for verb in verbs:
        verb_progress = progress.verbs.get(verb.id)
        if verb_progress is None:
            if len(today_verbs) < config["daily_new_verbs"]:
                today_verbs.append(verb)
        elif verb_progress.next_review <= date.today():
            today_verbs.append(verb)
    
    return today_verbs
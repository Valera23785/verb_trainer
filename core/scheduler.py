from core.models import UserProgress, Verb
from datetime import date

def get_todays_verbs(verbs: list[Verb], progress: UserProgress, config: dict) -> list[Verb]:
    ''' Returns a list of verbs that are due for review today based on the user's progress and the configuration. '''
    
    today_verbs = []
    new_verbs_added = 0
    for verb in verbs:
        verb_progress = progress.verbs.get(verb.id)
        if verb_progress is None:
            if new_verbs_added < config["daily_new_verbs"]:
                today_verbs.append(verb)
                new_verbs_added += 1
        elif verb_progress.next_review <= date.today():
            today_verbs.append(verb)
    
    return today_verbs
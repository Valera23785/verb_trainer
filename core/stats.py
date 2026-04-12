from core.models import UserProgress
from datetime import date, timedelta


def get_learned_count(progress: UserProgress) -> int:
    '''Returns the number of verbs that have been learned by the user.'''
    return sum(1 for verb_progress in progress.verbs.values() if verb_progress.status == "learned")


def get_streak(progress: UserProgress) -> int:
    '''Returns the user's current streak.'''
    return progress.streak


def update_streak(progress: UserProgress) -> None:
    '''Updates the user's streak based on their last session date.'''

    today = date.today()
    if progress.last_session == today - timedelta(days=1):
        progress.streak += 1
    elif progress.last_session < today - timedelta(days=1):
        progress.streak = 1
    progress.last_session = today

def get_accuracy(progress: UserProgress) -> dict[int, float]:
    '''Returns a dictionary mapping verb IDs to their accuracy percentage.'''
    accuracy = {}
    for verb_id, verb_progress in progress.verbs.items():
        if verb_progress.total_attempts > 0:
            accuracy[verb_id] = round(verb_progress.total_correct / verb_progress.total_attempts * 100, 1)
    return accuracy
from datetime import date, timedelta
from core.models import Verb, UserProgress, VerbProgress
import random

def get_verb_forms(verb: Verb) -> list[str]:
    ''' Returns a list of the verb forms (english, v2, v3) for a given verb. '''
    return [verb.english, verb.v2, verb.v3]

def run_flashcard(verb: Verb) -> bool:
    ''' Runs a flashcard test on a given verb. Returns True if the user knew it, False otherwise. '''
    print(f"Verb: {verb.english}")
    input("Press Enter to see the answer...")
    print(f"Translation: {verb.russian}\tV2: {verb.v2}\tV3: {verb.v3}")
    while True:
        answer = input("Did you know this verb? (y/n): ").lower()
        if answer in ("y", "н"):
            return True
        elif answer in ("n", "т"):
            return False
        else:
            print("Please enter 'y' for yes or 'n' for no.")

def run_quiz_manual(verb: Verb) -> bool:
    ''' Runs a quiz test on a given verb. Returns True if the user knew it, False otherwise. '''
    test_verb_list = get_verb_forms(verb)
    index = random.randint(0, 2)
    test_verb: str = test_verb_list.pop(index)
    print(f"Verb: {test_verb}")
    while True:
        user_answer = input("Input two other forms of the verb separated by space: ").lower().split()
        if len(user_answer) != 2:
            print("please input exactly two forms of the verb.")
        else:
            break
    if set(user_answer) == set(test_verb_list):
        print("Correct!")
        return True
    else:        
        print(f"Wrong! The correct answers were: {', '.join(test_verb_list)}")
        return False
    
def run_quiz_choice(verb: Verb, all_verbs: list[Verb]) -> bool:
    ''' Runs a multiple choice quiz test on a given verb. Returns True if the user knew it, False otherwise. '''
    form_names = {0: "V1", 1: "V2", 2: "V3"}
    forms = get_verb_forms(verb)
    index = random.randint(0, 2)
    correct = forms[index]
    options = [correct]

    while len(options) < 4:
        option = random.choice(all_verbs)
        option_verb_list = get_verb_forms(option)
        if option_verb_list[index] not in options:
            options.append(option_verb_list[index])

    random.shuffle(options)

    print(f'Which of the following is the correct {form_names[index]} form of the verb "{verb.russian}"?')
    for i, option in enumerate(options, start=1):
        print(f"{i}. {option}")
    while True:
        user_input = input("Your answer (1-4): ")
        if user_input in ("1", "2", "3", "4"):
            user_choice = options[int(user_input) - 1]
            if user_choice == correct:
                print("Correct!")
                return True
            else:
                print(f"Wrong! The correct answer was: {correct}")
                return False
        else:
            print("Please enter a number between 1 and 4.")

def update_progress(verb: Verb, progress: UserProgress, knew_it: bool, config: dict) -> None:
    ''' Updates the user's progress for a given verb based on whether they knew it or not. '''
    interval = {"hard": 1, "learning": 1, "review": 3, "learned": 7}
    if verb.id not in progress.verbs:
        progress.verbs[verb.id] = VerbProgress(next_review=date.today())
    vp = progress.verbs[verb.id]
    vp.total_attempts += 1
    progress.last_session = date.today()
    if knew_it:
        vp.total_correct += 1
        vp.consecutive_correct += 1
        vp.consecutive_errors = 0
        if vp.status == "new":
            vp.status = "learning"
        elif vp.status == "hard":
            if vp.consecutive_correct >= config["consecutive_correct_to_recover"]:
                vp.status = "learning"
        elif vp.status == "learning":
            vp.status = "review"
        elif vp.status == "review":
            vp.status = "learned"
    else:
        vp.consecutive_errors += 1
        vp.consecutive_correct = 0
        if vp.status in ("review", "learned", "new"):
            vp.status = "learning"
        if vp.consecutive_errors >= config["consecutive_errors_for_hard"]:
            vp.status = "hard"
    vp.next_review = date.today() + timedelta(days=interval[vp.status])
    
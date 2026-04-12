from core.models import Verb
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

    print(f"Choose the correct {form_names[index]} from the options below:")
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
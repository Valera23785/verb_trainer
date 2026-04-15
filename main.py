from storage.storage import load_verbs, load_progress, load_config, save_progress
from core.scheduler import get_todays_verbs
from core.quiz import run_flashcard, run_quiz_choice, run_quiz_manual, update_progress
from core.stats import get_learned_count, get_streak, update_streak, get_accuracy
import random

def print_menu():
    print("=== Verb Trainer ===")
    print("1. Flashcards")
    print("2. Quiz")
    print("3. Statistics")
    print("4. Exit")

def main():
    verbs = load_verbs()
    progress = load_progress()
    config = load_config()
    todays_verbs = get_todays_verbs(verbs, progress, config)
    session_started = False

    while True:
        print_menu()
        choice = input("Select an option: ")
        if choice == "1":
            verb = random.choice(todays_verbs)
            knew_it = run_flashcard(verb)
            update_progress(verb, progress, knew_it, config)
            if not session_started:
                update_streak(progress)
                session_started = True
        elif choice == "2":
            while True:
                type_quiz = input("Choose quiz type: 1 for multiple choice, 2 for manual input, 3 to go back")
                if type_quiz == "1":
                    verb = random.choice(todays_verbs)
                    knew_it = run_quiz_choice(verb, verbs)
                    update_progress(verb, progress, knew_it, config)
                    if not session_started:
                        update_streak(progress)
                        session_started = True
                elif type_quiz == "2":
                    verb = random.choice(todays_verbs)
                    knew_it = run_quiz_manual(verb)
                    update_progress(verb, progress, knew_it, config)
                    if not session_started:
                        update_streak(progress)
                        session_started = True
                elif type_quiz == "3":
                    break
                else:
                    print("Invalid quiz type. Please try again.")
        elif choice == "3":
            learned_count = get_learned_count(progress)
            streak = get_streak(progress)
            accuracy = get_accuracy(progress)
            print(f"Learned verbs: {learned_count}")
            print(f"Current streak: {streak} days")
            print("Accuracy per verb:")
            for verb_id, acc in accuracy.items():
                verb_name = next((verb.english for verb in verbs if verb.id == verb_id), "Unknown")
                print(f"{verb_name}: {acc}%")

        elif choice == "4":
            print("Goodbye!")
            save_progress(progress)
            break
        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()
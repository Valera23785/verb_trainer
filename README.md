#  Verb Trainer

A console-based spaced repetition application designed to help you master English regular and irregular verbs. It features adaptive flashcards, dynamic quizzes, progress tracking with daily streaks, and optional AI-powered contextual examples via the Claude API. Learn at your own pace, review on a smart schedule, and track your improvement over time.

##  Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Valera23785/verb_trainer.git
   cd verb_trainer
   ```
   
2. Install required dependencies
    ```bush
    pip install python-dotenv anthropic
    ```
    
# Configuration

The AI assistant requires a Claude API key. Create a .env file in the project root and add your key:

    ANTHROPIC_API_KEY=your_api_key_here

    (Security Note: The .env file is listed in .gitignore to prevent accidental exposure. Never commit your API key to version control.)

# Running the App

Start the trainer with a single command:

    python main.py

# How to Add New Verbs:
    1. Open data/verbs.csv in any text editor.
    2. Append a new line in the format: english,russian,v2,v3
        - Leave v2 and v3 empty for regular verbs (the script will auto-generate them with +ed).
        - Fill them manually for irregular verbs.
    3. Regenerate the JSON database:
       python scripts/generate_verbs.py

# Project Structure

verb_trainer/
├── data/                  # verbs.csv (source), verbs.json (auto-generated), progress.json, config.json
├── tools/                 # generate_verbs.py (CSV → JSON converter)
├── core/                  # Business logic: models, scheduler, quiz, stats
├── storage/               # JSON read/write utilities
├── ai/                    # claude_api.py (Claude API integration)
└── main.py                # CLI entry point & main menu
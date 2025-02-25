import sys
import os
from pathlib import Path
from dotenv import load_dotenv

# Define the project root (the directory containing your project)
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))


# Load environment variables from .env file
load_dotenv(PROJECT_ROOT / ".env")

from src.functions.workoutlogger import WorkoutLogger

# Retrieve file paths from environment variables
EXERCISE_DATABASE_FILEPATH = PROJECT_ROOT / os.getenv("EXERCISE_DATABASE_FILEPATH")
WORKOUT_LOG_DATABASE_FILEPATH = PROJECT_ROOT / os.getenv("WORKOUT_LOG_DATABASE_FILEPATH")
WORKOUT_ENTRY_LOG_FILEPATH = os.getenv("WORKOUT_ENTRY_LOG_FILEPATH")  # Keep absolute paths as strings


def main():
    """Main function to handle workflow."""
    try:
        logger = WorkoutLogger(WORKOUT_ENTRY_LOG_FILEPATH, WORKOUT_LOG_DATABASE_FILEPATH, EXERCISE_DATABASE_FILEPATH)
        logger.run()
        print("Workout log and database successfully updated!")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
import pytest
import pandas as pd
from unittest.mock import patch, MagicMock
from io import BytesIO
import sys
from pathlib import Path
# Define the project root (the directory containing your project)
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.functions.workoutlogger import WorkoutLogger

@pytest.fixture
def setup_workout_logger():
    """Sets up a WorkoutLogger instance with mock file paths."""
    # Mock file paths (they won't be used due to the mock)
    entry_file = 'mock_entry.xlsx'
    log_file = 'mock_log.xlsx'
    exercises_file = 'mock_exercises.xlsx'
    
    # Creating an instance of the WorkoutLogger
    logger = WorkoutLogger(entry_file, log_file, exercises_file)
    
    # Mock data for the tests
    entry_data = {
        'Date': ["2025-02-18", "2025-02-19"],  
        'Day': ["Tuesday", "Wednesday"],  
        'Exercise_ID': [101, 103],  
        'Exercise_Name': ["Squat", "Bench Press"],  
        'Sets': [4, 3],  
        'Reps': [10, 8],  
        'Weight': [225, 185],  
        'Rest Time (sec)': [90, 120],  
        'Effectiveness': [5, 4],  
        'Went to failure': [True, False],  
        'Notes': ["Felt strong", "Struggled on last rep"]  
    }
    #Intitilize an empty log_database
    # columns = ['log_ID', 'exercise_ID','exercise_name', 'date', 'sets', 'reps', 'weight', 'rest_time', 'effectiveness','failure', 'notes']

    exercises_data = {
        'exercise_ID': [101,102,103],
        'exercise_name': ['Squat', 'Deadlift', 'Bench Press'],
        'primary_muscle': ['Quads', 'Back', 'Chest'],
        'secondary_muscle': [['Glutes,Hamstrings'],['Hamstrings,Glutes,Forearms,Traps'],['Triceps,Front Delts']],
        'equipment': ['Barbell','Barbell','Dumbell'],
        'exercise_type': ['Compound','Compound','Isolation'],
        'effectiveness': ["","",""],
        'max_weight': ["","",""],
        'max_reps': ["","",""]
    }

    # Creating DataFrames from the mock data
    entry_df = pd.DataFrame(entry_data)
    log_df = pd.DataFrame()
    exercises_df = pd.DataFrame(exercises_data)
    
    # Mock the pandas read_excel method to return our mock DataFrames
    with patch('pandas.read_excel') as mock_read_excel:
        mock_read_excel.side_effect = [entry_df, log_df, exercises_df]
        yield logger, entry_df, log_df, exercises_df


def test_load_data(setup_workout_logger):
    """Test that data is loaded correctly."""
    logger, _, _, _ = setup_workout_logger
    
    # Run the method to load data
    logger.load_data()
    
    # Assert that the data was loaded into the dataframes
    assert not logger.entry_df.empty
    assert logger.log_df.empty
    assert not logger.exercises_df.empty


def test_update_log(setup_workout_logger):
    """Test that new workout entries are appended to the log."""
    logger, entry_df, log_df, _ = setup_workout_logger
    
    # Initial log length
    initial_length = len(log_df)
    
    # Run the update_log method
    logger.load_data()  # This will load mock data
    logger.update_log()
    print(log_df)
    # Assert that the log dataframe has been updated
    assert len(logger.log_df) == initial_length + len(entry_df)
    assert '2025-02-18' in logger.log_df['date'].values
    assert logger.log_df['log_ID'].max() == 2
    assert 'Bench Press' in logger.log_df['exercise_name'].values
    assert logger.log_df['failure'][0] == True

def test_reset_entry_log(setup_workout_logger):
    '''Test that entry is reset to an empty df with just column headers'''
    logger, entry_df, _, _ = setup_workout_logger

    # Run the update_log method
    logger.load_data()  # This will load mock data
    logger.update_log()
    logger.reset_entry_log()

    #Assert that the entry dataframe is empty
    assert logger.entry_df.empty

def test_update_exercise_database_simple(setup_workout_logger):
    '''Test the simple(just one entry) updating process of the exercise_database'''
    logger, entry_df, log_df, exercise_df = setup_workout_logger

    # Run the method
    logger.load_data()  # This will load mock data
    logger.update_log()
    logger.update_exercise_database()
    print(logger.exercises_df)
    #Assert that the exercise_database has updated correctly
    assert logger.exercises_df.loc[logger.exercises_df['exercise_name'] == 'Squat', 'effectiveness'].values[0] == 5
    assert logger.exercises_df.loc[logger.exercises_df['exercise_name'] == 'Squat', 'max_weight'].values[0] == 225
    assert logger.exercises_df.loc[logger.exercises_df['exercise_name'] == 'Squat', 'max_reps'].values[0] == 10
    assert logger.exercises_df.loc[logger.exercises_df['exercise_name'] == 'Bench Press', 'max_weight'].values[0] == 185

def test_update_exercise_database_complex(setup_workout_logger):
    '''Test the simple(multiple entry) updating process of the exercise_database'''
    logger, entry_df, log_df, exercise_df = setup_workout_logger

    # Run the method
    logger.load_data()  # This will load mock data
    logger.update_log()
    logger.reset_entry_log()

    entry_data = {
        'Date': ["2025-03-18", "2025-03-19"],  
        'Day': ["Tuesday", "Wednesday"],  
        'Exercise_ID': [101, 102],  
        'Exercise_Name': ["Squat", "Deadlift"],  
        'Sets': [3, 5],  
        'Reps': [5, 10],  
        'Weight': [250, 200],  
        'Rest Time (sec)': [90, 120],  
        'Effectiveness': [3, 4],  
        'Went to failure': [True, False],  
        'Notes': ["Felt weak", "Easy"]  
    }

    logger.entry_df = pd.DataFrame(entry_data)

    logger.update_log()
    print(logger.log_df)
    logger.update_exercise_database()
    print(logger.exercises_df)

    #Assert that the database has updated correctly
    assert logger.exercises_df.loc[logger.exercises_df['exercise_name'] == 'Squat', 'effectiveness'].values[0] == 4
    assert logger.exercises_df.loc[logger.exercises_df['exercise_name'] == 'Deadlift', 'max_weight'].values[0] == 200
    assert logger.exercises_df.loc[logger.exercises_df['exercise_name'] == 'Deadlift', 'max_reps'].values[0] == 10
    assert logger.exercises_df.loc[logger.exercises_df['exercise_name'] == 'Squat', 'max_weight'].values[0] == 250
    assert logger.exercises_df.loc[logger.exercises_df['exercise_name'] == 'Squat', 'max_reps'].values[0] == 5

def test_save_data(setup_workout_logger):
    """Test that save_data writes the correct data to Excel files."""
    logger, entry_df, log_df, exercise_df = setup_workout_logger

    logger.load_data()
    logger.update_log()
    logger.update_exercise_database()
    logger.reset_entry_log()

    # Mock the to_excel method to prevent actual file writing
    with patch("pandas.ExcelWriter") as mock_writer_class:
        mock_writer_instance = mock_writer_class.return_value.__enter__.return_value

        with patch.object(logger.log_df, "to_excel") as mock_log_to_excel, \
            patch.object(logger.exercises_df, "to_excel") as mock_exercises_to_excel, \
        patch.object(logger.entry_df, "to_excel") as mock_entry_to_excel:

            logger.save_data()

            # Assertions to check if to_excel was called correctly
            mock_log_to_excel.assert_called_once_with(mock_writer_instance, sheet_name='workout_log_database', index=False)
            mock_exercises_to_excel.assert_called_once_with(mock_writer_instance, sheet_name='exercise_database', index=False)
            mock_entry_to_excel.assert_called_once_with(mock_writer_instance, sheet_name='entry_sheet', index=False)

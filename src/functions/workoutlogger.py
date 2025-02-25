import pandas as pd



class WorkoutLogger:
    def __init__(self, entry_file, log_file, exercises_file):
        self.entry_file = entry_file
        self.log_file = log_file
        self.exercises_file = exercises_file

    def load_data(self):
        """Loads the workout entry table and workout log database."""
        self.entry_df = pd.read_excel(self.entry_file)
        self.log_df = pd.read_excel(self.log_file, sheet_name='workout_log_database')
        self.exercises_df = pd.read_excel(self.exercises_file, sheet_name='exercise_database')

    def update_log(self):
        """Appends new workout entries from the entry sheet to the workout log database."""
        # Make a copy of the entry data
        new_entries = self.entry_df.copy()

        # Rename columns to match the workout_log_database
        new_entries.rename(columns={
            'Date': 'date',
            'Day': 'day',
            'Exercise_ID': 'exercise_ID',
            'Exercise_Name': 'exercise_name',
            'Sets': 'sets',
            'Reps': 'reps',
            'Weight': 'weight',
            'Rest Time (sec)': 'rest_time',
            'Effectiveness': 'effectiveness',
            'Went to failure': 'failure',
            'Notes': 'notes'
        }, inplace=True)

        # Keep only the columns needed in the log database
        new_entries = new_entries[['date', 'exercise_ID','exercise_name', 'sets', 'reps', 'weight', 'rest_time', 'effectiveness', 'failure', 'notes']]

        # Generate log_ID for each new entry.
        # If log_df is empty, start at 1; otherwise, continue from the max existing log_ID.
        if self.log_df.empty:
            start_id = 1
        else:
            start_id = int(self.log_df['log_ID'].max() + 1)

        new_entries.insert(0, 'log_ID', range(start_id, start_id + len(new_entries)))

        # Append the new entries to the log
        self.log_df = pd.concat([self.log_df, new_entries], ignore_index=True)

    def reset_entry_log(self):
        """Resets the entry log back to a blank state with only the header columns."""
        columns = [
            'Date', 'Day', 'Exercise_ID', 'Exercise_Name', 
            'Sets', 'Reps', 'Weight', 'Rest Time (sec)', 
            'Effectiveness', 'Went to failure', 'Notes'
        ]
        self.entry_df = pd.DataFrame(columns=columns)

    def update_exercise_database(self):
        """Updates effectiveness and last weight in the Exercises Database from the log."""
        #Finds average effectiveness and updates it in excersise database
        avg_effectiveness = self.log_df.groupby('exercise_ID')['effectiveness'].mean()
        self.exercises_df.set_index('exercise_ID', inplace=True)
        self.exercises_df['effectiveness'] = avg_effectiveness
        self.exercises_df.reset_index(inplace=True)

        #Finds the weight and reps used on an excersise
        max_weight_idx = self.log_df.groupby('exercise_ID')['weight'].idxmax()
        max_weight_reps = self.log_df.loc[max_weight_idx, ['exercise_ID', 'weight', 'reps']].set_index('exercise_ID')
        self.exercises_df.set_index('exercise_ID', inplace=True)
        self.exercises_df['max_weight'] = max_weight_reps['weight']
        self.exercises_df['max_reps'] = max_weight_reps['reps']
        self.exercises_df.reset_index(inplace=True)

    def save_data(self):
        """Saves updated logs and exercises database to respective sheets in their files."""
        with pd.ExcelWriter(self.log_file, engine='openpyxl', mode='w') as writer:
            self.log_df.to_excel(writer, sheet_name='workout_log_database', index=False)

        with pd.ExcelWriter(self.exercises_file, engine='openpyxl', mode='w') as writer:
            self.exercises_df.to_excel(writer, sheet_name='exercise_database', index=False)

        with pd.ExcelWriter(self.entry_file, engine='openpyxl', mode='w') as writer:
            self.entry_df.to_excel(writer, sheet_name='entry_sheet', index=False)

    def run(self):
        """Runs the full update process."""
        self.load_data()
        self.update_log()
        self.update_exercise_database()
        self.reset_entry_log()
        self.save_data()

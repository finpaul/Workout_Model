# Workout Logger 🏋️‍♂️

A Python-based workout logging system that tracks your exercises, records performance, and dynamically updates a workout database to analyze progress over time.

  

### 📂 Project Structure
workout-logger/
├── src/
│   ├── files/            # Stores actual workout data (ignored in .gitignore)
│   ├── functions/
│   │   └── workoutlogger.py  # Main class for workout tracking
│   ├── main/             # Main file to run program
│   ├── output_files/     # Place to store output files
│   └── file_templates/   # Contains template files for first-time setup
├── tests/                # Contains unit tests
├── .env                  # Stores filepath variables (ignored in Git)
├── .gitignore            # Ensures local data is not pushed to GitHub
├── README.md             # Project documentation
└── requirements.txt      # Contains the requirements for the virtual environment

### 📌 Features
- ✅ **Log Workouts** – Save workout sessions, including sets, reps, weights, and effectiveness.
- ✅ **Dynamic Exercise Database** – Updates max weight, max reps, and effectiveness for each exercise.
- ✅ **Automated Logging** – Reads entries from an Excel file and appends them to a workout log.
- ✅ **Python & Pandas** – Uses pandas for efficient data handling.

### 🚀 Installation

1️⃣ **Clone the Repository**  
```bash
git clone https://github.com/your-username/workout-logger.git
cd workout-logger
```
2️⃣ **Set Up a Virtual Environment (Optional but Recommended)**
 ```bash 
 python -m venv venv 
 source venv/bin/activate # macOS/Linux 
 venv\Scripts\activate # Windows
 ```
Then install dependencies:
```bash
pip install -r requirements.txt
```
3️⃣ **Configure File Paths with .env**
Instead of hardcoding file paths, this project loads them from a .env file.
Create a .env file in the root directory:
```bash
EXERCISE_DATABASE_FILEPATH=src/files/workout_model_database.xlsx #Exercise database and workout log are in the same excel file
WORKOUT_LOG_DATABASE_FILEPATH=src/files/workout_model_database.xlsx
WORKOUT_ENTRY_LOG_FILEPATH='absolute/file/path' #I store this on the cloud so I can update it from my phone
```
4️⃣ **Using File Templates**
If you're starting fresh, copy the templates from file_templates/ into src/files/.
```bash
cp src/file_templates/workout_model_database_template.xlsx src/files/workout_model_database.xlsx
```
### 📊 Usage

Run the program using:
```bash
python src/main/main.py
```
### 🧪 Running Tests

To run unit tests:
```bash
pytest
```
### 🛠️ Future Improvements

🔹 Add algorithm for creating workouts based on parameter set.

🔹 Add a visual dashboard to analyze trends.

🔹 Implement an API to track workouts via a web or mobile app.

🔹 Improve error handling for invalid inputs.

🔹 Add support for multiple users.

### 🤝 Contributing

Feel free to open an issue or submit a pull request if you have improvements!

  

### 📜 License

MIT License – Free to use and modify.
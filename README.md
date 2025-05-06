# Active Reading Assistant

## Overview
cs422 group 1 ARA assignment

## Project Structure
```
ara
├── src
│   ├── main.py               # Entry point of the application
│   ├── pdf_manager.py        # Handles PDF operations
│   ├── note_manager.py       # Manages hierarchical notes
│   ├── windows.py            # Handles the entire display window
│   └── database_manager.py   # Manages database operations
├── requirements.txt          # Lists project dependencies
└── README.md                 # Documentation for the project
```

## Installation
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd ara
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
To run the application, execute the following command in your terminal:
```bash
python src/main.py
```

Note: You may have to use `python3` and `pip3` if using the latest Python version.

---

## README.txt
### Description of the System
The Active Reading Assistant (ARA) is a tool designed to enhance reading and note-taking using the SQ3R method (Survey, Question, Read, Recite, Review). It integrates PDF viewing, guided prompts, and structured note-taking into a single interface.

### Authors
Lucy Acheson, Luis Guzman-Cornejo, Harry Johnson, Evelyn Orrozco, Angel Rivera

### Creation Date
30 March 2025 - 5 May 2025

### Purpose
This project was created as part of the CS422 course assignment for Group 1.

### Compilation and Execution
1. Ensure Python 3.8+ is installed.
2. Install dependencies using `pip install -r requirements.txt`.
3. Run the program with `python src/windows.py`.

### Additional Setup
- Ensure `creds.json` is properly configured with valid user credentials.
- MongoDB must be running locally or remotely for database operations.

### Software Dependencies
- Python 3.8+
- Flask 2.0.3
- PyMuPDF 1.25.5
- Pillow 11.2.1
- pymongo 4.12.1

### Directory Structure
- **src**: Contains the source code, including the main application logic, PDF handling, note management, and database operations.
- **requirements.txt**: Lists all dependencies required to run the application.
- **README.md**: Documentation for the project.
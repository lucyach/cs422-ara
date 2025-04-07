# Active Reading Assistant

## Overview
The Active Reading Assistant is a standalone Python application designed to help users manage their reading materials and notes effectively. It allows users to load PDF files, highlight important sections, and create hierarchical notes. The application is operated through a command-line interface (CLI), making it accessible without a graphical user interface.

## Project Structure
```
ara
├── src
│   ├── main.py               # Entry point of the application
│   ├── pdf_manager.py        # Handles PDF operations
│   ├── note_manager.py       # Manages hierarchical notes
│   ├── server.py             # Sets up the command-line interface
│   ├── database_manager.py    # Manages database operations
│   └── cli.py                # Implements the command-line interface
├── requirements.txt          # Lists project dependencies
└── README.md                 # Documentation for the project
```

## Installation
1. Clone the repository:
   ```
   git clone <repository-url>
   cd ara
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage
To run the application, execute the following command in your terminal:
```
python src/main.py
```

Once the application is running, you can use the command-line interface to interact with the features of the Active Reading Assistant.

## Features
- Load and parse PDF files.
- Highlight important sections of PDFs.
- Create and manage hierarchical notes.
- Save and load notes from a SQLite database.

## Contributing
Contributions are welcome! Please feel free to submit a pull request or open an issue for any enhancements or bug fixes.

## License
This project is licensed under the MIT License. See the LICENSE file for more details.
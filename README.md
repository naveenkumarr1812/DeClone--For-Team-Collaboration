# 🛡️ DeClone--For-Team-Collaboration

DeClone--For-Team-Collaboration is a collaborative tool for teams to securely upload files and automatically check for duplicates using SHA-256 content hashing. It consists of a FastAPI backend and a Streamlit frontend, making it easy to prevent redundant file uploads and manage shared resources efficiently.

## Features
- **Duplicate Detection:** Prevents uploading files that already exist by checking content hashes.
- **Streamlit Frontend:** User-friendly web interface for uploading and managing files.
- **FastAPI Backend:** Handles file uploads, hashing, and database management.
- **SQLite Database:** Stores file hashes and filenames for quick lookup.
- **Delete Functionality:** Remove files and their hashes from the database directly from the UI.

## Project Structure
```
DeClone--For-Team-Collaboration/
├── app.py            # Streamlit frontend
├── main.py           # FastAPI backend
├── db.py             # Database models and session
├── utils.py          # Utility functions (hashing)
├── requirements.txt  # Python dependencies
├── uploads/          # Uploaded files storage
├── files.db          # SQLite database
└── README.md         # Project documentation
```

## Setup Instructions

### 1. Clone the Repository
```bash
git clone <repo-url>
cd "DupliDrop - For Team Collaboration"
```

### 2. Install Dependencies
It is recommended to use a virtual environment:
```bash
python -m venv .venv
.venv\Scripts\activate  # On Windows
pip install -r requirements.txt
```

### 3. Run the Backend (FastAPI)
```bash
python main.py
```
The backend will be available at `http://127.0.0.1:8000`.

### 4. Run the Frontend (Streamlit)
```bash
streamlit run app.py
```
The frontend will be available at `http://localhost:8501`.

## Usage
1. Open the Streamlit app in your browser.
2. Upload one or more files using the uploader.
3. Click the **Upload** button to send files to the backend.
4. The app will display success or duplicate warnings for each file.
5. View all stored files and their hashes in the database section.
6. Use the delete button to remove files from the database if needed.

## API Endpoint
- **POST** `/upload`: Upload files (used by the frontend).

## Contributing
Contributions are welcome! Please open an issue or submit a pull request for improvements or bug fixes.

## License
This project is open-source and available under the MIT License. See the full [Licence](./Licence) file for details.

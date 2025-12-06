# ClientConsult CRM

ClientConsult CRM is a simple, modern desktop application for managing your consulting clients. It allows you to store and organize client information, track their needs, and manage their status.

## Features

*   **Client Management:** Add, edit, view, and delete client records.
*   **Interaction History:** Track all client touchpoints including calls, emails, meetings, and notes with dates and next steps.
*   **Comprehensive Client Profiles:** Store detailed information for each client, including:
    *   Client & Business Name
    *   Business Type
    *   Contact Information (Email, Phone, Mailing Address)
    *   Specific Needs (e.g., "Database Setup", "AI Integration")
    *   Project Status
    *   General Notes
*   **Clickable Client Names:** Click any client name in the list to view their details and interaction history.
*   **Search Functionality:** Quickly find clients by name or business name.
*   **Modern Interface:** A clean and intuitive graphical user interface built with CustomTkinter.
*   **Persistent Storage:** All data is saved in a local SQLite database file (`clients.db`).

## Technologies Used

*   **Python:** The core programming language.
*   **CustomTkinter:** For the graphical user interface.
*   **SQLite:** For the database.

## Setup and Installation

1.  **Clone the repository:**
    ```bash
    git clone <your-repository-url>
    cd ClientConsult_CRM
    ```

2.  **Create a virtual environment:**
    ```bash
    python -m venv venv
    ```

3.  **Activate the virtual environment:**
    *   **Windows:**
        ```bash
        .\venv\Scripts\activate
        ```
    *   **macOS/Linux:**
        ```bash
        source venv/bin/activate
        ```

4.  **Install the required dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

5.  **Run the application:**
    ```bash
    python -m ClientConsult_CRM
    ```

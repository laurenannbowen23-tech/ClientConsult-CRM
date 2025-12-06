# main.py
# This is the main entry point for the application.
# It will initialize the database and start the GUI.

from . import gui
from . import database

def main():
    database.create_table()
    app = gui.App()
    app.mainloop()

if __name__ == "__main__":
    main()

from gui import *
import tkinter
from dbm import *


def main():

    initDB()
    app = ToDoList()
    app.mainloop()


main()
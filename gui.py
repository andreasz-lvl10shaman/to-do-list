from dbm import *
import tkinter as tk
from tkinter import ttk

LARGEFONT = ("Verdana", 35)


class ToDoList(tk.Tk):

    # __init__ function for class tkinterApp
    def __init__(self, *args, **kwargs):
        # __init__ function for class Tk
        tk.Tk.__init__(self, *args, **kwargs)
        self.shared_data = {
            "username": tk.StringVar()
}
        # creating a container
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # initializing frames to an empty array
        self.frames = {}

        # iterating through a tuple consisting
        # of the different page layouts
        for F in (LogIn, TaskList, Registration):
            frame = F(container, self)

            # initializing frame of that object from
            # startpage, page1, page2 respectively with
            # for loop
            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(LogIn)

    def get_page(self, page_class):
        return self.frames[page_class]

    # to display the current frame passed as
    # parameter
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


# --------------------------------------------------------------------------------------------------


class LogIn(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.wrong = tk.Label(self, text="nem jó jelszó, vagy a felhasználó. valamelyik nem klappol vaze")
        # label of frame Layout 2
        label = ttk.Label(self, text="Log In", font=LARGEFONT)

        label.grid(row=0, column=4, padx=10, pady=10)

        username_label = ttk.Label(self, text="Username :")
        username_label.grid(row=1, column=1)

        password_label = ttk.Label(self, text="Password:")
        password_label.grid(row=2, column=1)

        usrname_var = tk.StringVar()
        usrname_entry = ttk.Entry(self, textvariable=usrname_var)
        usrname_entry.grid(row=1, column=2)

        password_var = tk.StringVar()
        password_entry = ttk.Entry(self, textvariable=password_var)
        password_entry.grid(row=2, column=2)

        button1 = ttk.Button(self, text="Sign In",
                             command=lambda: self.LogFunction(usrname_var.get(), password_var.get()))

        # putting the button in its place by
        # using grid
        button1.grid(row=3, column=1, padx=10, pady=10)

        ## button to show frame 2 with text layout2
        button2 = ttk.Button(self, text="Registration",
                             command=lambda: controller.show_frame(Registration))

        # putting the button in its place by
        # using grid
        button2.grid(row=4, column=1, padx=10, pady=10)

    def LogFunction(self, username, password):
        if log_in_user(username, password):
            self.wrong.grid_forget()
            print("logging in..")
            username = username.upper()
            self.controller.shared_data["username"].set(username)
            self.controller.show_frame(TaskList)
        else:
            self.wrong.grid(row=100, column=100)



class TaskList(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.user_name = ""
        self.user_id = 0
        self.all_tasks = []
        self.shown_tasks = []
        self.shown_page = 0
        self.display_num = 0
        self.done = [tk.BooleanVar(), tk.BooleanVar(), tk.BooleanVar(), tk.BooleanVar(), tk.BooleanVar(),
                     tk.BooleanVar(), tk.BooleanVar(), tk.BooleanVar(), tk.BooleanVar(), tk.BooleanVar()]
        self.c_b = [ttk.Checkbutton(self), ttk.Checkbutton(self), ttk.Checkbutton(self), ttk.Checkbutton(self),
                    ttk.Checkbutton(self), ttk.Checkbutton(self), ttk.Checkbutton(self), ttk.Checkbutton(self),
                    ttk.Checkbutton(self), ttk.Checkbutton(self)]

        self.d_button = ttk.Button(self, text="Buli az Élet!",
                                   command=lambda: self.init_user())
        self.d_button.grid(row=0, column=0, padx=10, pady=10)
        self.taskname_var = tk.StringVar()
        self.taskname_entry = ttk.Entry(self, textvariable=self.taskname_var)
        self.addtask_button = ttk.Button(self, text="Add task",
                                         command=lambda: self.AddTask(self.taskname_var.get(),
                                                                      self.user_id))
        self.delete_button = ttk.Button(self, text="delete tasks",
                                        command=lambda: self.DeleteTask())
        self.n_button = ttk.Button(self, text="next 10", command=lambda: self.Next_Page())
        self.p_button = ttk.Button(self, text="previous 10", command=lambda: self.Prev_Page())
        self.out_button = ttk.Button(self, text="Sign Out", command=lambda: self.Sigh_Out())

    def init_user(self):

        self.user_name = self.controller.shared_data["username"].get()
        self.user_id = Get_Id(self.user_name)
        self.all_tasks = Return_All_Tasks(self.user_id)
        self.namelabel = ttk.Label(self, text=self.user_name, font=LARGEFONT)
        self.namelabel.grid(row=0, column=4, padx=10, pady=10)
        self.taskname_entry.grid(row=1, column=1)
        self.addtask_button.grid(row=1, column=3, padx=10, pady=10)
        self.delete_button.grid(row=5, column=5, padx=10, pady=10)
        self.n_button.grid(row=13, column=3, padx=10, pady=10)
        self.p_button.grid(row=13, column=0, padx=10, pady=10)
        self.out_button.grid(row=10, column=10, padx=10, pady=10)
        self.ShowTasks()

    def AddTask(self, taskname, id):
        Add_Task(taskname, id)
        self.all_tasks = Return_All_Tasks(self.user_id)
        self.ShowTasks()
        self.taskname_entry.delete(0, 'end')

    def ShowTasks(self):
        #törli a taskok megjelenítését a frissítéshez
        for i in range(10):
            self.c_b[i].destroy()
        self.Update_showntasks()
        #létrehozza a takokhoz a checkboxokat
        for i in range(self.display_num):

            self.c_b[i] = ttk.Checkbutton(self, text=self.shown_tasks[i][1], variable=self.done[i])
            #beállítja a pipákat a showntasks alapján
            if 0 == self.shown_tasks[i][3]:
                self.done[i].set(False)
            else:
                self.done[i].set(True)
            self.c_b[i].grid(row=(i + 2), column=0, padx=10, pady=10)

    def DeleteTask(self):
        #a pipákhoz igazítja hogy teljesítve van a task az adatbázisban
        self.Update_Doneness()
        #törli a kipipált taskokat
        for i in range(len(self.shown_tasks)):
            if self.done[i].get():
                Delete_Task(self.shown_tasks[i][0])
        #frissíti a Tasklistát
        self.ShowTasks()

    def Update_Doneness(self):
        # a pipákhoz igazítja hogy teljesítve van a task az adatbázisban
        for i in range(self.display_num):
            if self.done[i].get():
                Set_Done(1, self.shown_tasks[i][0])
            else:
                Set_Done(0, self.shown_tasks[i][0])

    def Update_showntasks(self):
        self.all_tasks = Return_All_Tasks(self.user_id)
        print(
            "lengh of all", len(self.all_tasks) ,
            "maradék", len(self.all_tasks) - (10 * (self.shown_page))
        )
        if len(self.all_tasks) - (10 * self.shown_page) >= 10:
            self.display_num = 10
            self.shown_tasks = self.all_tasks[(10 * self.shown_page):((10 * self.shown_page)+10)]
            print("display", self.display_num)
        else:
            print("[10:19]", len(self.shown_tasks))
            self.display_num = len(self.all_tasks) - (10 * (self.shown_page))
            self.shown_tasks = self.all_tasks[(10 * self.shown_page):len(self.all_tasks)+1]

            print("shown tasks", len(self.shown_tasks))

    def Next_Page(self):
        self.Update_Doneness()
        if len(self.all_tasks) - (10 * self.shown_page) >= 1:
            self.shown_page += 1
            self.ShowTasks()

    def Prev_Page(self):
        self.Update_Doneness()
        if self.shown_page > 0:
            self.shown_page -= 1
            self.ShowTasks()

    def Sigh_Out(self):
        # a pipákhoz igazítja hogy teljesítve van a task az adatbázisban
        self.Update_Doneness()
        self.namelabel.grid_forget()
        self.taskname_entry.grid_forget()
        self.addtask_button.grid_forget()
        self.delete_button.grid_forget()
        self.n_button.grid_forget()
        self.p_button.grid_forget()
        for i in range(10):
            self.c_b[i].destroy()
        self.out_button.grid_forget()
        self.controller.show_frame(LogIn)
        print("logging off, by ", self.user_name)

class Registration(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        label = ttk.Label(self, text="Registration", font=LARGEFONT)
        label.grid(row=0, column=4, padx=10, pady=10)
        name_label = ttk.Label(self, text="Username:")
        name_label.grid(row=1, column=0)
        pass1_label = ttk.Label(self, text="Password:")
        pass1_label.grid(row=2, column=0)
        pass2_label = ttk.Label(self, text="Password again:")
        pass2_label.grid(row=3, column=0)
        name_var = tk.StringVar()
        name_entry = ttk.Entry(self, textvariable=name_var)
        name_entry.grid(row=1, column=1)

        pass1_var = tk.StringVar()
        pass1_entry = ttk.Entry(self, textvariable=pass1_var)
        pass1_entry.grid(row=2, column=1)

        pass2_var = tk.StringVar()
        pass2_entry = ttk.Entry(self, textvariable=pass2_var)
        pass2_entry.grid(row=3, column=1)

        # button to show frame 2 with text
        # layout2
        button1 = ttk.Button(self, text="Registration", command=lambda:
        self.RegFunction(name_var.get(), pass1_var.get(), pass2_var.get()))

        # putting the button in its place by
        # using grid
        button1.grid(row=4, column=4, padx=10, pady=10)
        #szeretem a nórát
        # button to show frame 3 with text
        # layout3
        button2 = ttk.Button(self, text="Back to Login",
                             command=lambda: controller.show_frame(LogIn))

        # putting the button in its place by
        # using grid
        button2.grid(row=4, column=0, padx=10, pady=10)

    def RegFunction(self, name, pass1, pass2):

        if pass1 == pass2 and pass1 != "":
            submit_user(name, pass1)
            self.controller.show_frame(LogIn)
        else:
            popup = Tk()
            warning1 = Label(popup, text="Nem egyezik meg a két jelszó ")
            warning1.grid(row=0)
            popup.mainloop()

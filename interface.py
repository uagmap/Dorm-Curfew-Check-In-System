import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog
import os
import ra_ui

LARGE_FONT = ("Verdana", 12)

class ProjectUI(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        
        tk.Tk.wm_title(self, "Check-in System client")
        tk.Tk.wm_geometry(self, "500x500")
        
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand = True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (StartPage, LoginScreen, RegScreen, MenuScreen, Register_new_student_screen, reg, Status_screen_option, Status_screen_today, Status_screen_date):
            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):
        
        frame = self.frames[cont]
        frame.tkraise()

    
class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Login or Register", bg="cyan", width="300", height="2", font=("Calibri", 13))
        label.pack()
        tk.Label(self, text="").pack()

        button1 = tk.Button(self, text="Login", height="2", width="30",
                            command=lambda: controller.show_frame(LoginScreen))
        button1.pack()
        
        tk.Label(self, text="").pack()
        button2 = tk.Button(self, text="Register", height="2", width="30",
                            command=lambda: controller.show_frame(RegScreen))
        button2.pack()

class LoginScreen(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        self.controller = controller
        label = tk.Label(self, text="You need to log in the system.", font=LARGE_FONT)
        label.pack(pady=10, padx=10)
        tk.Label(self, text="").pack()
        
        global username_verify
        global password_verify
        global username_login_entry
        global password_login_entry
        
        username_verify = tk.StringVar()
        password_verify = tk.StringVar()
        
        tk.Label(self, text="Username: ").pack()
        username_login_entry = tk.Entry(self, textvariable = username_verify)
        username_login_entry.pack()
        tk.Label(self, text="").pack()
        
        tk.Label(self, text="Password: ").pack()
        password_login_entry = tk.Entry(self, textvariable = password_verify, show="*")
        password_login_entry.pack()
        tk.Label(self, text="").pack()

        button1 = tk.Button(self, text="Login", command = self.login_verification)
        button1.pack()
        
        button2 = tk.Button(self, text="Back to start",
                            command=lambda: controller.show_frame(StartPage))
        button2.pack()
        
    def login_verification(self):
        username1 = username_verify.get()
        password1 = password_verify.get()
        
        username_login_entry.delete(0, tk.END)
        password_login_entry.delete(0, tk.END)
        
        list_of_files = os.listdir("/home/pi/checkinsystem/users_info")
        
        if username1 in list_of_files:
            file1 = open("users_info/" + username1, "r")
            verify = file1.read().splitlines()
            if password1 in verify:
                tk.Label(self, text="Login Success", fg="green", font=("calibri", 11)).pack()
                tk.Button(self, text = "Go to menu",
                          command= lambda: self.controller.show_frame(MenuScreen)).pack()
            else:
                tk.Label(self, text="Invalid Password", fg="red", font=("calibri", 11)).pack()
        else:
            tk.Label(self, text="User doesn't exist", fg="red", font=("calibri", 11)).pack()
        

class RegScreen(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        
        global username
        global password
        global username_entry
        global password_entry
        
        username = tk.StringVar()
        password = tk.StringVar()
        
        tk.Label(self, text="Please enter details below", bg="cyan").pack()
        tk.Label(self, text="").pack()
        
        username_label = tk.Label(self, text="Username: ")
        username_label.pack()
        
        username_entry = tk.Entry(self, textvariable=username)
        username_entry.pack()
        
        password_label = tk.Label(self, text="Password: ")
        password_label.pack()
        
        password_entry = tk.Entry(self, textvariable=password, show='*')
        password_entry.pack()
        
        tk.Label(self, text="").pack()
        
        tk.Button(self, text="Register", width=10, height=1, bg="yellow", command=self.register_user).pack()
        tk.Button(self, text="Go back", width=10, height=1, bg="yellow",
                  command=lambda: controller.show_frame(StartPage)).pack()
        
    def register_user(self):
        username_info = username.get()
        password_info = password.get()
        
        file = open("users_info/" + username_info, "w")
        file.write(username_info + "\n")
        file.write(password_info + "\n")
        file.close()
        
        username_entry.delete(0, tk.END)
        password_entry.delete(0, tk.END)
    
        tk.Label(self, text="Registration Success", fg="green", font=("calibri", 11)).pack()

class MenuScreen(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        
        tk.Label(self, text="Select an option").pack()
        tk.Button(self, text = "register new student", height = "2", width = "30",
                  command = lambda: controller.show_frame(Register_new_student_screen)).pack(padx = 10, pady = 10)
        tk.Label(self, text = "").pack()
        tk.Button(self, text = "view residents' status", height = "2", width = "30",
                  command = lambda: controller.show_frame(Status_screen_option)).pack(padx = 10, pady = 10)

class Register_new_student_screen(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        self.controller = controller
        
        tk.Label(self, text = "Register new student in the check-in system").pack()
        
        #s = simpledialog.askfloat("input string", "enter your name")    
        #ask = tk.messagebox.askyesno("User already exists", "The student is already in the system. Overwrite?")
        
        tk.Button(self, text = "Scan a card", command = self.button_function).pack()
        tk.Button(self, text="Back to main menu", command = lambda: controller.show_frame(MenuScreen)).pack()
        
        
    def button_function(self):
        if ra_ui.read_rfid_card():
            ask = tk.messagebox.askyesno("User already exists",
                                         "A chip is already registered in the system. Overwrite?")
            if ask:
                ra_ui.overwrite_rfid()
                self.controller.show_frame(reg)
            else:
                self.controller.show_frame(MenuScreen)
        else:
            ra_ui.write_rfid()
            self.controller.show_frame(reg)
        
        
class reg(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        self.controller = controller
        tk.Label(self, text="").pack(padx=0, pady=10)
        tk.Button(self, text="Register", height = "3", width = "30", command = self.ask_and_register).pack(padx=0, pady=50)
        tk.Button(self, text="Back to main menu", height="3", width="30",
                  command = lambda: controller.show_frame(MenuScreen)).pack()
    
    def ask_and_register(self):
        name = simpledialog.askstring("Enter name", "Enter resident's name")
        room = simpledialog.askstring("Enter room number", "Enter resident's room number")
        if name != None and room != None:
            ra_ui.cursor_execute(name, room)
            tk.messagebox.showinfo("Success!", "New resident has been saved")
            
class Status_screen_option(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        
        tk.Button(self, text="Records for today", height="3", width="30",
                  command = lambda: controller.show_frame(Status_screen_today)).pack()
        tk.Button(self, text="Records for specified date", height="3", width="30",
                  command = lambda: controller.show_frame(Status_screen_date)).pack()
        tk.Button(self, text="Back to main menu", height="3", width="30",
                  command = lambda: controller.show_frame(MenuScreen)).pack()

class Status_screen_today(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        
        #tk.Label(self, text = "here you can view current \n or specified by date residents' status").pack()
        #tk.Label(self, text = ra_ui.show_status()).pack()
        i = 0
        for record in ra_ui.show_status_today():
            for j in range(len(record)):
                e = tk.Entry(self, width=20, fg='blue')
                e.grid(row=i, column = j)
                e.insert(tk.END, record[j])
            i += 1
        btn = tk.Button(self, text = "go back",
                  command = lambda: controller.show_frame(Status_screen_option))
        btn.grid(row=i+1, column=1)

class Status_screen_date(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        
        
        tk.Button(self, text = "Enter date", command = self.ask_date).grid(row=0, column=5)
        tk.Button(self, text = "go back",
                  command = lambda: controller.show_frame(Status_screen_option)).grid(row=10, column=1)
                  

          
        
    def ask_date(self):
        i = 0
        date = simpledialog.askstring("Enter wanted date", "What date are we looking for? (year-mon-day)")
        if ra_ui.show_status_date(date) == "":#there are no records
            tk.Label(self, text="Looks like there are no records for that date.").grid(row=0, column=0)
        
        else:            
            for record in ra_ui.show_status_date(date):
                for j in range(len(record)):
                    e = tk.Entry(self, width=20, fg='blue')
                    e.grid(row=i, column = j)
                    e.insert(tk.END, record[j])
                i += 1
                
            #tk.Button(self, text = "go back",
            #      command = lambda: controller.show_frame(Status_screen_option)).grid(row=i+1, column=1)
                  

            


app = ProjectUI()
app.mainloop()

import customtkinter
from tkinter import messagebox
from pyautogui import size as screenSize
from BEAN.bean import DB
import CGV
import hashlib

class App:
    db=DB()
    user=None
    app=None

    def __init__(self):
        ap=self.db.selectAll(self.db.APP_CONFIG_TABLE, "name='appearance'")
        if ap:
            customtkinter.set_appearance_mode(ap[0]["value"])
        else:
            customtkinter.set_appearance_mode("dark")
            self.db.insert(self.db.APP_CONFIG_TABLE, {"name": "appearance", "value": "dark"})

        customtkinter.set_default_color_theme("green")
        self.LoginWindow()

    def goto(self, window):
        self.app.destroy()
        window()

    def register(self, fullname, username, password):
        if not fullname.strip() or not username.strip() or not password.strip():
            messagebox.showinfo("Erro", "Preencha todos os campos!")
            return False
        if username.count(" ")>0 or len(username)>20:
            messagebox.showinfo("Erro", "Username precisa ter até 20 caracteres e não ter espaços!")
            return False
        try:
            self.db.insert(self.db.USERS_TABLE, {"fullname": fullname, "username": username.lower(), "password": hashlib.sha256(password.encode()).hexdigest()})
            self.goto(self.LoginWindow)
        except:
            messagebox.showinfo("Erro", "Usuário já existe!")
            return False
        
    def login(self, username, password):
        if not username.strip() or not password.strip():
            messagebox.showinfo("Erro", "Preencha todos os campos!")
            return False
        users=self.db.selectAll(self.db.USERS_TABLE, f"username='{username.lower()}' AND password='{hashlib.sha256(password.encode()).hexdigest()}'")
        if users:
            self.user=users[0]
            self.goto(self.HomeWindow)
        else:
            messagebox.showinfo("Erro", "Usuário ou senha incorretos!")


    def LoginWindow(self):

        windowWidth=400
        windowHeight=400
        windowX=round(screenSize()[0]/2-windowWidth/2)
        windowY=round(screenSize()[1]/2-windowHeight/2)

        self.app = customtkinter.CTk()
        self.app.geometry("{}x{}+{}+{}".format(str(windowWidth),str(windowHeight),str(windowX),str(windowY)))
        self.app.title("Login")
        self.app.iconbitmap("imgs/icon.ico")

        mainFrame=customtkinter.CTkFrame(master=self.app, width=windowWidth, height=windowHeight)
        mainFrame.pack(pady=20, padx=20, fill="both", expand=True)

        customtkinter.CTkLabel(master=mainFrame,text="Login", width=windowWidth/2, height=windowHeight/10, font=("Arial", 25)).pack(pady=20)

        customtkinter.CTkLabel(master=mainFrame,text="Username", width=windowWidth/2, height=windowHeight/10).pack()

        username=customtkinter.CTkEntry(master=mainFrame, width=windowWidth/2, height=windowHeight/10)
        username.pack()

        customtkinter.CTkLabel(master=mainFrame, text="Senha", width=windowWidth/2, height=windowHeight/10).pack()

        password=customtkinter.CTkEntry(master=mainFrame, width=windowWidth/2, height=windowHeight/10, show="*")
        password.pack()

        loginButton=customtkinter.CTkButton(master=mainFrame,text="Login",command=lambda:self.login(username.get(), password.get()))
        loginButton.pack(pady=15, padx=15)

        gotoRegisterButton=customtkinter.CTkButton(master=mainFrame, text="Fazer Registro", width=20, command=lambda:self.goto(self.RegisterWindow))
        gotoRegisterButton.pack(pady=20, padx=15, side="right")

        self.app.mainloop()
    
    def RegisterWindow(self):

        windowWidth=400
        windowHeight=600
        windowX=round(screenSize()[0]/2-windowWidth/2)
        windowY=round(screenSize()[1]/2-windowHeight/2)

        self.app = customtkinter.CTk()
        self.app.geometry("{}x{}+{}+{}".format(str(windowWidth),str(windowHeight),str(windowX),str(windowY)))
        self.app.title("Registro")
        self.app.iconbitmap("imgs/icon.ico")

        mainFrame=customtkinter.CTkFrame(master=self.app, width=windowWidth, height=windowHeight)
        mainFrame.pack(pady=20, padx=20, fill="both", expand=True)

        customtkinter.CTkLabel(master=mainFrame,text="Registro", width=windowWidth/2, height=windowHeight/10, font=("Arial", 25)).pack(pady=20)

        customtkinter.CTkLabel(master=mainFrame,text="Nome Completo",width=windowWidth/2,height=windowHeight/10).pack()
        fullname=customtkinter.CTkEntry(master=mainFrame, width=windowWidth/2, height=windowHeight/14)
        fullname.pack()

        customtkinter.CTkLabel(master=mainFrame,text="Username",width=windowWidth/2,height=windowHeight/10).pack()
        username=customtkinter.CTkEntry(master=mainFrame, width=windowWidth/2, height=windowHeight/14)
        username.pack()

        customtkinter.CTkLabel(master=mainFrame,text="Senha",width=windowWidth/2,height=windowHeight/10).pack()
        password=customtkinter.CTkEntry(master=mainFrame, width=windowWidth/2, height=windowHeight/14, show="*")
        password.pack()

        RegisterButton=customtkinter.CTkButton(master=mainFrame, text="Registrar", command=lambda:self.register(fullname.get(), username.get(), password.get()))
        RegisterButton.pack(pady=15, padx=15)

        gotoLoginButton=customtkinter.CTkButton(master=mainFrame, text="Fazer Login", width=20, command=lambda:self.goto(self.LoginWindow))
        gotoLoginButton.pack(pady=20, padx=15, side="right")

        self.app.mainloop()
    
    def HomeWindow(self):

        def changeFrameTo(frame):
            self.now.grid_forget()
            self.now=frame
            self.now.grid(row=0, column=1, pady=10, padx=10, sticky="snew")

        def change_appearance_mode_event(v):
            new=v.lower()
            customtkinter.set_appearance_mode(new)
            self.db.execute(f"UPDATE {self.db.APP_CONFIG_TABLE} SET value='{new}' WHERE name='appearance'")

        windowWidth=1200
        windowHeight=800
        windowX=round(screenSize()[0]/2-windowWidth/2)
        windowY=round(screenSize()[1]/2-windowHeight/2)

        self.app = customtkinter.CTk()
        self.app.geometry("{}x{}+{}+{}".format(str(windowWidth),str(windowHeight),str(windowX),str(windowY)))
        self.app.title("Home")
        self.app.iconbitmap("imgs/icon.ico")

        self.app.grid_columnconfigure(1, weight=1)
        self.app.grid_columnconfigure((2, 3), weight=0)
        self.app.grid_rowconfigure((0, 1), weight=1)

        leftFrame=customtkinter.CTkFrame(self.app, width=140, corner_radius=0)
        leftFrame.grid(row=0,column=0, rowspan=2, sticky="snew")
        leftFrame.grid_rowconfigure(4, weight=1)
        

        frame1=customtkinter.CTkFrame(self.app, width=600, height=600)
        label1=customtkinter.CTkLabel(frame1, text="frame1", font=customtkinter.CTkFont(size=20, weight="bold"))
        label1.grid(row=0, column=3, padx=20, pady=(20, 10))
        frame2=customtkinter.CTkFrame(self.app, width=600, height=600)
        label2=customtkinter.CTkLabel(frame2, text="frame2", font=customtkinter.CTkFont(size=20, weight="bold"))
        label2.grid(row=0, column=1, padx=20, pady=(20, 10))
        frame3=customtkinter.CTkFrame(self.app, width=600, height=600)
        label3=customtkinter.CTkLabel(frame3, text="fuihibin", font=customtkinter.CTkFont(size=20, weight="bold"))
        label3.grid(row=0, column=2, padx=20, pady=(20, 10))
        frame4=customtkinter.CTkFrame(self.app, width=600, height=600)
        label4=customtkinter.CTkLabel(frame4, text="Olá mundo!", font=customtkinter.CTkFont(size=20, weight="bold"))
        label4.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.now=frame1
        self.now.grid(row=0, column=1, pady=10, padx=10, sticky="snew")


        leftFrame_button1=customtkinter.CTkButton(leftFrame, width=50, height=50, text=" ", command=lambda:changeFrameTo(frame1))
        leftFrame_button1.grid(row=0, column=0, padx=10, pady=10, sticky="n")
        leftFrame_button2=customtkinter.CTkButton(leftFrame, width=50, height=50, text=" ", command=lambda:changeFrameTo(frame2))
        leftFrame_button2.grid(row=1, column=0, padx=10, pady=10, sticky="n")
        leftFrame_button3=customtkinter.CTkButton(leftFrame, width=50, height=50, text=" ", command=lambda:changeFrameTo(frame3))
        leftFrame_button3.grid(row=2, column=0, padx=10, pady=10, sticky="n")
        leftFrame_button4=customtkinter.CTkButton(leftFrame, width=50, height=50, text=" ", command=lambda:changeFrameTo(frame4))
        leftFrame_button4.grid(row=3, column=0, padx=10, pady=10, sticky="n")
        leftFrame_button5=customtkinter.CTkButton(leftFrame, width=50, height=50, text=" ", command=0)
        leftFrame_button5.grid(row=4, column=0, padx=10, pady=10, sticky="n")
        appearance_mode_label=customtkinter.CTkLabel(leftFrame, text="Appearance Mode:", anchor="w")
        appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0), sticky="n")
        appearance_mode_optionemenu=customtkinter.CTkComboBox(leftFrame, values=["Light", "Dark", "System"], command=change_appearance_mode_event)
        appearance_mode_optionemenu.set(self.app._get_appearance_mode().title())
        appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 10), sticky="n")

        self.app.mainloop()

App()
import customtkinter
from tkinter import messagebox
import pyautogui
from BEAN.bean import DB
import CGV
import hashlib

class App:
    db=DB()
    user=None
    app=None

    def __init__(self):
        customtkinter.set_appearance_mode("dark-blue")
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
        windowX=round(pyautogui.size()[0]/2-windowWidth/2)
        windowY=round(pyautogui.size()[1]/2-windowHeight/2)

        self.app = customtkinter.CTk()
        self.app.geometry("{}x{}+{}+{}".format(str(windowWidth),str(windowHeight),str(windowX),str(windowY)))
        self.app.title("Login")

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
        windowX=round(pyautogui.size()[0]/2-windowWidth/2)
        windowY=round(pyautogui.size()[1]/2-windowHeight/2)

        self.app = customtkinter.CTk()
        self.app.geometry("{}x{}+{}+{}".format(str(windowWidth),str(windowHeight),str(windowX),str(windowY)))
        self.app.title("Registro")

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
        windowWidth=650
        windowHeight=450
        windowX=round(pyautogui.size()[0]/2-windowWidth/2)
        windowY=round(pyautogui.size()[1]/2-windowHeight/2)

        self.app = customtkinter.CTk()
        self.app.geometry("{}x{}+{}+{}".format(str(windowWidth),str(windowHeight),str(windowX),str(windowY)))
        self.app.title("Home")

        mainFrame=customtkinter.CTkFrame(master=self.app, width=windowWidth, height=windowHeight)
        mainFrame.pack(pady=20, padx=20, fill="both", expand=True)

        customtkinter.CTkLabel(master=mainFrame,text="Home", width=windowWidth/2, height=windowHeight/10, font=("Arial", 25)).pack(pady=20)
        customtkinter.CTkLabel(master=mainFrame,text="Hi, "+self.user["fullname"].split(" ")[0]+"!", width=windowWidth/2, height=windowHeight/10).pack(pady=20)
        self.app.mainloop()

App()
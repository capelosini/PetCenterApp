import customtkinter
import pyautogui

class App:
    def __init__(self):
        customtkinter.set_appearance_mode("dark-blue")
        customtkinter.set_default_color_theme("blue")
        self.LoginWindow()

    def goto(self, app, window):
        app.destroy()
        window()

    def LoginWindow(self):
        windowWidth=400
        windowHeight=400
        windowX=round(pyautogui.size()[0]/2-windowWidth/2)
        windowY=round(pyautogui.size()[1]/2-windowHeight/2)

        app = customtkinter.CTk()
        app.geometry("{}x{}+{}+{}".format(str(windowWidth),str(windowHeight),str(windowX),str(windowY)))
        app.title("Login")

        mainFrame=customtkinter.CTkFrame(master=app, width=windowWidth, height=windowHeight)
        mainFrame.pack(pady=20, padx=20, fill="both", expand=True)

        customtkinter.CTkLabel(master=mainFrame,text="Login", width=windowWidth/2, height=windowHeight/10, font=("Arial", 25)).pack(pady=20)

        customtkinter.CTkLabel(master=mainFrame,text="Nome de Usuario", width=windowWidth/2, height=windowHeight/10).pack()

        username=customtkinter.CTkEntry(master=mainFrame, width=windowWidth/2, height=windowHeight/10)
        username.pack()

        customtkinter.CTkLabel(master=mainFrame, text="Senha", width=windowWidth/2, height=windowHeight/10).pack()

        password=customtkinter.CTkEntry(master=mainFrame, width=windowWidth/2, height=windowHeight/10, show="*")
        password.pack()

        loginButton=customtkinter.CTkButton(master=mainFrame,text="Login",command=lambda:print("Login"))
        loginButton.pack(pady=15, padx=15)

        gotoRegisterButton=customtkinter.CTkButton(master=mainFrame, text="Fazer Registro", width=20, command=lambda:self.goto(app,self.RegisterWindow))
        gotoRegisterButton.pack(pady=20, padx=15, side="right")

        app.mainloop()
    
    def RegisterWindow(self):

        windowWidth=400
        windowHeight=400
        windowX=round(pyautogui.size()[0]/2-windowWidth/2)
        windowY=round(pyautogui.size()[1]/2-windowHeight/2)

        app = customtkinter.CTk()
        app.geometry("{}x{}+{}+{}".format(str(windowWidth),str(windowHeight),str(windowX),str(windowY)))
        app.title("Registro")

        mainFrame=customtkinter.CTkFrame(master=app, width=windowWidth, height=windowHeight)
        mainFrame.pack(pady=20, padx=20, fill="both", expand=True)

        customtkinter.CTkLabel(master=mainFrame,text="Registro", width=windowWidth/2, height=windowHeight/10, font=("Arial", 25)).pack(pady=20)

        customtkinter.CTkLabel(master=mainFrame,text="Email",width=windowWidth/2,height=windowHeight/10).pack()

        email=customtkinter.CTkEntry(master=mainFrame,width=windowWidth/2,height=windowHeight/10)
        email.pack()

        customtkinter.CTkLabel(master=mainFrame,text="Senha",width=windowWidth/2,height=windowHeight/10).pack()

        password=customtkinter.CTkEntry(master=mainFrame,width=windowWidth/2,height=windowHeight/10, show="*")
        password.pack()

        RegisterButton=customtkinter.CTkButton(master=mainFrame, text="Registrar", command=lambda:print("Register"))
        RegisterButton.pack(pady=15, padx=15)

        gotoLoginButton=customtkinter.CTkButton(master=mainFrame, text="Fazer Login", width=20, command=lambda:self.goto(app,self.LoginWindow))
        gotoLoginButton.pack(pady=20, padx=15, side="right")

        app.mainloop()

App()
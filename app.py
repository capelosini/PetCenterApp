import customtkinter
from tkinter import messagebox
from pyautogui import size as screenSize
from BEAN.bean import DB
import CGV
import hashlib
from PIL import Image

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

        self.app.bind("<Return>", lambda e:self.login(username.get(), password.get()))
        
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
            self.now.grid(row=1, column=1, columnspan=2, pady=10, padx=10, sticky="snew")

        def change_appearance_mode_event(v):
            new=v.lower()
            customtkinter.set_appearance_mode(new)
            self.db.execute(f"UPDATE {self.db.APP_CONFIG_TABLE} SET value='{new}' WHERE name='appearance'")

        windowWidth=1200
        windowHeight=800
        windowX=round(screenSize()[0]/2-windowWidth/2)
        windowY=round(screenSize()[1]/2-windowHeight/2)

        #imagens
        userIcon=customtkinter.CTkImage(light_image=Image.open("imgs/user.ico"), dark_image=Image.open("imgs/user.ico"), size=(50, 50))
        calendarIcon=customtkinter.CTkImage(light_image=Image.open("imgs/calendar.ico"), dark_image=Image.open("imgs/calendar.ico"), size=(35, 35))
        cartIcon=customtkinter.CTkImage(light_image=Image.open("imgs/cart.ico"), dark_image=Image.open("imgs/cart.ico"), size=(35, 35))

        self.app = customtkinter.CTk()
        self.app.geometry("{}x{}+{}+{}".format(str(windowWidth),str(windowHeight),str(windowX),str(windowY)))
        self.app.title("Home")
        self.app.iconbitmap("imgs/icon.ico")

        self.app.grid_columnconfigure(1, weight=1)
        self.app.grid_columnconfigure((2, 3), weight=0)
        self.app.grid_rowconfigure(1, weight=1)

        leftFrame=customtkinter.CTkFrame(self.app, width=140, corner_radius=0)
        leftFrame.grid(row=0,column=0, rowspan=2, sticky="snew")
        leftFrame.grid_rowconfigure(4, weight=1)

        userButton=customtkinter.CTkButton(self.app, width=60, text="", image=userIcon, corner_radius=15, command=self.UserWindow)
        userButton.grid(row=0, column=2, padx=10, pady=0, sticky="snew")
        searchBar=customtkinter.CTkEntry(self.app, placeholder_text="Digite sua pesquisa")
        searchBar.grid(row=0, column=1, padx=10, pady=0, sticky="we")
        
        #configurações do frame de serviços
        frame1=customtkinter.CTkFrame(self.app, width=600, height=600)
        label1=customtkinter.CTkLabel(frame1, text="frame1", font=customtkinter.CTkFont(size=20, weight="bold"))
        label1.grid(row=0, column=3, padx=20, pady=(20, 10))


        #configurações do frame de compras
        frame2=customtkinter.CTkFrame(self.app, width=600, height=600)
        frame2.grid_columnconfigure(0, weight=1)
        frame2.grid_rowconfigure(1, weight=1)
        label2=customtkinter.CTkLabel(frame2, text="Estoque", font=customtkinter.CTkFont(size=20, weight="bold"))
        label2.grid(row=0, column=0, padx=20, pady=(20, 10))
        frameProdutos=customtkinter.CTkScrollableFrame(frame2, width=700, height=700)
        frameProdutos.grid(row=1, column=0, padx=20, pady=20, sticky="w")
        frameProdutos.grid_columnconfigure(0, weight=1)
        self.produtos=[]
        for i in range(10):
            produto = customtkinter.CTkLabel(frameProdutos, text=f"Produto {i+1}")
            produto.grid(row=i, column=0, padx=20, pady=10)
            botãoComprar=customtkinter.CTkButton(frameProdutos, text="Comprar", fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"))
            botãoComprar.grid(row=i, column=1, padx=20, pady=10, sticky="e")
            botãoEditar=customtkinter.CTkButton(frameProdutos, text="EditarProduto", fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"))
            botãoEditar.grid(row=i, column=2, padx=20, pady=10, sticky="e")
            self.produtos.append(produto)
            self.produtos.append(botãoComprar)
            self.produtos.append(botãoEditar)
        addButton=customtkinter.CTkButton(frame2, text="Adicionar novo item +")
        addButton.grid(row=2, column=0, padx=20, pady=20, sticky="w")
        

        #configurações do frame de adoção
        frame3=customtkinter.CTkFrame(self.app, width=600, height=600)
        frame3.grid_columnconfigure(0, weight=1)
        frame3.grid_rowconfigure(1, weight=1)
        label3=customtkinter.CTkLabel(frame3, text="PETs para adoção", font=customtkinter.CTkFont(size=20, weight="bold"))
        label3.grid(row=0, column=0, padx=20, pady=(20, 10))
        frameAnimais=customtkinter.CTkScrollableFrame(frame3)
        frameAnimais.grid(row=1, column=0, padx=20, pady=20, sticky="snew")
        frameAnimais.grid_columnconfigure(0, weight=1)
        self.animais=[]
        for i in range(10):
            animal = customtkinter.CTkLabel(frameAnimais, text=f"Animal {i+1}", font=customtkinter.CTkFont(size=20, weight="bold"))
            animal.grid(row=i, column=0, padx=20, pady=10)
            cadastrarAdoção=customtkinter.CTkButton(frameAnimais, text="Cadastrar adoção", fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"))
            cadastrarAdoção.grid(row=i, column=1, padx=20, pady=10, sticky="e")
            botãoEditar=customtkinter.CTkButton(frameAnimais, text="Editar perfil", fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"))
            botãoEditar.grid(row=i, column=2, padx=20, pady=10, sticky="e")
            self.animais.append(animal)
            self.animais.append(cadastrarAdoção)
            self.animais.append(botãoEditar)
        addButton=customtkinter.CTkButton(frame3, text="Adicionar novo animal +")
        addButton.grid(row=2, column=0, padx=20, pady=20, sticky="w")

        #configurações do frame de cadastros
        frame4=customtkinter.CTkFrame(self.app, width=600, height=600)
        frame4.grid_columnconfigure(0, weight=1)
        frame4.grid_rowconfigure(1, weight=1)
        tab = customtkinter.CTkTabview(frame4, width=250)
        tab.grid(row=1, column=0, padx=20, pady=(20, 10), sticky="snew")
        tab.add("Clientes")
        tab.tab("Clientes").grid_rowconfigure(0, weight=1)
        tab.tab("Clientes").grid_columnconfigure(0, weight=1)
        tab.add("Fornecedores")
        tab.tab("Fornecedores").grid_rowconfigure(0, weight=1)
        tab.tab("Fornecedores").grid_columnconfigure(0, weight=1)
        frameClientes=customtkinter.CTkScrollableFrame(tab.tab("Clientes"))
        frameClientes.grid(row=0, column=0, padx=20, pady=20, sticky="snew")
        frameClientes.grid_columnconfigure(0, weight=1)
        self.clientes=[]
        for i in range(10):
            cliente = customtkinter.CTkLabel(frameClientes, text=f"Cliente {i+1}", font=customtkinter.CTkFont(size=20, weight="bold"))
            cliente.grid(row=i, column=0, padx=20, pady=10)
            botãoEditar=customtkinter.CTkButton(frameClientes, text="Editar perfil", fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"))
            botãoEditar.grid(row=i, column=2, padx=20, pady=10, sticky="e")
            self.clientes.append(cliente)
            self.clientes.append(botãoEditar)
        frameFornecedores=customtkinter.CTkScrollableFrame(tab.tab("Fornecedores"))
        frameFornecedores.grid(row=0, column=0, padx=20, pady=20, sticky="snew")
        frameFornecedores.grid_columnconfigure(0, weight=1)
        self.fornecedores=[]
        for i in range(4):
            fornecedor = customtkinter.CTkLabel(frameFornecedores, text=f"Fornecedor {i+1}", font=customtkinter.CTkFont(size=20, weight="bold"))
            fornecedor.grid(row=i, column=0, padx=20, pady=10)
            botãoEditar=customtkinter.CTkButton(frameFornecedores, text="Editar perfil", fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"))
            botãoEditar.grid(row=i, column=2, padx=20, pady=10, sticky="e")
            self.fornecedores.append(fornecedor)
            self.fornecedores.append(botãoEditar)
        addButton=customtkinter.CTkButton(frame4, text="Adicionar novo Cliente +")
        addButton.grid(row=2, column=0, padx=20, pady=20, sticky="w")

        #configurações do frame da equipe
        frame5=customtkinter.CTkFrame(self.app, width=600, height=600)
        frame5.grid_columnconfigure(0, weight=1)
        frame5.grid_rowconfigure(1, weight=1)
        tab2 = customtkinter.CTkTabview(frame5, width=250)
        tab2.grid(row=1, column=0, padx=20, pady=(20, 10), sticky="snew")
        tab2.add("Funcionários")
        tab2.tab("Funcionários").grid_rowconfigure(0, weight=1)
        tab2.tab("Funcionários").grid_columnconfigure(0, weight=1)
        tab2.add("Veterinários")
        tab2.tab("Veterinários").grid_rowconfigure(0, weight=1)
        tab2.tab("Veterinários").grid_columnconfigure(0, weight=1)
        frameFunc=customtkinter.CTkScrollableFrame(tab2.tab("Funcionários"))
        frameFunc.grid(row=0, column=0, padx=20, pady=20, sticky="snew")
        frameFunc.grid_columnconfigure(0, weight=1)
        self.funcs=[]
        for i in range(10):
            func = customtkinter.CTkLabel(frameFunc, text=f"Funcionário {i+1}", font=customtkinter.CTkFont(size=20, weight="bold"))
            func.grid(row=i, column=0, padx=20, pady=10)
            botãoEditar=customtkinter.CTkButton(frameFunc, text="Editar perfil", fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"))
            botãoEditar.grid(row=i, column=2, padx=20, pady=10, sticky="e")
            self.funcs.append(func)
            self.funcs.append(botãoEditar)
        frameVet=customtkinter.CTkScrollableFrame(tab2.tab("Veterinários"))
        frameVet.grid(row=0, column=0, padx=20, pady=20, sticky="snew")
        frameVet.grid_columnconfigure(0, weight=1)
        self.vets=[]
        for i in range(4):
            vet = customtkinter.CTkLabel(frameVet, text=f"Veterinário {i+1}", font=customtkinter.CTkFont(size=20, weight="bold"))
            vet.grid(row=i, column=0, padx=20, pady=10)
            botãoEditar=customtkinter.CTkButton(frameVet, text="Editar perfil", fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"))
            botãoEditar.grid(row=i, column=2, padx=20, pady=10, sticky="e")
            self.vets.append(vet)
            self.vets.append(botãoEditar)
        addButton=customtkinter.CTkButton(frame5, text="Adicionar novo Funcionário +")
        addButton.grid(row=2, column=0, padx=20, pady=20, sticky="w")


        self.now=frame1
        self.now.grid(row=1, column=1, columnspan=2, pady=10, padx=10, sticky="snew")

        #configurações do frame lateral
        leftFrame_button1=customtkinter.CTkButton(leftFrame, width=80, height=80, text="", image=calendarIcon, command=lambda:changeFrameTo(frame1))
        leftFrame_button1.grid(row=0, column=0, padx=10, pady=10, sticky="n")
        leftFrame_button2=customtkinter.CTkButton(leftFrame, width=80, height=80, text="", image=cartIcon, command=lambda:changeFrameTo(frame2))
        leftFrame_button2.grid(row=1, column=0, padx=10, pady=10, sticky="n")
        leftFrame_button3=customtkinter.CTkButton(leftFrame, width=80, height=80, text="Adoção", command=lambda:changeFrameTo(frame3))
        leftFrame_button3.grid(row=2, column=0, padx=10, pady=10, sticky="n")
        leftFrame_button4=customtkinter.CTkButton(leftFrame, width=80, height=80, text="Gerenciamento\n de clientes", command=lambda:changeFrameTo(frame4))
        leftFrame_button4.grid(row=3, column=0, padx=10, pady=10, sticky="n")
        leftFrame_button5=customtkinter.CTkButton(leftFrame, width=80, height=80, text="Equipe", command=lambda:changeFrameTo(frame5))
        leftFrame_button5.grid(row=4, column=0, padx=10, pady=10, sticky="n")
        appearance_mode_label=customtkinter.CTkLabel(leftFrame, text="Appearance Mode:", anchor="w")
        appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0), sticky="n")
        appearance_mode_optionemenu=customtkinter.CTkComboBox(leftFrame, values=["Light", "Dark", "System"], command=change_appearance_mode_event)
        appearance_mode_optionemenu.set(self.app._get_appearance_mode().title())
        appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 10), sticky="n")

        #configurações da barra de pesquisa


        self.app.mainloop()

    
    def UserWindow(self):

        def exitBTN():
            self.user=None
            app.destroy()
            self.goto(self.LoginWindow)

        windowWidth=200
        windowHeight=200
        windowX=round(screenSize()[0]/2-windowWidth/2)
        windowY=round(screenSize()[1]/2-windowHeight/2)

        app = customtkinter.CTk()
        app.geometry("{}x{}+{}+{}".format(str(windowWidth),str(windowHeight),str(windowX+500),str(windowY-240)), )
        app.title("Conta")
        app.iconbitmap("imgs/icon.ico")

        app.grid_rowconfigure(0, weight=1)

        mainFrame=customtkinter.CTkFrame(app, width=180, height=100)
        mainFrame.grid(row=0, column=0, padx=10, pady=10, sticky="snew")
        logoutButton=customtkinter.CTkButton(app, width=180, height=50, text="Sair", command=exitBTN)
        logoutButton.grid(row=1, column=0, sticky="snew")

        app.mainloop()

App()
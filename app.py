import customtkinter
from tkinter import messagebox
from pyautogui import size as screenSize
from BEAN.bean import DB
import CGV
import hashlib
from PIL import Image
from datetime import datetime

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
            self.db.insert(self.db.USERS_TABLE, {"fullname": CGV.enc(fullname), "username": CGV.enc(username.lower()), "password": hashlib.sha256(password.encode()).hexdigest()})
            self.goto(self.LoginWindow)
        except:
            messagebox.showinfo("Erro", "Usuário já existe!")
            return False
        
    def login(self, username, password):
        if not username.strip() or not password.strip():
            messagebox.showinfo("Erro", "Preencha todos os campos!")
            return False
        users=self.db.selectAll(self.db.USERS_TABLE, f"username='{CGV.enc(username.lower())}' AND password='{hashlib.sha256(password.encode()).hexdigest()}'")
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

        self.app.bind("<Return>", lambda e:self.register(fullname.get(), username.get(), password.get()))

        self.app.mainloop()
    
    def HomeWindow(self):

        def changeFrameTo(frameFunc):
            self.now.grid_forget()
            self.now=frameFunc()
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
        adoptIcon=customtkinter.CTkImage(light_image=Image.open("imgs/adopt.png"), dark_image=Image.open("imgs/adopt.png"), size=(35, 35))
        clientsIcon=customtkinter.CTkImage(light_image=Image.open("imgs/clients.ico"), dark_image=Image.open("imgs/clients.ico"), size=(35, 35))
        employeesIcon=customtkinter.CTkImage(light_image=Image.open("imgs/employees.ico"), dark_image=Image.open("imgs/employees.ico"), size=(35, 35))
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
        
        def frame1Func():
        #configurações do frame de serviços
            frame1=customtkinter.CTkFrame(self.app, width=600, height=600)
            frame1.grid_rowconfigure(1, weight=1)
            frame1.grid_columnconfigure(0, weight=1)
            label1=customtkinter.CTkLabel(frame1, text="Calendário de serviços", font=customtkinter.CTkFont(size=20, weight="bold"))
            label1.grid(row=0, column=0, padx=20, pady=(20, 10))
            tabview=customtkinter.CTkTabview(frame1, width=250)
            tabview.grid(row=1, column=0, padx=10,pady=10, sticky="snew")
            tabview.add("Consulta veterinária")
            tabview.tab("Consulta veterinária").grid_rowconfigure((1,2,3,4,5), weight=1)
            tabview.tab("Consulta veterinária").grid_columnconfigure((0,1,2,3,4,5,6), weight=1)
            schedules=self.db.selectAll(self.db.SCHEDULES_TABLE)[:30]
            rowStatus=[0,0,0,0,0,0,0]
            for i in range(len(schedules)):
                date=CGV.dec(schedules[i]["date"])
                hour=CGV.dec(schedules[i]["hour"])
                d=datetime(day=int(date.split("/")[0]), month=int(date.split("/")[1]), year=int(date.split("/")[2]))
                rowStatus[d.weekday()]+=1
                day=customtkinter.CTkFrame(tabview.tab("Consulta veterinária"), width=100, height=80)
                day.grid(row=rowStatus[d.weekday()], column=d.weekday(), padx=10, pady=10, sticky="snew")
                customtkinter.CTkLabel(day, text=f"Dia: {date}").grid(row=0, column=0, padx=10, pady=10)
                customtkinter.CTkLabel(day, text=f"Horário: {hour}").grid(row=1, column=0, padx=10, pady=10)
           
            days = ["SEG", "TER", "QUA", "QUI", "SEX", "SAB", "DOM"]
            for i in range(len(days)):
                customtkinter.CTkLabel(tabview.tab("Consulta veterinária"), text=days[i]).grid(row=0, column=i, padx=10, pady=10)


            customtkinter.CTkButton(frame1, text="Agendar novo Serviço +", command=0).grid(row=2, column=0, padx=20, pady=20, sticky="w")

            return frame1

        def frame2Func():
        #configurações do frame de compras
            frame2=customtkinter.CTkFrame(self.app, width=600, height=600)
            frame2.grid_columnconfigure((0, 1), weight=1)
            frame2.grid_rowconfigure(1, weight=1)
            label2=customtkinter.CTkLabel(frame2, text="Estoque", font=customtkinter.CTkFont(size=20, weight="bold"))
            label2.grid(row=0, column=0, columnspan=2, padx=20, pady=(20, 10))
            frameProdutos=customtkinter.CTkScrollableFrame(frame2, width=700, height=700)
            frameProdutos.grid(row=1, column=0, columnspan=2, padx=20, pady=20, sticky="snew")
            frameProdutos.grid_columnconfigure((0,1), weight=1)
            products=self.db.selectAll(self.db.PRODUCTS_TABLE)[:50]
            for i in range(len(products)):
                p=products[i]
                customtkinter.CTkLabel(frameProdutos, text=f"Nome: {CGV.dec(p['name'])} | Marca: {CGV.dec(p['brand'])} | QTD: {p['stock']}", font=customtkinter.CTkFont(size=15, weight="bold")).grid(row=i, column=0, padx=20, pady=10, sticky="w")
                customtkinter.CTkButton(frameProdutos, text="Cadastrar compra", fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"), command=lambda:self.AddWindow("compra")).grid(row=i, column=1, padx=20, pady=10, sticky="e")
                customtkinter.CTkButton(frameProdutos, text="EditarProduto", fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE")).grid(row=i, column=2, padx=20, pady=10, sticky="e")
            customtkinter.CTkButton(frame2, text="Adicionar novo item +", command=lambda:self.AddWindow("produto")).grid(row=2, column=0, padx=20, pady=20, sticky="w")
            customtkinter.CTkButton(frame2, text="Histórico de compras").grid(row=2, column=1, padx=20, pady=20, sticky="e")
            return frame2
        
        def frame3Func():
        #configurações do frame de adoção
            frame3=customtkinter.CTkFrame(self.app, width=600, height=600)
            frame3.grid_columnconfigure(0, weight=1)
            frame3.grid_rowconfigure(1, weight=1)
            tab0 = customtkinter.CTkTabview(frame3, width=250)
            tab0.grid(row=1, column=0, padx=10, pady=10, sticky="snew")
            tab0.add("Pets")
            tab0.tab("Pets").grid_rowconfigure(0, weight=1)
            tab0.tab("Pets").grid_columnconfigure(0, weight=1)
            tab0.add("Para adoção")
            tab0.tab("Para adoção").grid_rowconfigure(0, weight=1)
            tab0.tab("Para adoção").grid_columnconfigure(0, weight=1)
            frameAdopt=customtkinter.CTkScrollableFrame(tab0.tab("Para adoção"))
            frameAdopt.grid(row=0, column=0, padx=20, pady=20, sticky="snew")
            frameAdopt.grid_columnconfigure(0, weight=1)
            adoptAnimals=self.db.selectAll(self.db.ANIMALS_TABLE, where="owner is null")[:50]
            for i in range(len(adoptAnimals)):
                a=adoptAnimals[i]
                customtkinter.CTkLabel(frameAdopt, text=f"Nome: {CGV.dec(a['name'])} | Idade: {CGV.dec(a['age'])}", font=customtkinter.CTkFont(size=20, weight="bold")).grid(row=i, column=0, padx=20, pady=10, sticky="w")
                customtkinter.CTkButton(frameAdopt, text="Cadastrar adoção", fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE")).grid(row=i, column=1, padx=20, pady=10, sticky="e")
                customtkinter.CTkButton(frameAdopt, text="Editar perfil", fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE")).grid(row=i, column=2, padx=20, pady=10, sticky="e")
            customtkinter.CTkButton(tab0.tab("Para adoção"), text="Adicionar novo animal +", command=lambda:self.AddWindow("animal para adoção")).grid(row=2, column=0, padx=20, pady=20, sticky="w")
            
            frameAnimais=customtkinter.CTkScrollableFrame(tab0.tab("Pets"))
            frameAnimais.grid(row=0, column=0, padx=20, pady=20, sticky="snew")
            frameAnimais.grid_columnconfigure(0, weight=1)
            animals=self.db.selectAll(self.db.ANIMALS_TABLE, where="owner NOT NULL")[:50]
            for i in range(len(animals)):
                a=animals[i]
                customtkinter.CTkLabel(frameAnimais, text=f"Nome: {CGV.dec(a['name'])} | Idade: {CGV.dec(a['age'])}", font=customtkinter.CTkFont(size=20, weight="bold")).grid(row=i, column=0, padx=20, pady=10, sticky="w")
                customtkinter.CTkButton(frameAnimais, text="Editar perfil", fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE")).grid(row=i, column=2, padx=20, pady=10, sticky="e")
            customtkinter.CTkButton(tab0.tab("Pets"), text="Adicionar novo animal +", command=lambda:self.AddWindow("animal")).grid(row=2, column=0, padx=20, pady=20, sticky="w")
            return frame3

        def frame4Func():
        #configurações do frame de cadastros
            frame4=customtkinter.CTkFrame(self.app, width=600, height=600)
            frame4.grid_columnconfigure(0, weight=1)
            frame4.grid_rowconfigure(1, weight=1)
            tab = customtkinter.CTkTabview(frame4, width=250)
            tab.grid(row=1, column=0, padx=10, pady=10, sticky="snew")
            tab.add("Clientes")
            tab.tab("Clientes").grid_rowconfigure(0, weight=1)
            tab.tab("Clientes").grid_columnconfigure(0, weight=1)
            tab.add("Fornecedores")
            tab.tab("Fornecedores").grid_rowconfigure(0, weight=1)
            tab.tab("Fornecedores").grid_columnconfigure(0, weight=1)
            frameClientes=customtkinter.CTkScrollableFrame(tab.tab("Clientes"))
            frameClientes.grid(row=0, column=0, padx=20, pady=20, sticky="snew")
            frameClientes.grid_columnconfigure(0, weight=1)
            clients=self.db.selectAll(self.db.CLIENTS_TABLE)[:50]
            for i in range(len(clients)):
                c=clients[i]
                customtkinter.CTkLabel(frameClientes, text=f"Nome: {CGV.dec(c['name'])}", font=customtkinter.CTkFont(size=20, weight="bold")).grid(row=i, column=0, padx=20, pady=10, sticky="w")
                customtkinter.CTkButton(frameClientes, text="Editar perfil", fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE")).grid(row=i, column=2, padx=20, pady=10, sticky="e")
            
            frameFornecedores=customtkinter.CTkScrollableFrame(tab.tab("Fornecedores"))
            frameFornecedores.grid(row=0, column=0, padx=20, pady=20, sticky="snew")
            frameFornecedores.grid_columnconfigure(0, weight=1)
            suppliers=self.db.selectAll(self.db.SUPPLIERS_TABLE)[:50]
            for i in range(len(suppliers)):
                s=suppliers[i]
                customtkinter.CTkLabel(frameFornecedores, text=f"Nome: {CGV.dec(s['name'])}", font=customtkinter.CTkFont(size=20, weight="bold")).grid(row=i, column=0, padx=20, pady=10, sticky="w")
                customtkinter.CTkButton(frameFornecedores, text="Editar perfil", fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE")).grid(row=i, column=2, padx=20, pady=10, sticky="e")
            customtkinter.CTkButton(tab.tab("Clientes"), text="Adicionar novo cliente +", command=lambda:self.AddWindow("cliente")).grid(row=2, column=0, padx=20, pady=20, sticky="w")
            customtkinter.CTkButton(tab.tab("Fornecedores"), text="Adicionar novo fornecedor +", command=lambda:self.AddWindow("fornecedor")).grid(row=2, column=0, padx=20, pady=20, sticky="w")
            return frame4

        def frame5Func():
            #configurações do frame da equipe
            frame5=customtkinter.CTkFrame(self.app, width=600, height=600)
            frame5.grid_columnconfigure(0, weight=1)
            frame5.grid_rowconfigure(1, weight=1)
            tab2 = customtkinter.CTkTabview(frame5, width=250)
            tab2.grid(row=1, column=0, padx=10, pady=10, sticky="snew")
            tab2.add("Funcionários")
            tab2.tab("Funcionários").grid_rowconfigure(0, weight=1)
            tab2.tab("Funcionários").grid_columnconfigure(0, weight=1)
            tab2.add("Veterinários")
            tab2.tab("Veterinários").grid_rowconfigure(0, weight=1)
            tab2.tab("Veterinários").grid_columnconfigure(0, weight=1)
            frameFunc=customtkinter.CTkScrollableFrame(tab2.tab("Funcionários"))
            frameFunc.grid(row=0, column=0, padx=20, pady=20, sticky="snew")
            frameFunc.grid_columnconfigure(0, weight=1)
            employees=self.db.selectAll(self.db.EMPLOYEES_TABLE)[:50]
            for i in range(len(employees)):
                e=employees[i]
                customtkinter.CTkLabel(frameFunc, text=f"Nome: {CGV.dec(e['name'])}", font=customtkinter.CTkFont(size=20, weight="bold")).grid(row=i, column=0, padx=20, pady=10, sticky="w")
                customtkinter.CTkButton(frameFunc, text="Editar perfil", fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE")).grid(row=i, column=2, padx=20, pady=10, sticky="e")
            
            frameVet=customtkinter.CTkScrollableFrame(tab2.tab("Veterinários"))
            frameVet.grid(row=0, column=0, padx=20, pady=20, sticky="snew")
            frameVet.grid_columnconfigure(0, weight=1)
            veterinarians=self.db.selectAll(self.db.VETERINARIANS_TABLE)[:50]
            for i in range(len(veterinarians)):
                v=veterinarians[i]
                customtkinter.CTkLabel(frameVet, text=f"Nome: {CGV.dec(v['name'])}", font=customtkinter.CTkFont(size=20, weight="bold")).grid(row=i, column=0, padx=20, pady=10, sticky="w")
                customtkinter.CTkButton(frameVet, text="Editar perfil", fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE")).grid(row=i, column=2, padx=20, pady=10, sticky="e")
            customtkinter.CTkButton(tab2.tab("Funcionários"), text="Adicionar novo funcionário +", command=lambda:self.AddWindow("funcionário")).grid(row=2, column=0, padx=20, pady=20, sticky="w")
            customtkinter.CTkButton(tab2.tab("Veterinários"), text="Adicionar novo veterinário +", command=lambda:self.AddWindow("veterinário")).grid(row=2, column=0, padx=20, pady=20, sticky="w")
            return frame5

        self.now=frame1Func()
        self.now.grid(row=1, column=1, columnspan=2, pady=10, padx=10, sticky="snew")

        #configurações do frame lateral
        leftFrame_button1=customtkinter.CTkButton(leftFrame, width=80, height=80, text="", image=calendarIcon, command=lambda:changeFrameTo(frame1Func))
        leftFrame_button1.grid(row=0, column=0, padx=10, pady=10, sticky="n")
        leftFrame_button2=customtkinter.CTkButton(leftFrame, width=80, height=80, text="", image=cartIcon, command=lambda:changeFrameTo(frame2Func))
        leftFrame_button2.grid(row=1, column=0, padx=10, pady=10, sticky="n")
        leftFrame_button3=customtkinter.CTkButton(leftFrame, width=80, height=80, text="", image=adoptIcon, command=lambda:changeFrameTo(frame3Func))
        leftFrame_button3.grid(row=2, column=0, padx=10, pady=10, sticky="n")
        leftFrame_button4=customtkinter.CTkButton(leftFrame, width=80, height=80, text="", image=clientsIcon, command=lambda:changeFrameTo(frame4Func))
        leftFrame_button4.grid(row=3, column=0, padx=10, pady=10, sticky="n")
        leftFrame_button5=customtkinter.CTkButton(leftFrame, width=80, height=80, text="", image=employeesIcon, command=lambda:changeFrameTo(frame5Func))
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

        windowWidth=365
        windowHeight=200
        windowX=round(screenSize()[0]/2-windowWidth/2)
        windowY=round(screenSize()[1]/2-windowHeight/2)

        app = customtkinter.CTk()
        app.geometry("{}x{}+{}+{}".format(str(windowWidth),str(windowHeight),str(windowX+400),str(windowY-240)))
        app.title("Conta")
        app.iconbitmap("imgs/icon.ico")

        app.grid_rowconfigure(0, weight=1)

        mainFrame=customtkinter.CTkFrame(app, width=180, height=100)
        mainFrame.grid(row=0, column=0, padx=10, pady=10, sticky="snew")
        mainFrame.grid_columnconfigure(1,weight=1)
        mainFrame.grid_rowconfigure(0, weight=1)
        profilePicFrame=customtkinter.CTkFrame(mainFrame, width=100, height=100, corner_radius=100)
        profilePicFrame.grid(row=0, column=0, rowspan=2, padx=10, pady=10)
        customtkinter.CTkLabel(mainFrame, text=f"Usuário: {CGV.dec(self.user['username'])[:10]}", font=customtkinter.CTkFont(size=20, weight="bold"), width=180).grid(row=0, column=1, padx=10, pady=10, sticky="w")
        customtkinter.CTkLabel(mainFrame, text=f"Nome: {CGV.dec(self.user['fullname']).split(' ')[0]}").grid(row=1, column=1, padx=10, pady=10, sticky="w") 
        logoutButton=customtkinter.CTkButton(app, width=180, height=50, text="Sair", command=exitBTN)
        logoutButton.grid(row=1, column=0, sticky="snew")

        app.mainloop()
    
    def AddWindow(self, var):

        windowWidth=400
        windowHeight=400
        windowX=round(screenSize()[0]/2-windowWidth/2)
        windowY=round(screenSize()[1]/2-windowHeight/2)

        app = customtkinter.CTk()
        app.geometry("{}x{}+{}+{}".format(str(windowWidth),str(windowHeight),str(windowX),str(windowY)), )
        app.title(f"Novo {var}")
        app.iconbitmap("imgs/icon.ico")

        mainFrame=customtkinter.CTkFrame(app)
        mainFrame.pack(padx=10, pady=10, fill="both", expand=True)
        titleLabel=customtkinter.CTkLabel(mainFrame, text=f"Novo {var}", font=customtkinter.CTkFont(size=20, weight="bold"))
        titleLabel.pack(padx=10, pady=10)

        if var =="cliente":
            def add():
                for i in atribs: 
                    if i.get().strip() == "": return messagebox.showinfo("Erro", "Preencha todos os campos!")

                name=CGV.enc(nameEntry.get().strip())
                email=CGV.enc(emailEntry.get().strip())
                cpf=CGV.enc(cpfEntry.get().strip())
                phone=CGV.enc(phoneEntry.get().strip())
                address=CGV.enc(addressEntry.get().strip().title())

                if len(cpf) != 11: return messagebox.showinfo("Erro", "CPF inválido")

                try:
                    self.db.execute(f"INSERT INTO {self.db.CLIENTS_TABLE} (name, email, cpf, phone, address) VALUES ('{name}','{email}','{cpf}','{phone}','{address}')")
                    messagebox.showinfo("Sucesso", "Cliente adicionado com sucesso!")
                    app.destroy()
                    
                except:
                    messagebox.showinfo("Erro", "Erro ao adicionar cliente, talvez cliente já exista")

            atribs=[]
            nameEntry=customtkinter.CTkEntry(mainFrame, width=300, placeholder_text="Nome")
            nameEntry.pack(padx=10, pady=10)
            emailEntry=customtkinter.CTkEntry(mainFrame, width=300, placeholder_text="Email")
            emailEntry.pack(padx=10, pady=10)
            cpfEntry=customtkinter.CTkEntry(mainFrame, width=300, placeholder_text="CPF")
            cpfEntry.pack(padx=10, pady=10)
            phoneEntry=customtkinter.CTkEntry(mainFrame, width=300, placeholder_text="Telefone")
            phoneEntry.pack(padx=10, pady=10)
            addressEntry=customtkinter.CTkEntry(mainFrame, width=300, placeholder_text="Endereço")
            addressEntry.pack(padx=10, pady=10)
            addButton=customtkinter.CTkButton(mainFrame, text="Adicionar", command=add)
            addButton.pack(padx=10, pady=10)
            atribs.append(nameEntry)
            atribs.append(emailEntry)
            atribs.append(cpfEntry)
            atribs.append(phoneEntry)
            atribs.append(addressEntry)

        elif var =="animal":
            def add():
                for i in atribs: 
                    if i.get().strip() == "": return messagebox.showinfo("Erro", "Preencha todos os campos!")

                name=CGV.enc(nameEntry.get().strip())
                age=CGV.enc(ageEntry.get().strip())
                owner=CGV.enc(ownerEntry.get().strip())
                clients=self.db.selectAll(self.db.CLIENTS_TABLE, where=f"cpf={owner}")
                if not clients:
                    return messagebox.showinfo("Erro", "Dono do animal não existe")
                owner=str(clients[0]["clientID"])
                try:
                    self.db.execute(f"INSERT INTO {self.db.ANIMALS_TABLE} (name, age, type, owner) VALUES ('{name}','{age}','{typeBox.get().strip()}',{owner})")
                    messagebox.showinfo("Sucesso", "Animal adicionado com sucesso!")
                    app.destroy()
                    
                except:
                    messagebox.showinfo("Erro", "Erro ao adicionar animal, talvez animal já exista")
            atribs=[]
            nameEntry=customtkinter.CTkEntry(mainFrame, width=300, placeholder_text="Nome")
            nameEntry.pack(padx=10, pady=10)
            ownerEntry=customtkinter.CTkEntry(mainFrame, width=300, placeholder_text="Dono(CPF) do animal")
            ownerEntry.pack(padx=10, pady=10)
            ageEntry=customtkinter.CTkEntry(mainFrame, placeholder_text="Idade")
            ageEntry.pack(padx=10, pady=10)
            typeLabel=customtkinter.CTkLabel(mainFrame, text="Espécie do animal:")
            typeLabel.pack(padx=10, pady=(10,0))
            typeBox=customtkinter.CTkComboBox(mainFrame, values=["Cachorro", "Gato", "Hamster", "Peixe", "Pássaro"])
            typeBox.pack(padx=10, pady=10)
            addButton=customtkinter.CTkButton(mainFrame, text="Adicionar", command=add)
            addButton.pack(padx=10, pady=10)
            atribs.append(nameEntry)
            atribs.append(ageEntry)
            atribs.append(typeBox)
            atribs.append(ownerEntry)

        elif var =="animal para adoção":
            def add():
                for i in atribs: 
                    if i.get().strip() == "": return messagebox.showinfo("Erro", "Preencha todos os campos!")

                name=CGV.enc(nameEntry.get().strip())
                age=CGV.enc(ageEntry.get().strip())
                owner="NULL"
                try:
                    self.db.execute(f"INSERT INTO {self.db.ANIMALS_TABLE} (name, age, type, owner) VALUES ('{name}','{age}','{typeBox.get().strip()}', {owner})")
                    messagebox.showinfo("Sucesso", "Animal adicionado com sucesso!")
                    app.destroy()
                    
                except:
                    messagebox.showinfo("Erro", "Erro ao adicionar animal, talvez animal já exista")
            atribs=[]
            nameEntry=customtkinter.CTkEntry(mainFrame, width=300, placeholder_text="Nome")
            nameEntry.pack(padx=10, pady=10)
            ageEntry=customtkinter.CTkEntry(mainFrame, placeholder_text="Idade")
            ageEntry.pack(padx=10, pady=10)
            typeLabel=customtkinter.CTkLabel(mainFrame, text="Espécie do animal:")
            typeLabel.pack(padx=10, pady=(10,0))
            typeBox=customtkinter.CTkComboBox(mainFrame, values=["Cachorro", "Gato", "Hamster", "Peixe", "Pássaro"])
            typeBox.pack(padx=10, pady=10)
            addButton=customtkinter.CTkButton(mainFrame, text="Adicionar", command=add)
            addButton.pack(padx=10, pady=10)
            atribs.append(nameEntry)
            atribs.append(ageEntry)
            atribs.append(typeBox)

        elif var =="produto":
            def add():
                for i in atribs: 
                    if i.get().strip() == "": return messagebox.showinfo("Erro", "Preencha todos os campos!")

                name=CGV.enc(nameEntry.get().strip())
                price=priceEntry.get().strip().replace(",", ".")
                brand=CGV.enc(brandEntry.get().strip())
                stock=stockEntry.get().strip()
                description=CGV.enc(descriptionEntry.get().strip())
                supplier=CGV.enc(supplierEntry.get().strip())
                suppliers=self.db.selectAll(self.db.SUPPLIERS_TABLE, where=f"cnpj='{supplier}'")
                if suppliers: supplier=str(suppliers[0]["supplierID"])
                else: return messagebox.showinfo("Erro", "Fornecedor não existe")
                
                try:
                    self.db.execute(f"INSERT INTO {self.db.PRODUCTS_TABLE} (name, price, brand, stock, description, supplier) VALUES ('{name}',{price},'{brand}',{stock},'{description}',{supplier})")
                    messagebox.showinfo("Sucesso", "Produto adicionado com sucesso!")
                    app.destroy()
                    
                except:
                    messagebox.showinfo("Erro", "Erro ao adicionar produto, talvez produto já exista")
            atribs=[]
            nameEntry=customtkinter.CTkEntry(mainFrame, width=300, placeholder_text="Nome")
            nameEntry.pack(padx=10, pady=10)
            priceEntry=customtkinter.CTkEntry(mainFrame, width=300, placeholder_text="Preço")
            priceEntry.pack(padx=10, pady=10)
            brandEntry=customtkinter.CTkEntry(mainFrame, width=300, placeholder_text="Marca")
            brandEntry.pack(padx=10, pady=10)
            stockEntry=customtkinter.CTkEntry(mainFrame, placeholder_text="Em estoque")
            stockEntry.pack(padx=10, pady=10)
            descriptionEntry=customtkinter.CTkEntry(mainFrame, width=300, placeholder_text="Descrição")
            descriptionEntry.pack(padx=10, pady=10)
            supplierEntry=customtkinter.CTkEntry(mainFrame, width=300, placeholder_text="Fornecedor(CNPJ)")
            supplierEntry.pack(padx=10, pady=10)
            addButton=customtkinter.CTkButton(mainFrame, text="Adicionar", command=add)
            addButton.pack(padx=10, pady=10)
            atribs.append(nameEntry)
            atribs.append(priceEntry)
            atribs.append(brandEntry)
            atribs.append(stockEntry)
            atribs.append(descriptionEntry)
            atribs.append(supplierEntry)

        elif var =="fornecedor":
            def add():
                for i in atribs: 
                    if i.get().strip() == "": return messagebox.showinfo("Erro", "Preencha todos os campos!")

                name=CGV.enc(nameEntry.get().strip())
                address=CGV.enc(addressEntry.get().strip())
                phone=CGV.enc(phoneEntry.get().strip())
                email=CGV.enc(emailEntry.get().strip())
                cnpj=CGV.enc(cnpjEntry.get().strip())

                if len(cnpj) != 14: return messagebox.showinfo("Erro", "CNPJ inválido")
                
                try:
                    self.db.execute(f"INSERT INTO {self.db.SUPPLIERS_TABLE} (name, address, phone, email, cnpj) VALUES ('{name}','{address}','{phone}','{email}','{cnpj}')")
                    messagebox.showinfo("Sucesso", "Fornecedor adicionado com sucesso!")
                    app.destroy()
                    
                except:
                    messagebox.showinfo("Erro", "Erro ao adicionar fornecedor, talvez fornecedor já exista")
            atribs=[]
            nameEntry=customtkinter.CTkEntry(mainFrame, width=300, placeholder_text="Nome")
            nameEntry.pack(padx=10, pady=10)
            addressEntry=customtkinter.CTkEntry(mainFrame, width=300, placeholder_text="Endereço")
            addressEntry.pack(padx=10, pady=10)
            phoneEntry=customtkinter.CTkEntry(mainFrame, width=300, placeholder_text="Telefone")
            phoneEntry.pack(padx=10, pady=10)
            emailEntry=customtkinter.CTkEntry(mainFrame, width=300, placeholder_text="Email")
            emailEntry.pack(padx=10, pady=10)
            cnpjEntry=customtkinter.CTkEntry(mainFrame, width=300, placeholder_text="CNPJ")
            cnpjEntry.pack(padx=10, pady=10)
            addButton=customtkinter.CTkButton(mainFrame, text="Adicionar", command=add)
            addButton.pack(padx=10, pady=10)
            atribs.append(nameEntry)
            atribs.append(addressEntry)
            atribs.append(phoneEntry)
            atribs.append(emailEntry)
            atribs.append(cnpjEntry)

        elif var=="veterinário":
            def add():
                for i in atribs: 
                    if i.get().strip() == "": return messagebox.showinfo("Erro", "Preencha todos os campos!")

                name=CGV.enc(nameEntry.get().strip())
                phone=CGV.enc(phoneEntry.get().strip())
                email=CGV.enc(emailEntry.get().strip())
                cpf=CGV.enc(cpfEntry.get().strip())
                wage=wageEntry.get().strip().replace(",", ".")
                address=CGV.enc(addressEntry.get().strip())

                if len(cpf) != 11: return messagebox.showinfo("Erro", "CPF inválido")
                
                try:
                    self.db.execute(f"INSERT INTO {self.db.VETERINARIANS_TABLE} (name, phone, email, cpf, wage, address) VALUES ('{name}', '{phone}', '{email}', '{cpf}', {wage}, '{address}')")
                    messagebox.showinfo("Sucesso", "Veterinário adicionado com sucesso!")
                    app.destroy()
                    
                except:
                    messagebox.showinfo("Erro", "Erro ao adicionar veterinário, talvez o veterianário já exista")

            atribs=[]
            nameEntry=customtkinter.CTkEntry(mainFrame, width=300, placeholder_text="Nome")
            nameEntry.pack(padx=10, pady=10)
            phoneEntry=customtkinter.CTkEntry(mainFrame, width=300, placeholder_text="Telefone")
            phoneEntry.pack(padx=10, pady=10)
            emailEntry=customtkinter.CTkEntry(mainFrame, width=300, placeholder_text="Email")
            emailEntry.pack(padx=10, pady=10)
            cpfEntry=customtkinter.CTkEntry(mainFrame, width=300, placeholder_text="CPF")
            cpfEntry.pack(padx=10, pady=10)
            wageEntry=customtkinter.CTkEntry(mainFrame, placeholder_text="Salário")
            wageEntry.pack(padx=10, pady=10)
            addressEntry=customtkinter.CTkEntry(mainFrame, width=300, placeholder_text="Endereço")
            addressEntry.pack(padx=10, pady=10)
            addButton=customtkinter.CTkButton(mainFrame, text="Adicionar", command=add)
            addButton.pack(padx=10, pady=10)
            atribs.append(nameEntry)
            atribs.append(phoneEntry)
            atribs.append(emailEntry)
            atribs.append(cpfEntry)
            atribs.append(wageEntry)
            atribs.append(addressEntry)

        elif var=="funcionário":
            def add():
                for i in atribs: 
                    if i.get().strip() == "": return messagebox.showinfo("Erro", "Preencha todos os campos!")

                name=CGV.enc(nameEntry.get().strip())
                email=CGV.enc(emailEntry.get().strip())
                cpf=CGV.enc(cpfEntry.get().strip())
                phone=CGV.enc(phoneEntry.get().strip())
                wage=wageEntry.get().strip().replace(",", ".")
                office=CGV.enc(officeEntry.get().strip())
                days=CGV.enc(daysEntry.get().strip())
                address=CGV.enc(addressEntry.get().strip())

                if len(cpf) != 11: return messagebox.showinfo("Erro", "CPF inválido")

                try:
                    self.db.execute(f"INSERT INTO {self.db.EMPLOYEES_TABLE} (name, email, cpf, phone, wage, office, hired_day, address) VALUES ('{name}', '{email}', '{cpf}', '{phone}', {wage}, '{office}', '{days}', '{address}')")
                    messagebox.showinfo("Sucesso", "Funcionário adicionado com sucesso!")
                    app.destroy()
                    
                except:
                    messagebox.showinfo("Erro", "Erro ao adicionar funcionário, talvez o funcionário já exista")

            app.geometry("{}x{}+{}+{}".format(str(windowWidth),500,str(windowX),str(windowY)))

            atribs=[]
            nameEntry=customtkinter.CTkEntry(mainFrame, width=300, placeholder_text="Nome")
            nameEntry.pack(padx=10, pady=10)
            emailEntry=customtkinter.CTkEntry(mainFrame, width=300, placeholder_text="Email")
            emailEntry.pack(padx=10, pady=10)
            cpfEntry=customtkinter.CTkEntry(mainFrame, width=300, placeholder_text="CPF")
            cpfEntry.pack(padx=10, pady=10)
            phoneEntry=customtkinter.CTkEntry(mainFrame, width=300, placeholder_text="Telefone")
            phoneEntry.pack(padx=10, pady=10)
            wageEntry=customtkinter.CTkEntry(mainFrame, placeholder_text="salário")
            wageEntry.pack(padx=10, pady=10)
            daysEntry=customtkinter.CTkEntry(mainFrame, width=300, placeholder_text="Data da contratação")
            daysEntry.pack(padx=10, pady=10)
            officeEntry=customtkinter.CTkComboBox(mainFrame, width=300, values=["Gerente", "Vendedor", "Atendente", "Limpeza", "Segurança", "TI"])
            officeEntry.pack(padx=10, pady=10)
            addressEntry=customtkinter.CTkEntry(mainFrame, width=300, placeholder_text="Endereço")
            addressEntry.pack(padx=10, pady=10)
            addButton=customtkinter.CTkButton(mainFrame, text="Adicionar", command=add)
            addButton.pack(padx=10, pady=10)
            atribs.append(nameEntry)
            atribs.append(emailEntry)
            atribs.append(cpfEntry)
            atribs.append(phoneEntry)
            atribs.append(wageEntry)
            atribs.append(daysEntry)
            atribs.append(addressEntry)

        app.mainloop()

App()
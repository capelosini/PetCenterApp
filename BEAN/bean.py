import sqlite3

class DB:
    USERS_TABLE="userlogin"
    CLIENTS_TABLE="client"
    ANIMALS_TABLE="animal"
    PRODUCTS_TABLE="product"
    SUPPLIERS_TABLE="supplier"
    VETERINARIANS_TABLE="veterinarian"
    EMPLOYEES_TABLE="employee"
    QUERIES_TABLE="query"
    SCHEDULES_TABLE="schedule"
    SALES_TABLE="sale"

    def __init__(self):

        dbStructure=[
            f"CREATE TABLE IF NOT EXISTS {self.USERS_TABLE} (userID INTEGER PRIMARY KEY AUTOINCREMENT, fullname TEXT NOT NULL, username varchar(20) UNIQUE NOT NULL, password char(32) NOT NULL)",
            f"CREATE TABLE IF NOT EXISTS {self.CLIENTS_TABLE} (clientID INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, email varchar(35) UNIQUE NOT NULL, cpf char(11) UNIQUE NOT NULL, phone varchar(13) UNIQUE NOT NULL, address TEXT NOT NULL)",
            f"CREATE TABLE IF NOT EXISTS {self.ANIMALS_TABLE} (animalID INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, age int(100) NOT NULL, type TEXT NOT NULL, owner INTEGER NOT NULL, FOREIGN KEY(owner) REFERENCES {self.CLIENTS_TABLE}(clientID))",
            f"CREATE TABLE IF NOT EXISTS {self.PRODUCTS_TABLE} (produtctID INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, price REAL NOT NULL, brand TEXT NOT NULL, stock INTEGER NOT NULL, description TEXT NOT NULL, supplier INTEGER NOT NULL, FOREIGN KEY(supplier) REFERENCES {self.SUPPLIERS_TABLE}(supplierID))",
            f"CREATE TABLE IF NOT EXISTS {self.SUPPLIERS_TABLE} (supplierID INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, address TEXT NOT NULL, phone varchar(13) UNIQUE NOT NULL, email varchar(35) UNIQUE NOT NULL, CNPJ char(14) UNIQUE NOT NULL)",
            f"CREATE TABLE IF NOT EXISTS {self.VETERINARIANS_TABLE} (veterinarianID INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, phone varchar(13) unique NOT NULL, email varchar(35) UNIQUE NOT NULL, CPF char(11) UNIQUE not NULL, wage REAL NOT NULL, address TEXT NOT NULL)",
            f"CREATE TABLE IF NOT EXISTS {self.EMPLOYEES_TABLE} (employeeID INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, email varchar(35) UNIQUE NOT NULL, CPF char(11) UNIQUE NOT NULL, phone varchar(13) UNIQUE NOT NULL, wage REAL NOT NULL, office TEXT NOT NULL, hired_day varchar(10) NOT NULL, address TEXT NOT NULL)",
            f"CREATE TABLE IF NOT EXISTS {self.QUERIES_TABLE} (query_ID INTEGER PRIMARY KEY AUTOINCREMENT, type TEXT NOT NULL, date varchar(10) NOT NULL, animalqry INTEGER NOT NULL, veterinarianqry INTEGER NOT NULL, FOREIGN KEY(animalqry) REFERENCES {self.ANIMALS_TABLE}(animalid), FOREIGN KEY(veterinarianqry) REFERENCES {self.VETERINARIANS_TABLE}(veterinarianid))",
            f"CREATE TABLE IF NOT EXISTS {self.SCHEDULES_TABLE} (scheduleID INTEGER PRIMARY KEY AUTOINCREMENT, date varchar(10) NOT NULL, hour varchar(5) NOT NULL, client_schdl INTEGER NOT NULL, animal_schdl INTEGER NOT NULL, veterinarian_schdl INTEGER NOT NULL, FOREIGN KEY(client_schdl) REFERENCES {self.CLIENTS_TABLE}(clientid), FOREIGN KEY(animal_schdl) REFERENCES {self.ANIMALS_TABLE}(animalid), FOREIGN KEY(veterinarian_schdl) REFERENCES {self.VETERINARIANS_TABLE}(veterinarianid))",
            f"CREATE TABLE IF NOT EXISTS {self.SALES_TABLE} (saleID INTEGER PRIMARY KEY AUTOINCREMENT, sale_date varchar(10) NOT NULL, client_sale INTEGER NOT NULL, product_sale INTEGER NOT NULL, total REAL NOT NULL, payment TEXT NOT NULL, FOREIGN KEY(client_sale) REFERENCES {self.CLIENTS_TABLE}(clientid), FOREIGN KEY(product_sale) REFERENCES {self.PRODUCTS_TABLE}(produtctid))"
        ]

        self.conn = sqlite3.connect('BEAN/PetShopApp.db')
        self.cur = self.conn.cursor()
        for i in dbStructure:
            self.cur.execute(i)
        self.conn.commit()

    def selectToJson(self, x):
        out=[]
        for data in x:
            t={}
            for i in range(len(data)):
                t[self.cur.description[i][0]]=data[i]
            out.append(t)
        return out

    def insert(self, table, values):
        vs = list(dict.values(values))
        for v in range(len(vs)): vs[v]='"'+vs[v]+'"'
        self.cur.execute(f"INSERT INTO {table} ({','.join(dict.keys(values))}) VALUES ({','.join(vs)})")
        self.conn.commit()

    def selectAll(self, table, where=None):
        w=""
        if where:
            w=f"WHERE {where}"
        self.cur.execute(f"SELECT * FROM {table} {w}")
        return self.selectToJson(self.cur.fetchall())
    
    def delete(self, table, where):
        if not where.strip(): return
        self.cur.execute(f"DELETE FROM {table} WHERE {where}")
        self.conn.commit()

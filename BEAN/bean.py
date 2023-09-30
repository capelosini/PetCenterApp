import sqlite3

class DB:
    USERS_TABLE="userlogin"
    CLIENTS_TABLE="client"
    ANIMALS_TABLE="animal"
    PRODUCTS_TABLE="product"
    SUPPLIERS_TABLE="supplier"
    VETERINARIANS_TABLE="veterinarian"

    def __init__(self):
        self.conn = sqlite3.connect('BEAN/PetShopApp.db')
        self.cur = self.conn.cursor()
        self.cur.execute(f"CREATE TABLE IF NOT EXISTS {self.USERS_TABLE} (userID INTEGER PRIMARY KEY AUTOINCREMENT, fullname TEXT NOT NULL, username varchar(20) UNIQUE NOT NULL, password char(32) NOT NULL)")
        self.conn.commit()

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
        return self.cur.fetchall()
    
    def delete(self, table, where):
        if not where.strip(): return
        self.cur.execute(f"DELETE FROM {table} WHERE {where}")
        self.conn.commit()

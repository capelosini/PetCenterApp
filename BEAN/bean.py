import sqlite3

class DB:
    USERS_TABLE="users"

    def __init__(self):
        self.conn = sqlite3.connect('BEAN/PetShopApp.db')
        self.cur = self.conn.cursor()
        self.cur.execute(f"CREATE TABLE IF NOT EXISTS {self.USERS_TABLE} (id INTEGER PRIMARY KEY AUTOINCREMENT, username varchar(20), password varchar(30))")
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

db=DB()
db.insert(db.USERS_TABLE, {'username':'teste1', 'password':'teste1'})
print(db.selectAll(db.USERS_TABLE))
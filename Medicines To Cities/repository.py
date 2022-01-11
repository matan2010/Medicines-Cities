import sqlite3

from DAO import _Vaccines, _Suppliers, _Clinics, _Logistics


class _Repository:
    def __init__(self):
        self._conn = sqlite3.connect('database.db')
        self.vaccines = _Vaccines(self._conn)
        self.suppliers = _Suppliers(self._conn)
        self.clinics = _Clinics(self._conn)
        self.logistics = _Logistics(self._conn)

    def crate_tables(self):
        self._conn.executescript("""
            CREATE TABLE logistics(
                id INTEGER PRIMARY KEY,  
                name STRING NOT NULL,
                count_sent INTEGER NOT NULL, 
                count_received INTEGER NOT NULL
            );
            
            CREATE TABLE clinics(
                id INTEGER PRIMARY KEY, 
                location STRING NOT NULL, 
                demand INTEGER NOT NULL,
                logistic INTEGER REFERENCES logistics(id)
            );
            
            CREATE TABLE suppliers(
                id INTEGER PRIMARY KEY,
                name STRING NOT NULL,
                logistic INTEGER REFERENCES logistics(id)
            );
            
            CREATE TABLE vaccines(
                id INTEGER PRIMARY KEY,
                date DATE NOT NULL,
                supplier INTEGER REFERENCES suppliers(id), 
                quantity INTEGER NOT NULL
            );"""
                                 )

    def get_total_demand(self):
        return (self._conn.execute("""
            SELECT sum(clinics.demand)
            from clinics
        """
                                   )).fetchone()

    def get_total_inventory(self):
        return (self._conn.execute("""
            SELECT sum(vaccines.quantity)
            from vaccines
        """
                                   )).fetchone()

    def get_total_received(self):
        return (self._conn.execute("""
            SELECT sum(logistics.count_received)
            from logistics
        """
                                   )).fetchone()

    def get_total_sent(self):
        return (self._conn.execute("""
            SELECT sum(logistics.count_sent)
            from logistics
        """)).fetchone()

    def get_max_id_vaccines(self):
        return (self._conn.execute("""
            SELECT max(vaccines.id)
            from vaccines
        """)).fetchone()

    def get_id_supplier(self, supplier):
        return (self._conn.execute("""
            SELECT suppliers.id
            from suppliers
            WHERE suppliers.name=(?)
        """, [supplier])).fetchone()

    def update_log_count_received(self, ans):
        self._conn.execute("""
             UPDATE logistics
             SET count_received = count_received+(?)
             WHERE logistics.id=(?)
        """, [ans(0), ans(1)])

    def update_demand(self, location, demand):
        self._conn.execute("""
            UPDATE clinics
            SET demand=demand-(?)
            WHERE clinics.location=(?)
        """, [int(demand), location])

    def get_clinics_logistic(self, location):
        return (self._conn.execute("""
            SELECT clinics.logistic
            FROM clinics
            WHERE clinics.location=(?)
        """, [location])).fetchone()

    def get_vaccines(self):
        return (self._conn.execute("""
                    SELECT *
                    FROM vaccines
                    ORDER BY date('now') - date DESC
                """)).fetchall()

    def update_count_sent(self, amount, id):
        self._conn.execute("""
            UPDATE logistics
            SET count_sent=count_sent+(?)
            WHERE logistics.id=(?)
        """, [int(amount), int(id)])

    def remove_vaccine(self, date,id):
        self._conn.execute("""
            DELETE FROM vaccines
            WHERE vaccines.date=(?) AND vaccines.id=(?)
            """, [str(date),str(id)]
                           )

    def update_vaccine_quantity(self, amount, id):
        self._conn.execute("""
            UPDATE vaccines
            SET quantity = quantity - (?)
            WHERE vaccines.id = (?)
        """, [int(amount), int(id)])

    def update_count_received(self, amount, id):
        self._conn.execute("""
                    UPDATE logistics
                    SET count_received = count_received + (?)
                    WHERE logistics.id = (?)
                """, [int(amount), int(id)])

    def close_db(self):
        self._conn.commit()
        self._conn.close()


repo = _Repository()

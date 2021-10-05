import psycopg2 as psycopg2
import argparse
import os

class DatabaseManager:
    """Class that contains function to manage the pgSQL database"""

    cloudip = os.environ.get('CLOUD_IP')
    cloudpassword = os.environ.get('CLOUD_PASSWORD')

    localpassword = os.environ.get('DB_PASSWORD')

    def __init__(self):
        return

    def createDB(self, new_dbname, host='local'):
        if host == 'cloud':
            con = psycopg2.connect(database='postgres', user="postgres", password=self.cloudpassword, host=self.cloudip, port='5432')
        else:
            con = psycopg2.connect(database='postgres', user="postgres", password=self.localpassword, host="127.0.0.1", port="5432")

        cur = con.cursor()
        cur.execute(f'''CREATE DATABASE {new_dbname}''')
        con.commit()
        con.close()
        print(f"Database {new_dbname} created")
        return
# ------------------------------- Function that creates a table in a pgSQL database ----------------------------------
    def createTable(self, database, name, cols, dtype, host='local'):

        if host == 'cloud':
            con = psycopg2.connect(database=database, user="postgres", password=self.cloudpassword, host=self.cloudip, port='5432')
        else:
            con = psycopg2.connect(database=database, user="postgres", password=self.localpassword, host="127.0.0.1", port="5432")

        cur = con.cursor()
        assert isinstance(name, object)
        i = 0
        str = ['id serial PRIMARY KEY']
        while i < len(cols):
            a = cols[i]
            b = dtype[i]
            c = a + " " + b
            str.append(c)
            i = i+1

        fullstr= ", ".join(str)
        cur.execute('''CREATE TABLE {} ({})'''.format(name, fullstr))
        con.commit()
        con.close()
        print("Table {} created".format(name))
        return

    def deleteTable(self, database, table, host='local'):

        if host == 'cloud':
            con = psycopg2.connect(database=database, user="postgres", password=self.cloudpassword, host=self.cloudip, port='5432')
        else:
            con = psycopg2.connect(database=database, user="postgres", password=self.localpassword, host="127.0.0.1", port="5432")

        cur = con.cursor()
        cur.execute('DROP TABLE IF EXISTS {}'.format(table))
        con.commit()
        con.close()
        print('Table {} deleted'.format(table))

# ----------------------------------- Function to insert a query -------------------------------------------------

    def insertQ(self, database, tname, params, vals, host='local'):

        if host == 'cloud':
            con = psycopg2.connect(database=database, user="postgres", password=self.cloudpassword, host=self.cloudip, port='5432')
        else:
            con = psycopg2.connect(database=database, user="postgres", password=self.localpassword, host="127.0.0.1", port="5432")

        cur = con.cursor()
        assert isinstance(tname, object)
        parameters = ", "
        parameters = parameters.join(params)

        for i in range(len(vals)):
            vals[i] = "'{}'".format(str(vals[i]))

        values = ", "
        values = values.join(vals)
        cur.execute("INSERT INTO {} ({}) VALUES({})".format(tname, parameters, values))
        # print("Query has been committed to {}".format(tname))
        con.commit()
        con.close()
        return

# ------------------------------- Function to select all queries ------------------------------------------------------
    def selectAll(self, database, tname, cols, host='local'):

        if host == 'cloud':
            con = psycopg2.connect(database=database, user="postgres", password=self.cloudpassword, host=self.cloudip,
                                   port='5432')
        else:
            con = psycopg2.connect(database=database, user="postgres", password=self.localpassword, host="127.0.0.1", port="5432")

        cur = con.cursor()
        if isinstance(cols, tuple):
            parameters = ", "
            parameters = parameters.join(cols)
        else:
            parameters = cols

        cur.execute(
            "SELECT {} FROM {};".format(parameters, tname))  # This statement will limit the list
        entries = cur.fetchall()  # Fetch all retrieved values
        # entries = cur.fetchmany(10)
        result = []
        for entry in entries:
            for i in range(len(entry)):
                if isinstance(cols, tuple):
                    thisEntry = str(cols[i]) + ':' + str(entry[i])
                    result.append(thisEntry)
                else:
                    thisEntry = str(entry[i])
                    result.append((thisEntry))
        con.close()
        return result

    # todo: add a select latest function
    # todo: add a select all parameters method that can be used as "select * from ..." -> might need GUI for this
# ------------------------------ Function to select a single query ---------------------------------------------
    def select(self, database, tname, cols, pattern, host='local'):
        # Cols are the columns that you want to select from the table.
        # pattern is <parameter of interest> operator <value>
        if host == 'cloud':
            con = psycopg2.connect(database=database, user="postgres", password=self.cloudpassword, host=self.cloudip, port='5432')
        else:
            con = psycopg2.connect(database=database, user="postgres", password=self.localpassword, host="127.0.0.1", port="5432")

        cur = con.cursor()
        if isinstance(cols, tuple) or isinstance(cols, list):
            parameters = ", "
            parameters = parameters.join(cols)
        else:
            parameters = cols

        cur.execute("SELECT {} FROM {} WHERE {};".format(parameters, tname, pattern))  # This statement will limit the list
        entries = cur.fetchall()  # Fetch all retrieved values
        # entries = cur.fetchmany(10)
        result = []
        for entry in entries:
            for i in range(len(entry)):
                if isinstance(cols, tuple) or isinstance(cols, list):
                    thisEntry = str(cols[i]) + ':' + str(entry[i])
                    result.append(thisEntry)
                else:
                    thisEntry = str(entry[i])
                    result.append(thisEntry)
        con.close()
        return result

    # Select function for the weather readings (due to large number of weather entries)
    def Wselect(self, database, tname, cols, pattern, host='local'):
        # Cols are the columns that you want to select from the table.
        # pattern is <parameter of interest> operator <value>
        if host == 'cloud':
            con = psycopg2.connect(database=database, user="postgres", password=self.cloudpassword, host=self.cloudip, port='5432')
        else:
            con = psycopg2.connect(database=database, user="postgres", password=self.localpassword, host="127.0.0.1", port="5432")

        cur = con.cursor()
        if isinstance(cols, tuple):
            parameters = ", "
            parameters = parameters.join(cols)
        else:
            parameters = cols

        cur.execute("SELECT {} FROM {} WHERE {} ORDER BY ID ASC;".format(parameters, tname, pattern))  # This statement will limit the list
        # entries = cur.fetchall()  # Fetch all retrieved values
        entries = cur.fetchone()
        result = []
        i = 0
        for entry in entries:
            if isinstance(cols, tuple):
                thisEntry = str(cols[i]) + ':' + str(entry)
                result.append(thisEntry)
                i = i + 1
            else:
                thisEntry = str(entry)
                result.append(thisEntry)
                i = i + 1
        con.close()
        return result

# ------------------------------ Function to update a query ------------------------------------------------------
    def updateQ(self, database, tname, param, val, id, host='local'):
        if host == 'cloud':
            con = psycopg2.connect(database=database, user="postgres", password=self.cloudpassword, host=self.cloudip, port='5432')
        else:
            con = psycopg2.connect(database=database, user="postgres", password=self.localpassword, host="127.0.0.1", port="5432")

        cur = con.cursor()
        cur.execute("UPDATE {} set {} = {} where id={}".format(tname, param, str(val), str(id)))
        con.commit()
        con.close()

    def createTrigger(self, database, host='local'):
        if host == 'cloud':
            con = psycopg2.connect(database=database, user="postgres", password=self.cloudpassword, host=self.cloudip, port='5432')
        else:
            con = psycopg2.connect(database=database, user="postgres", password=self.localpassword, host="127.0.0.1", port="5432")

        cur = con.cursor()
        cur.execute('CREATE TRIGGER UPDATERT BEFORE INSERT ON PUBLIC.BATTERY FOR EACH ROW EXECUTE PROCEDURE'
                    ' PUBLIC.UPDATE_BATTERYRT();')
        con.commit()
        con.close()

    def updateQ2(self, database, tname, param, val, helio_id, host='local'):
        if host == 'cloud':
            con = psycopg2.connect(database=database, user="postgres", password=self.cloudpassword, host=self.cloudip,
                                   port='5432')
        else:
            con = psycopg2.connect(database=database, user="postgres", password=self.localpassword, host="127.0.0.1", port="5432")

        cur = con.cursor()
        cur.execute("UPDATE {} set {} = '{}' where helio_id = '{}'".format(tname, param, str(val), str(helio_id)))
        con.commit()
        con.close()

# # Run to reset local database
if __name__=='__main__':
    DB = DatabaseManager()
    dbname = 'default'

    parser = argparse.ArgumentParser('Enter database name')
    parser.add_argument('-dbname', dest='dbname', metavar='dbname',
                        help='Enter the name of the desired local database to be setup')

    args = parser.parse_args()

    if args.dbname is not None:
        dbname = args.dbname

    # for i in range(13, 26):
        # for j in range(1, 7):
            # helio_id = f'{i}{j}'
            # DB.deleteTable(dbname, f'local_helio{helio_id}', 'local')

    # DB.deleteTable(dbname, 'local_helio_list', 'local')
    # DB.deleteTable(dbname, 'local_pod_list', 'local')
    # DB.deleteTable(dbname, 'helio_status', 'local')

    DB.createTable(dbname, 'local_helio_list', ['helio_id', 'date'],
                   ['varchar(50) unique not null', 'timestamp not null'], 'local')

    DB.createTable(dbname, 'local_pod_list', ['pod_id', 'helio_id', 'helio_status', 'helio_location', 'date'],
                   ['varchar(50) not null', 'varchar(50) not null', 'varchar(50) not null',
                    'varchar(127)', 'timestamp not null'], 'local')

    DB.createTable(dbname, 'helio_status', ['helio_id', 'status', 'date', 'set_motor1', 'set_motor2'],
                   ['varchar(50) not null', 'varchar(50) not null', 'timestamp not null', 'real', 'real'], 'local')
                   
    # DB.createTable('aggdata', 'agg1', ['pod_id', 'pod_status', 'helio_status', 'date'],
                   # ['varchar(50) not null', 'varchar(50) not null',
                    # 'json', 'timestamp not null'])

# Run to reset cloud database
# if __name__ == '__main__':
    # DB = DatabaseManager()

    # for i in range(1, 58):
        # for j in range(1, 7):
            # helio_id = f'{i}{j}'
            # DB.deleteTable('appdata', f'helio{helio_id}', 'cloud')

    # DB.deleteTable('appdata', 'helio_list', 'cloud')
    # DB.deleteTable('appdata', 'pod_list', 'cloud')
    # DB.deleteTable('aggdata', 'agg1', 'cloud')

    # DB.createTable('appdata', 'helio_list', ['helio_id', 'date'],
                   # ['varchar(50) unique not null', 'timestamp not null'], 'cloud')

    # DB.createTable('appdata', 'pod_list', ['pod_id', 'helio_id', 'helio_status', 'helio_location', 'date'],
                   # ['varchar(50) not null', 'varchar(50) not null', 'varchar(50) not null',
                    # 'varchar(127)', 'timestamp not null'], 'cloud')

    # DB.createTable('aggdata', 'agg1', ['pod_id', 'pod_status', 'helio_status', 'date'],
                   # ['varchar(50) not null', 'varchar(50) not null',
                    # 'json', 'timestamp not null'], 'cloud')


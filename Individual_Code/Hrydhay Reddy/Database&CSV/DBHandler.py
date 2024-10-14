
import psycopg2
import json
import csv
#---------------------------------------------------------------------------------------------------

DB_NAME = "leafDB"
DB_USER = "postgres"
DB_PASS = "12345"
DB_HOST = "localhost"
DB_PORT = "5432"

#---------------------------------------------------------------------------------------------------

def SaveData():
    TestConnection()

def TestConnection():
    try:
        conn = psycopg2.connect(database=DB_NAME,
                                user=DB_USER,
                                password=DB_PASS,
                                host=DB_HOST,
                                port=DB_PORT)
        print("Database connected successfully")
    except:
        print("Database not connected successfully")
    
    selectDB(conn)

# def insertDB(table):
    # cur = conn.cursor()
    # cur.execute("INSERT * FROM public.\"Dummy\"")
    # rows = cur.fetchall()
    # SaveToCSV(rows)

# def deleteDB(table):
    # cur = conn.cursor()
    # cur.execute("DELETE FROM public.\"Dummy\"")
    # rows = cur.fetchall()
    # SaveToCSV()

# def updateDB(table):
    # cur = conn.cursor()
    # cur.execute("UPDATE * FROM public.\"Dummy\"")
    # rows = cur.fetchall()
    # SaveToCSV()

def selectDB(conn):
    cur = conn.cursor()
    cur.execute("SELECT * FROM public.\"dummy\"")
    rows = cur.fetchall()
    conn.close()
    SaveToCSV(rows)

def SaveToCSV(rows):
    for data in rows:
        data = [{'id': data[0], 'name': data[1], 'surname': data[2]}]
        
        try:
            with open('output.csv', 'a', newline='') as csvfile:
                fieldnames = ['id', 'name', 'surname']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                #writer.writeheader()
                writer.writerows(data)
        except:
            print("Error in creating file.\nFile already exists")
    print('Data fetched successfully')
    print(data)

SaveData()


# SQL Insert for Dummy Table - Tempory
# INSERT INTO public.dummy(
# 	id, name, surname)
# 	VALUES (1,'Jacques','Van Niekerk'),
# 			(2,'Hrudhay','Reddy');
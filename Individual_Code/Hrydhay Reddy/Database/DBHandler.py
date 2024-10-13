
import psycopg2
import json

#---------------------------------------------------------------------------------------------------

DB_NAME = "leafDB"
DB_USER = "postgres"
DB_PASS = "12345"
DB_HOST = "localhost"
DB_PORT = "5432"

#---------------------------------------------------------------------------------------------------

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
    cur = conn.cursor()
    cur.execute("SELECT * FROM public.\"Dummy\"") #public.\"Registration\"
    rows = cur.fetchall()
    for data in rows:
        print("ID :" + str(data[0]))
        print("NAME :" + data[1])
        print("SURNAME :" + data[2])
    print('Data fetched successfully')
    conn.close()
    
    #Data to be written
    dictionary = {
        "id": [data[0]],
        "name":[data[1]],
        'surname':[data[2]]
    }
    
    SaveToJson(dictionary)

#---------------------------------------------------------------------------------------------------

def SaveToJson(dictionary):
    # Serializing json
    json_object = json.dumps(dictionary, indent=4)

    # Writing to sample.json
    with open("sample.json", "w") as outfile:
        outfile.write(json_object)

#---------------------------------------------------------------------------------------------------

TestConnection()

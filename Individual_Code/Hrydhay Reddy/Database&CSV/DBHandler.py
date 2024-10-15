
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
        conn = 'null'
    finally:
        return conn

# =========================================== SELECT STATEMENTS ===========================================

def selectDetails(conn):
    cur = conn.cursor()
    cur.execute("SELECT * FROM public.\"details\"")
    rows = cur.fetchall()
    cur.close()
    return rows

def selectImages(conn):
    cur = conn.cursor()
    cur.execute("SELECT * FROM public.\"images\"")
    rows = cur.fetchall()
    cur.close()
    return rows

def selectImageData(conn):
    cur = conn.cursor()
    cur.execute("SELECT * FROM public.\"imagedata\"")
    rows = cur.fetchall()
    cur.close()
    return rows

# =========================================== INSERT STATEMENTS ===========================================

def insertDetails(conn):
    cur = conn.cursor()
    cur.execute(f'INSERT INTO public.\"details\" (Details_ID,ImageLocation,ImageDate) ' 
                + 'VALUES {data1},{data2},{data3}')
    conn.commit()
    cur.close()

def insertImages(conn):
    cur = conn.cursor()
    cur.execute('INSERT INTO public.\"images\" (Image_ID, Details_ID, ImagePathBack, ImagePathFront) '
                + 'VALUES {data4},{data5},{data6},{data7}')
    conn.commit()
    cur.close()

def insertImageData(conn):
    cur = conn.cursor()
    cur.execute('INSERT INTO public.\"imagedata\" (ImageData_ID,Image_ID,ImageLable,Lamina_Area,Lamina_Length,Lamina_Width,Scar_Count,Scar_Area,DamagePercentage,Petiole_Length) ' 
                + 'VALUES {data8},{data9},{data10},{data11},{data12},{data13},{data14},{data15},{data16},{data17}')
    conn.commit()
    cur.close()

# =========================================== UPDATE STATEMENTS ===========================================

def updateDetails(conn):
    cur = conn.cursor()
    cur.execute("UPDATE public.\"details\" SET ImageLocation = {data1}, ImageDate = {data2} WHERE Details_ID = {data3}")
    conn.commit()
    cur.close()

def updateImages(conn):
    cur = conn.cursor()
    cur.execute("UPDATE public.\"images\" SET Details_ID = {data4}, ImagePathBack = {data5}, ImagePathFront = {data6} WHERE Image_ID = {data7}")
    conn.commit()
    cur.close()

def updateImageData(conn):
    cur = conn.cursor()
    cur.execute("UPDATE public.\"imagedata\" SET Image_ID = {data8}, ImageLable = {data9}, Lamina_Area = {data10}, Lamina_Length = {data11}, Lamina_Width = {data12}, Scar_Count = {data13}, Scar_Area = {data14}, DamagePercentage = {data15}, Petiole_Length = {data16}  WHERE ImageData_ID = {data17}")
    conn.commit()
    cur.close()

# =========================================== DELETE STATEMENTS ===========================================

def deleteDetails(conn):
    cur = conn.cursor()
    cur.execute("DELETE FROM public.\"details\" WHERE Details_ID = {data1}")
    conn.commit()
    #totalAffectedRows = cur.rowcount
    cur.close()

def deleteImages(conn):
    cur = conn.cursor()
    cur.execute("DELETE FROM public.\"images\" WHERE Image_ID = {data2}")
    conn.commit()
    #totalAffectedRows = cur.rowcount
    cur.close()

def deleteImageData(conn):
    cur = conn.cursor()
    cur.execute("DELETE FROM public.\"imagedata\" WHERE ImageData_ID = {data3}")
    conn.commit()
    #totalAffectedRows = cur.rowcount
    cur.close()

# =========================================== COLLECTION STATEMENTS ===========================================

def selectCollection():
    conn = TestConnection()
    if conn == 'null':
        print('No Connection String')
    elif conn != 'null':
        print('Connection String Found')
        tableData1 = selectDetails(conn)
        tableData2 = selectImages(conn)
        tableData3 = selectImageData(conn)
        conn.close()
        #return tableData1, tableData2, 
tableData3
def insertCollection():
    conn = TestConnection()
    if conn == 'null':
        print('No Connection String')
    elif conn != 'null':
        print('Connection String Found')
        insertDetails(conn)
        insertImages(conn)
        insertImageData(conn)
        conn.close()

def updateCollection():
    conn = TestConnection()
    if conn == 'null':
        print('No Connection String')
    elif conn != 'null':
        print('Connection String Found')
        updateDetails(conn)
        updateImages(conn)
        updateImageData(conn)
        conn.close()

def deleteCollection():
    conn = TestConnection()
    if conn == 'null':
        print('No Connection String')
    elif conn != 'null':
        print('Connection String Found')
        deleteDetails(conn)
        deleteImages(conn)
        deleteImageData(conn)
        conn.close()

# =========================================== CALLING STATEMENTS ===========================================



# def SaveToCSV(rows):
#     tableData1, tableData2, tableData3 = selectCollection()
#     for data in rows:
#         data = [{'id': data[0], 'name': data[1], 'surname': data[2]}]
        
#         try:
#             with open('output.csv', 'a', newline='') as csvfile:
#                 fieldnames = ['id', 'name', 'surname']
#                 writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
#                 #writer.writeheader()
#                 writer.writerows(data)
#         except:
#             print("Error in creating file.\nFile already exists")
#     print('Data fetched successfully')
#     print(data)
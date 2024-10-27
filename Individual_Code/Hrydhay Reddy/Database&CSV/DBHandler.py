# =========================================== IMPORT STATEMENTS ===========================================

import psycopg2
import json
import csv

# =========================================== DB LOGIN CREDENTIALS ===========================================

DB_NAME = "leafDB"
DB_USER = "postgres"
DB_PASS = "12345"
DB_HOST = "localhost"
DB_PORT = "5432"

# =========================================== TEST CONNECTION ===========================================

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

def selectAllData(conn, imagedata_id):
    cur = conn.cursor()
    cur.execute(f'''
        SELECT imagedata_id, imagelocation, imagedate, imagepathback, imagepathfront , imagelable, lamina_area, lamina_length, lamina_width, scar_count, scar_area, damagepercentage, petiole_length
            FROM public.\"details\"
                FULL JOIN public.\"images\" ON public.\"details\".details_id = public.\"images\".details_id
                FULL JOIN public.\"imagedata\" ON public.\"images\".image_id = public.\"imagedata\".image_id
                    WHERE imagedata_id = {imagedata_id}
                ''')
    rows = cur.fetchall()
    cur.close()
    return rows

# =========================================== INSERT STATEMENTS ===========================================

def insertAllData(conn, data1, data2, data3, data4, data5, data6, data7, data8, data9, data10, data11, data12, data13, data14, data15, data16, data17):
    cur = conn.cursor()
    cur.execute(f'''
        INSERT INTO public.\"details\" (Details_ID,ImageLocation,ImageDate) 
        VALUES ({data1},'{data2}','{data3}');
        
        INSERT INTO public.\"images\" (Image_ID, Details_ID, ImagePathBack, ImagePathFront)
        VALUES ({data4},{data5},'{data6}','{data7}');
        
        INSERT INTO public.\"imagedata\" (ImageData_ID,Image_ID,ImageLable,Lamina_Area,Lamina_Length,Lamina_Width,Scar_Count,Scar_Area,DamagePercentage,Petiole_Length)
        VALUES ({data8},{data9},'{data10}',{data11},{data12},{data13},{data14},{data15},{data16},{data17});
                ''')
    conn.commit()
    cur.close()

# =========================================== UPDATE STATEMENTS ===========================================

def updateAllData(conn, data1, data2, data3, data4, data5, data6, data7, data8, data9, data10, data11, data12, data13, data14, data15, data16, data17):
    cur = conn.cursor()
    cur.execute(f'''
        UPDATE public.\"details\"
        SET ImageLocation = '{data2}', ImageDate = '{data3}'
        WHERE Details_ID = {data1};
        
        UPDATE public.\"images\"
        SET ImagePathBack = '{data6}', ImagePathFront = '{data7}'
        WHERE Image_ID = {data4};
        
        UPDATE public.\"imagedata\"
        SET ImageLable = '{data10}', Lamina_Area = {data11}, Lamina_Length = {data12}, Lamina_Width = {data13}, Scar_Count = {data14}, Scar_Area = {data15}, DamagePercentage = {data16}, Petiole_Length = {data17}
        WHERE ImageData_ID = {data8};
                ''')
    conn.commit()
    cur.close()

# =========================================== DELETE STATEMENTS ===========================================
# NOTE there might be a chance that we only need to delete details table or data found inside that table
# as PostgreSQL does cascading delete if 1 value (FK) gets deleted from Details table

# NOTE I have confirmed that this is the case, but further investigation is needed

def deleteDetails(conn, data1):
    cur = conn.cursor()
    cur.execute(f'''
        DELETE FROM public.\"details\" WHERE Details_ID = '{data1}';
                ''')
    conn.commit()
    cur.close()

# =========================================== COLLECTION STATEMENTS ===========================================

def selectCollection(imagedata_id):
    conn = TestConnection()
    if conn == 'null':
        print('No Connection String')
    elif conn != 'null':
        print('Connection String Found')
        tableData = selectAllData(conn, imagedata_id)
        conn.close()
        return tableData

def insertCollection(data1, data2, data3, data4, data5, data6, data7, data8, data9, data10, data11, data12, data13, data14, data15, data16, data17):
    conn = TestConnection()
    if conn == 'null':
        print('No Connection String')
    elif conn != 'null':
        print('Connection String Found')
        insertAllData(conn, data1, data2, data3, data4, data5, data6, data7, data8, data9, data10, data11, data12, data13, data14, data15, data16, data17)
        conn.close()

def updateCollection(data1, data2, data3, data4, data5, data6, data7, data8, data9, data10, data11, data12, data13, data14, data15, data16, data17):
    conn = TestConnection()
    if conn == 'null':
        print('No Connection String')
    elif conn != 'null':
        print('Connection String Found')
        updateAllData(conn, data1, data2, data3, data4, data5, data6, data7, data8, data9, data10, data11, data12, data13, data14, data15, data16, data17)
        conn.close()

def deleteCollection(data1):
    conn = TestConnection()
    if conn == 'null':
        print('No Connection String')
    elif conn != 'null':
        print('Connection String Found')
        deleteDetails(conn, data1)
        conn.close()

# =========================================== CALLING STATEMENTS ===========================================

def selectData(conn):
    cur = conn.cursor()
    cur.execute(f'''
        SELECT imagedata_id, imagelocation, imagedate, imagepathback, imagepathfront , imagelable, lamina_area, lamina_length, lamina_width, scar_count, scar_area, damagepercentage, petiole_length
            FROM public.\"details\"
                FULL JOIN public.\"images\" ON public.\"details\".details_id = public.\"images\".details_id
                FULL JOIN public.\"imagedata\" ON public.\"images\".image_id = public.\"imagedata\".image_id
                ''')
    rows = cur.fetchall()
    cur.close()
    return rows

def SaveToCSV(tableData):
    try:
        with open('output.csv', 'w', newline='') as csvfile:
            fieldnames = ['imagedata_id', 'imagelocation', 'imagedate', 'imagepathback', 'imagepathfront', 'imagelable', 'lamina_area', 'lamina_length', 'lamina_width', 'scar_count', 'scar_area', 'damagepercentage', 'petiole_length']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
    except:
        print("Error in creating file.\nFile already exists")
    
    for data in tableData:
        data = [{'imagedata_id': data[0], 'imagelocation': data[1], 'imagedate': data[2], 'imagepathback':data[3], 'imagepathfront':data[4], 'imagelable':data[5], 'lamina_area':data[6], 'lamina_length':data[7], 'lamina_width':data[8], 'scar_count':data[9], 'scar_area':data[10], 'damagepercentage':data[11], 'petiole_length':data[12]}]
        
        try:
            with open('output.csv', 'a', newline='') as csvfile:
                fieldnames = ['imagedata_id', 'imagelocation', 'imagedate', 'imagepathback', 'imagepathfront', 'imagelable', 'lamina_area', 'lamina_length', 'lamina_width', 'scar_count', 'scar_area', 'damagepercentage', 'petiole_length']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writerows(data)
        except:
            print("Error in creating file.\nFile already exists")
    print('Data fetched successfully')
    print(data)

def SaveProcess():
    conn = TestConnection()
    if conn == 'null':
        print('No Connection String')
    elif conn != 'null':
        print('Connection String Found')
        tableData = selectData(conn)
        conn.close()
        SaveToCSV(tableData)

# =========================================== TEST FEATURES STATEMENTS ===========================================

#* SELECT
# imagedata_id = "5";
# tableData = selectCollection(imagedata_id)
# print(tableData)

#* INSERT
# data1 = 7
# data2 = 'Johannesburg'
# data3 = '2024-01-01'
# data4 = 7
# data5 = 7
# data6 = './image7_back.png'
# data7 = './image7_front.png'
# data8 = 7
# data9 = 7
# data10 = 'image7'
# data11 = 278
# data12 = 14
# data13 = 15
# data14 = 14
# data15 = 26
# data16 = 0.146
# data17 = 7
# insertCollection(data1, data2, data3, data4, data5, data6, data7, data8, data9, data10, data11, data12, data13, data14, data15, data16, data17)

#* UPDATE
# data1 = 7
# data2 = 'Joburg'
# data3 = '2024-01-01'
# data4 = 7
# data5 = 7
# data6 = './image7_back333.png'
# data7 = './image7_front333.png'
# data8 = 7
# data9 = 7
# data10 = 'image744'
# data11 = 278
# data12 = 14
# data13 = 15
# data14 = 14
# data15 = 26
# data16 = 0.146
# data17 = 7
# updateCollection(data1, data2, data3, data4, data5, data6, data7, data8, data9, data10, data11, data12, data13, data14, data15, data16, data17)

#* DELETE
# data1 = 7
# deleteCollection(data1)

#* SAVE DATA PROCESS
# SaveProcess()
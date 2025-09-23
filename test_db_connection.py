# test_db_connection.py
#import mysql.connector
#from config_server import DB_CONFIG

#def test_connection():
 #   try:
  #      conn = mysql.connector.connect(**DB_CONFIG)
   #     cur = conn.cursor()
    #    cur.execute("SELECT NOW();")
     #   result = cur.fetchone()
      #  print("✅ Conexión exitosa a MySQL en Railway")
       # print("🕒 Hora del servidor MySQL:", result[0])
    #except Exception as e:
     #   print("❌ Error al conectar a MySQL:", e)
    #finally:
     #   if 'cur' in locals():
      #      cur.close()
       # if 'conn' in locals() and conn.is_connected():
        #    conn.close()

#if __name__ == "__main__":
 #   test_connection()
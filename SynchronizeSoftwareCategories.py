import mysql


cnx = mysql.connector.connect(user='admin', password='1',
                              host='127.0.0.1',
                              database='capterra')
cnx.close()
import mysql.connector
from mysql.connector import errorcode


config = dict(user='root',
              password='1',
              host='127.0.0.1',
              database='capterra',
              raise_on_warnings=True,
              use_pure=True)

DB_NAME = 'capterra'
TABLES = {'categories': (
    "CREATE TABLE `categories` ("
    "  `id` smallint NOT NULL AUTO_INCREMENT,"
    "  `name` varchar(100) NOT NULL,"
    "  `description` varchar(5000) NOT NULL,"
    "  PRIMARY KEY (`id`)"
    ") ENGINE=InnoDB"),
    'softwares': (
    "CREATE TABLE `softwares` ("
    "  `id` int NOT NULL AUTO_INCREMENT,"
    "  `name` varchar(100) NOT NULL,"
    "  `rating` tinyint NOT NULL,"
    "  `summary` varchar(5000) NOT NULL,"
    "  `features` json NOT NULL,"
    "  `website` varchar(1000) NOT NULL,"
    "  `about` json NOT NULL,"
    "  `pricing` json NOT NULL,"
    "  `deployment` json NOT NULL,"
    "  `alternative` json NOT NULL,"
    "  `reviews` json NOT NULL,"
    "  PRIMARY KEY (`id`)"
    ") ENGINE=InnoDB"
    )
}


def create_database(cur, data_name):
    try:
        cur.execute(
            "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8mb4'".format(data_name))
    except mysql.connector.Error as ex:
        print("Failed creating database: {}".format(ex))
        exit(1)


try:
    cnx = mysql.connector.connect(**config)
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Something is wrong with your user name or password")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist")
    else:
        print(err)
else:
    cursor = cnx.cursor()
    try:
        cursor.execute("USE {}".format(DB_NAME))
        print("Database {} exists and skip database creation.".format(DB_NAME))
    except mysql.connector.Error as ex:
        print("Database {} does not exists.".format(DB_NAME))
        if ex.errno == errorcode.ER_BAD_DB_ERROR:
            create_database(cursor, DB_NAME)
            print("Database {} created successfully.".format(DB_NAME))
            cnx.database = DB_NAME
        else:
            print(ex)
            exit(1)

    for table_name in TABLES:
        table_description = TABLES[table_name]
        try:
            print("Creating table {}: ".format(table_name), end='')
            cursor.execute(table_description)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                print("already exists.")
            else:
                print(err.msg)
        else:
            print("OK")

    cursor.close()
    cnx.close()

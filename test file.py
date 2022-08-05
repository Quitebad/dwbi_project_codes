import mysql.connector
from fact_sales import fact_sales
from product import rand_product

cnx = mysql.connector.connect(user='root', password='root',
                              host='127.0.0.1',
                              database='dwbi_project')

cursor = cnx.cursor()

fact_sales(cursor)

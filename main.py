import mysql.connector
from dim_customers import new_customers, new_memberships
from fact_sales import fact_sales

cnx = mysql.connector.connect(user='root', password='root',
                              host='127.0.0.1',
                              database='dwbi_project')
cursor = cnx.cursor()

# Creates customer data, new birthday, age, and random membership tier with 1/1/2017 as startdate
# ^ if membership tier != 0

new_customers(cursor)
# Changing membership, using type 2 slowly chaging dimension
new_memberships(cursor)
# only run fucntions above if dim_customer is uncompleted

fact_sales(cursor)

cnx.commit()

from date_creation import random_string_date
from product import rand_product
import random
import math
import datetime
import numpy as np


def dim_time(cursor):
    purchase_date = random_string_date("1/1/2017", "20/7/2022", random.random())
    purchase_date = datetime.datetime.strptime(purchase_date, '%d/%m/%Y').date()

    quarter = math.ceil(purchase_date.month / 3)
    month = purchase_date.month
    year = purchase_date.year

    new_time = "INSERT INTO dim_time (purchase_date, month, quarter, year) VALUES (%s, %s, %s, %s);"
    cursor.execute(new_time, (purchase_date, month, quarter, year))
    return purchase_date


def choose_promotion(membership, mem_start, mem_end, date, cursor):
    # (3, 'New Years 2017', '1/1/2017', '4/1/2017', 20, 0, 'National Holiday') e.g of dim_promotion row

    purchase_date = date
    mem_start = datetime.datetime.strptime(mem_start, '%d/%m/%Y').date()
    mem_end = datetime.datetime.strptime(mem_end, '%d/%m/%Y').date()
    # if customer has membership
    if membership != '0':
        # SELECT all rows WHERE remained of promotion_id/2 is 0/promotion_id is an even number, and promotion_id more
        # than 2 (removes none rows)
        temp = "SELECT * FROM dwbi_project.dim_promotions WHERE MOD(promotion_id, 2) = 0 AND promotion_id > 2;"
        cursor.execute(temp)
        row_number = 0
        # loop for all rows in dim_promotions
        for row in cursor.fetchall():
            promo_start = row[2]  # get promotion start date
            promo_end = row[3]  # get promotion end date
            promo_startdate = datetime.datetime.strptime(promo_start, '%d/%m/%Y %H:%M:%S').date()  # turn both start and end date
            promo_enddate = datetime.datetime.strptime(promo_end, '%d/%m/%Y %H:%M:%S').date()  # to date object
            # if purchase_date falls between or on start/end date
            if (promo_startdate <= purchase_date <= promo_enddate) and (mem_start <= purchase_date <= mem_end):
                # set row number to promotion_id of above promotion
                row_number = row[0]
                break
            else:
                # else, set row number to 2 (or None w/ membership promotion_id)
                row_number = 2
        # return promotion_id
        return row_number

    # if customer no membership
    else:
        temp = "SELECT * FROM dwbi_project.dim_promotions WHERE MOD(promotion_id, 2) = 1 AND promotion_id > 2;"
        cursor.execute(temp)

        row_number = 0
        for row in cursor.fetchall():
            promo_start = row[2]
            promo_end = row[3]
            promo_startdate = datetime.datetime.strptime(promo_start, '%d/%m/%Y %H:%M:%S').date()
            promo_enddate = datetime.datetime.strptime(promo_end, '%d/%m/%Y %H:%M:%S').date()
            if promo_startdate <= purchase_date <= promo_enddate:
                row_number = row[0]
                break
            else:
                row_number = 1

        return row_number


def fact_sales(cursor):
    temp = "SELECT * FROM dwbi_project.dim_customers;"
    cursor.execute(temp)

    i = 1
    j = 1
    for row in cursor.fetchall():
        # (customer_name, customer_age, birthday, phone_number, address, membership_tier
        # membership_startdate, membership_enddate)
        random_prob = np.random.rand()
        j = 1
        while random_prob < j:
            customer_id = int(row[0])
            # choose_promotion(membership, mem_start, mem_end, date, cursor)
            promotion_id = choose_promotion(row[6], row[7], row[8], dim_time(cursor), cursor)
            product = rand_product(promotion_id, cursor)
            product_id = product[0][0]
            time_id = int(i)
            i += 1
            insert_sales = "INSERT INTO fact_sales " \
                           "(dim_promotions_id, dim_customers_id, dim_products_id, dim_time_id, Quantity) " \
                           "VALUES (%s, %s, %s, %s, %s);"

            quantity = int(np.random.choice([1, 2, 3, 4, 5]))
            cursor.execute(insert_sales, (promotion_id, customer_id, product_id, time_id, quantity))
            j -= 0.05

    return "Hey It Hasn't Failed!"

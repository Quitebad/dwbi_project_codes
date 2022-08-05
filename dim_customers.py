from date_creation import random_string_date
import random
import datetime
import numpy as np


def new_customers(cursor):
    add_customer = "UPDATE dim_customers SET customer_age = %s, " \
                   "birthday = %s, membership_tier = %s, membership_startdate = %s, " \
                   "membership_enddate = %s WHERE customer_id = %s;"
    # values needed to add (customer_age, birthday,  membership_tier, membership_startdate, membership_enddate,
    # customer_id)
    # code here creates above values for all 1000 rows of customers
    for i in range(1001):
        # customer_age, random integer is created
        customer_age = int(np.random.choice(np.arange(13, 70)))

        # birthday, random date ,but year is based of age from above
        birthday_date = random_string_date("1/1/2022", "31/12/2022", random.random())

        if datetime.datetime.strptime(birthday_date, '%d/%m/%Y') > datetime.datetime(2022, 7, 22):
            # change above date to whatever you want, this fixes the "you are 21 until you are 22 argument"
            temp_date = datetime.datetime.strptime(birthday_date, '%d/%m/%Y')
            temp_date = temp_date - datetime.timedelta(days=(customer_age + 1) * 365)
            birthday = temp_date.strftime("%d/%m/%Y")
        else:
            temp_date = datetime.datetime.strptime(birthday_date, '%d/%m/%Y')
            temp_date = temp_date - datetime.timedelta(days=customer_age * 365)
            # if birthday not celebrated yet, year will add 1 to the customer age to compensate
            birthday = temp_date.strftime("%d/%m/%Y")

        # membership tier, randomly created
        # fun fact, 51% of all starbucks customers are members
        membership_tier = int(np.random.choice([0, 1, 2]))
        membership_startdate = "1/1/2017"
        membership_enddate = "20/7/2022"

        customer_id = i

        cursor.execute(add_customer, (customer_age, birthday, membership_tier, membership_startdate, membership_enddate,
                                      customer_id))


def new_memberships(cursor):
    temp = "SELECT * FROM dwbi_project.dim_customers;"
    cursor.execute(temp)

    customer_enddate = "UPDATE dim_customers SET membership_enddate = %s WHERE customer_id = %s;"
    customer_tier_change = "INSERT INTO dim_customers " \
                           "(customer_name, customer_age, birthday, phone_number, address, membership_tier, " \
                           "membership_startdate, membership_enddate) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);"

    count = 1
    for row in cursor.fetchall():
        membership_tier = row[6]
        membership_startdate = random_string_date("2/1/2017", "20/7/2022", random.random())

        temp_date = datetime.datetime.strptime(membership_startdate, '%d/%m/%Y')
        temp_date = temp_date - datetime.timedelta(days=1)
        membership_enddate = temp_date.strftime("%d/%m/%Y")
        if membership_tier == "0":
            random_prob = np.random.rand()
            if random_prob < 0.4:
                membership_tier = "1"
                cursor.execute(customer_enddate, (membership_enddate, count))
                cursor.execute(customer_tier_change, (row[1], row[2], row[3], row[4], row[5], membership_tier,
                                                      membership_startdate, "20/7/2022"))
                count += 1
            else:
                count += 1
        elif membership_tier == "1":
            random_prob = np.random.rand()
            if random_prob < 0.4:
                membership_tier = str(np.random.choice([0, 2]))

                cursor.execute(customer_enddate, (membership_enddate, count))
                cursor.execute(customer_tier_change, (row[1], row[2], row[3], row[4], row[5], membership_tier,
                                                      membership_startdate, "20/7/2022"))
                count += 1
            else:
                count += 1
        elif membership_tier == "2":
            random_prob = np.random.rand()
            if random_prob < 0.4:
                membership_tier = str(np.random.choice([0, 1]))

                cursor.execute(customer_enddate, (membership_enddate, count))
                cursor.execute(customer_tier_change, (row[1], row[2], row[3], row[4], row[5], membership_tier,
                                                      membership_startdate, "20/7/2022"))
                count += 1
            else:
                count += 1
        else:
            print("FAIL")
            break

import random
import numpy as np


def rand_product(promotion_id, cursor):
    if (promotion_id != 1) and (promotion_id != 2):
        temp = "SELECT product_id FROM dim_products ORDER BY RAND() LIMIT 1;"
        cursor.execute(temp)
        product = cursor.fetchall()
        return product
    else:
        temp = "SELECT product_id FROM dim_products WHERE is_seasonal = 0 ORDER BY RAND() LIMIT 1;"
        cursor.execute(temp)
        product = cursor.fetchall()
        return product

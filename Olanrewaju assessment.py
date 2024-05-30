#!/usr/bin/env python
# coding: utf-8

# In[1]:


pip install pandas mysql-connector-python openpyxl


# In[2]:


# main.py

import mysql.connector
import pandas as pd
from openpyxl import Workbook

# Database connection
conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='larryq.01',
    database='coffeestoredata'
)
cursor = conn.cursor(dictionary=True)


# In[3]:


# Task 1: Total number of times each item has been ordered and total revenue generated
query_task1 = '''
SELECT 
    i.item_id AS itemId,
    i.sku AS sku,
    i.item_name AS name,
    i.item_cat AS category,
    i.item_size AS size,
    SUM(o.quantity) AS numberSold,
    SUM(o.quantity * i.item_price) AS revenue
FROM Orders o
JOIN Items i ON o.item_id = i.item_id
GROUP BY i.item_id, i.sku, i.item_name, i.item_cat, i.item_size
ORDER BY revenue DESC
'''
cursor.execute(query_task1)
task1_result = pd.DataFrame(cursor.fetchall())


# In[11]:


# Task 2: Calculate cost to produce each coffee item and determine profitability
query_task2 = '''
SELECT 
    i.item_id AS itemId,
    i.sku AS sku,
    i.item_name AS name,
    i.Item_cat AS category,
    i.item_size AS size,
    SUM(o.quantity) AS numberSold,
    SUM(o.quantity * i.item_price) AS revenue,
    (
        SELECT SUM(r.quantity * ing.ing_price)
        FROM recipes r
        JOIN ingredients ing ON r.ing_id = ing.ing_id
        WHERE r.recipe_id = i.sku
    ) AS productionCost,
    (SUM(o.quantity * i.item_price) - 
        (
            SELECT SUM(r.quantity * ing.ing_price)
            FROM recipes r
            JOIN ingredients ing ON r.ing_id = ing.ing_id
            WHERE r.recipe_id = i.sku
        )) AS profitability
FROM Orders o
JOIN items i ON o.item_id = i.item_id
GROUP BY i.item_id, i.sku, i.item_name, i.item_cat, i.item_size
ORDER BY profitability DESC
'''
cursor.execute(query_task2)
task2_result = pd.DataFrame(cursor.fetchall())


# In[22]:


# Task 3: Calculate the number of orders, sales, and profit for each hour the store is open
query_task3 = '''
SELECT 
    HOUR(o.created_at) AS hour,
    COUNT(o.order_id) AS numberOfOrders,
    SUM(o.quantity * i.item_price) AS totalSales,
    (SUM(o.quantity * i.item_price) - 
        SUM(r.quantity * ing.ing_price)
    ) AS totalProfit
FROM Orders o
JOIN Items i ON o.item_id = i.item_id
JOIN Recipes r ON i.sku = r.recipe_id
JOIN Ingredients ing ON r.ing_id = ing.ing_id
GROUP BY HOUR(o.created_at)
ORDER BY hour
'''

# Execute the query
cursor.execute(query_task3)
task3_result = pd.DataFrame(cursor.fetchall())


# In[25]:


# Task 4: Calculate the total hours worked by each staff member and their corresponding daily salaries
query_task4 = '''
SELECT 
    s.staff_id,
    CONCAT(s.first_name, ' ', s.last_name) AS staffName,
    s.position,
    SUM(TIMESTAMPDIFF(HOUR, sh.start_time, sh.end_time)) AS totalHoursWorked,
    SUM(TIMESTAMPDIFF(HOUR, sh.start_time, sh.end_time) * s.sal_per_hour) AS totalSalariesEarned
FROM Rota r
JOIN Staff s ON r.staff_id = s.staff_id
JOIN Shift sh ON r.shift_id = sh.shift_id
GROUP BY s.staff_id, staffName, s.position
'''

cursor.execute(query_task4)
task4_result = pd.DataFrame(cursor.fetchall())


# In[26]:


# Task 5: Retrieve the aggregate profit for dine-in and takeout orders, grouped by their respective categories
query_task5 = '''
SELECT 
    i.item_cat,
    o.in_or_out AS orderType,
    SUM(o.quantity * i.item_price) AS totalRevenue,
    SUM(r.quantity * ing.ing_price) AS totalCost,
    (SUM(o.quantity * i.item_price) - SUM(r.quantity * ing.ing_price)) AS totalProfit
FROM Orders o
JOIN Items i ON o.item_id = i.item_id
JOIN Recipes r ON i.sku = r.recipe_id
JOIN Ingredients ing ON r.ing_id = ing.ing_id
GROUP BY i.item_cat, orderType
ORDER BY totalProfit DESC
'''

cursor.execute(query_task5)
task5_result = pd.DataFrame(cursor.fetchall())


# In[28]:


# Task 6: Which shift is the busiest?
query_task6 = '''
SELECT 
    sh.shift_id,
    sh.day_of_week,
    sh.start_time,
    sh.end_time,
    COUNT(o.order_id) AS totalOrders
FROM Rota r
JOIN Shift sh ON r.shift_id = sh.shift_id
JOIN Orders o ON o.row_id = r._id
GROUP BY sh.shift_id, sh.day_of_week, sh.start_time, sh.end_time
ORDER BY totalOrders DESC
'''

cursor.execute(query_task6)
task6_result = pd.DataFrame(cursor.fetchall())


# In[29]:


# Close the database connection
cursor.close()
conn.close()

# Write results to Excel file
with pd.ExcelWriter('output.xlsx', engine='openpyxl') as writer:
    task1_result.to_excel(writer, sheet_name='TotalSalesAndRevenue', index=False)
    task2_result.to_excel(writer, sheet_name='CostAndProfitability', index=False)
    task3_result.to_excel(writer, sheet_name='SalesAndProfitByHour', index=False)
    task4_result.to_excel(writer, sheet_name='StaffHoursAndSalaries', index=False)
    task5_result.to_excel(writer, sheet_name='ProfitByOrderType', index=False)
    task6_result.to_excel(writer, sheet_name='BusiestShift', index=False)

print("Excel file 'output.xlsx' created successfully!")


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





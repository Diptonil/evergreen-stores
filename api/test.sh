#!/bin/sh


# This script is to perform basic tests on the endpoints locally. The response obtained is to be the testament of the app's functionality.
# This app does not use Python's in-house testing tools in favour of a lightweight build.
# This does not get included in the Docker build.


# Users
# 1: Create an incorrect user without an email.
curl -d '{"first_name": "Test", "last_name": "Last"}' -H 'Content-Type: application/json'  http://127.0.0.1:5000/user 

# 2: Create an incorrect user without a first name.
curl -d '{"email": "test@test.com", "last_name": "Last"}' -H 'Content-Type: application/json'  http://127.0.0.1:5000/user 

# 3: Create an incorrect user without a last name.
curl -d '{"email": "test@test.com", "first_name": "Test"}' -H 'Content-Type: application/json'  http://127.0.0.1:5000/user 

# 4: Create a correct user.
curl -d '{"email": "test@test.com", "first_name": "Test", "last_name": "Last"}' -H 'Content-Type: application/json'  http://127.0.0.1:5000/user 

# 5: Retrieve the user.
curl http://localhost:5000/user?email=test@test.com

# 6: Update the user.
curl -d '{"email": "test@test.com", "first_name": "Bruce", "last_name": "Wayne"}' -H 'Content-Type: application/json' -X PUT http://localhost:5000/user

# 7: Delete the user.
curl -d '{"email": "test@test.com"}' -H 'Content-Type: application/json' -X DELETE http://localhost:5000/user


# Products
# 1: Create an incorrect product without an ID.
curl -d '{"name": "Mark I", "category": "Weapons", "company": "Stark Industries", "is_sold": "No", "date_manufactured": "10.04.1999", "cost": 100000}' -H 'Content-Type: application/json'  http://127.0.0.1:5000/product 

# 2: Create an incorrect product without a name.
curl -d '{"id": "sh65", "category": "Weapons", "company": "Stark Industries", "is_sold": "No", "date_manufactured": "10.04.1999", "cost": 100000}' -H 'Content-Type: application/json'  http://127.0.0.1:5000/product 

# 3: Create an incorrect product without a company.
curl -d '{"id": "sh65", "category": "Weapons", "name": "Mark I", "is_sold": "No", "date_manufactured": "10.04.1999", "cost": 100000}' -H 'Content-Type: application/json'  http://127.0.0.1:5000/product 

# 4: Create an incorrect product without a category.
curl -d '{"id": "sh65", "name": "Mark I", "company": "Stark Industries", "is_sold": "No", "date_manufactured": "10.04.1999", "cost": 100000}' -H 'Content-Type: application/json'  http://127.0.0.1:5000/product 

# 5: Create an incorrect product without a sale status.
curl -d '{"id": "sh65", "category": "Weapons", "company": "Stark Industries", "name": "Mark I", "date_manufactured": "10.04.1999", "cost": 100000}' -H 'Content-Type: application/json'  http://127.0.0.1:5000/product 

# 6: Create an incorrect product without a date of manufacture.
curl -d '{"id": "sh65", "category": "Weapons", "company": "Stark Industries", "is_sold": "No", "name": "Mark I", "cost": 100000}' -H 'Content-Type: application/json'  http://127.0.0.1:5000/product 

# 7: Create an incorrect product without a cost.
curl -d '{"id": "sh65", "category": "Weapons", "company": "Stark Industries", "is_sold": "No", "date_manufactured": "10.04.1999", "name": "Mark I"}' -H 'Content-Type: application/json'  http://127.0.0.1:5000/product 

# 8: Create an correct product.
curl -d '{"id": "sh65", "name": "Mark I", "category": "Weapons", "company": "Stark Industries", "is_sold": "No", "date_manufactured": "10.04.1999", "cost": 100000}' -H 'Content-Type: application/json'  http://127.0.0.1:5000/product 

# 9: Retrieve the product.
curl http://localhost:5000/product?id=sh65

# 10: Update the product.
curl -d '{"id": "sh65", "name": "Mark II", "category": "Weapons", "company": "Stark Industries", "is_sold": "No", "date_manufactured": "01.01.2000, "cost": 800000}' -H 'Content-Type: application/json' -X PUT http://localhost:5000/product

# 7: Delete the product.
curl -d '{"id": "sh65"}' -H 'Content-Type: application/json' -X DELETE http://localhost:5000/product

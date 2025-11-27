from xmlrpc import client as xmlrpc_client
import os
from dotenv import load_dotenv

load_dotenv()

url = os.getenv("URL")
db = os.getenv("DB")
username = os.getenv("USER")
password = os.getenv("PASSWORD")

#Connect Odoo authentication service
common = xmlrpc_client.ServerProxy(f"{url}/xmlrpc/2/common")

uid = common.authenticate(db, username, password, {})

if uid:
    print("Authentication successful.")
    print(f"Authenticated User ID: {uid}")

    models = xmlrpc_client.ServerProxy(f"{url}/xmlrpc/2/object")
    products = models.execute_kw(
        db, uid, password,
        'product.product', 
        'search_read',      
        [[]],               
        {
            'fields': ['name', 'standard_price', 'id'],
            'limit' :5
        }
    )

    print('Fetched products from Odoo:')
    for product in products:
        print(f"ID: {product['id']} | Name: {product['name']} | Cost: {product['standard_price']}")
else:
    print("Authentication failed. Please check your credentials or database name.")
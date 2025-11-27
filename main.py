from fastapi import FastAPI
import xmlrpc.client
import os
from dotenv import load_dotenv

load_dotenv()

URL = os.getenv("URL")
DB = os.getenv("DB")
USER = os.getenv("USER")
PASSWORD = os.getenv("PASSWORD")

app = FastAPI()

def get_odoo_connection():
    common = xmlrpc.client.ServerProxy(f'{URL}/xmlrpc/2/common')
    uid = common.authenticate(DB, USER, PASSWORD, {})
    
    if not uid:
        raise Exception("Odoo Authentication Failed")
        
    models = xmlrpc.client.ServerProxy(f'{URL}/xmlrpc/2/object')
    
    return models, uid

@app.get("/products")
def fetch_products():
    try:
        models, uid = get_odoo_connection()

        products = models.execute_kw(
            DB, uid, PASSWORD,
            'product.product',  
            'search_read',      
            [[]],               
            {
                'fields': ['name', 'standard_price', 'default_code', 'id'], # Internal reference / SKU = default_code
                'limit': 20  
            }
        )
                

        return {"status": "success", "data": products}

    except Exception as e:
        return {"status": "error", "message": str(e)}
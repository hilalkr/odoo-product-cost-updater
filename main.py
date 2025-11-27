from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
import xmlrpc.client
import os
from dotenv import load_dotenv

load_dotenv()

URL = os.getenv("URL")
DB = os.getenv("DB")
USER = os.getenv("USER")
PASSWORD = os.getenv("PASSWORD")

app = FastAPI()

templates = Jinja2Templates(directory="templates")

def get_odoo_connection():
    common = xmlrpc.client.ServerProxy(f'{URL}/xmlrpc/2/common')
    uid = common.authenticate(DB, USER, PASSWORD, {})
    
    if not uid:
        raise Exception("Odoo Authentication Failed")
        
    models = xmlrpc.client.ServerProxy(f'{URL}/xmlrpc/2/object')
    
    return models, uid

@app.get("/") 
def dashboard(request: Request):
    try:
        models, uid = get_odoo_connection()
        products = models.execute_kw(
            DB, uid, PASSWORD,
            'product.product', 'search_read', [[]],
            {
                'fields': ['name', 'standard_price', 'default_code', 'id'], 
                'limit': 20
            }
        )
        
        return templates.TemplateResponse("index.html", {
            "request": request, 
            "products": products
        })

    except Exception as e:
        return {"status": "error", "message": str(e)}
    
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
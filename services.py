import xmlrpc.client
from config import URL, DB, USER, PASSWORD

def get_odoo_connection():
    common = xmlrpc.client.ServerProxy(f'{URL}/xmlrpc/2/common')
    uid = common.authenticate(DB, USER, PASSWORD, {})
    
    if not uid:
        raise Exception("Odoo Authentication Failed")
        
    models = xmlrpc.client.ServerProxy(f'{URL}/xmlrpc/2/object')
    return models, uid

def fetch_products_from_odoo():
    models, uid = get_odoo_connection()
    
    products = models.execute_kw(
        DB, uid, PASSWORD,
        'product.product',
        'search_read',
        [[]],
        {
            'fields': ['name', 'standard_price', 'default_code', 'id'], # Internal reference / SKU = default_code
        }
    )
    return products

def update_product_cost_in_odoo(product_id, new_cost):
    models, uid = get_odoo_connection()
    
    success = models.execute_kw(
        DB, uid, PASSWORD,
        'product.product',
        'write',
        [[product_id], {'standard_price': new_cost}]
    )
    return success

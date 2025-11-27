from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from schemas import UpdateCostRequest
from services import fetch_products_from_odoo, update_product_cost_in_odoo
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

templates = Jinja2Templates(directory="templates")



@app.get("/")
def dashboard(request: Request):
    try:
        products = fetch_products_from_odoo()
        
        return templates.TemplateResponse("index.html", {
            "request": request, 
            "products": products
        })
    except Exception as e:
        return {"status": "error", "message": str(e)}


@app.post("/update_cost")
def update_cost(data: UpdateCostRequest):
    try:
        if data.new_cost < 0:
            return {"status": "error", "message": "Cost cannot be negative!"}

        success = update_product_cost_in_odoo(data.product_id, data.new_cost)

        if success:
            return {"status": "success", "message": "Price updated successfully!"}
        else:
            return {"status": "error", "message": "Update failed in Odoo."}

    except Exception as e:
        return {"status": "error", "message": str(e)}
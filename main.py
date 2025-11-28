from fastapi import FastAPI, HTTPException, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse
from schemas import UpdateCostRequest
from services import fetch_products_from_odoo, update_product_cost_in_odoo
from xmlrpc.client import Fault, ProtocolError
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

templates = Jinja2Templates(directory="templates")



XMLRPC_ERRORS = (Fault, ProtocolError, ConnectionError, OSError)


@app.get("/")
def dashboard(request: Request):
    try:
        products = fetch_products_from_odoo()
    except XMLRPC_ERRORS as e:
        return JSONResponse(
            status_code=502,
            content={"status": "error", "detail": f"Odoo connection failed: {e}"}
        )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"status": "error", "detail": str(e)}
        )

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"products": products},
    )


@app.post("/update_cost")
def update_cost(data: UpdateCostRequest):
    if data.new_cost < 0:
        raise HTTPException(status_code=400, detail="Cost cannot be negative!")

    try:
        success = update_product_cost_in_odoo(data.product_id, data.new_cost)

        if success:
            return {"status": "success", "message": "Price updated successfully!"}

        return JSONResponse(
            status_code=500,
            content={"status": "error", "detail": "Update failed in Odoo."}
        )

    except XMLRPC_ERRORS as e:
        return JSONResponse(
            status_code=502,
            content={"status": "error", "detail": f"Odoo connection failed: {e}"}
        )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"status": "error", "detail": str(e)}
        )

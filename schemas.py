from pydantic import BaseModel

class UpdateCostRequest(BaseModel):
    product_id: int
    new_cost: float
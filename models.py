from pydantic import BaseModel, Field


class FlightSearchRequest(BaseModel):
    origin: str
    destination: str
    date: str
    number_of_passengers: int = Field(..., ge=1)


class Flight(BaseModel):
    flight_no: str
    origin: str
    destination: str
    date: str
    price: float
    available_seats: int


class DiscountRule(BaseModel):
    promo_amount: float
    cashback_rate: float
    miles_value: float


class PricedFlight(BaseModel):
    flight_no: str
    price: float
    total_base_price: float
    price_after_promo: float
    cashback_value: float
    final_price: float
from pydantic import BaseModel, Field


class FlightSearchRequest(BaseModel):
    origin: str
    destination: str
    date: str
    number_of_passengers: int = Field(..., ge=1)
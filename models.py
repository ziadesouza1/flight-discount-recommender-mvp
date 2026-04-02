from pydantic import BaseModel


class FlightSearchRequest(BaseModel):
    origin: str
    destination: str
    date: str
    number_of_passengers: int
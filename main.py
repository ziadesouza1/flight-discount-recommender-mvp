from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class FlightSearchRequest(BaseModel):
    origin: str
    destination: str
    date: str
    number_of_passengers: int


@app.get("/")
def root():
    return {"message": "Flight Discount Recommender is running"}


@app.post("/recommend")
def recommend_flights(request: FlightSearchRequest):
    return {
        "message": "Recommend endpoint is working",
        "your_input": request.dict()
    }
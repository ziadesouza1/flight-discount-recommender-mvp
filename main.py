from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd

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
    flights_df = pd.read_csv("data/flights.csv")

    matching_flights = flights_df[
        (flights_df["origin"] == request.origin) &
        (flights_df["destination"] == request.destination) &
        (flights_df["date"] == request.date)
    ]

    return {
        "message": "Matching flights found",
        "results": matching_flights.to_dict(orient="records")
    }
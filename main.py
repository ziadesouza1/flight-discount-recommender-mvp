from fastapi import FastAPI
import pandas as pd
from models import FlightSearchRequest
from pricing import apply_discounts

app = FastAPI()


@app.get("/")
def root():
    return {"message": "Flight Discount Recommender is running"}


@app.post("/recommend")
def recommend_flights(request: FlightSearchRequest):
    flights_df = pd.read_csv("data/flights.csv")
    discounts_df = pd.read_csv("data/discounts.csv")

    matching_flights = flights_df[
        (flights_df["origin"] == request.origin) &
        (flights_df["destination"] == request.destination) &
        (flights_df["date"] == request.date)
    ].copy()

    if matching_flights.empty:
        return {
            "message": "No matching flights found",
            "results": []
        }

    matching_flights = apply_discounts(
        matching_flights,
        discounts_df,
        request.number_of_passengers
    )

    matching_flights = matching_flights.sort_values(by="final_price")

    return {
        "message": "Matching flights with discounts applied and ranked",
        "results": matching_flights.to_dict(orient="records")
    }
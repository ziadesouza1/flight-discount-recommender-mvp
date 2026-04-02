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
    discounts_df = pd.read_csv("data/discounts.csv")

    matching_flights = flights_df[
        (flights_df["origin"] == request.origin) &
        (flights_df["destination"] == request.destination) &
        (flights_df["date"] == request.date)
    ].copy()

    promo_amount = discounts_df.loc[0, "promo_amount"]
    cashback_rate = discounts_df.loc[0, "cashback_rate"]
    miles_value = discounts_df.loc[0, "miles_value"]

    matching_flights["total_base_price"] = (
        matching_flights["price"] * request.number_of_passengers
    )

    matching_flights["price_after_promo"] = (
        matching_flights["total_base_price"] - promo_amount
    )

    matching_flights["cashback_value"] = (
        matching_flights["price_after_promo"] * cashback_rate
    )

    matching_flights["final_price"] = (
        matching_flights["price_after_promo"]
        - matching_flights["cashback_value"]
        - miles_value 
    )

    return {
        "message": "Matching flights with discounts applied",
        "results": matching_flights.to_dict(orient="records")
    }
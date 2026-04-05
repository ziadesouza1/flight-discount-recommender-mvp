from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
from models import FlightSearchRequest
from pricing import apply_discounts

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.get("/")
def root():
    return {
        "message": "Flight Discount Recommender API is running", 
        "main_endpoint": "/recommend"
        }


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/recommend")
def recommend_flights(request: FlightSearchRequest):
    flights_df = pd.read_csv("data/flights.csv")
    discounts_df = pd.read_csv("data/discounts.csv")

    matching_flights = flights_df[
        (flights_df["origin"] == request.origin) &
        (flights_df["destination"] == request.destination) &
        (flights_df["date"] == request.date) &
        (flights_df["available_seats"] >= request.number_of_passengers)
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

    results = matching_flights[
        [
            "flight_no",
            "price",
            "total_base_price",
            "cashback_value",
            "final_price"
        ]
    ]

    return {
        "message": "Matching flights with discounts applied and ranked",
        "results": results.to_dict(orient="records")
    }
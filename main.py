from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from models import FlightSearchRequest
from repositories import FlightRepository, DiscountRepository
from pricing import PricingEngine
from services import RecommendationService

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

flight_repository = FlightRepository("data/flights.csv")
discount_repository = DiscountRepository("data/discounts.csv")
pricing_engine = PricingEngine()
recommendation_service = RecommendationService(
    flight_repository,
    discount_repository,
    pricing_engine,
)


@app.get("/")
def root():
    return {
        "message": "Flight Discount Recommender API is running",
        "main_endpoint": "/recommend",
    }


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/recommend")
def recommend_flights(request: FlightSearchRequest):
    results = recommendation_service.recommend_flights(request)

    if not results:
        return {
            "message": "No matching flights found",
            "results": [],
        }

    return {
        "message": "Matching flights with discounts applied and ranked",
        "results": [flight.model_dump() for flight in results],
    }
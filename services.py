from models import FlightSearchRequest, Flight, PricedFlight
from repositories import FlightRepository, DiscountRepository
from pricing import PricingEngine


class RecommendationService:
    def __init__(
        self,
        flight_repository: FlightRepository,
        discount_repository: DiscountRepository,
        pricing_engine: PricingEngine,
    ):
        self.flight_repository = flight_repository
        self.discount_repository = discount_repository
        self.pricing_engine = pricing_engine

    def recommend_flights(
        self, request: FlightSearchRequest
    ) -> list[PricedFlight]:
        all_flights = self.flight_repository.get_all_flights()

        matching_flights = [
            flight
            for flight in all_flights
            if flight.origin == request.origin
            and flight.destination == request.destination
            and flight.date == request.date
            and flight.available_seats >= request.number_of_passengers
        ]

        if not matching_flights:
            return []

        discount_rule = self.discount_repository.get_discount_rule()

        priced_flights = self.pricing_engine.apply_discounts(
            matching_flights,
            discount_rule,
            request.number_of_passengers,
        )

        priced_flights.sort(key=lambda flight: flight.final_price)
        return priced_flights
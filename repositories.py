import pandas as pd
from models import Flight, DiscountRule


class FlightRepository:
    def __init__(self, file_path: str = "data/flights.csv"):
        self.file_path = file_path

    def get_all_flights(self) -> list[Flight]:
        df = pd.read_csv(self.file_path)
        return [Flight(**row) for row in df.to_dict(orient="records")]


class DiscountRepository:
    def __init__(self, file_path: str = "data/discounts.csv"):
        self.file_path = file_path

    def get_discount_rule(self) -> DiscountRule:
        df = pd.read_csv(self.file_path)
        row = df.iloc[0].to_dict()
        return DiscountRule(**row)
import pandas as pd


def apply_discounts(matching_flights: pd.DataFrame, discounts_df: pd.DataFrame, number_of_passengers: int) -> pd.DataFrame:
    promo_amount = discounts_df.loc[0, "promo_amount"]
    cashback_rate = discounts_df.loc[0, "cashback_rate"]
    miles_value = discounts_df.loc[0, "miles_value"]

    matching_flights["total_base_price"] = (
        matching_flights["price"] * number_of_passengers
    )

    matching_flights["price_after_promo"] = (
        matching_flights["total_base_price"] - promo_amount
    )

    matching_flights["cashback_value"] = (
        matching_flights["price_after_promo"] * cashback_rate
    ).round(2)

    matching_flights["final_price"] = (
        matching_flights["price_after_promo"]
        - matching_flights["cashback_value"]
        - miles_value
    ).round(2)

    return matching_flights
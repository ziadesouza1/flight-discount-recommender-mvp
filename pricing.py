from models import Flight, DiscountRule, PricedFlight


class PricingEngine:
    def apply_discounts(
        self,
        flights: list[Flight],
        discount_rule: DiscountRule,
        number_of_passengers: int,
    ) -> list[PricedFlight]:
        priced_flights = []

        for flight in flights:
            total_base_price = flight.price * number_of_passengers
            price_after_promo = total_base_price - discount_rule.promo_amount
            cashback_value = round(
                price_after_promo * discount_rule.cashback_rate, 2
            )
            final_price = round(
                price_after_promo - cashback_value - discount_rule.miles_value,
                2,
            )

            priced_flights.append(
                PricedFlight(
                    flight_no=flight.flight_no,
                    price=flight.price,
                    total_base_price=total_base_price,
                    price_after_promo=price_after_promo,
                    cashback_value=cashback_value,
                    final_price=final_price,
                )
            )

        return priced_flights
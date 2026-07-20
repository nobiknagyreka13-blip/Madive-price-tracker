from hotels.base_hotel import Hotel


class Dhigali(Hotel):

    name = "Dhigali Maldives"

    preferred_rooms = [
        "Beach Villa",
        "Family Villa"
    ]

    meal_plan = "All Inclusive"

    def get_price(self):
        # Később ide kerül a valódi árlekérés
        return None

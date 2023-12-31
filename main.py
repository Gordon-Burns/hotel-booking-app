import pandas as pd

df = pd.read_csv("hotels.csv", dtype=str)
df_cards = pd.read_csv("cards.csv", dtype=str).to_dict(orient="records")
df_card_security = pd.read_csv("card_security.csv", dtype=str)


class Hotel:
    def __init__(self, hotel_ID):
        self.hotel_id = hotel_ID
        self.hotel_name = df.loc[df["id"] == self.hotel_id, "name"].squeeze()
        self.price = "£" + df.loc[df["id"] == self.hotel_id, "price"].squeeze()

    def book(self):
        """Books the hotel by changing its availability to no """
        df.loc[df["id"] == self.hotel_id, "available"] = "no"
        df.to_csv("hotels.csv", index=False)

    def available(self):
        """Check the hotel is available"""
        availability = df.loc[df["id"] == self.hotel_id, "available"].squeeze()
        if availability == "yes":
            return True
        else:
            return False


class Reservation:
    def __init__(self, cust_name, hotel_object):
        self.customer_name = cust_name
        self.hotel = hotel_object

    def generate(self):
        """Generates the content for the reservation"""
        content = f"""
        Hello {self.customer_name} Thanks for your reservation!
        Here are your booking details:
        Name: {self.customer_name}
        Hotel ID: {self.hotel.hotel_id}
        Hotel Name: {self.hotel.hotel_name}
        Price: {self.hotel.price}

        """
        return content


class CreditCard:
    def __init__(self, number):
        self.number = number

    def validate(self, expiry, holder, cvc):
        card_data = {"number": self.number, "expiration": expiry, "holder": holder, "cvc": cvc}
        if card_data in df_cards:
            return True
        else:
            return False


class SecureCreditCard(CreditCard):

    def authenticate(self, given_password):
        password = df_card_security.loc[df_card_security["number"]
                                        == self.number, "password"].squeeze()
        if password == given_password:
            return True
        else:
            return False


print(df)
hotel_ID = input("Enter the ID of the hotel: ")

hotel = Hotel(hotel_ID)
if hotel.available():
    credit_card = SecureCreditCard(number="1234")
    if credit_card.validate(expiry="12/26", holder="JOHN SMITH", cvc="123"):
        input_password = input("Enter your 2FA Password: ")
        if credit_card.authenticate(given_password=input_password):
            hotel.book()
            name = input("Enter your name: ")
            reservation = Reservation(cust_name=name, hotel_object=hotel)
            print(reservation.generate())
        else:
            print("Additional Authentication Failed")
    else:
        print("There is a problem validating your card")

else:
    print("Hotel is Full")

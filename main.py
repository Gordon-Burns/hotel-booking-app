import pandas as pd

df = pd.read_csv("hotels.csv")


class Hotel:
    def __init__(self, hotel_id):
        self.hotel_id = hotel_ID
        self.hotel_name = df.loc[df["id"] == self.hotel_id, "name"].squeeze()

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
        Hello {name} Thanks for your reservation!
        Here are your booking details:
        Name: {self.customer_name}
        Hotel ID: {self.hotel.hotel_id}
        Hotel Name: {self.hotel.hotel_name}


        """
        return content


print(df)
hotel_ID = int(input("Enter the ID of the hotel: "))

hotel = Hotel(hotel_ID)
if hotel.available():
    hotel.book()
    name = input("Enter your name: ")
    reservation = Reservation(cust_name=name, hotel_object=hotel)
    print(reservation.generate())
else:
    print("Hotel is Full")

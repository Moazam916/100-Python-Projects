import requests
from datetime import datetime
import time
import smtplib

MY_EMAIL = "moazamshahzzad1234@gmail.com"
PASSWORD = "whlmokvkczrkasbn"
MY_LAT = 51.507351  # Your latitude
MY_LONG = -0.127758  # Your longitude


def sending_an_email():
    with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
        connection.starttls()
        connection.login(user=MY_EMAIL, password=PASSWORD)
        connection.sendmail(from_addr=MY_EMAIL,
                            to_addrs="moazamshahzad118@gmail.com",
                            msg=f"Subject:ISS POSITION\n\nPlease lookup ISS is right above you"
                            )


# X represents the longitude and y represent the latitude
def iss_current_position_checker():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()
    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])
    print(iss_longitude, iss_latitude)
    if (iss_longitude - 5.0) < MY_LONG < (iss_longitude + 5.0) and 0 < MY_LAT < (iss_latitude+5):
        return True
    else:
        False


def dark_outside():
    current_position = iss_current_position_checker()
    print(current_position)
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0
    }
    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])
    print(sunrise, sunset)
    time_now = datetime.now()
    current_hour = time_now.hour
    if (sunset < current_hour or current_hour < sunrise) and current_position == True:
        sending_an_email()
        time.sleep(60)
        print("calling function it self")
        dark_outside()
    else:
        exit(0)


dark_outside()

# Your position is within +5 or -5 degrees of the ISS position.


# If the ISS is close to my current position
# and it is currently dark
# Then send me an email to tell me to look up.
# BONUS: run the code every 60 seconds.

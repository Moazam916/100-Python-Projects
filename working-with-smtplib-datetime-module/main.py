import smtplib
import datetime as dt
import random
my_email = "moazamshahzzad1234@gmail.com"
passowrd = "whlmokvkczrkasbn"
with open("quotes.txt", encoding="utf-8") as file:
    quotes_string = file.readlines()
    quote= random.choice(quotes_string)
    print(quote)
now = dt.datetime.now()
day = now.day
print(day)
if day == 1:
    print("coming inside of if condition")
    with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
        connection.starttls()
        connection.login(user=my_email, password=passowrd)
        connection.sendmail(from_addr=my_email,
                            to_addrs="moazamshahzad118@gmail.com",
                            msg=f"Subject:Motivational Quotes\n\n{quote}".encode("utf-8")
                            )

# import datetime as dt
# now = dt.datetime.now()
# year = now.year
# month = now.month
# day = now.day
# hour = now.hour
# seconds = now.second
# print(now)
# print(year)
# print(month)
# print(day)
# print(hour)
# print(seconds)
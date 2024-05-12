import smtplib
import os



my_email = "atuony0312@gmail.com"
password = os.environ.get('SMTP_PASSWORD')

with smtplib.SMTP_SSL('smtp.gmail.com',465) as connection:
    connection.login(user=my_email,password=password)
    connection.sendmail(
       from_addr=my_email,
       to_addrs=my_email,
       msg="Subject:Hello from python\n\nThis will go into the body of the email"
    )
import random
import math
import requests
import json
import time
import smtplib, ssl
import getpass
import sys

smtp_server = "smtp.gmail.com"
port = 587  # For starttls
sender_email = "slipschitz@webadon.com"
password = getpass.getpass("Type your password and press enter: ")

mailing = {
    "Rebecca Wolk":"rebecca.wolk@gmail.com",
    "Seth Lipschitz":"sethlipschitz@gmail.com"
}

message = """\
Subject: Rockets Firing in Israel

Dear {name},

    Another rocket was fired at Israel aiming at the city of {location}.
    As a parent who has a high school son that is studying in Israel, every
    time I receive an alert, I worry about my son and the innocent people who are being
    attacked by a recognized terrorist group.

    Over 3,100 rockets and missiles have been fired at Israeli cities and towns since Monday.
    Millions of families have spent the week in bomb shelters, as rockets rain down overhead
    and the lifesaving Iron Dome system intercepts as many missiles as it can detect.

    While Hamas deliberately targets innocent civilians, and puts countless Palestinians
    in harm's way by using the people of Gaza as human shields, there are many voices blaming
    Israel and justifying Hamas’s terrorism.

    I urge you to denounce Hamas as a terrorist organization, and insist that Hamas stops
    firing rockets into Israel.

    I hope and pray, that one day soon there will be peace for both the innocent Israelis
    and Palestinians.

    Sincerely,
    Seth Lipschitz

"""

class AlertPeople():

    def __init__(self):

        self.headers = {
            "Content-Type":"application/x-www-form-urlencoded; charset=UTF-8",
            "X-Requested-With": "XMLHttpRequest",
            "Referer": "https://www.oref.org.il/11088-13708-he/Pakar.aspx",
            "sec-ch-ua":'"Not A;Brand";v="99", "Chromium";v="90", "Google Chrome";v="90"',
            "sec-ch-ua-mobile": "?0",
            "User-Agent":""
        }
        self.proxy = {
            "https":"https://212.179.18.75:3128"
        }



    def get_red_alerts(self):

        # get red alerts
        HOST = "https://www.oref.org.il/WarningMessages/alert/alerts.json"
        #HOST = "http://www.oref.org.il/WarningMessages/Alert/alerts.json?v=1"
        r = requests.get(HOST, headers=self.headers, proxies=self.proxy)
        if(r.content == b''):
            return None
        # parse the json response
        j = json.loads(r.content)
        # check if there is no alerts - if so, return null.
        if(len(j["data"]) == 0):
            return None
        # initialize the current timestamp to know when the rocket alert started
        j["timestamp"] = time.time()
        return j

def main():

    # initalize the red alert object
    alert = AlertPeople()
    # check for alerts all the time and do stuff, never stop.
    while True:
        # sleep 1 second before checking alerts over again to not put pressure on the server.
        time.sleep(1)
        # get alerts from pikud ha-oref website
        red_alerts = alert.get_red_alerts()
        # if there is red alerts right now, get into action, quickly!
        if(red_alerts != None):
            # loop through each city there is red alert currently

            print (red_alerts)

            for alert_code in red_alerts["data"]:

                # get unique alert id for the current looping alerts
                alert_id = red_alerts["id"]

                for person in mailing:

                    # Create a secure SSL context
                    context = ssl.create_default_context()

                    # Try to log in to server and send email
                    try:
                        server = smtplib.SMTP(smtp_server,port)
                        server.ehlo() # Can be omitted
                        server.starttls(context=context) # Secure the connection
                        server.ehlo() # Can be omitted
                        server.login(sender_email, password)

                        server.sendmail(sender_email, mailing[person], message.format(name=person, location=alert_code).encode(encoding='UTF-8',errors='strict'))

                    except Exception as e:
                        # Print any error messages to stdout
                        print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)

                    finally:
                        server.quit()

        else:
            print("[-] No alerts for now, keep checking ...")

if __name__ == "__main__":
    main()

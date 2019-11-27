#!/bin/python3.6

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class Gmail():

    def sendFile(self, subject, file):
        try:
            filetxt = open(file, "r")
            msgtext = MIMEText(filetxt.read(), "plain")
            to = "Alerts"
            recipients = ["@gmail.com"]
            msg = MIMEMultipart()
            msg['To'] = to
            msg['From'] = "Alerts"
            msg['Subject'] = ' %s ' % subject
            msg.attach(msgtext)
            filetxt.close()
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login("@gmail.com", "xxx")  # Add Google App password to login method
            server.sendmail("@gmail.com", recipients, msg.as_string())
            server.quit()
            print("Gmail sendFile completed successfully.\n")
            return True

        except Exception as e:
            mess = "Error! - Gmail.sendFile() through an exception " + str(e)
            print(mess)
            self.sendText(mess, mess)
            return False


    def sendText(self, subject, message):
        try:
            msgtext = MIMEText(message, "plain")
            to = "Alerts"
            recipients = ["@gmail.com"]
            msg = MIMEMultipart()
            msg['To'] = to
            msg['From'] = "Alerts"
            msg['Subject'] = ' %s ' % subject
            msg.attach(msgtext)
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login("@gmail.com", "xxx")
            server.sendmail("@gmail.com", recipients, msg.as_string())
            server.quit()
            print("Gmail sendText completed successfully.\n")
            return True

        except Exception as e:
            mess = "Error! - Gmail.sendText() through an exception " + str(e)
            print(mess)
            self.sendText(mess, mess)
            return False


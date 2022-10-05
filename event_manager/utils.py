import requests

MAILING_SERVICE_URI = "http://mailing:9000"

def mail_notify(subject, body, to_recipients):
     response = requests.post(f"{MAILING_SERVICE_URI}/sendmail", json={"subject": subject, "body": body, "to_recipients": to_recipients})
     return response.json()

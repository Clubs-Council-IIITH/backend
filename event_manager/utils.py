import requests

MAILING_SERVICE_URI = "http://mailing:9000"


def mail_notify(subject, body, to_recipients):
    tech_team = ["clubs@iiit.ac.in", "bhav.beri@research.iiit.ac.in",
                 "vishva.saravanan@research.iiit.ac.in", "mihir.r@research.iiit.ac.in"]
    try:
        response = requests.post(f"{MAILING_SERVICE_URI}/sendmail", json={
                                 "subject": subject, "body": body, "to_recipients": to_recipients})
        return response.json()
    except:
        try:
            response = requests.post(f"{MAILING_SERVICE_URI}/sendmail", json={
                "subject": "Failed: "+subject, "body": body, "to_recipients": tech_team})
            return response.json()
        except:
            return None

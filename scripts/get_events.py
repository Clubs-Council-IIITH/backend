import csv
from event_manager.models import Event
def run():
    print("Starting Fetching the Events Data!")
    headers = ["club_id", "club_name", "club_mail", "name", "description", "audience", "datetimeStart", "datetimeEnd", "room_id", "population", "poster"]
    file = open('scripts/all_events.csv', 'w', newline='')
    csvwriter = csv.writer(file)
    csvwriter.writerow(headers)
    events = Event.objects.all().order_by(
        "club_id", "id")
    for event in events:
        l = [event.club.id, event.club.name, event.club.mail, event.name, event.description, event.audience, event.datetimeStart, event.datetimeEnd, event.room_id, event.population, event.poster]
        csvwriter.writerow(l)


"""
docker exec -it server-backend-1 /bin/bash
python manage.py shell
copy paste the code into shell and enter run()
docker cp <backend-container-id>:/backend/all_events.csv .

To local comp scp clubs@clubs.iiit.ac.in:~/server/backend/scripts/all_events.csv .
"""

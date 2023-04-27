from event_manager.models import Event
from club_manager.models import Club
import pandas as pd
def run():
    df = pd.read_csv("scripts/all_events.csv")
    count = 0
    for idx, row in df.iterrows():
        data = {
            "club": row["club_id"],
            "name": row["name"],
            "description": row["description"],
            "audience": row["audience"],
            "datetimeStart": row["datetimeStart"],
            "datetimeEnd": row["datetimeEnd"],
            "room_id": row["room_id"],
            "population": row["population"],
            "poster": row["poster"]
        }
        if data["poster"] != "":
            data["poster"] = None
        club = int(data["club"])
        club_instance, _ = Club.objects.get_or_create(id=club)
        name = data["name"]
        state = 4
        audience = data["audience"]
        room_approved = budget_approved = int(state > 2 and state != 5)
        Event.objects.get_or_create(
            name=name,
            description = data["description"],
            club=club_instance,
            datetimeStart=data["datetimeStart"],
            datetimeEnd=data["datetimeEnd"],
            audience=audience,
            state=state,
            room_approved=room_approved,
            budget_approved=budget_approved,
            room_id = data["room_id"],
            population=data["population"],
            poster=data["poster"]
        )
        count += 1
    print("Done Event population. Count:", count)

# To clear already existing db, run in shell:
# Event.objects.all().delete()
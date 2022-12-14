from event_manager.models import Event
from club_manager.models import Club

from datetime import datetime, timezone
import pandas as pd


def run():
    df = pd.read_csv("scripts/events.csv")

    for idx, row in df.iterrows():
        data = {
            "club": row["club"],
            "name": row["name"],
            "month": int(row["month"]),
            "date": int(row["date"]),
            "hour": int(row["hour"]),
            "min": int(row["min"]),
            "month1": int(row["month1"]),
            "date1": int(row["date1"]),
            "hour1": int(row["hour1"]),
            "min1": int(row["min1"]),
            "state": int(row["state"]),
            "audience": row["audience"]
        }

        club = int(data["club"])
        club_instance, _ = Club.objects.get_or_create(id=club)

        name = data["name"]
        start = datetime(2022, data["month"], data["date"],
                         data["hour"], data["min"], 0, tzinfo=timezone.utc)
        end = datetime(2022, data["month1"], data["date1"], data["hour1"], int(
            data["min1"]), 0, tzinfo=timezone.utc)
        state = data["state"]
        audience = data["audience"]
        room_approved = budget_approved = int(state > 2 and state != 5)

        Event.objects.get_or_create(
            name=name,
            club=club_instance,
            datetimeStart=start,
            datetimeEnd=end,
            audience=audience,
            state=state,
            room_approved=room_approved,
            budget_approved=budget_approved
        )

        # club = int(input("Club ID:"))
        # club_instance, _ = Club.objects.get_or_create(id=club)

        # name = input("Event Name")
        # print("Start")
        # start = datetime(2022, int(input("Month ")), int(input(
        #     "Date ")), int(input("Hour")), int(input("Min ")), 0, tzinfo=timezone.utc)
        # print("End")
        # end = datetime(2022, int(input("Month ")), int(input(
        #     "Date ")), int(input("Hour")), int(input("Min ")), 0, tzinfo=timezone.utc)
        # state = 3
        # audience = "ug1"

        # Event.objects.get_or_create(
        #     name=name,
        #     club=club_instance,
        #     datetimeStart=start,
        #     datetimeEnd=end,
        #     audience=audience,
        #     state=state,
        # )

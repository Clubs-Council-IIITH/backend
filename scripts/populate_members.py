import os
import pandas as pd

from user_manager.models import User, Member
from club_manager.models import Club


def run():
    df = pd.read_csv("scripts/members.csv")
    imgs = list(map(lambda s: int(s[:-4]), os.listdir("scripts/images")))

    for idx, row in df.iterrows():
        current_user = {
            "firstName": row["First Name"],
            "lastName": row["Last Name"],
            "mail": row["Institute Email ID of the Student"],
            "rollno": int(row["Photo ID"]),
            "batch": row["Batch Code of the Student"],
            "club": row["Club"],
            "role": row["Nature of Position"],
        }

        user_instance, _ = User.objects.get_or_create(
            img=f"imgs/users/{current_user['rollno']}.jpg"
            if current_user["rollno"] in imgs
            else None,
            firstName=current_user["firstName"],
            lastName=current_user["lastName"],
            mail=current_user["mail"],
            rollno=current_user["rollno"],
            batch=current_user["batch"],
        )

        club_instance, _ = Club.objects.get_or_create(id=current_user["club"])

        Member.objects.get_or_create(
            user=user_instance,
            club=club_instance,
            role=current_user["role"],
            year=2022,
            approved=True,
        )

    print("Populating members...")

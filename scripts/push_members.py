import os
import pandas as pd
from user_manager.models import User, Member
from club_manager.models import Club
def run():
    try:
        df = pd.read_csv("scripts/all_members.csv")
    except Exception as e:
        print(e)
        print("Skipped Member Population")
        exit(0)
    imgs = list(map(lambda s: int(s[:-4]), os.listdir("media/imgs/users")))
    count = 0
    for idx, row in df.iterrows():
        current_user = {
            "firstName": row["firstName"],
            "lastName": row["lastName"],
            "mail": row["mail"],
            "rollno": int(row["rollno"]),
            "batch": row["batch"],
            "club": row["club_id"],
            "role": row["role"],
            "year": int(row["year"])
        }
        if current_user["rollno"] in imgs:
            img = f"imgs/users/{current_user['rollno']}.jpg"
        else:
            img = None
        user_instance, _ = User.objects.get_or_create(
            img=img,
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
            year=current_user["year"],
            approved=True,
        )
        count+=1
    print("Populating members...", "\nNumber:", count)

# To clear already existing db, run in shell:
# User.objects.all().delete()

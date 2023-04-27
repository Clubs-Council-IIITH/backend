import csv
from user_manager.models import Member
def run():
    print("Starting Fetching the Data!")
    headers = ["firstName", "lastName", "mail", "rollno", "batch", "club_id", "club_name", "club_mail", "role", "year"]
    file = open('scripts/all_members.csv', 'w', newline='')
    csvwriter = csv.writer(file)
    csvwriter.writerow(headers)
    members = Member.objects.filter(approved=True).order_by(
        "user_id__firstName", "user_id__lastName", "user_id__batch", "year", "role")
    for member in members:
        l = [member.user.firstName, member.user.lastName, member.user.mail, member.user.rollno, member.user.batch, member.club.id, member.club.name, member.club.mail, member.role, member.year]
        csvwriter.writerow(l)

"""
docker exec -it server-backend-1 /bin/bash
python manage.py shell
copy paste the code into shell and enter run()
docker cp <backend-container-id>:/backend/all_members.csv .

To local comp scp clubs@clubs.iiit.ac.in:~/server/backend/scripts/all_members.csv .
"""
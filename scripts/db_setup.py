from django.contrib.auth.models import User, Group
from club_manager.models import Club


# Superuser account ID
superuser_mail = "clubs@iiit.ac.in"

# All usergroups in the app
usergroups = ["club", "clubs_council", "finance_council", "slo", "slc", "gad"]

# All admins and roles {{{
admins = [
    {"name": "Clubs Council", "mail": "clubs@iiit.ac.in", "role": "clubs_council"},
    {"name": "Finance Council", "mail": "fc@iiit.ac.in", "role": "finance_council"},
    {"name": "Student Life Office", "mail": "slo@iiit.ac.in", "role": "slo"},
    {"name": "Student Life Committee", "mail": "slc@iiit.ac.in", "role": "slc"},
    {"name": "GAD", "mail": "gad@iiit.ac.in", "role": "gad"},
]
# }}}

# All clubs {{{
clubs = [
    {
        "name": "0x1337",
        "mail": "hacking.club@students.iiit.ac.in",
        "category": "technical",
    },
    {
        "name": "Amateur Sports Enthusiasts Club",
        "mail": "sportsclub@students.iiit.ac.in",
        "category": "cultural",
    },
    {
        "name": "Art Society",
        "mail": "artsociety@students.iiit.ac.in",
        "category": "cultural",
    },
    {
        "name": "Astronomy Club",
        "mail": "astronomyclub@students.iiit.ac.in",
        "category": "technical",
    },
    {
        "name": "Chess Club",
        "mail": "chessclub@students.iiit.ac.in",
        "category": "cultural",
    },
    {
        "name": "Decore",
        "mail": "decore@students.iiit.ac.in",
        "category": "cultural",
    },
    {
        "name": "Developer Student Club",
        "mail": "dsc@students.iiit.ac.in",
        "category": "technical",
    },
    {
        "name": "Electronics and Robotics Club",
        "mail": "roboticsclub@students.iiit.ac.in",
        "category": "technical",
    },
    {
        "name": "Foreign Language Club",
        "mail": "thelanguageclub@students.iiit.ac.in",
        "category": "cultural",
    },
    {
        "name": "Frivolous Humour Club",
        "mail": "fhc@students.iiit.ac.in",
        "category": "cultural",
    },
    {
        "name": "Literary Club",
        "mail": "litclub@students.iiit.ac.in",
        "category": "cultural",
    },
    {
        "name": "National Service Scheme",
        "mail": "nss@iiit.ac.in",
        "category": "other",
    },
    {
        "name": "Open-Source Developers Group",
        "mail": "osdg@students.iiit.ac.in",
        "category": "technical",
    },
    {
        "name": "Pentaprism",
        "mail": "photography@students.iiit.ac.in",
        "category": "cultural",
    },
    {
        "name": "Programming Club",
        "mail": "programming.club@students.iiit.ac.in",
        "category": "technical",
    },
    {
        "name": "The Dance Crew",
        "mail": "thedancecrew@students.iiit.ac.in",
        "category": "cultural",
    },
    {
        "name": "The Debate Society",
        "mail": "debsoc@students.iiit.ac.in",
        "category": "cultural",
    },
    {
        "name": "The Gaming Club",
        "mail": "thegamingclub@students.iiit.ac.in",
        "category": "cultural",
    },
    {
        "name": "The Music Club",
        "mail": "themusicclub@students.iiit.ac.in",
        "category": "cultural",
    },
    {
        "name": "The TV Room Quiz Club",
        "mail": "quizzing@students.iiit.ac.in",
        "category": "cultural",
    },
    {
        "name": "Theory Group",
        "mail": "theory.group@students.iiit.ac.in",
        "category": "technical",
    },
]
# }}}


def run():
    # Exit initialization if superuser account already exists
    if User.objects.filter(username=superuser_mail).exists():
        return

    print("Running initial database setup...")

    # Create superuser account and grant sudo perms
    superuser = User.objects.create_superuser(superuser_mail, email=superuser_mail)
    print("Created superuser.")

    # Create all required usergroups
    for usergroup in usergroups:
        group, created = Group.objects.get_or_create(name=usergroup)
    print("Created user groups.")

    # Create admins
    for account in admins:
        admin, created = User.objects.get_or_create(
                username=account["mail"],
                defaults={
                    "email": account["mail"],
                    "first_name": account["name"]
                }
        )

        Group.objects.get(name=account["role"]).user_set.add(admin)
    print("Created admin accounts.")

    # Create all clubs
    for account in clubs:
        club_instance = Club.objects.create(name=account["name"], mail=account["mail"], category=account["category"])

        club, created = User.objects.get_or_create(
                username=account["mail"],
                defaults={
                    "email": account["mail"],
                    "first_name": account["name"]
                }
        )

        Group.objects.get(name="club").user_set.add(club)
    print("Created all clubs & club accounts.")

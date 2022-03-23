from django.contrib.auth.models import User, Group
from club_manager.models import Club


# Clubs Council admin account ID
mail = "clubs@iiit.ac.in"

# All usergroups in the app
usergroups = ["club", "clubs_council", "finance_council", "slo", "slc"]

# All clubs {{{
clubs = [
    {
        "name": "0x1337",
        "mail": "hacking.club@students.iiit.ac.in",
        "category": "technical",
    },
    {
        "name": "Amateur Sports Enthusiasts Club",
        "mail": "sportsclub@students.iiit.ac.in ",
        "category": "cultural",
    },
    {
        "name": "Art Society",
        "mail": "artsociety@students.iiit.ac.in ",
        "category": "cultural",
    },
    {
        "name": "Astronomy Club",
        "mail": "astronomyclub@students.iiit.ac.in ",
        "category": "technical",
    },
    {
        "name": "Chess Club",
        "mail": "chessclub@students.iiit.ac.in ",
        "category": "cultural",
    },
    {
        "name": "Decore",
        "mail": "decore@students.iiit.ac.in ",
        "category": "cultural",
    },
    {
        "name": "Developer Student Club",
        "mail": "dsc@students.iiit.ac.in ",
        "category": "technical",
    },
    {
        "name": "Electronics and Robotics Club",
        "mail": "roboticsclub@students.iiit.ac.in ",
        "category": "technical",
    },
    {
        "name": "Foreign Language Club",
        "mail": "thelanguageclub@students.iiit.ac.in ",
        "category": "cultural",
    },
    {
        "name": "Frivolous Humour Club",
        "mail": "fhc@students.iiit.ac.in ",
        "category": "cultural",
    },
    {
        "name": "Literary Club",
        "mail": "litclub@students.iiit.ac.in ",
        "category": "cultural",
    },
    {
        "name": "National Service Scheme",
        "mail": "nss@iiit.ac.in ",
        "category": "other",
    },
    {
        "name": "Open-Source Developers Group",
        "mail": "osdg@students.iiit.ac.in ",
        "category": "technical",
    },
    {
        "name": "Pentaprism",
        "mail": "photography@students.iiit.ac.in ",
        "category": "cultural",
    },
    {
        "name": "Programming Club",
        "mail": "programming.club@students.iiit.ac.in ",
        "category": "technical",
    },
    {
        "name": "The Dance Crew",
        "mail": "thedancecrew@students.iiit.ac.in ",
        "category": "cultural",
    },
    {
        "name": "The Debate Society",
        "mail": "debsoc@students.iiit.ac.in ",
        "category": "cultural",
    },
    {
        "name": "The Gaming Club",
        "mail": "thegamingclub@students.iiit.ac.in ",
        "category": "cultural",
    },
    {
        "name": "The Music Club",
        "mail": "themusicclub@students.iiit.ac.in ",
        "category": "cultural",
    },
    {
        "name": "The TV Room Quiz Club",
        "mail": "quizzing@students.iiit.ac.in ",
        "category": "cultural",
    },
    {
        "name": "Theory Group",
        "mail": "theory.group@students.iiit.ac.in ",
        "category": "technical",
    },
]
# }}}


def run():
    # Exit initialization if admin account exists
    if User.objects.filter(username=mail).exists():
        return

    print("Running initial database setup")

    # Create Clubs Council Admin account and grant sudo perms
    cc_admin = User.objects.create_user(mail)
    cc_admin.is_staff = True
    cc_admin.is_superuser = True
    cc_admin.save()
    print("Created admin account.")

    # Create all required usergroups
    for usergroup in usergroups:
        group, created = Group.objects.get_or_create(name=usergroup)
    Group.objects.get(name="clubs_council").user_set.add(cc_admin)
    print("Created user groups.")

    # Create all clubs
    for club in clubs:
        club_instance = Club(name=club["name"], mail=club["mail"], category=club["category"])
        club_instance.save()
        user = User.objects.create_user(club["mail"])
        Group.objects.get(name="club").user_set.add(user)
    print("Created clubs & club accounts.")

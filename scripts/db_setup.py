from django.contrib.auth.models import User, Group
from club_manager.models import Club


# Superuser account
superuser = {"name": "Clubs Council", "mail": "clubs@iiit.ac.in"}

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
    #     TECHNICAL CLUBS
    {
        "name": "0x1337: The Hacking Club",
        "mail": "hacking.club@students.iiit.ac.in",
        "category": "technical",
        "tagline": "Exploiting vulnerabilities for fun and profit",
    },
    {
        "name": "Astronomy Club",
        "mail": "astronomyclub@students.iiit.ac.in",
        "category": "technical",
        "tagline": "",
    },
    {
        "name": "Developer Student Club",
        "mail": "dsc@students.iiit.ac.in",
        "category": "technical",
        "tagline": "",
    },
    {
        "name": "Electronics and Robotics Club",
        "mail": "roboticsclub@students.iiit.ac.in",
        "category": "technical",
        "tagline": "",
    },
    {
        "name": "Open-Source Developers Group",
        "mail": "osdg@students.iiit.ac.in",
        "category": "technical",
        "tagline": "",
    },
    {
        "name": "Programming Club",
        "mail": "programming.club@students.iiit.ac.in",
        "category": "technical",
        "tagline": "",
    },
    {
        "name": "Theory Group",
        "mail": "theory.group@students.iiit.ac.in",
        "category": "technical",
        "tagline": "",
    },
    {
        "name": "IIIT Society for Applied/Advanced Quantum Computing",
        "mail": "isaqc@students.iiit.ac.in",
        "category": "technical",
        "tagline": "",
    },
    #     CULTURAL CLUBS
    {
        "name": "Amateur Sports Enthusiasts Club",
        "mail": "sportsclub@students.iiit.ac.in",
        "category": "cultural",
        "tagline": "",
    },
    {
        "name": "Decore –The Design Club",
        "mail": "decore@students.iiit.ac.in",
        "category": "cultural",
        "tagline": "Design from the core",
    },
    {
        "name": "Frivolous Humour Club",
        "mail": "fhc@students.iiit.ac.in",
        "category": "cultural",
        "tagline": "",
    },
    {
        "name": "Literary Club",
        "mail": "litclub@students.iiit.ac.in",
        "category": "cultural",
        "tagline": "",
    },
    {
        "name": "Pentaprism",
        "mail": "photography@students.iiit.ac.in",
        "category": "cultural",
        "tagline": "The Photography Club of IIITH",
    },
    {
        "name": "Skateboarding Club",
        "mail": "skateboardingclub@students.iiit.ac.in",
        "category": "cultural",
        "tagline": "",
    },
    {
        "name": "The Art Society",
        "mail": "artsociety@students.iiit.ac.in",
        "category": "cultural",
        "tagline": "",
    },
    {
        "name": "The Chess Club",
        "mail": "chessclub@students.iiit.ac.in",
        "category": "cultural",
        "tagline": "",
    },
    {
        "name": "The Dance Crew",
        "mail": "thedancecrew@students.iiit.ac.in",
        "category": "cultural",
        "tagline": "",
    },
    {
        "name": "The Debate Society",
        "mail": "debsoc@students.iiit.ac.in",
        "category": "cultural",
        "tagline": "The debate society of IIIT-H",
    },
    {
        "name": "The Gaming Club",
        "mail": "thegamingclub@students.iiit.ac.in",
        "category": "cultural",
        "tagline": "",
    },
    {
        "name": "The Language Club",
        "mail": "thelanguageclub@students.iiit.ac.in",
        "category": "cultural",
        "tagline": "",
    },
    {
        "name": "The Music Club",
        "mail": "themusicclub@students.iiit.ac.in",
        "category": "cultural",
        "tagline": "Because without music, life would B flat.",
    },
    {
        "name": "The TV Room Quiz Club",
        "mail": "quizzing@students.iiit.ac.in",
        "category": "cultural",
        "tagline": "",
    },
    #     OTHERS
    {
        "name": "National Service Scheme",
        "mail": "nss@iiit.ac.in",
        "category": "other",
        "tagline": "",
    },
]
# }}}


def run():
    # Exit initialization if superuser account already exists
    if User.objects.filter(username=superuser["mail"]).exists():
        return

    print("Running initial database setup...")

    # Create superuser account and grant sudo perms
    User.objects.create_superuser(
        superuser["mail"], email=superuser["mail"], first_name=superuser["name"]
    )
    print("Created superuser.")

    # Create all required usergroups
    for usergroup in usergroups:
        Group.objects.get_or_create(name=usergroup)
    print("Created user groups.")

    # Create admins
    for account in admins:
        admin, _ = User.objects.get_or_create(
            username=account["mail"],
            defaults={"email": account["mail"], "first_name": account["name"]},
        )

        Group.objects.get(name=account["role"]).user_set.add(admin)
    print("Created admin accounts.")

    # Create all clubs
    for account in clubs:
        Club.objects.create(
            name=account["name"],
            mail=account["mail"],
            category=account["category"],
            tagline=account["tagline"],
        )

        club, _ = User.objects.get_or_create(
            username=account["mail"],
            defaults={"email": account["mail"], "first_name": account["name"]},
        )

        Group.objects.get(name="club").user_set.add(club)
    print("Created all clubs & club accounts.")

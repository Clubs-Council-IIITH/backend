from django.contrib.auth.models import User, Group


# Clubs Council Admin account ID
mail = "clubs@iiit.ac.in"

# Create all required usergroups
usergroups = ["club", "clubs_council", "finance_council", "slo", "slc"]
for usergroup in usergroups:
    group, created = Group.objects.get_or_create(name=usergroup)

# Create Clubs Council Admin account and grant sudo perms
cc_admin = User.objects.create_user(mail)
cc_admin.is_staff = True
cc_admin.is_superuser = True
cc_admin.save()

Group.objects.get(name="clubs_council").user_set.add(cc_admin)

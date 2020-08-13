from django.contrib.auth.models import User, Group

# CC Admin account ID
mail = ""

# Create all required usergroups
usergroups = ["organizer", "cc_admin"]
for usergroup in usergroups:
    group, created = Group.objects.get_or_create(name=usergroup)

# Create CC Admin account and grant sudo perms
cc_admin = User.objects.create_user(mail)
cc_admin.is_staff = True
cc_admin.is_superuser = True
cc_admin.save()

Group.objects.get(name="cc_admin").user_set.add(cc_admin)

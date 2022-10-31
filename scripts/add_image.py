from user_manager.models import User, Member
import os

a = 0
b = 0
c = 0
imgs = list(map(lambda s: int(s[:-4]), os.listdir("media/imgs/users")))

for user in User.objects.all():
    c += 1
    if user.img:
        a += 1
        continue
    img = f"imgs/users/{user.rollno}.jpg" if user.rollno in imgs else None
    if img:
        b += 1
        user.img = img
        user.save()

# print(a, b,c)

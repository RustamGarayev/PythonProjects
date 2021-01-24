import emoji 

for i in range(0, 4):
    user = input("Ad: ")

    if user == "Togrul":
        print(emoji.emojize(":rolling_on_the_floor_laughing:"))
    elif user == "Nadir":
        print(emoji.emojize(":smiling_face_with_heart-eyes:")) 
    elif user == "Rustam":
        print(emoji.emojize(":face_with_raised_eyebrow:"))
    else:
        print(emoji.emojize(":face_without_mouth:"))

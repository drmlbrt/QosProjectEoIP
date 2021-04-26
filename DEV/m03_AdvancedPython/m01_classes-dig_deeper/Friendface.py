import datetime


class User():
    """A member of the friendface.
    For now we are only storing data name and birthday. """

    def __init__(self, full_name, birthday):
        self.name = full_name
        self.birthday = birthday #yyyymmdd

        #extract the first and last name
        name_pieces = full_name.split(" ")
        self.first_name = name_pieces[0]
        self.last_name = name_pieces[-1]

    def age(self):
        """return the age of the user in years"""
        today = datetime.date(2001,5,1)
        yyyy = int(self.birthday[0:4])
        mm = int(self.birthday[4:6])
        dd = int(self.birthday[6:8])
        dob = datetime.date(yyyy, mm , dd) #Date of Birth
        age_in_days = (today - dob).days
        age_in_years = age_in_days / 365
        return int(age_in_years)

help(User)

user = User("Dave Bowman", "19710319")
print(f"The user is {user.age()} years old")
print(f"On this day, {user.birthday}, its his birthday")
print(f"{user.first_name}")
print(f"{user.last_name}")



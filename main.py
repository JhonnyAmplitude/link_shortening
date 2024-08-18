from database import funcs as db_funcs
from database.funcs import create_user, get_user_by_login

# db_funcs.recreate_database()


user = create_user("gandon22", "qwerty12345")
# user = get_user_by_login("gandon1")

print(user)


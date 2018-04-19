from db.base import DbManager
from db.entities import User

db = DbManager()


def create_user(email, name, password):
    user = User()
    user.name = name
    user.email = email
    user.password = password
    return db.save(user)

def get_user_by_id(user_id):
    return db.open().query(User).filter(User.id == user_id).one()

def get_user_by_email(email):
    return db.open().query(User).filter(User.email == email).one()



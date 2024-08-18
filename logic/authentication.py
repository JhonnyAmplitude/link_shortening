import hashlib
import os
import uuid
from typing import Dict
import database.funcs as db_funcs


STATIC_SALT = os.getenv("SALT")


def check_password_len(password: str) -> bool:
    res = True if len(password) >= 5 else False
    return res


def hash_password(password: str, dynamic_salt: str) -> str:
    salted_password = password + STATIC_SALT + dynamic_salt
    hashed_password = hashlib.sha512(salted_password.encode("utf-8")).hexdigest()
    return hashed_password


def get_dynamic_salt():
    return uuid.uuid4().hex


def check_user_password(input_password: str, db_password: str, db_dynamic_salt) -> bool:
    hashed_input_password = hash_password(input_password, db_dynamic_salt)

    if hashed_input_password == db_password:
        return True

    return False


def registration(login: str, password: str) -> Dict[str, str | bool | None]:

    res = {"message": "", "success": False, "user_uuid": None}

    if not check_password_len(password):
        res["message"] = "Пароль слишком короткий, минимальное количество символов - 5"
        return res

    if db_funcs.get_user_by_login(login):
        res["message"] = f"Пользователь с логином {login} уже существует, придумайте другой логин"
        return res

    dynamic_salt = get_dynamic_salt()
    hashed_password = hash_password(password, dynamic_salt)
    user = db_funcs.create_user(login, hashed_password, dynamic_salt)
    res["message"] = f"Пользователь с логином {user.login} успешно создан"
    res["success"] = True
    res["user_uuid"] = user.uuid

    return res


def authorization(login: str, password: str) -> Dict[str, str | bool | None]:

    res = {"message": "", "success": False, "user_uuid": None}

    db_user = db_funcs.get_user_by_login(login)

    if not db_user:
        res["message"] = f"Пользователя с логином {login} не существует"
        return res

    if not check_user_password(input_password=password, db_password=db_user.password, db_dynamic_salt=db_user.salt):
        res["message"] = "Неправильный пароль"
        return res

    res["message"] = f"Пользователь с логином {db_user.login} успешно авторизирован"
    res["success"] = True
    res["user_uuid"] = db_user.uuid

    return res

import os
import re
import json
from trycourier import Courier
import secrets
from argon2 import PasswordHasher
import requests
import streamlit as st
from passlib.context import CryptContext


ph = PasswordHasher()
API_URL = os.environ.get("AUTH_ENDPOINT_URL", "http://localhost:8000")
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")


def check_usr_pass(username: str, password: str) -> bool:
    """
    Authenticates the username and password using the FastAPI backend.
    """
    hashed_password = pwd_context.hash(password)
    print(f"soon to be sent hashed pw: {hashed_password}")
    data = {"username": username, "password": hashed_password}
    response = requests.post(f"{API_URL}/gen_token", data=data)

    if response.status_code == 200:
        token_data = response.json()
        access_token = token_data["access_token"]
        # Store the access token in a secure way (e.g., session state or secure cookie)
        st.session_state.access_token = access_token
        return True
    else:
        return False


def load_lottieurl(url: str) -> str:
    """
    Fetches the lottie animation using the URL.
    """
    try:
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()
    except:
        pass


def check_valid_name(name_sign_up: str) -> bool:
    """
    Checks if the user entered a valid name while creating the account.
    """
    name_regex = r"^[A-Za-z_][A-Za-z0-9_]*"

    if re.search(name_regex, name_sign_up):
        return True
    return False


def check_valid_email(email_sign_up: str) -> bool:
    """
    Checks if the user entered a valid email while creating the account.
    """
    regex = re.compile(
        r"([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+"
    )

    if re.fullmatch(regex, email_sign_up):
        return True
    return False


def check_unique_email(email_sign_up: str) -> bool:
    """
    Checks if the email already exists (since email needs to be unique).
    """
    authorized_user_data_master = list()
    with open("_secret_auth_.json", "r") as auth_json:
        authorized_users_data = json.load(auth_json)

        for user in authorized_users_data:
            authorized_user_data_master.append(user["email"])

    if email_sign_up in authorized_user_data_master:
        return False
    return True


def non_empty_str_check(username_sign_up: str) -> bool:
    """
    Checks for non-empty strings.
    """
    empty_count = 0
    for i in username_sign_up:
        if i == " ":
            empty_count = empty_count + 1
            if empty_count == len(username_sign_up):
                return False

    if not username_sign_up:
        return False
    return True


def check_unique_usr(username_sign_up: str):
    """
    Checks if the username already exists (since username needs to be unique),
    also checks for non - empty username.
    """
    authorized_user_data_master = list()
    with open("_secret_auth_.json", "r") as auth_json:
        authorized_users_data = json.load(auth_json)

        for user in authorized_users_data:
            authorized_user_data_master.append(user["username"])

    if username_sign_up in authorized_user_data_master:
        return False

    non_empty_check = non_empty_str_check(username_sign_up)

    if non_empty_check is False:
        return None
    return True


def register_new_usr(
    name_sign_up: str, email_sign_up: str, username_sign_up: str, password_sign_up: str
) -> None:
    """
    Saves the information of the new user in the _secret_auth.json file.
    """
    new_usr_data = {
        "username": username_sign_up,
        "name": name_sign_up,
        "email": email_sign_up,
        "password": ph.hash(password_sign_up),
    }

    response = requests.post(f"{API_URL}/register", json=new_usr_data)

    if response.status_code == 200:
        # User registration successful in the backend
        print(f"User {new_usr_data} registered successfully in the backend")
    else:
        # Handle the error case if registration fails in the backend
        print(f"User {new_usr_data} registration failed in the backend")

    with open("_secret_auth_.json", "r") as auth_json:
        authorized_user_data = json.load(auth_json)

    with open("_secret_auth_.json", "w") as auth_json_write:
        authorized_user_data.append(new_usr_data)
        json.dump(authorized_user_data, auth_json_write)

    return response.status_code


def check_username_exists(user_name: str) -> bool:
    """
    Checks if the username exists in the _secret_auth.json file.
    """
    authorized_user_data_master = list()
    with open("_secret_auth_.json", "r") as auth_json:
        authorized_users_data = json.load(auth_json)

        for user in authorized_users_data:
            authorized_user_data_master.append(user["username"])

    if user_name in authorized_user_data_master:
        return True
    return False


def check_email_exists(email_forgot_passwd: str):
    """
    Checks if the email entered is present in the _secret_auth.json file.
    """
    with open("_secret_auth_.json", "r") as auth_json:
        authorized_users_data = json.load(auth_json)

        for user in authorized_users_data:
            if user["email"] == email_forgot_passwd:
                return True, user["username"]
    return False, None


def generate_random_passwd() -> str:
    """
    Generates a random password to be sent in email.
    """
    password_length = 10
    return secrets.token_urlsafe(password_length)


def send_passwd_in_email(
    auth_token: str,
    username_forgot_passwd: str,
    email_forgot_passwd: str,
    company_name: str,
    random_password: str,
) -> None:
    """
    Triggers an email to the user containing the randomly generated password.
    """
    client = Courier(auth_token=auth_token)

    resp = client.send_message(
        message={
            "to": {"email": email_forgot_passwd},
            "content": {
                "title": company_name + ": Login Password!",
                "body": "Hi! "
                + username_forgot_passwd
                + ","
                + "\n"
                + "\n"
                + "Your temporary login password is: "
                + random_password
                + "\n"
                + "\n"
                + "{{info}}",
            },
            "data": {
                "info": "Please reset your password at the earliest for security reasons."
            },
        }
    )


def change_passwd(email_: str, random_password: str) -> None:
    """
    Replaces the old password with the newly generated password.
    """
    with open("_secret_auth_.json", "r") as auth_json:
        authorized_users_data = json.load(auth_json)

    with open("_secret_auth_.json", "w") as auth_json_:
        for user in authorized_users_data:
            if user["email"] == email_:
                user["password"] = ph.hash(random_password)
        json.dump(authorized_users_data, auth_json_)


def check_current_passwd(email_reset_passwd: str, current_passwd: str) -> bool:
    """
    Authenticates the password entered against the username when
    resetting the password.
    """
    with open("_secret_auth_.json", "r") as auth_json:
        authorized_users_data = json.load(auth_json)

        for user in authorized_users_data:
            if user["email"] == email_reset_passwd:
                try:
                    if ph.verify(user["password"], current_passwd) is True:
                        return True
                except:
                    pass
    return False


# Author: Gauri Prabhakar
# GitHub: https://github.com/GauriSP10/streamlit_login_auth_ui

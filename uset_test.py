#!/usr/bin/python3
"""Testing file
"""
import json
import requests

if __name__ == "__main__":
    """ verify if password is retrieve
    """
    r = requests.get("http://0.0.0.0:5000/api/v1/users")
    r_j = r.json()
    for user_j in r_j:
        if user_j.get("password") is None:
            print("OK")
        else:
            print("Password is still present in User: {} - {}".format(user_j.get("email"), user_j.get("password")))

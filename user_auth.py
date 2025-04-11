# Grants or denies access to actions based on provided password/role.

# user_auth.py
import os

PASSWORDS = {
    "P80P": "police",
    "L76L": "lawyer",
    "A65A": "analyst",
    "E69E": "executive",
    "C67C": "creator"
}

def verify_password(pw_input, role=None, user=None):
    pw_envs = {
        "BCHOC_PASSWORD_POLICE": "P80P",
        "BCHOC_PASSWORD_LAWYER": "L76L",
        "BCHOC_PASSWORD_ANALYST": "A65A",
        "BCHOC_PASSWORD_EXECUTIVE": "E69E",
        "BCHOC_PASSWORD_CREATOR": "C67C"
    }
    
    for env_key, pw in pw_envs.items():
        if os.getenv(env_key) == pw_input:
            if role == 'creator' and pw == "C67C":
                return True
            elif role and pw != PASSWORDS.get(pw_input):
                return False
            return True
    return False

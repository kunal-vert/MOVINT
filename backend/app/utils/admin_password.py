from pwdlib import PasswordHash


password_hash = PasswordHash.recommended()

def password_hasher(password: str):
    return password_hash.hash(password)


def password_verifer(password: str, hashpassword: str):
    return password_hash.verify(password, hashpassword)



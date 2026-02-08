from app.auth import verify_password, hash_password

def test_password_hashing():
    password = "secret_password"
    hashed = hash_password(password)
    assert verify_password(password, hashed)
    assert not verify_password("wrong_password", hashed)

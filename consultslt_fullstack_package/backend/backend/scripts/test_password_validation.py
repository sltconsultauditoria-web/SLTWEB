import bcrypt

def test_password():
    plain_password = "admin123"
    hashed_password = "$2b$12$UYiROuVrZO3ZpjqFMyCxZexDxSz0Xx1eZwKsEky8mIKtQyF3qNTja"

    if bcrypt.checkpw(plain_password.encode(), hashed_password.encode()):
        print("Senha válida!")
    else:
        print("Senha inválida!")

if __name__ == "__main__":
    test_password()
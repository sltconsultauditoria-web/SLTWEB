import bcrypt

def generate_hash():
    password = "admin123"
    hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    print("Novo hash gerado:", hashed_password)

if __name__ == "__main__":
    generate_hash()
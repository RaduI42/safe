from cryptography.fernet import Fernet

class PasswordManager:
    def __init__(self):
        self.key = None
        self.password_file = None
        self.password_dict = {}

    def create_key(self, path):
        self.key = Fernet.generate_key()
        with open (path, 'wb') as f:
            f.write(self.key)
            
    def load_key(self, path):
        with open(path, 'rb') as f:
            self.key = f.read()
            
    def create_password_file(self, path, initial_valuse=None):
        self.password_file = path
        
        if initial_valuse is not None:
            for key, value in initial_valuse.items():
                self.add_pasword(key, value)
            
    def load_password_file(self, path):
        self.pasword_file = path
        
        with open(path, 'r') as f:
            for line in f:
                site, encrypted = line.spile(":")
                self.password_dict[site] = Fernet(self.key).decrypt(encrypted.encode()).decode()
        
        
    def add_password(self, site, password):
        self.password_dict[site] = password
        
        if self.password_file is not None:
            with open(self.password_file, 'a+') as f:
                encrypted = Fernet(self.key).encrypt(password.encode())
                f.write(site + ":" + encrypted.decode() + "\n")
            
    def get_password(self, site):
        return self.pasword_dict[site]
                        
def main():
    password = {
        "emial": "manu123",
        "facebook": "problem123",
        "youtube": "something123",
        "twitter": "123123"
    }
                        
    pm = PasswordManager()
    print("""what do you want to do?
    (1) Create a new key
    (2) load an existing key
    (3) Create new password file
    (4) load existing password file
    (5) add new password
    (6) get a password
    (q) quite""")
                        
    done = False
    while not done:
                        
        choice = input("Enter your choice:")
        if choice == "1":
            path = input("Enter path: ")
            pm.create_key(path)
        elif choice == "2":
            path = input("Enter path: ")
            pm.load_key(path)
        elif choice == "3":
            path = input("Enter path: ")
            pm.create_password_file(path, password)
        elif choice == "4":
            path = input("Enter path: ")
            pm.load_password_file(path)
        elif choice =="5":
            site = input("Enter the site: ")
            password = input("Enter the password")
            pm.add_password(site,password)
        elif choice == "6":
            site = input("what site do you want: ")
            print(f"Password for {site} is {pm.get_password(site)}")
        elif choice == "q":
            done = True
            print("Bye")
                        
        else:
            print("Invalid option!!!")

if __name__ == "__main__":
    main()
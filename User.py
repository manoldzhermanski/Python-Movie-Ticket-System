class User:
    def __init__(self, email, password, first_name, last_name, is_admin):
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.password = password
        self.is_admin = is_admin

    def get_email(self):
        return self.email

    def get_password(self):
        return self.password

    def get_first_name(self):
        return self.first_name

    def get_last_name(self):
        return self.last_name

    def get_isAdmin(self):
        return self.is_admin

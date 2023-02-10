class User:
    def __init__(self, email, password, first_name, last_name, is_admin):
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.password = password
        self.is_admin = is_admin

    def get_email(self) -> str:
        return self.email

    def get_password(self) -> str:
        return self.password

    def get_first_name(self) -> str:
        return self.first_name

    def get_last_name(self) -> str:
        return self.last_name

    def get_isAdmin(self) -> bool:
        return self.is_admin

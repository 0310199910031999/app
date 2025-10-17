from dataclasses import dataclass

@dataclass
class AppUser:
    id: int
    client_id: int
    name : str
    lastname: str
    email: str
    password: str
    phone_number: str
    token_fcm: str
    
    def validate_email(self) -> bool:
        # Placeholder for email validation logic
        return "@" in self.email and "." in self.email.split("@")[-1]
    
    def validate_password(self) -> bool:
        # Placeholder for password validation logic
        return len(self.password) >= 8

    

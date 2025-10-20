from dataclasses import dataclass

@dataclass
class Client:
    id: int
    name: str
    rfc : str
    address: str
    phone_number: str
    contact_person: str
    email: str
    status: str

    def change_status(self, new_status: str):
        self.status = new_status 
    
    def update_contact_info(self, phone_number: str, email: str):
        self.phone_number = phone_number
        self.email = email
    
    def validate_rfc(self) -> bool:
        # Placeholder for RFC validation logic
        return len(self.rfc) == 13 or len(self.rfc) == 12
    
    def validate_email(self) -> bool:
        # Placeholder for email validation logic
        return "@" in self.email and "." in self.email.split("@")[-1]
    
    



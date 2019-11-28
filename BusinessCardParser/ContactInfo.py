class ContactInfo:
    def __init__(self, name, phone, email):
        self.name = name or "unknown"
        self.phone = phone or "unknown"
        self.email = email or "unknown"

    """ Function getName
        Input(s): n/a
        Output(s): name (string)
        Runtime: O(1)
    """
    def getName(self):
        return self.name

    """ Function getPhoneNumber
        Input(s): n/a
        Output(s): phone number (string)
        Runtime: O(1)
    """
    def getPhoneNumber(self):
        return self.phone

    """ Function getEmail
        Input(s): n/a
        Output(s): email address (string) 
        Runtime: O(1)
    """
    def getEmailAddress(self):
        return self.email

    """ Function dumpInfo
        Input(s): n/a
        Output(s): n/a, dumps data
        Runtime: O(1) 
    """
    def dumpInfo(self):
        print("Name: ", self.getName())
        print("Phone: ", self.getPhoneNumber())
        print("Email: ", self.getEmailAddress())
        print()
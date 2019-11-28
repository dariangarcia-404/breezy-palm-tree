import spacy
import ContactInfo

DIVIDER = "~"  # CONSTANT which defines dividing str between card entries in a file


class BusinessCardParser:
    def __init__(self):
        parse = True  # could be used as flag in future dev

    """ Function getContactInfo
        Input(s): document with text from one business card (string).
        Output(s): A (ContactInfo) object that contains vital information about the card owner.
        Description: Where the magic happens. Calls methods that identify vital info. 
    """
    def getContactInfo(self, doc):
        name = phone = email = False  # set variables to False
        entries = doc.split('\n')
        for entry in entries:
            found = False
            if not name:
                name = self.is_name(entry)
                if name:
                    found = True
            if not phone and not found:
                phone = self.is_phone(entry)
                if phone:
                    found = True
            if not email and not found:
                email = self.is_email(entry)
        contact = ContactInfo.ContactInfo(name, phone, email)
        contact.dumpInfo()
        return contact

    """ Function isName
        Input(s): an entry (string) from a business card string
        Output(s): a (string) if it is a name, else false (boolean).
        Runtime: > O(m), m = characters in entry. Takes long b/c of NLP machine learning
    """
    def is_name(self, entry):
        nlp = spacy.load("en_core_web_sm")
        doc = nlp(entry)
        for ent in doc.ents:
            if ent.label_ == 'PERSON':
                return entry
        return False

    """ Function isPhone
        Input(s): an entry (string) from a business card string
        Output(s): a (string) if it is a phone, else false (boolean).
        Runtime: O(2m) => O(m), m = characters in entry
    """
    def is_phone(self, entry):
        new_phone = ''
        if 'fax' in entry.lower():
            return False
        for char in entry:
            if char.isdigit():  # if we're looking at a number
                new_phone += char  # add it to the phone number
        if len(new_phone) == 10 or len(new_phone) == 11:
            return new_phone
        return False

    """ Function isEmail
        Input(s): an entry (string) from a business card string
        Output(s): a (string) if it is a email, else false (boolean).
        Runtime: O(2m) => O(m), m = characters in entry
    """
    def is_email(self, entry):
        words = entry.split(" ")
        for word in words:
            if '@' in word:
                return word
        return False


""" Function starter 
    * does the heavy lifting (I/O, calling methods)
    Input(s): n/a
    Output(s): a (dictionary) containing contacts with name (string) as key
    Runtime: O(n), n = number of business cards
"""
def starter():
    parser = BusinessCardParser()
    print("Welcome to the Business Card Parser!")
    print("You can input a file of business cards, divided by", DIVIDER, "by inputting the file name.")
    print("You can input a business card manually, line by line, by hitting ENTER")
    response = input("Input file name or hit ENTER to continue: ")
    contacts = {}
    if response == "":  # user wants to enter card manually
        business_card = ""
        while True:
            response = input("enter line (or 'END' to stop):")
            if response.upper() == "END":
                break
            else:
                business_card += (response + '\n')  # add new line to manual business card
        contact = parser.getContactInfo(business_card)
        contacts[contact.getName()] = contact
    else:  # we got a file (hopefully)
        cards_file = open(response, "r")
        all_lines = cards_file.readlines()
        business_card = ""
        for line in all_lines:
            if DIVIDER in line:
                contact = parser.getContactInfo(business_card)
                contacts[contact.getName()] = contact
                business_card = ""
            else:
                business_card += (line + '\n')
        contact = parser.getContactInfo(business_card)
        contacts[contact.getName()] = contact
        return contacts


def main():
    _contacts = starter()  # contains a dictionary of contacts for future use & dev


if __name__ == '__main__':
    main()

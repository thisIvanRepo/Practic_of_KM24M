"""
Validation Module

This module provides the `Validation` class, which includes methods for validating various types of user input,
such as phone numbers, email addresses, birthdays, names, addresses, note keys, and note tags. The class uses
regular expressions to match the input against predefined patterns.

Classes:
    - Validation: A class that provides methods for validating different types of input data.

Example usage:
    validator = Validation()
    if validator.validate_phone("+380123456789"):
        print("Valid phone number")
    else:
        print("Invalid phone number")
"""
import re


class Validation:
    PhonePattern = r"^\+?38[ _-]?\(?\d{3}\)?[ _-]?\d{3}[ _-]?\d{2}[ _-]?\d{2}$"
    EmailPattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    BirthdayPattern = r"^(0[1-9]|[12][0-9]|3[01])\.(0[1-9]|1[0-2])\.(19|20)\d{2}$"
    NamePattern = r"^[a-zA-Z-]+$"
    AddressPattern = r"^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d, ]+$"
    NotesKeyPattern = r"^[A-Za-z0-9_-]+$"
    NotesTagPattern = r"^[A-Za-z0-9_-]+$"

    def validate_phone(self, phone):
        match = re.match(self.PhonePattern, phone)
        if match:
            return True
        return False

    def validate_email(self, email):
        match = re.match(self.EmailPattern, email)
        if match:
            return True
        return False

    def validate_birthday(self, birthday):
        match = re.match(self.BirthdayPattern, birthday)
        if match:
            return True
        return False

    def validate_name(self, name):
        match = re.match(self.NamePattern, name)
        if match:
            return True
        return False

    def validate_address(self, address):
        match = re.match(self.AddressPattern, address)
        if match:
            return True
        return False

    def validate_key(self, key):
        match = re.match(self.NotesKeyPattern, key)
        if match:
            return True
        return False

    def validate_text(self, text):
        if len(text) > 0:
            return True
        return False

    def validate_tag(self, tag):
        match = re.match(self.NotesTagPattern, tag)
        if match:
            return True
        return False

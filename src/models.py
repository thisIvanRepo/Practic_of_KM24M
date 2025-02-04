"""
This module defines classes for managing notes and contact records.
It includes `Note` and `Record` classes to handle data, as well as
supporting field classes like `Field`, `NameField`, `PhoneField`,
`AddressField`, `EmailField`, and `BirthdayField`
"""


class Note:
    """
    A class representing a note, which includes a key, text, creation date, and tags.
    """

    def __init__(self, key, text, create_date):
        """
        Initialize the Note with a key, text, and creation date.

        :param key: The unique identifier for the note.
        :param text: The text content of the note.
        :param create_date: The date when the note was created.
        """
        self._key = key
        self._text = text
        self._create_date = create_date
        self._tags = []

    def __str__(self):
        """
        Return a string representation of the note, including key, text, creation date, and tags.

        :return: A string representing the note.
        """
        str = f"Key: {self._key}  Text: {
            self._text}  Created: {self._create_date}"
        if len(self._tags) > 0:
            str += f"\nTags: {','.join(self._tags)}"
        return str

    @property
    def key(self):
        """
        Get the key of the note.

        :return: The key of the note.
        """
        return self._key

    @key.setter
    def key(self, key):
        """
        Set a new key for the note.

        :param key: The new key for the note.
        """
        self._key = key

    @property
    def text(self):
        """
        Get the text of the note.

        :return: The text of the note.
        """
        return self._text

    @text.setter
    def text(self, text):
        """
        Set a new text for the note.

        :param text: The new text for the note.
        """
        self._text = text

    @property
    def tags(self):
        """
        Get the tags associated with the note.

        :return: A list of tags associated with the note.
        """
        return self._tags

    @tags.setter
    def tags(self, tags):
        """
        Set new tags for the note.

        :param tags: A list of new tags for the note.
        """
        self._tags = tags

    def add_tag(self, tag):
        """
        Add a tag to the note.

        :param tag: The tag to be added.
        """
        self._tags.append(tag)

    def remove_tag(self, tag):
        """
        Remove a tag from the note.

        :param tag: The tag to be removed.
        """
        for t in self._tags:
            if t == tag:
                self._tags.remove(t)

    def has_tag(self, tag):
        """
        Check if the note has a specific tag.

        :param tag: The tag to check for.
        :return: True if the tag is found, False otherwise.
        """
        for t in self._tags:
            if t == tag:
                return True
        return False


class Record:
    """
    A class representing a contact record, which includes a name, phone numbers, 
    email, address, and birthday.
    """

    def __init__(self, name: str):
        """
        Initialize the Record with a name and optional contact details.

        :param name: The name associated with the record.
        """
        self._name = NameField(name)
        self._phones = []
        self._email = None
        self._address = None
        self._birthday = None

    def __str__(self):
        """
        Return a string representation of the contact record.

        :return: A string representing the contact record.
        """
        str = ""

        if self._name:
            str += f"{self._name}\n"

        if self._phones:
            for phone in self._phones:
                str += f"{phone}\n"

        if self._email:
            str += f"{self._email}\n"

        if self._address:
            str += f"{self._address}\n"

        if self._birthday:
            str += f"{self._birthday}\n"

        return str.strip()

    @property
    def name(self):
        """
        Get the name of the contact record.

        :return: The name of the contact record.
        """
        return self._name

    @name.setter
    def name(self, name):
        """
        Set a new name for the contact record.

        :param name: The new name for the contact record.
        """
        self._name = NameField(name)

    @property
    def address(self):
        """
        Get the address of the contact record.

        :return: The address of the contact record.
        """
        return self._address

    @address.setter
    def address(self, address):
        """
        Set a new address for the contact record.

        :param address: The new address for the contact record.
        """
        self._address = AddressField(address)

    @property
    def email(self):
        """
        Get the email of the contact record.

        :return: The email of the contact record.
        """
        return self._email

    @email.setter
    def email(self, email):
        """
        Set a new email for the contact record.

        :param email: The new email for the contact record.
        """
        self._email = EmailField(email)

    @property
    def birthday(self):
        """
        Get the birthday of the contact record.

        :return: The birthday of the contact record.
        """
        return self._birthday

    @birthday.setter
    def birthday(self, birthday):
        """
        Set a new birthday for the contact record.

        :param birthday: The new birthday for the contact record.
        """
        self._birthday = BirthdayField(birthday)

    @property
    def phones(self):
        """
        Get the list of phone numbers associated with the contact record.

        :return: A list of phone numbers.
        """
        return self._phones

    @phones.setter
    def phones(self, value):
        """
        Set a new list of phone numbers for the contact record.

        :param value: A list of phone numbers.
        """
        self._phones = value

    def add_phone(self, phone):
        """
        Add a new phone number to the contact record.

        :param phone: The phone number to be added.
        """
        self._phones.append(PhoneField(phone))

    def remove_phone(self, phone):
        """
        Remove a phone number from the contact record.

        :param phone: The phone number to be removed.
        """
        for p in self._phones:
            if p.value == phone:
                self._phones.remove(p)

    def has_phone(self, phone):
        """
        Check if the contact record has a specific phone number.

        :param phone: The phone number to check for.
        :return: True if the phone number is found, False otherwise.
        """
        for p in self._phones:
            if p.value == phone:
                return True
        return False


class Field:
    """
    A base class representing a generic field with a name and value.
    """

    def __init__(self, name, value):
        """
        Initialize the Field with a name and value.

        :param name: The name of the field.
        :param value: The value of the field.
        """
        self.name = name
        self.value = value

    def __str__(self):
        """
        Return a string representation of the field.

        :return: A string representing the field.
        """
        return f"{self.name.capitalize()}: {self.value}"


class NameField(Field):
    """
    A class representing the name field in a contact record.
    """

    def __init__(self, value):
        """
        Initialize the NameField with a value.

        :param value: The name value.
        """
        super().__init__("name", value)


class PhoneField(Field):
    """
    A class representing the phone field in a contact record.
    """

    def __init__(self, value):
        """
        Initialize the PhoneField with a value.

        :param value: The phone number value.
        """
        super().__init__("phone", value)


class AddressField(Field):
    """
    A class representing the address field in a contact record.
    """

    def __init__(self, value):
        """
        Initialize the AddressField with a value.

        :param value: The address value.
        """
        super().__init__("address", value)


class EmailField(Field):
    """
    A class representing the email field in a contact record.
    """

    def __init__(self, value):
        """
        Initialize the EmailField with a value.

        :param value: The email address value.
        """
        super().__init__("email", value)


class BirthdayField(Field):
    """
    A class representing the birthday field in a contact record.
    """

    def __init__(self, value):
        """
        Initialize the BirthdayField with a value.

        :param value: The birthday value.
        """
        super().__init__("birthday", value)

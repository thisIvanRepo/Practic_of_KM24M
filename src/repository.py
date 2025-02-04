"""
This module provides classes for saving, updating, and managing records in files.
It includes `Saver`, `AddressBook`, and `NotesBook` classes for handling persistent
storage and retrieval of address book and note data.
"""

from collections import UserDict
import pickle
from datetime import datetime, timedelta
from models import Note
from constants import Messages


class Saver:
    """
    Class responsible for saving and loading data to and from a file using pickle.
    """

    def __init__(self, path):
        """
        Initialize the Saver with a file path.

        :param path: The path to the file where data will be saved and loaded.
        """
        self.__file_name = path

    def save(self, data):
        """
        Save the provided data to the file.

        :param data: The data to be saved.
        """
        with open(self.__file_name, "wb") as f:
            pickle.dump(data, f)

    def load(self) -> list:
        """
        Load and return the data from the file. If the file does not exist, return an empty list.

        :return: The loaded data or an empty list if the file does not exist.
        """
        try:
            with open(self.__file_name, "rb") as f:
                return pickle.load(f)
        except OSError:
            return {}


class AddressBook(UserDict):
    """
    A class that manages contact records in an address book and persists them using a Saver.
    """

    def __init__(self, saver: Saver):
        """
        Initialize the AddressBook with a Saver instance.

        :param saver: An instance of the Saver class for file operations.
        """
        self.__saver = saver
        self.data = self.__saver.load()

    def get_all(self):
        """
        Get all contact records.

        :return: A list of all contact records.
        """
        return list(self.data.values())

    def add_record(self, name, record):
        """
        Add a new contact record to the address book.

        :param name: The name associated with the record.
        :param record: The contact record to be added.
        """
        self.data[name] = record
        self.__saver.save(self.data)

    def update_record(self, name, record):
        """
        Update an existing contact record in the address book.

        :param name: The name associated with the record.
        :param record: The updated contact record.
        """
        self.data[name] = record
        self.__saver.save(self.data)

    def get_upcoming_birthday(self, days):
        """
        Get a list of contacts with upcoming birthdays within a given number of days.

        :param days: The number of days to check for upcoming birthdays.
        :return: A string listing contacts with upcoming birthdays or a message if none are found.
        """
        upcoming_birthdays = ""
        today = datetime.today().date()
        next_date = today + timedelta(days=int(days))

        for record in self.data.values():
            if record.birthday:
                birthday_in_datetime = datetime.strptime(
                    record.birthday.value, "%d.%m.%Y").date()
                birthday_this_year = birthday_in_datetime.replace(
                    year=today.year)
                if today <= birthday_this_year <= next_date:
                    if len(upcoming_birthdays) != 0:
                        upcoming_birthdays = upcoming_birthdays + '\n'
                    upcoming_birthdays = upcoming_birthdays + f"{record.name} {
                        Messages.UpcomingBirthdayMiddlePart} {birthday_this_year.strftime('%d.%m.%Y')}."

        if len(upcoming_birthdays) == 0:
            upcoming_birthdays = Messages.NoUpcomingBirthday

        return upcoming_birthdays

    def delete_record(self, name):
        """
        Delete a contact record from the address book.

        :param name: The name associated with the record to be deleted.
        """
        del self.data[name]
        self.__saver.save(self.data)

    def find_by_name(self, name):
        """
        Find and return a contact record by name.

        :param name: The name associated with the record.
        :return: The contact record, or None if not found.
        """
        return self.data.get(name)

    def find(self, field_name, value):
        """
        Find and return a contact record by a specific field value.

        :param field_name: The field to search by (e.g., 'phone').
        :param value: The value to search for.
        :return: The contact record, or None if not found.
        """
        for record in self.data.values():
            if field_name == "phone":
                if record.has_phone(value):
                    return record
            else:
                field = getattr(record, field_name, None)
                if field and field.value == value:
                    return record
        return None


class NotesBook(UserDict):
    """
    A class that manages notes and persists them using a Saver.
    """

    def __init__(self, saver: Saver):
        """
        Initialize the NotesBook with a Saver instance.

        :param saver: An instance of the Saver class for file operations.
        """
        self.__saver = saver
        self.data = self.__saver.load()

    def get_all(self):
        """
        Get all notes.

        :return: A list of all notes.
        """
        return list(self.data.values())

    def find_by_key(self, key) -> Note:
        """
        Find and return a note by its key.

        :param key: The key associated with the note.
        :return: The note, or None if not found.
        """
        return self.data.get(key)

    def find_by_tag(self, tag):
        """
        Find and return notes that contain a specific tag.

        :param tag: The tag to search for.
        :return: A list of notes containing the tag.
        """
        return [n for n in self.get_all() if tag in n.tags]

    def add(self, key, note: Note):
        """
        Add a new note to the NotesBook.

        :param key: The key associated with the note.
        :param note: The note to be added.
        """
        self.data[key] = note
        self.__saver.save(self.data)

    def update_note(self, key, note: Note):
        """
        Update an existing note in the NotesBook.

        :param key: The key associated with the note.
        :param note: The updated note.
        """
        self.data[key] = note
        self.__saver.save(self.data)

    def delete_note(self, key):
        """
        Delete a note from the NotesBook.

        :param key: The key associated with the note to be deleted.
        """
        del self.data[key]
        self.__saver.save(self.data)

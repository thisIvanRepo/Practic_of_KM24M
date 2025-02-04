"""
This module provides a simple command execution framework using a registry of
commands. Commands can be registered with the `register_command` decorator and
then executed through the `create_command_executor` functin.

Usage:
1. Define commands using the `@register_command('command_name')` decorator.
2. Create a command executor using `create_command_executor()`.
3. Call the executor with the command string and arguments to execute the
registered command.

Example:
    @register_command('add')
    def add_contact(name, phone):
        print(f"Adding contact: {name} with phone {phone}")

    @register_command('list')
    def list_contacts():
        print("Listing all contacts")

    command_executor = create_command_executor({})
    command_executor("add", "John", "+38098442123")
    command_executor("list")
"""
from datetime import datetime
from models import Note, Record
from constants import Messages, Paths
from repository import AddressBook, NotesBook, Saver
from validation import Validation

_command_registry = {}
_addressbook = AddressBook(Saver(Paths.addressbook_file))
_notesbook = NotesBook(Saver(Paths.notesbook_file))
_validator = Validation()


def create_command_executor():
    """
    Creates and returns a command executor function.
    """
    def run_command(command_str: str, *args):
        """Executes a command based on the command string."""
        command_func = _command_registry.get(command_str.lower())
        if command_func:
            return command_func(args)
        else:
            return Messages.InvalidCommand
    return run_command


def get_commands():
    """returns the list of the existing commands"""
    return list(_command_registry.keys())


def register_command(name):
    """
    Decorator to register a command function.
    """
    def decorator(func):
        # Register the function in the command_registry dictionary
        _command_registry[name.lower()] = func
        return func
    return decorator


def usage(usage):
    def input_error(func):
        """
        Decorator for handling input error
        """
        def inner(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except ValueError:
                return f"{Messages.WrongParameters}... {usage}"
        return inner
    return input_error

# Define commands using the decorator


@register_command('add_contact')
@usage(Messages.AddCommandUsage)
def add_contact(args):
    """
    Command to add a contact with the given name and phone number to a storage
    """
    name, phone, *_ = args
    email = args[2] if len(args) > 2 else None
    address = args[3] if len(args) > 3 else None
    birthday = args[4] if len(args) > 4 else None

    if not _validator.validate_name(name):
        return Messages.WrongNameValue
    if not _validator.validate_phone(phone):
        return Messages.WrongPhoneNumber
    record = _addressbook.find_by_name(name)
    if record is not None:
        return Messages.ContactAlreadyExists
    record = Record(name)
    record.add_phone(phone)
    _addressbook.add_record(name, record)
    if email and _validator.validate_email(email):
        record.email = email
        _addressbook.update_record(name, record)

    if address and _validator.validate_address(address):
        record.address = address
        _addressbook.update_record(name, record)

    if birthday and _validator.validate_birthday(birthday):
        record.birthday = birthday
        _addressbook.update_record(name, record)

    return Messages.ContactAdded


@register_command('add_phone')
@usage(Messages.AddPhoneUsage)
def add_phone(args):
    name, phone, *_ = args
    if not _validator.validate_phone(phone):
        return Messages.WrongPhoneNumber
    record = _addressbook.find_by_name(name)
    if record is None:
        return Messages.ContactDoesNotExist
    record.add_phone(phone)
    _addressbook.update_record(name, record)
    return Messages.PhoneAdded


@register_command('update_phone')
@usage(Messages.UpdatePhoneUsage)
def update_phone(args):
    name, old_phone, new_phone, *_ = args
    if not _validator.validate_phone(old_phone):
        return Messages.WrongPhoneNumber
    if not _validator.validate_phone(new_phone):
        return Messages.WrongPhoneNumber
    record = _addressbook.find_by_name(name)
    if record is None:
        return Messages.ContactDoesNotExist
    if not record.has_phone(old_phone):
        return Messages.GiveNameWithOldAndNewPhones
    record.remove_phone(old_phone)
    record.add_phone(new_phone)
    _addressbook.update_record(name, record)
    return Messages.ContactUpdated


@register_command('update_email')
@usage(Messages.UpdateEmailUsage)
def update_email(args):
    name, email, *_ = args
    if not _validator.validate_email(email):
        return Messages.EmailNotValid
    record = _addressbook.find_by_name(name)
    if record is None:
        return Messages.ContactDoesNotExist
    record.email = email
    _addressbook.update_record(name, record)
    return Messages.ContactUpdated


@register_command('update_address')
@usage(Messages.UpdateAddressUsage)
def update_address(args):
    name, address, *_ = args
    if not _validator.validate_address(address):
        return Messages.WrongAddress
    record = _addressbook.find_by_name(name)
    if record is None:
        return Messages.ContactDoesNotExist
    record.address = address
    _addressbook.update_record(name, record)
    return Messages.ContactUpdated


@register_command('update_birthday')
@usage(Messages.UpdateBirthdayUsage)
def update_birthday(args):
    name, date, *_ = args
    if not _validator.validate_birthday(date):
        return Messages.BirthdayNotValid
    record = _addressbook.find_by_name(name)
    if record:
        record.birthday = date
        _addressbook.update_record(name, record)
    return Messages.ContactUpdated


@register_command('show_birthday')
@usage(Messages.ShowBirthdayUsage)
def show_birthday(args):
    name, *_ = args
    record = _addressbook.find_by_name(name)
    if record and record.birthday:
        return record.birthday
    return Messages.BirthdayNotSet


@register_command('show_upcoming_birthday')
def show_upcoming_birthday(args):
    days, *_ = args or [7]
    return _addressbook.get_upcoming_birthday(days)


@register_command('list_addressbook')
def list_contacts(args):
    """
    Command to list all contacts.
    """
    contacts_string = "\n".join([str(record)
                                for record in _addressbook.get_all()])

    if not contacts_string:
        return Messages.ContactListEmpty

    return contacts_string


@register_command('delete')
@usage(Messages.DeleteUsage)
def delete_contact(args):
    """
    The command to delete a contact by name
    """
    name, *_ = args
    record = _addressbook.find_by_name(name)
    if record is None:
        return Messages.ContactDoesNotExist

    _addressbook.delete_record(name)
    return Messages.ContactDeleted


@register_command('find_contact')
@usage(Messages.FindUsage)
def find_contact(args):
    """
    The command to find a contact by name, phone, email or birthday
    """
    value, *_ = args
    record = _addressbook.find_by_name(value)
    if record is not None:
        return record

    if _validator.validate_phone(value):
        record = _addressbook.find("phone", value)

    if _validator.validate_email(value):
        record = _addressbook.find("email", value)

    if _validator.validate_birthday(value):
        record = _addressbook.find("birthday", value)

    return str(record) if record is not None else Messages.ContactDoesNotExist


@register_command("add_note")
@usage(Messages.AddNoteUsage)
def add_note(args):
    key, *text_args = args
    text = ' '.join(text_args)
    if not _validator.validate_key(key):
        return Messages.WrongKey
    if not _validator.validate_text(text):
        return Messages.WrongText
    note = _notesbook.find_by_key(key)
    if note is not None:
        return Messages.NoteWithThisKeyAlreadyExists
    note = Note(key, text, datetime.now())
    _notesbook.add(key, note)
    return Messages.NoteAdded


@register_command("list_notesbook")
def list_notesbook(args):
    notes_string = "\n".join([str(note)
                              for note in _notesbook.get_all()])

    if not notes_string:
        return Messages.NotesListEmpty

    return notes_string


@register_command("delete_note")
@usage(Messages.DeleteNoteUsage)
def delete_note(args):
    key, *_ = args
    note = _notesbook.find_by_key(key)
    if note is None:
        return Messages.NoteWithThisKeyNotExists
    _notesbook.delete_note(key)
    return Messages.NoteDeleted


@register_command("update_note")
@usage(Messages.UpdateNoteUsage)
def update_note(args):
    key, *text_args = args
    text = ' '.join(text_args)
    if not _validator.validate_key(key):
        return Messages.WrongKey
    if not _validator.validate_text(text):
        return Messages.WrongText
    note = _notesbook.find_by_key(key)
    if note is None:
        return Messages.NoteWithThisKeyNotExists
    note.text = text
    _notesbook.update_note(key, note)
    return Messages.NoteUpdated


@register_command("add_tag")
@usage(Messages.AddTagUsage)
def add_tag(args):
    key, tag, *_ = args
    if not _validator.validate_tag(tag):
        return Messages.WrongTag
    note = _notesbook.find_by_key(key)
    if note is None:
        return Messages.NoteWithThisKeyNotExists
    if note.has_tag(tag):
        return Messages.TagAlreadyExists
    note.add_tag(tag)
    _notesbook.update_note(key, note)
    return Messages.TagAdded


@register_command("delete_tag")
@usage(Messages.DeleteTagUsage)
def delete_tag(args):
    key, tag, *_ = args
    note = _notesbook.find_by_key(key)
    if note is None:
        return Messages.NoteWithThisKeyNotExists
    if not note.has_tag(tag):
        return Messages.TagDoesNotExist
    note.remove_tag(tag)
    _notesbook.update_note(key, note)
    return Messages.TagDeleted


@register_command("find_note_by_tag")
@usage(Messages.FindNoteByTagUsage)
def find_note_by_tag(args):
    tag, *_ = args
    if not _validator.validate_tag(tag):
        return Messages.WrongTag
    notes_by_tag = [str(n) for n in _notesbook.get_all() if n.has_tag(tag)]
    notes_by_tag_str = '\n'.join(notes_by_tag)
    if not notes_by_tag_str:
        return Messages.NotesListEmpty

    return notes_by_tag_str


@register_command("find_in_notes_text")
@usage(Messages.FindInNotesTextUsage)
def find_in_notes_text(args):
    text, *_ = args
    if not _validator.validate_text(text):
        return Messages.WrongText
    notes_by_text = [str(n) for n in _notesbook.get_all() if (
        text.lower() in n.text.lower())]
    notes_by_text_str = '\n'.join(notes_by_text)
    if not notes_by_text_str:
        return Messages.NotesListEmpty

    return notes_by_text_str

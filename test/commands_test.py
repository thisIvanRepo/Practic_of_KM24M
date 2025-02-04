"""test suit for commands"""
# flake8: noqa
import conftest
from datetime import datetime
import unittest
from unittest.mock import MagicMock
import command_registry as command_service
from constants import Messages, Paths
from repository import AddressBook, NotesBook, Saver
from models import Note


class TestCommand(unittest.TestCase):

    def setUp(self):
        self.saver = Saver(Paths.addressbook_file)
        self.saver.load = MagicMock(return_value={})
        self.saver.save = MagicMock()
        command_service._addressbook = AddressBook(self.saver)
        command_service._notesbook = NotesBook(self.saver)
        self.command_executor = command_service.create_command_executor()

    def test_non_existing_command(self):
        result = self.command_executor("noneExistingCommand")
        self.assertEqual(
            result, Messages.InvalidCommand)

    def test_add_command_with_no_enough_args(self):
        result = self.command_executor("add_contact")
        self.assertIn(
            Messages.AddCommandUsage, result)

    def test_add_commands_with_all_args(self):
        result = self.command_executor("add_contact", "John", "+380981171922", "john@example.com", "23 Main St",
                                       "01.01.2000")
        self.assertEqual(result, Messages.ContactAdded)

    def test_add_command_with_wrong_number(self):
        result = self.command_executor("add_contact", "John", "12422424")
        self.assertEqual(
            result, Messages.WrongPhoneNumber)

    def test_add_command_with_name_and_correct_number(self):
        result = self.command_executor("add_contact", "John", "+380981171922")
        self.assertEqual(result, Messages.ContactAdded)

    def test_add_command_when_contact_already_existing(self):
        self.command_executor("add_contact", "John", "+380981171922")
        result = self.command_executor("add_contact", "John", "+380981171922")
        self.assertEqual(result, Messages.ContactAlreadyExists)

    def test_add_command_when_name_is_wrong(self):
        result = self.command_executor("add_contact", "1111", "+380981171922")
        self.assertEqual(result, Messages.WrongNameValue)

    def test_add_phone_to_existing_contact(self):
        self.command_executor("add_contact", "John", "+380981171922")
        result = self.command_executor("add_phone", "John", "+380987654321")
        self.assertEqual(result, Messages.PhoneAdded)

    def test_add_phone_when_phone_is_wrong(self):
        result = self.command_executor(
            "add_phone", "John", "+3809876543211222")
        self.assertEqual(result, Messages.WrongPhoneNumber)

    def test_add_phone_to_non_existing_contact(self):
        result = self.command_executor("add_phone", "John", "+380987654321")
        self.assertEqual(result, Messages.ContactDoesNotExist)

    def test_update_phone_with_wrong_old_number(self):
        self.command_executor("add_contact", "John", "+380981171922")
        result = self.command_executor(
            "update_phone", "John", "+38098117192234", "+380987654321")
        self.assertEqual(result, Messages.WrongPhoneNumber)

    def test_update_phone_with_wrong_new_number(self):
        self.command_executor("add_contact", "John", "+380981171922")
        result = self.command_executor(
            "update_phone", "John", "+380981171922", "+38098765432122")
        self.assertEqual(result, Messages.WrongPhoneNumber)

    def test_update_phone_when_contact_does_not_exist(self):
        result = self.command_executor(
            "update_phone", "John", "+380981171922", "+380987654321")
        self.assertEqual(result, Messages.ContactDoesNotExist)

    def test_update_phone_in_existing_contact(self):
        self.command_executor("add_contact", "John", "+380981171922")
        result = self.command_executor(
            "update_phone", "John", "+380981171922", "+380987654321")
        self.assertEqual(result, Messages.ContactUpdated)

    def test_update_phone_when_old_phone_does_not_exist(self):
        self.command_executor("add_contact", "John", "+380981171922")
        result = self.command_executor(
            "update_phone", "John", "+380000000000", "+380987654321")
        self.assertEqual(result, Messages.GiveNameWithOldAndNewPhones)

    def test_update_email_in_existing_contact(self):
        self.command_executor("add_contact", "John", "+380981171922")
        result = self.command_executor(
            "update_email", "John", "john@example.com")
        self.assertEqual(result, Messages.ContactUpdated)

    def test_update_email_when_email_is_wrong(self):
        self.command_executor("add_contact", "John", "+380981171922")
        result = self.command_executor(
            "update_email", "John", "johnexample.com")
        self.assertEqual(result, Messages.EmailNotValid)

    def test_update_email_when_contact_does_not_exist(self):
        result = self.command_executor(
            "update_email", "John", "johne@xample.com")
        self.assertEqual(result, Messages.ContactDoesNotExist)

    def test_update_address_in_existing_contact(self):
        self.command_executor("add_contact", "John", "+380981171922")
        result = self.command_executor("update_address", "John", "123 Main St")
        self.assertEqual(result, Messages.ContactUpdated)

    def test_update_address_when_address_is_wrong(self):
        self.command_executor("add_contact", "John", "+380981171922")
        result = self.command_executor("update_address", "John", "122")
        self.assertEqual(result, Messages.WrongAddress)

    def test_update_address_contact_does_not_exist(self):
        result = self.command_executor("update_address", "John", "123 Main St")
        self.assertEqual(result, Messages.ContactDoesNotExist)

    def test_update_birthday_when_birthday_is_wrong(self):
        self.command_executor("add_contact", "John", "+380981171922")
        result = self.command_executor("update_birthday", "John", "01.27.2000")
        self.assertEqual(result, Messages.BirthdayNotValid)

    def test_update_birthday_in_existing_contact(self):
        self.command_executor("add_contact", "John", "+380981171922")
        result = self.command_executor("update_birthday", "John", "01.01.2000")
        self.assertEqual(result, Messages.ContactUpdated)

    def test_show_birthday_for_contact(self):
        self.command_executor("add_contact", "John", "+380981171922")
        self.command_executor("update_birthday", "John", "01.01.2000")
        result = self.command_executor("show_birthday", "John")
        self.assertEqual(result.value, "01.01.2000")

    def test_show_birthday_for_contact_with_no_birthday(self):
        self.command_executor("add_contact", "John", "+380981171922")
        result = self.command_executor("show_birthday", "John")
        self.assertEqual(result, Messages.BirthdayNotSet)

    def test_show_upcoming_birthday(self):
        self.command_executor("add_contact", "John", "+380981171922")
        self.command_executor("update_birthday", "John",
                              datetime.today().strftime("%d.%m.%Y"))
        result = self.command_executor("show_upcoming_birthday", "7")
        self.assertIn(Messages.UpcomingBirthdayMiddlePart, result)

    def test_delete_contact(self):
        self.command_executor("add_contact", "John", "+380981171922")
        result = self.command_executor("delete", "John")
        self.assertEqual(result, Messages.ContactDeleted)

    def test_delete_when_contact_does_not_exist(self):
        result = self.command_executor("delete", "John")
        self.assertEqual(result, Messages.ContactDoesNotExist)

    def test_find_contact_by_name(self):
        self.command_executor("add_contact", "John", "+380981171922")
        result = self.command_executor("find_contact", "John")
        self.assertIn("John", str(result))

    def test_find_contact_by_phone(self):
        self.command_executor("add_contact", "John", "+380981171922")
        result = self.command_executor("find_contact", "+380981171922")
        self.assertIn("John", str(result))

    def test_find_contact_by_email(self):
        self.command_executor("add_contact", "John", "+380981171922")
        self.command_executor("update_email", "John", "john@example.com")
        result = self.command_executor("find_contact", "john@example.com")
        self.assertIn("John", str(result))

    def test_find_contact_by_birthday(self):
        self.command_executor("add_contact", "John", "+380981171922")
        self.command_executor("update_birthday", "John", "01.01.2000")
        result = self.command_executor("find_contact", "01.01.2000")
        self.assertIn("John", str(result))

    def test_find_contact_by_non_existent_name(self):
        result = self.command_executor("find_contact", "NonExistentName")
        self.assertEqual(result, Messages.ContactDoesNotExist)

    def test_list_when_there_are_no_contacts(self):
        self.command_executor("add_contact", "John", "+380981171922")
        result = self.command_executor("list_addressbook")
        self.assertIn("John", str(result))

    def test_list_is_not_empty_when_contacts_exist(self):
        result = self.command_executor("list_addressbook")
        self.assertEqual(result, Messages.ContactListEmpty)

    def test_get_commands_is_not_empty(self):
        self.assertNotEqual(len(command_service.get_commands()), 0)

    def test_add_note_with_empty_key(self):
        result = self.command_executor("add_note", "")
        self.assertEqual(result, Messages.WrongKey)

    def test_add_note_with_empty_text(self):
        result = self.command_executor("add_note", "key", "")
        self.assertEqual(result, Messages.WrongText)

    def test_add_node_with_existing_key(self):
        result = self.command_executor("add_note", "key", "text")
        result = self.command_executor("add_note", "key", "text2")
        self.assertEqual(result, Messages.NoteWithThisKeyAlreadyExists)

    def test_add_note_successfully(self):
        result = self.command_executor("add_note", "valid_key", "Some text")
        self.assertEqual(result, Messages.NoteAdded)
        note = command_service._notesbook.find_by_key("valid_key")
        self.assertIsNotNone(note)
        self.assertEqual(note.text, "Some text")

    def test_add_note_with_existing_key(self):
        command_service._notesbook.add("existing_key", Note(
            "existing_key", "Existing text", datetime.now()))
        result = self.command_executor("add_note", "existing_key", "New text")
        self.assertEqual(result, Messages.NoteWithThisKeyAlreadyExists)

    def test_list_notesbook_empty(self):
        self.command_executor("add_note", "key", "text")
        result = self.command_executor("list_notesbook")
        self.assertIn("Key: key  Text: text", result)

    def test_list_notesbook(self):
        command_service._notesbook.get_all = MagicMock(return_value=[])
        result = self.command_executor("list_notesbook")
        self.assertEqual(result, Messages.NotesListEmpty)

    def test_delete_note_with_nonexistent_key(self):
        command_service._notesbook.find_by_key = MagicMock(return_value=None)
        result = self.command_executor("delete_note", "nonexistent_key")
        self.assertEqual(result, Messages.NoteWithThisKeyNotExists)

    def test_delete_note_successfully(self):
        self.command_executor("add_note", "key", "Some text")
        result = self.command_executor("delete_note", "key")
        self.assertEqual(result, Messages.NoteDeleted)

    def test_update_note_with_invalid_key(self):
        result = self.command_executor("update_note", "@@@@", "Updated text")
        self.assertEqual(result, Messages.WrongKey)

    def test_update_note_with_invalid_text(self):
        result = self.command_executor("update_note", "valid_key", "")
        self.assertEqual(result, Messages.WrongText)

    def test_update_note_with_nonexisting_key(self):
        result = self.command_executor(
            "update_note", "valid_key", "updated text")
        self.assertEqual(result, Messages.NoteWithThisKeyNotExists)

    def test_update_note_successfully(self):
        existing_note = Note("valid_key", "Old text", datetime.now())
        command_service._notesbook.find_by_key = MagicMock(
            return_value=existing_note)
        result = self.command_executor(
            "update_note", "valid_key", "Updated text")
        self.assertEqual(result, Messages.NoteUpdated)
        updated_note = command_service._notesbook.find_by_key("valid_key")
        self.assertEqual(updated_note.text, "Updated text")

    def test_add_tag_with_invalid_tag(self):
        result = self.command_executor("add_tag", "key", "@@@")
        self.assertEqual(result, Messages.WrongTag)

    def test_add_tag_successfully(self):
        existing_note = Note("key", "Text", datetime.now())
        command_service._notesbook.find_by_key = MagicMock(
            return_value=existing_note)
        result = self.command_executor("add_tag", "key", "new_tag")
        self.assertEqual(result, Messages.TagAdded)
        self.assertTrue(existing_note.has_tag("new_tag"))

    def test_add_tag_to_nonexisting_note(self):
        result = self.command_executor("add_tag", "key", "tag_to_delete")
        self.assertEqual(result, Messages.NoteWithThisKeyNotExists)

    def test_add_tag_to_existing_tag(self):
        existing_note = Note("key", "Text", datetime.now())
        existing_note.add_tag("existing_tag")
        command_service._notesbook.find_by_key = MagicMock(
            return_value=existing_note)
        result = self.command_executor("add_tag", "key", "existing_tag")
        self.assertEqual(result, Messages.TagAlreadyExists)

    def test_delete_tag_with_nonexistent_tag(self):
        self.command_executor("add_note", "key", "text")
        result = self.command_executor("delete_tag", "key", "tag_to_delete")
        self.assertEqual(result, Messages.TagDoesNotExist)

    def test_delete_tag_with_nonexistent_note(self):
        result = self.command_executor("delete_tag", "key", "nonexistent_tag")
        self.assertEqual(result, Messages.NoteWithThisKeyNotExists)

    def test_delete_tag_successfully(self):
        self.command_executor("add_note", "key", "Text")
        self.command_executor("add_tag", "key", "tag_to_delete")
        result = self.command_executor("delete_tag", "key", "tag_to_delete")
        self.assertEqual(result, Messages.TagDeleted)

    def test_find_note_by_tag(self):
        self.command_executor("add_note", "key", "Text")
        self.command_executor("add_tag", "key", "keyTag")
        result = self.command_executor("find_note_by_tag", "keyTag")
        self.assertIn("Key: key  Text: Text", result)

    def test_find_note_by_tag_with_invalid_tag(self):
        result = self.command_executor("find_note_by_tag", "@@@@")
        self.assertEqual(result, Messages.WrongTag)

    def test_find_note_by_tag_no_notes(self):
        command_service._notesbook.get_all = MagicMock(return_value=[])
        result = self.command_executor("find_note_by_tag", "some_tag")
        self.assertEqual(result, Messages.NotesListEmpty)

    def test_find_in_notes_text_with_invalid_text(self):
        self.command_executor("add_note", "key", "text")
        result = self.command_executor("find_in_notes_text", "")
        self.assertEqual(result, Messages.WrongText)

    def test_find_in_notes_text_with_empty_notes(self):
        result = self.command_executor("find_in_notes_text", "text")
        self.assertEqual(result, Messages.NotesListEmpty)

    def test_find_in_notes_text(self):
        self.command_executor("add_note", "key", "text")
        result = self.command_executor("find_in_notes_text", "text")
        self.assertIn("Key: key  Text: text  Created:", result)


if __name__ == '__main__':
    unittest.main()

# fields with all available commands to keep them all in one place
import os
from pathlib import Path
from colorama import Fore, Style, init

# Colorama initialize (normalize the operation of the colorama module)
init(autoreset=True)


class Messages:
    Welcome = f"{Fore.GREEN}{
        Style.BRIGHT}Welcome to the assistant bot!{Style.RESET_ALL}"
    EnterACommand = "Enter a command: "
    HowCanIHelpYou = f"{Fore.GREEN}How can I help you?{Style.RESET_ALL}"
    InvalidCommand = f"{Fore.RED}{
        Style.BRIGHT}Invalid command.{Style.RESET_ALL}"
    AddCommandUsage = f"{
        Fore.YELLOW}Usage: add_command [NAME] [PHONE] [EMAIL*] [ADDRESS*] [BIRTHDAY*]{Style.RESET_ALL}"
    AddPhoneUsage = f"{Fore.YELLOW}Usage: add_phone [NAME] [PHONE]{
        Style.RESET_ALL}"
    UpdatePhoneUsage = f"{
        Fore.YELLOW}Usage: update_phone [NAME] [OLD_PHONE] [NEW_PHONE]{Style.RESET_ALL}"
    UpdateEmailUsage = f"{
        Fore.YELLOW}Usage: update_email [NAME] [EMAIL]{Style.RESET_ALL}"
    UpdateAddressUsage = f"{
        Fore.YELLOW}Usage: update_address [NAME] [ADDRESS]{Style.RESET_ALL}"
    UpdateBirthdayUsage = f"{
        Fore.YELLOW}Usage: update_birthday [NAME] [BIRTHDAY]{Style.RESET_ALL}"
    ShowBirthdayUsage = f"{
        Fore.YELLOW}Usage: show_birthday [NAME]{Style.RESET_ALL}"
    DeleteUsage = f"{Fore.YELLOW}Usage: delete [NAME]{Style.RESET_ALL}"
    FindUsage = f"{Fore.YELLOW}Usage: find_contact [NAME or PHONE or EMAIL or BIRTHDAY]{
        Style.RESET_ALL}"
    AddNoteUsage = f"{Fore.YELLOW}Usage: add_note [KEY] [TEXT]{
        Style.RESET_ALL}"
    DeleteNoteUsage = f"{Fore.YELLOW}Usage: delete_note [KEY]{Style.RESET_ALL}"
    UpdateNoteUsage = f"{
        Fore.YELLOW}Usage: update_note [KEY] [TEXT]{Style.RESET_ALL}"
    AddTagUsage = f"{Fore.YELLOW}Usage: add_tag [KEY] [TEXT]{Style.RESET_ALL}"
    DeleteTagUsage = f"{Fore.YELLOW}Usage: delete_tag [KEY_NOTE] [KEY_TAG]{
        Style.RESET_ALL}"
    FindNoteByTagUsage = f"{
        Fore.YELLOW}Usage: find_note_by_tag [KEY_TAG]{Style.RESET_ALL}"
    FindInNotesTextUsage = f"{
        Fore.YELLOW}Usage: find_in_notes_text [TEXT]{Style.RESET_ALL}"
    WrongParameters = f"{Fore.RED}Wrong parameters{Style.RESET_ALL}"
    WrongPhoneNumber = f"{
        Fore.RED}Wrong phone number. Must be 12 numbers starting with 38{Style.RESET_ALL}"
    WrongAddress = f"{Fore.RED}Wrong address. Only allowed letters, numbers, comas and spaces{
        Style.RESET_ALL}"
    WrongBirthdayValue = f"{
        Fore.RED}Wrong birthday value, should be DD.MM.YYYY{Style.RESET_ALL}"
    WrongNameValue = f"{
        Fore.RED}Wrong name value. Should contain only letters and hyphens.{Style.RESET_ALL}"
    ContactDoesNotHaveBirthdayValue = f"{
        Fore.YELLOW}Contact does not have birthday value{Style.RESET_ALL}"
    EnterUserName = f"{Fore.CYAN}Enter user name{Style.RESET_ALL}"
    GiveNameAndPhone = f"{
        Fore.CYAN}Give me name and phone please.{Style.RESET_ALL}"
    GiveNameWithOldAndNewPhones = f"{
        Fore.CYAN}Give me name with old and new phones please.{Style.RESET_ALL}"
    ContactAlreadyExists = f"{Fore.RED}Contact already exists{Style.RESET_ALL}"
    ContactDoesNotExist = f"{Fore.RED}Contact does not exist{Style.RESET_ALL}"
    ContactUpdated = f"{Fore.GREEN}{
        Style.BRIGHT}Contact updated.{Style.RESET_ALL}"
    ContactAdded = f"{Fore.GREEN}{Style.BRIGHT}Contact added.{Style.RESET_ALL}"
    PhoneAdded = f"{Fore.GREEN}{Style.BRIGHT}Phone added.{Style.RESET_ALL}"
    PhoneAlreadyExists = f"{Fore.YELLOW}Phone already exists.{Style.RESET_ALL}"
    ContactDeleted = f"{Fore.GREEN}{
        Style.BRIGHT}Contact deleted.{Style.RESET_ALL}"
    BirthdayAdded = f"{Fore.GREEN}{
        Style.BRIGHT}Birthday added.{Style.RESET_ALL}"
    GoodBye = f"{Fore.GREEN}{Style.BRIGHT}Good bye!{Style.RESET_ALL}"
    PhoneNotValid = f"{Fore.RED}Invalid phone number format{Style.RESET_ALL}"
    EmailNotValid = f"{Fore.RED}Invalid email format{Style.RESET_ALL}"
    BirthdayNotValid = f"{
        Fore.RED}Invalid date format. Use DD.MM.YYYY{Style.RESET_ALL}"
    ContactListEmpty = f"{Fore.YELLOW}Contact list is empty{Style.RESET_ALL}"
    NotesListEmpty = f"{Fore.YELLOW}Notes list is empty{Style.RESET_ALL}"
    BirthdayNotSet = f"{Fore.YELLOW}Birthday not set.{Style.RESET_ALL}"
    UpcomingBirthdayMiddlePart = f"{
        Fore.CYAN}has an upcoming birthday on{Style.RESET_ALL}"
    NoUpcomingBirthday = f"{
        Fore.YELLOW}You have no contacts with upcoming birthday{Style.RESET_ALL}"
    NoteAdded = f"{Fore.GREEN}{
        Style.BRIGHT}Note is successfully added{Style.RESET_ALL}"
    NoteUpdated = f"{Fore.GREEN}{
        Style.BRIGHT}Note is successfully updated{Style.RESET_ALL}"
    NoteDeleted = f"{Fore.GREEN}{
        Style.BRIGHT}Note is successfully deleted{Style.RESET_ALL}"
    NoteWithThisKeyNotExists = f"{
        Fore.RED}Note with this key does not exist. Please provide correct key{Style.RESET_ALL}"
    NoteWithThisKeyAlreadyExists = f"{
        Fore.RED}Note with this key already exists. Please provide unique key{Style.RESET_ALL}"
    ProvideKeyAndText = f"{
        Fore.CYAN}To add a note please provide a unique key and text of the note{Style.RESET_ALL}"
    TagAlreadyExists = f"{
        Fore.YELLOW}This tag already exists at this note{Style.RESET_ALL}"
    TagDoesNotExist = f"{
        Fore.YELLOW}This tag does not exist at this note{Style.RESET_ALL}"
    TagAdded = f"{Fore.GREEN}{Style.BRIGHT}Tag added{Style.RESET_ALL}"
    TagDeleted = f"{Fore.GREEN}{Style.BRIGHT}Tag deleted{Style.RESET_ALL}"
    WrongKey = f"{Fore.RED}Wrong key for note. Should be on alphanumeric value{
        Style.RESET_ALL}"
    WrongText = f"{Fore.RED}You can't add empty note{Style.RESET_ALL}"
    WrongTag = f"{Fore.RED}Wrong tag for note. Should be on alphanumeric value{
        Style.RESET_ALL}"
    NoCommandEntered = f"{
        Fore.CYAN}No command entered. Press 'Tab' to view the list of available commands{Style.RESET_ALL}"


class Paths:
    addressbook_file = str(Path.home()) + os.sep + "addressbook.pkl"
    notesbook_file = str(Path.home()) + os.sep + "notesbook.pkl"

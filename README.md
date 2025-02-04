# Assistant from Team-08

## Installable Package

### Build
In the root directory of the project, run the following command to build the package.
This will create a dist directory with the package.
```bash
python3 -m build
```

### Install (without push to PyPI)
To install the package, run the following command in the root directory of the project.
This will install the package from the dist directory to site-packages.
```bash
pip install --find-links ./dist assistant_team_08
```
### Features
**Add Contacts**:
  Add new contacts with name, phone number, email, and birthday.
**Find Contacts**:
  Search for contacts by name, phone number, email, or birthday. Supports partial matching.
**Edit Contacts**:
  Update existing contact details.
**Delete Contacts**:
  Remove contacts from the contact book.
**List All Contacts**:
  Display all contacts in the contact book.
**Birthday Reminders**:
  List upcoming birthdays within a specified number of days.

### Run
Get the bin directory path first, usually package install executable in same directory as python executable.
```bash
which python3 | sed 's/\/bin\/python3/\/bin/'`
```
Then run the assistant
```bash
$PATH_TO_EXECUTABLE/assistant_team_08
```

### Use the following commands within the program:
*Add a contact:*
```bash
add <name> <phone_number> <email> <birthday>
```
*Find contact:*
```bash
find <name|phone|email|birthday>
```
*Change a contact's phone number:*
```bash
change <name> <old_phone_number> <new_phone_number>
```
*Show all contacts:*
```bash
all
```
*Add a birthday to a contact:*
```bash
add-birthday <name> <DD.MM.YYYY>
```
*Show a contact's birthday:*
```bash
show-birthday <name>
```
*List upcoming birthdays:*
```bash
birthdays
```
*Exit the program:*
```bash
exit
```

### How It Works
- The program uses a command-line interface to interact with a contact book.
- Each command corresponds to a specific function, such as adding a new contact, finding contacts by name, phone number, email, or birthday, and displaying all contacts.
- The contact book is persisted between sessions using serialization. When the program is started, it loads the contact book from a file, and when the program is closed, it saves the contact book back to the file.


### Uninstall
```bash
pip uninstall assistant_team_08
```
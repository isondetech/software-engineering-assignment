# software-engineering-assignment

The Event Listing Web Application is designed to assist any organisation in efficiently managing and showcasing events.
To view and manage events, you'll need to be registered and logged in. Attempting to access login required pages when not logged in will result in being redirected to the login page.

### Admin Login Details

- Username: User001
- Password: 123

### Note

Where ever visible, these containers can be scrolled up or down to reveal hidden events.

<img src="https://github.com/isondetech/software-engineering-assignment/assets/111745965/8b59a530-da61-49cf-b1d9-0fd266fe8fae" width="350">

# Manual

## Navigating To Dashboard

You can navigate to the dashboard via the landing page (home page).

<img src="https://github.com/isondetech/software-engineering-assignment/assets/111745965/e34bf7c4-b9a9-43f9-b3bb-f4429ca14b7c" width="350">

A dashboard hyperlink will be within the landing page, clicking it will redirect you to the dashboard page

<img src="https://github.com/isondetech/software-engineering-assignment/assets/111745965/5d803141-1147-43a8-9075-5ebc5acd8f57" width="350">

## Adding An Event

- Navigate to the Dashboard > Click Add > Input Date > Input Title > Click Add
- Click cancel to go back to the Dashboard

## Updating An Event

- Navigate to the Dashboard > Locate An Event > Click The Paper Icon Next To The Event > Make Your ammendments > Click Yes
- Click cancel to go back to the Dashboard

## Deleting An Event

You'll have to be an admin user to perform deletes. You'll know you're an admin user if next to your username you have "Admin" like so:

<img src="https://github.com/isondetech/software-engineering-assignment/assets/111745965/aeed12ef-6f50-4645-ab17-dc5604a82c69" width="350">

- Navigate to the Dashboard > Locate An Event > Click The Bin Icon Next To The Event > Click Yes
- Click cancel to go back to the Dashboard

# Very Important Notice

Heroku clears changes made to the SQLite database at least once in a day. 

### Heroku on this

> SQLite runs in memory, and backs up its data store in files on disk. While this strategy works well for development, Heroku’s Cedar stack has an ephemeral filesystem. You can write to it, and you can read from it, but the contents will be cleared periodically. If you were to use SQLite on Heroku, you would lose your entire database at least once every 24 hours.

Therefore, this not a defect of the application, data can be modified, added and deleted from the SQLite database, but Heroku wipes this data at least once a day, this is just how Heroku operates.






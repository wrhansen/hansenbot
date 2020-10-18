# HansenBot

This is just a simple bot I created to use with my family's chat room on
GroupMe.


## Commands

I created a simple command invocation scheme to get the bot to react to messages.

### `help` command

It is invoked in the following way:

`!hb help`

This command lists out all of the available commands that can be invoked.

### `birthday` command

It is invoked in the following way:

`!hb birthday`

This command prints out a list of everyone's birthday in the family. This also
gives their current age and also says which person has the next closest birthday,
and how many days away that birthday is.

*NOTE*: This command requires setting up a database and logging into the included
admin so that you can set birthdays.

### `dadjoke` command

It is invoked in the following way:

`!hb dadjoke`

This command retrieves a dad joke at random from the https://icanhazdadjoke.com
api and returns it to the group.

### `weather` command

Invoked in the following way:

`!hb weather`

This command retrieves current weather from openweathermap API for some locations
setup in the database. This `Weather` location database can be setup in the
admin portal.

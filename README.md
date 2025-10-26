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

Update: openweathermap data sucks. It always seems to be off by 5-10 degrees F.
So I'm trying out weatherapi.com for now. So far I think it looks fine.

### `ai` command

Invoked in the following way:

`!hb ai <prompt>`

This command uses the OpenAI *completion* api to respond to whatever the user
enters in the `<prompt>`.

## Run tests (locally)

To run tests locally, just run the following command:

```bash
$ ./manage.py test --settings=website.local_settings
```

NOTE: the `website.local_settings` option is necessary for running the tests
in the right environment.


## AWS ElasticBeanstalk notes

From project root on local machine:
`eb ssh hansenbot-env`

Change to the current app directory
`cd /var/app/current/`

Activate the virtual env
`source $(find /var/app/venv/*/bin/activate)`

Load your environment variables
`export $(sudo cat /opt/elasticbeanstalk/deployment/env | xargs)`

Now you can run management commands
`python manage.py shell`

**NOTE**: Now that the github action is all set up all you have to do is push
your changes to master and a new build will automatically deploy to github. Neat!

## Useful Links

* GroupMe Developer Bots portal: https://dev.groupme.com/bots
* Github Action used: https://github.com/einaregilsson/beanstalk-deploy

## Need to update the platform because it's been retired on AWS?

Try using `eb config` command from cli. It will download a temp config file in an
terminal editor that you can edit. Change the platform and any other thing you
wanted to upgrade and then save and exit the editor. It will automatically kick
off elastic beanstalk to update the platform.

It might take several minutes (30 minutes to an hour even), but eventually it
does upgrade the platform.

# Changelog

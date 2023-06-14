# Billiken Bot

Billiken Bot is a Slack Application that serves as a login info assistant! It can store, retrieve, change, and remove usernames and passwords for different accounts the user has.

## Requirements

This project is capable to run on any systems compatible with Python 3.1 and later, this includes MacOS, Windows, Linux, etc.

A list of these dependencies can be found in our [requirements](https://git.cs.slu.edu/courses/spring23/csci_3300/zahmed2/-/blob/main/requirements.txt) file.

Installation of dependencies is handled in the [Getting Started](#getting-started) section.

## Getting Started

1. [Create](https://api.slack.com/apps) a new App in Slack.
2. Get your App Level Token and OAuth Tokens for your App.
3. Clone this repository.
   ```bash
   git clone https://github.com/em-henken/slackbot-password-manager.git
   ```
4. Create and activate your virtual environment.
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```
5. Install dependencies via requirements file.
   ```bash
   pip install -r requirements.txt
   ```
6. Export your Tokens and run your app!
   ```bash
   export SLACK_BOT_TOKEN=<your-bot-token>
   export SLACK_APP_TOKEN=<your-app-level-token>
   python3 src/app.py
   ```

## Commands

Billiken Bot can perform a number of tasks as your password manager! Here is a list of commands to try:


#### /pw-manager-join < access-code >

Adds you to BillikenBot password database.

#### /pw-manager-set < username/password > < account-name > < username-or-password > < access-code >

Save a username or password for an account.

#### /pw-manager-get < username/password > < account-name > < access-code >

Retrieve a username or password.

#### /pw-manager-change < username/password > < account-name > < access-code >

Change username/password data.

#### /pw-manager-remove < account-name > < access-code >

Remove an account's login data.



## SQLite Database and Documentation

The Billiken Bot also utilizes the SQLite database, which is a lightweight and easy-to-use database management system that is integrated into Python. The documentation for SQLite can be found [here](https://sqlite.org/docs.html).

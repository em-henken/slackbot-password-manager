# Billiken Bot

Billiken Bot is a Slack Application that serves as a SLU-oriented professional assistant. Billiken Bot can set/create reminders, create and store schedules, translate multiple languages, and keep Slack members up to date with SLU information!

## Requirements

This project is capable to run on any systems compatible with Python 3.1 and later, this includes MacOS, Windows, Linux, etc.

A list of these dependencies can be found in our [requirements](https://git.cs.slu.edu/courses/spring23/csci_3300/zahmed2/-/blob/main/requirements.txt) file.

Installation of dependencies is handled in the [Getting Started](#getting-started) section.

## Getting Started

1. [Create](https://api.slack.com/apps) a new App in Slack.
2. Get your App Level Token and OAuth Tokens for your App.
3. Clone this repository.
   ```bash
   git clone git@git.cs.slu.edu:courses/spring23/csci_3300/zahmed2.git
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

Billiken Bot can perform a number of tasks as your personal assistant! This involves translations, scheduling events/reminders, as well as looking up numerous bits of SLU information. Billiken Bot can get up-to-date news articles featured on SLU's page, open dining options on SLU's campus, as well as recreational center hours and final exam schedules for students! Here is a list of commands to try:

#### /translate < target-language > < message >

Translate any message to a given language.

#### /schedule < event-name > < (start) yyyy-mm-dd hh:mm > < (end) yyyy-mm-dd hh:mm >

Schedule an event.

#### /get-schedule

Retrieve all your scheduled events, in order.

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

#### /rec

Retrieve recreational center hours.

#### /dining

Retrieve open dining spots and their hours.

#### /finals

Retrieve current semester finals schedule.

#### /news

Retrieve current SLU news.

## Translate Library and Documentation

The Billiken Bot uses an open-source Python library that connects to Google Translate API. This library is capable of making free unlimited translation calls with a limit of 15,000 characters at a time. Library documentation can be found [here](https://pypi.org/project/googletrans/).

## BeautifulSoup4 Library and Documentation

The Billiken Bot uses an open-source Python library called BeautifulSoup4, which is used for web scraping and parsing HTML and XML documents. The documentation for BeautifulSoup4 can be found [here](https://www.crummy.com/software/BeautifulSoup/bs4/doc/).

## SQLite Database and Documentation

The Billiken Bot also utilizes the SQLite database, which is a lightweight and easy-to-use database management system that is integrated into Python. The documentation for SQLite can be found [here](https://sqlite.org/docs.html).

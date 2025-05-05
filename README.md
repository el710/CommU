>Kim Oleg <theel710@gmail.com>
Human! Protect the Flame of Prometheus from the darkness of ignorance.

# Project "CommU"

  It is a Life-service project that helps to make & manage your projects. Community oriented. Interface: Web-site, telegram bot, mobile application. Django based

---

  [1. Setup and run](#setup-and-run)
  [2. How it works](#how-it-works)

---

## Setup and run

   1.1 Setup Python interpreter 3.11.9 (<https://www.python.org/>)

   1.2 Setup git 2.38.0 (<https://git-scm.com/>)

   1.3 Setup VS Code (<https://code.visualstudio.com>)

   1.4 Make directory: 'p-CommU'

   1.5 Make Git repository in 'p-CommU':

   ```text
   git init
   ```

   1.6 Pull project from GitHub.com:

   ```text
  git remote add origin https://github.com/el710/CommU
  git pull --set-upstream origin main
   ```

   1.7 Setup Telegram token in 'id_bot.py'

   ```text
      tel_token = "xxxxxxxxxxx:xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
   ```

   1.5 Open directory 'DJPRO' in VSCode.

   1.6 Choose python interpreter: 'p-CommU\DJpro\.venv\Scripts\python.exe'

   ```text
    - ctrl + shift + p - python select interpreter
   ```
  
   1.7 Start Commu.py
  
 ---

## How it works

  The "Guest" user can simply view public skills, contracts & projects.
  To become a real user, you need to be a Human and register.

Here are some utems:

>### Skill

  A skill is a simple action that a person can perform independently.
  All you need is to set a time to turn a skill into an event.

  Create your own skill or choose one from the public ones and add it as an event in your Life.
  You have the option to change the skill (event) or delete it.

>### Contract

  A contract is a deal between two people whereby each person must perform some action(event) for the other person.

  An event for one person is a 'credit', and for another person it is a 'debit'.

  Create your own contract or choose one of the public ones and offer it to your contact.
  If your contact accepts your offer, the contract will be added to each other's projects.

```text
  Love is a contract without obligations.
```

>### Project

  Your main project is your Life.

 Create your own project or choose one of the public ones and add it to your Life.
 Add partners to your project and the offer will be sent to them.
 If your partners accept your offer, the project will exist until the last partner leaves. (even without you)

TODO:

- utem functionality - CRUD
  - contract
  - project

- FunctionalConstants (Magic numbers & strings)
- International
  
- testing (Unit)
- database (MySQL, PostgreSQL)
  - all user data must be scrambled
- UEngine
  - user's today agenda (schedule)
- telebot (Aiogram, Telethon)
- multyuser
- hosting

### 2. Link menegment

- Base of contacts (User class)
- business communities: <partner> - <hired worker> - <customer> deals (no any cheif)
- online mandat (for residencial / functionality ...) on/off by realtime votes of funcional members
- membership in project (mandat) by:
  - invitation
  - accepting the laws
      laws - set of tabus (Don't ...), common and local
      rules - "how to do"

>access by passing through the Test as anonimous:
there are questions with answers of candidat.
answers should correspond to laws.
Confirm by func memebers
Question & answers - is a passport of member

### 3. Dial menegment

- Base of skills/projects templates
- control time, credit/debet of dial with Bases
- base of process makets (reglaments, typical solves, technologies)

### 4. Time menegment

4.1 Planing ( S.M.A.R.T.)
    - calendar of events (event - part of deal with someone else)
    - daily event list
    - dials events
    - bases for week days
    - location referance
    - route & navigation
4.2 Control
    - alarms
    - combination plans between people

### 5. Source menegment

- money menegment
  - simple accounting with contacts
  - monetary system (e-bank)
- staff menegment
  - stock in/out
  - synchronize buys/exchange/throw out

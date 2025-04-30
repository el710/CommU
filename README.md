Copyright (c) 2024 Kim Oleg <theel710@gmail.com>
>Human! Protect the Flame of Prometheus from the darkness of ignorance.

# Project "CommU"
---
## CommU
It is a Life-service project that helps to make & manage your projects. Community oriented.
Interface: Web-site, telegram bot, mobile application.

---


  [1. Setup & run ](#Setup-&-run)

  [2. How it works ](#How-it-works)


---
## Setup & run
   1.1 Setup Python interpreter 3.11.9 (https://www.python.org/)

   1.2 Setup git 2.38.0 (https://git-scm.com/)

   1.3 Setup VS Code (https://code.visualstudio.com)

   1.4 Make directory: 'p-CommU'

   1.5 Make Git repository in 'p-CommU':
   ```
   git init
   ```
   1.6 Pull project from GitHub.com:
   ```
  git remote add origin https://github.com/el710/CommU
  git pull --set-upstream origin main
   ```
   1.7 Setup Telegram token in 'id_bot.py'
   ```
      tel_token = "xxxxxxxxxxx:xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
   ```
   1.5 Open directory 'DJPRO' in VSCode.

   1.6 Choose python interpreter: 'p-CommU\DJpro\.venv\Scripts\python.exe'
   ```
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
```
  Love is a contract without obligations.
```

>### Project
  Your main project is your Life.

 Create your own project or choose one of the public ones and add it to your Life.
 Add partners to your project and the offer will be sent to them.
 If your partners accept your offer, the project will exist until the last partner leaves. (even without you)



TODO:
- utem functionality
- testing (Unit)
- database (MySQL, PostgreSQL)
- UEngine
- telebot (Aiogram)
- multyuser 
- hosting
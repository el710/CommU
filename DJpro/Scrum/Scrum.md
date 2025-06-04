# Product backlog 

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

## 2. Link menegment

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

## 3. Dial menegment

- Base of skills/projects templates
- control time, credit/debet of dial with Bases
- base of process makets (reglaments, typical solves, technologies)

## 4. Time menegment

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

## 5. Source menegment
- money menegment
  - simple accounting with contacts
  - monetary system (e-bank)
- staff menegment
  - stock in/out
  - synchronize buys/exchange/throw out

### sprint backlog
1 refactoring: make parent tree and UtemBase
+ new user get utembase & storage
+ show user: refresh all utems in user's storage
+ load all founded utems to UtemBase
+ show_user: all utems has the same link: <type/id>
+ Life from UtemBase: walk_by_tree() from root - no sub trees - only lists  
+ make template lists from UtemBase: projects, contracts, skills
+ choose utem - open in CRUD page
~~show info about choosen utem - self.work_utem~~
+ if event made first - skill doesn't save it
+ executor add  when skill save to project
+ BUG: after load utems ids has changed FIXED: function hash() depends on wprk session
+ BUG: after choose one skill can't choose other: FIXED: work_utem = None at user page
+ Life  - user_id.ptp
  + init with hard_token = user_id
  + dont make token if there is hard_token
+ sinchronize storage & UtemBase: class KeepManager()
+ refactored skill-event CRUD
+ add context to utem as parent


Next sprint
- check out existance of utems in projects and contracts accorded with files
- only project can be root - choosen project becomes root
- find user_id.ptp after log in
- contruct CRUD
switch credit/debit in contract
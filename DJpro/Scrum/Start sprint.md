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

send parent Title to skill CRUD


Next sprint
- check out existance of utems in projects and contracts accorded with files
- only project can be root - choosen project becomes root
- find user_id.ptp after log in
- contruct CRUD
  - switch credit/debit in contract
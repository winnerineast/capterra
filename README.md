# Capterra Clone
this is project to create a clone database of capterra website.

## How to use

- The project can only run on Ubuntu. (we tested in Ubuntu 18.04)
- Install mySQL database.
- Install mysql-connector for python. 
- Update username and password in create_database.py.
- Run create_database.py to setup empty database for capterra.
- Run main.py to synchronize the online website with local database.
- main.py has the following features:
    * automatically detect the software categories by name of category
    * automatically detect the software by name of software
    * both category and software information will be overridden (!!!)
    * No overridden for review data and only appending
    
- (incoming) a local website to read local database
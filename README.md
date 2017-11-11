# Facility Space Allocation
## Introduction

A Simple Python CLI that allocates persons `staff` or `manager` to Offices and/or Living Space available at the facility

### Features

* Create and allocate Offices and Living Space
* Create and allocate Managers and Staff members
* Print allocations to stdout. (optionally save to filename)
* Print unallocated persons. (optionally save to filename)
* Relocate a person to another room
* Print persons allocated to a particular room

### Setting Up

Reccomended python version python 3.6

Make a folder in home dir:

  `$ mkdir ~/work-dir
  $ cd ~/work-dir`

Clone this repo:

  `$ git clone https://github.com/andela-amutava/Amity/tree/master 
   $ cd ~/Facility`
(Optional) Create and activate a virtual enviroment

  `$ virtualenv venv --python=python3'6
   $ . venv/bin/activate`
Install project requirements

`pip install -r requirements.txt
Launch the app using
(venv)$ python main -i`

#### Commands available for Interactive mode

Below is a description of command available in the interative mode. Type help at anytime to list all commands 

`create_room  <room_name><room_type>...`

This creates a room or a list of rooms where room_type can either be office or living. Example usage:


`add_person <first_name> <last_name> <role> [<wants_accommodation>]`

create a new person of role either staff or fellow and allocate to a random room: i.e staff is allocated office while fellow is allocate office and optionally a living space if requested

Example usage:

`reallocate_person <firstname> <lastname> <new_room_name>`

Move a person with person_id to new_room_name.

Constraints:

Can only move allocate person to room of same type i.e office to office and living space to living space
the new room should have atleast one vacant space.
Staff cannot be relocated to living spaces

`load_people <file_name>`

Add people to the program by reading a txt file as shown in the sample


`print_allocations [<file_name>]`

Prints a list of current person allocated in the rooms. (optional) file_name writes the data to the file


`print_unallocated [file_name]`

print a list of unallocated persons to the screen (optional) file_name writes the data to the file


`print_room <room_name>`

Prints the names of occupants inroom_name on the screen.


`save_state [sqlite_database]`

Save state of app to sqlite database: facility.sqlite . (optional) save to custom sqlite_db name

`load_state <sqlite_database>`

Loads application state from the specified database into the application. default loads facility.db


`quit`

This exits the application.


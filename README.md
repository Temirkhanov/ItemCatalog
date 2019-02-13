# Item Catalog

Ruslan Temirkhanov

## Skills used:

- Python
- Flask
- SQLAlchemy
- Javascript
- HTML
- SASS (CSS)
- OAuth
- Google Sign In

## Features

The Item Catalog is a web server application that provides many different features:

- CRUD. (Create, Read, Update and Delete data.)
- User Authentication and Authorization
- Google Sign-in/Sing-up
- JSON endpoints

### Prerequisites

Download the following:  
 Python 3
Vagrant
VirtualBox
Preconfigured vagrant folder [Download](https://s3.amazonaws.com/video.udacity-data.com/topher/2018/April/5acfbfa3_fsnd-virtual-machine/fsnd-virtual-machine.zip)

### How to run the program

1. In the terminal cd and unzip\move downloaded project files into \FSND-Virtual-Machine\vagrant
2. In the terminal run 'vagrant up'
3. After installation use 'vagrant ssh'
4. Cd into vagrant folder and then project folder
5. Run 'python db_setup.py' to create database
6. Run 'python populate.py' to populate data. (You will randomly own some of the data when registered)
7. Then run 'python main.py'
8. Go to http://localhost:8000 in your browser and enjoy!

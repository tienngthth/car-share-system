                  g0@@@@@@@@@@@@@@@@@@@@@8
              $@@@@@@@@@@@@@@@8888888@@@@@@>
           %@@@@X       @@@@@            @@@@%
          @@@^         @@@@@@              @@@g
       0@@@@          @@@@@@@`               @@@8 
     g@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@>
    @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
  @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@^
@@@@@@@@@@@@@@@@@@@@@@@@@CLOUDCAR@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@8
   0@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@8
           @@@@00@@@@@8@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@00@@@@
           C@@@00@@@@                                   @@@@00@@@
            ~@@@@@@@                                      @@@@@8

# Car-Share-System IoT Programming
``` 
RMIT University Vietnam
Course: COSC2790 Programming Internet of Things
Semester: 2020A
Assessment: Assessment 1: Python & Sense HAT programming
Student Name - ID: 
    1. Nguyen Thi Nguyet Minh  s3651351
    2. Nguyen Thanh Tam - s3747274
    3. Nguyen Quoc Cuong - s3748840
    4. Nguyen Thi Thuy Tien - s3757934
https://github.com/tienngthth/car-share-system
```
## Getting Started

This project has been built as an Python automation Car Share System to work with Raspberry Pi. The whole process includes a Master Pi and an Agent Pi serving four types of different users, which are customers, admin, manger and engineer. The final product includes a web application working with cloud database, a console based application and project documentation.

This document describes:

1. [Activities](#activities) 
  _[Git Usage](#git) 
  _[Trello Usage](#trello) 
2. [Architecture](#architecture)
   _[Master Pi](#master-pi)
    _[Web application API endpoints](#####-web-application-api-endpoints)
   _[Cloud database](###-Cloud-database)
    _[Clould database API end points](#####-clould-database-AapiPI-endpoints)
   _[Agent Pi](###-agent-pi)
   _[Local database](###-local-database)
   _[Object recognition](###-object-recognition)
   _[Socket communication](###-socket-communication)
3. [Instruction](##-instruction)
   _[Master Pi](###-master-Pi)
   _[Agent Pi](###-agent-Pi)
4. [Acknowledgments]

## Activities

This project has been developed for around 6 weeks. Git, git hub, Trello, Google Drive have been used from the beginning of the project to manage the work and help contributors to collaborate with each other. 

### Git

#### Repository

This respository is private and shared between 4 contributors and 2 observers.

There are 15 different branches beside the default master. Contributors are using different branches to develop different components. Enventually, all the branches are mereged to the two seperate main branches, which are ap for Agent Pi Application and mp for Master Pi Application.

Review [distribution.txt](https://github.com/tienngthth/car-share-system/distribution.txt) for more work distribution details.

#### Activities

Contributors pull code from the appropriate branch everytime to continue working on the solution. Commit and push activities happen continuously after some new parts of the solution are coded serveral times per week or per day.

For the first half of the cycle, contributors worked on small, seperate components.

For the second half of the cycle, contributors merged the repaired components to the main branches (mp-test and ap) and work on the work flow.

* Images go here

Following is the instruction to run the applications.

### Trello

* Images go here

## Architecture
* images go here

### Master Pi

Brief discussion

#### Web application API endpoints

0. Auth endpoints

    localhost:5000/login
    localhost:5000/logout
    localhost:5000/register

1. Admin endpoints (admin login required)

   localhost:5000/admin/users
   localhost:5000/admin/update/user
   localhost:5000/admin/delete/user
   localhost:5000/admin/cars
   localhost:5000/admin/car/bookings
   localhost:5000/admin/create/car
   localhost:5000/admin/update/car
   localhost:5000/admin/delete/car
   localhost:5000/admin/report/car

2. Customer endpoints (customer login required)

   localhost:5000/customer/cars
   localhost:5000/customer/book/car
   localhost:5000/customer/confirm/booking
   localhost:5000/customer/send/calendar
   localhost:5000/customer/authorize
   localhost:5000/customer/oauth2callback
   localhost:5000/customer/bookings
   localhost:5000/customer/bookings/details
   localhost:5000/customer/bookings/cancel

3. Engineer endpoints (engineer login required)

   localhost:5000/engineer/backlogs
   localhost:5000/engineer/location
   localhost:5000/engineer/close/backlog

4. Manager endpoints (manager login required)

   localhost:5000/manager/dashboard
   localhost:5000/manager/bar_chart
   localhost:5000/manager/line_chart
   localhost:5000/manager/pie_chart




### Cloud database

Brief discussion

#### Clould database API end points

1. Backlog endpoints

    localhost:8080/backlogs/create?assigned_engineer_id=&car_id&=status=&description=&
    localhost:8080/backlogs/close?signed_engineer_id=&car_id=&
    localhost:8080/backlogs/get/data
    localhost:8080/backlogs/get/all
    localhost:8080/backlogs/get/engineer/id?car_id=
    localhost:8080/backlogs/remove/assigned/engineer?id=
    localhost:8080/backlogs/remove/signed/engineer?id=
    localhost:8080/backlogs/remove/car?car_id=

2. Booking endpoints

    localhost:8080/bookings/create?customer_id=&car_id=&rent_time=&return_time=&total_cost=
    localhost:8080/bookings/update?status=&id=
    localhost:8080/bookings/read?car_id=&customer_id=
    localhost:8080/bookings/get/profit/data
    localhost:8080/bookings/get/most/profit
    localhost:8080/bookings/get/data
    localhost:8080/bookings/get/longest/duration
    localhost:8080/bookings/get/all?car_id=&customer_id=
    localhost:8080/bookings/get/by/time?car_id=&customer_id=&start=&end=
    localhost:8080/bookings/remove/customer?customer_id=
    localhost:8080/bookings/remove/car?car_id=

3. Car endpoints

    localhost:8080/cars/create?mac_address=&brand=&type=&location_id=&status=&color=&seat=&cost=
    localhost:8080/cars/update?mac_address=&brand=&type=&location_id=&status=&color=&seat=&cost=&id=
    localhost:8080/cars/read?mac_address=&brand=&type=&status=&color=&seat=&cost=&id=
    localhost:8080/cars/status/available?mac_address=&brand=&type=&status=&color=&seat=&cost=&id=
    localhost:8080/cars/get/id?mac_address=
    localhost:8080/cars/history?id=

4. Customer endpoints

    localhost:8080/customers/create?username=&password=&first_name=&last_name=&email=&phone=
    localhost:8080/customers/read?username=&password=&first_name=&last_name=&email=&phone=&id=
    localhost:8080/customers/update?username=&password=&first_name=&last_name=&email=&phone=&id=
    localhost:8080/customers/delete?id=
    localhost:8080/customers/get/id?username=
    localhost:8080/customers/check/existed/username?username=

5. Location endpoints

    localhost:8080/customers/location/get?id=

6. Staff endpoints

    localhost:8080/staffs/read?id=&username=&first_name=&last_name=&email=&phone=&user_type=
    localhost:8080/staffs/check/existed/username?username=
    localhost:8080/staffs/get/engineer/mac/address?id=


### Agent Pi

Brief discussion

### Local database

Store what?

### Object recognition

Code and facial

### Socket communication

brief discussion

## Instruction

Review [requirements.txt](https://github.com/tienngthth/car-share-system/requirements.txt) and make sure all packages have been installed.

### Master Pi

1. Download the mp-test branch.
2. Run ./run.sh in your console to initiate the web application and the cloud APIs.
3. Run ./cloud.sh to initiate the cloud database connection.
    Password:
4. Access to web application at localhost:5000 , please use Google Chrome Browser.
    A customer credential: tiennguyen | 2@aA2222
    The admin credential: minh_nguyen | 2@aA3333
    The manager credential: tam_nguyen | 3#aA4444
    The engineer credential: cuong_nguyen | 1!aA2222

detail stories

### Agent Pi

1. Download the ap branch.
2. Run ./mainMenu.py in your console to start the console based application.

detail stories

## Acknowledgments

* please include acknoledgements for all the technologies: google calendar, cloud, facial, ...


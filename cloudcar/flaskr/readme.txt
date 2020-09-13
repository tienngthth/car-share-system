
                  g0@@@@@@@@@@@@@@@@@@@@@8
              $@@@@@@@@@@@@@@@8888888@@@@@@>
           %@@@@X       @@@@@            @@@@%
          @@@^         @@@@@@              @@@g
       0@@@@          @@@@@@@`               @@@8 
     g@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@>
    @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
  .@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@^
@@@@@@@@@@@@@@@@@@@@@@@@@CLOUDCAR@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@8
   0@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@8
           @@@@00@@@@@8@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@00@@@@
           C@@@00@@@@                                   @@@@00@@@
            ~@@@@@@@                                      @@@@@8

MP User Interface and API Documentation

This document describes:

1. The architecture of the user interface and it's API
2. The API Endpoints and who can use them
3. A detailed explanation of how one of the API endpoints works (customer car search)
4. How user authentication works and how to change it if we need to
5. Features not implemented yet
6. Known bugs

------------1. Architechture------------
The main file is blog.py. This contains most of the API endpoints and code.
auth.py contains all features and API endpoints used for user creation and authentication
schema.sql is a simple placeholder database. It uses the same table and column names as our specification does. 
forms.py is a library of forms. Both user authentication and the main API file use it.

The static folder contains the CSS and the cloudcar logo image

The templates folder contains the core Jinjia2 template that all other pages are build around (e.g. the header, logo, footer)

Inside the templates folder, the auth folder contains all the Jinjia2 templates for user authentication, and the blog folder contains all the main application page templates


------------2. API Endpoints------------

/auth/register
Allows a new user of usertype=Customer to register (only admins can create other user types)

/auth/login
Allows users to log in

/createadmin
This creates an admin user with username=admin and password=admin. It's a temporary helper function to be removed later.

/ requires usertype = any valid
redirects the user to a different page depending on their user type: Managers go to the dashboard, admins to the admin car search, engineers to the repair log, and customers to the car booking search

/index.html requires usertype=customer
This is where users can search for available cars to book. It will ony show cars once dates are selected (because it checks for overlapping bookings).

/bookings requires usertype=customer
This is where a user can see their bookings, and cancel one if needed.

/<int:id>/confirm requires usertype=customer
This is never accessed directly. This generates a confirmation page to help a customer make a booking. 

/<int:id>/createbooking requires usertype=customer
This is never accessed directly. It takes the booking data after the user confirms it and creates a booking.

/adminusers requires usertype=admin
This is a page for admin users to create and search users, and also edit them, or delete them.

/admincars requires usertype=admin
This is the admin car search page. It lets an admin flag a car for repair, add a new car, update a car, and delete a car

/create requires usertype=admin
This is never accessed directly. It takes form data submitted by an admin and uses it to create a new car.

/<int:id>/update requires usertype=admin
This is never accessed directly. If it receives a GET request, it displays a car update form. If it receives a POST request, it uses submitted form data to update a car.

/<int:id>/delete requires usertype=admin
This is never accessed directly. It lets an admin user delete a car

/<int:id>/repair requires usertype=admin
This is never accessed directly. It lets an admin user flag a car for repairs

/createuser requires usertype=admin
This is never accessed directly. It takes form data submitted by an admin and uses it to create a new user.

/<int:id>/updateuser requires usertype=admin
This is never accessed directly. If it receives a GET request, it displays a user update form. If it receives a POST request, it uses submitted form data to update a user.

/<int:id>/deleteuser requires usertype=admin
This is never accessed directly. It lets an admin delete a user

/<int:id>/carbookings requires usertype=admin
This is never accessed directly. It creates a page for the admin user that contains the booking history of a particular car

/engineercars requires usertype=engineer
This lets an engineer see a list of cars to repair, mark a car as repaired, and show car details including a map

/<int:id>/location requires usertype=engineer
This is never accessed directly, it creates the car details page with a map for the engineer

/<int:id>/fix requires usertype=engineer
This is never accessed directly, it allows an engineer to clear a repair flag from a car

/<int:id>/deletebooking requires usertype = Admin or Customer
This is never accessed directly. It lets you delete a booking. An admin can delete anyone's booking, but a User can only delete their own bookings (the API checks for this)

/manager requires usertype = manager
This lets you select a graph to view

/<int:id>/sendmail
Unimplemented. This is where the mail sending function goes

/<int:id>/calendar
Unimplemented. This is where the calendar sending function goes

------------3. Description of an API Endpoint------------

The example below uses /index.html, the page where users can search for and book a car. 

We start by checking what type of user is here. Only customers need to be here, so we redirect other users.
Then, we define our database and search form
If we receive a POST request, we know someone has submitted a search for available cars, so we load the search form variables.
Next, we do data validation (validation is also done client-side), e.g. cost has to be a number that can be converted into a float. If there's a problem, we display an appropriate error message.
If there are no errors, we search for all cars that match the user's search criteria.
Then, we take those cars, and for every car we count the rows in our Bookings table that conflict with the user's selected dates. If there are no conflicts, we add that car to a list of available cars.
Finally, we render a html view to show users the list of available cars that match their search criteria.

If we receive a GET request, we know the user has navigated to this page directly, e.g. after login or by clicking on the menu. We return a render with no cars, and a search from for them to fill out.  

------------4. User Authentication------------

We've used Werkzeug's integrated password hasher to handle secure password hashing. If we need to swith that to something, else, that's ok. We'll just need to add the new function to auth.py.
---> The team needs to decide what to do about this. It currently meets requirements.


------------5. Missing Features------------
i) Sending an email to the engineer doesn't work. We have tried the following and it didn't work:

We wrote a script that uses Gmail to send a rendered Jinjia2 HTML email template with the car details. It works, but seems not to be compatible with Flask. Calling it as an external command with the os library causes it to run, but the email still doesn't get sent somehow! 

Probably we need to use the Flask_email library. However, it depends on a Werkzeug library that has a bug in Python 3 where it uses some incorrect imports. It's pretty easy to patch it, but I still haven't figured out how to use the library.

Our next step needs to be to investigate the Flask_email library in detail to try and find a working solution. Alternatively, we could as a last resort use Mailchimp or another email delivery service to handle this, but I don't think it's what the professor intends for us to use.

ii) Calendar integration -- we understand that this works in a seperate Python script but I don't know how to integrate it. I've left an API endpoint for it so someone else who understands it better can easily add it in easily.

iii) Manager graphs -- Doesn't presently work because I haven't set it up yet. It has API endpoints set up for it though.

iv) Google cloud DB is not connected -- I'm running on a local SQLite3 database to speed up development. It should be easy to switch it over.

------------6. Known Bugs------------

Server-side validation should do a regex on location to make sure it's a valid longitude/latitude (which the maps feature absolutely relies on). This would take a while to do and test since it's a regex, so I don't think it has a high priority right now.

Users can search for car availability dates in the past. This doesn't break anything but it's a weird thing to allow. Can be fixed by getting datetime.now() and doing a timedelta on the user-selected start time. If it's negative, reject the query with an informative error message. Since this doesn't break anything, but is easy to fix, I would say this is a medium priority bug.

The main UI API file and other things are named 'blog' --> need to change it to something more sensible and update all files that need to access it. This is easy to do and it looks unprofessional as is, we can do this right before submitting the code, but it is a high priority.

The UI and auth API functions are in an arbitrary order in blog.py. They should be ordered by usertype required for access or similar so it's easier for us to find things. This doesn't affect program performance but we could lose marks for it. We can do it right before code submission, but it is high priority.

Finally, we should remove the /createadmin function when we can. I just created it for fast testing. This is high priority and only takes 1 minute.



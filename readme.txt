// // // // // // // // // // // // // // // // // //
//                                                 //
// @File: Readme.txt                               //
// @Author: CTN Team                               //
//                                                 //
// This file describes how our software works      //
// as well as a brief description on how to load it//
//                                                 //
// // // // // // // // // // // // // // // // // //

Welcome to the HealthNet Documentation

To load this software, unzip all .zip files in this directory. 

To run this software, simply run runserver.bat, located in the Code directory.
If this fails (or your operating system cannot run the file), use your command line and cd into this directory. Issue the command 

			       python manage.py runserver 

The server should boot up fine. 
Now access localhost:8000 using your web browser of choice, and you should be all set.



Known bugs: 

1. Must create profile correctly the first time in order for the system to generate the user correctly
2. Appointments still can be added with conflicts and in the past
3. Sometimes upon successful Authentication, no redirect occurs. Healthnet Logo needs to include such link.  
4. Doctors must use the admin page to add prescriptions or admit/discharge from hospital
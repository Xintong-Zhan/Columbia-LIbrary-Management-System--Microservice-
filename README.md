# Columbia-LIbrary-Management-System--Microservice-
Based on the single server version of library management system, created the microservice structure of the system.

Overview

The program is a library management system. It uses HTML, CSS, and JavaScript as the presentation tier, Python Flask as the application tier, and MySql database as the data tier. The system's functions include user login, user information modification, book location query, new book registration, book borrowing, book returning, book information query, user’s borrowed book query, and library map display. The system has two types of users: administrator users and normal student users. Normal student users don’t have to log in, and they can check book information, check their own borrow records with their library ids, and check the Library Map. Administrator users have to log in, and they have access to all the functions. For all functions, if the entered information is incorrect, an error message will be displayed.

Function Display

Main Page The main page includes admin login and student query without login. Student query is placed on the top bar, circled in red, and the functions of Student Information Query, Book Information Query, and Library Map are the same as functions 7, 8, and 9, which will be displayed later.

Index After a successful admin login, the index page will be shown. (Currently, the Login ID can be xz3165 or fz2348, and the Password is 123)The function navigator is displayed on the left, and the user name and head portrait are displayed on the top right.

New Book Storage Click on the Storage button, and the user can add a new book to the library. First, the user register for the book information; then, the user adds storage information to the registered book.

Borrow Book Click on the Borrow button, and the user can lend books to a student with the student’s CUID. This page includes a search function, where book names can be searched by keywords. After the user clicks on the lend button, the book will be lent to the student and removed from storage.

Return Book Click on the Return button, and the user can return books for a student with the student’s CUID. After the user clicks on the return button, the book will be returned to the library storage.

User Information Modification Click on the Information Setting button, and the admin user can change a user’s information and level of authority.

Student Information Query Click on the Student Information Query button, and the user can check a certain student’s borrowed book with the student’s library card number. This function can also be accessed directly on the home page with the button Student Information Query on the top bar without admin login.

Book Information Query Click on the Book Information Query button, and the user can check a book’s information with its book name, author, class name, or ISBN. This function can also be accessed directly on the home page with the button Book Information Query on the top bar without admin login.

Columbia University Library Map Click on the CU Library Map button, and the user will be directed to a digital map with information on it. The user can get back to the library system with the button Back To Library at the bottom. This function can also be accessed directly on the home page with the button Library Map on the top bar without admin login.

# Household
#### Video Demo: https://youtu.be/Ga-1W86hk_A
#### Description: 
Household is a web application that connects customers with providers of cleaning services across all cities in Serbia. The purpose of this web application is to build a trustworthy community which relies on comments and review system.
## Functionality:
When filling registration form, user chooses a role-**cleaner** or **customer**. Depending on the selected role, the user experience is dynamically tailored: \
**-Customers**- are shown a list of cleaners <ins>in their own city</ins>. They can <ins>find contact details(email and/or phone number), description of the work, reviews and comments</ins> for each cleaner. <ins>Average rating</ins> for each cleaner is also displayed.\
**-Cleaners**- can <ins>add short description of their previous experience, services and prices.</ins> They can see recent reviews and ratings their customers left. According to them they can improve their services and make better offers for other customers. Additionaly, they are shown a list of other cleaners for their city in order to see the dynamic of the marketplace. 


I wanted to create a trustworthy platform where users don't rely solely on polished self-descriptions, but can instead base their decisions on real experiences shared by other customers. **<ins>Public reviews ensure transparency and help build credibility, allowing users to make informed choices based on honest feedback.</ins>**


Note that **<ins>user is able to change profile details any time</ins>**, including their role (customer or cleaner). This flexibility removes the need for users to delete their account and register again if their needs change.(e.g. If a user initially registers as a cleaner but later wants to become a customer, he can simply update his user type via the profile editing form. His cleaner data (like phone, description, and reviews) will no longer be displayed on other users' homepages. However, if he decides to switch back to the cleaner role, all of his previous reviews, comments, and average rating are automatically restored, ensuring continuity and preserving reputation).


## Files:
### Python:
**<ins>app.py</ins>** \
This is the main file of my Household web application. It contains:
1) Flask app initialization (routing, templates,sessions,dynamic content with JSON)
2) Secure password handling (hashing and verifying passwords) with werkzeug
3) Import of customer helper functions created in helpers.py (login_required and appology)
4) Connection with SQLite database
5) Two tables created in household.db: users and reviews\
    <ins>users</ins> stores: username, name, surname, email, password, user type, city, phone, description \
    <ins>reviews</ins> stores: reviewer id, cleaner id, rating(between 1 and 5), comment, time when review is created
6) Routes creation:\
    <ins>index</ins>: If user is not logged in (no sesion), he is shown index page. Otherwiese he is redirected to customer or cleaner homepage(based on the role).\
    <ins>login</ins>: If user has an account, he is able to login. Username and password are required to be entered in order to login. Username and password's hash are checked in database. If they are both valid, person is redirected to either customer or cleaner homepage(based on the role). Otherweise error is displayed using appology function. \
    <ins>logout</ins>: Clears session and redirects to homepage.\
    <ins>register</ins>: For successful registration username, password, password confirmation, name, surname, email, user type and city are required. If either of them is missing, error is dislayed using appology function. If user met all the requirements(email matches pattern, password matches password confirmation, city is in list of cities) his data are added to the database and he is successfully registered and redirected to the appropriate user homepage(based on the role).\
    <ins>change password</ins>: Logged-in users could easily change password by entering old password, new password and confirmation of new password. If new password and password confirmation does not match, error is displayed using appology function. If validation is successful, password is updated in the database(hashed).\
    <ins>my_profile</ins> Displays currently logged-in user's profile. If user is a cleaner their profile will also display average rating, total number of reviews and a list of reviews left (with reviewer's name). \ 
    <ins>edit_profile</ins> Information users can edit are username, name, surname, email, user type and city. Besides that, cleaners will have an opportunity to add a phone number and describe themselves and their services. If user met all the requirements(all required fields are filled, email matches pattern, city is in list of cities) his changes are updated in the database and confirmation message is shown.\
    <ins>customer_home</ins> Displays a list of cleaners in the same city as the logged-in customer. For each cleaner, the page shows: profile details, contact information, short description of services (if provided),average rating, number of reviews received and option for reading comments others wrote.\
    <ins>cleaner_home</ins> Displays a list of cleaners in the same city as the logged-in cleaner. For each cleaner, the page shows: profile details, contact information, short description of services (if provided),average rating, number of reviews received and option for reading comments others wrote in order to see the dynamic of the marketplace.\
    <ins>load_more_comments</ins> For the required cleaner, 5 most recent comments are retrieved from the database.\
    <ins>leave_review</ins> Allows logged-in users to leave a review for a cleaner. The review includes a rating (1–5) and an optional comment. The application checks that the user is not reviewing themselves. After successful submission, the review is stored in the database, and the user is redirected to the homepage.\
7) Other functions:\
    <ins>is_valid_email</ins>: checks if email matches pattern.\
    List of cities in Serbia.


**<ins>helpers.py</ins>**\
This is the auxiliary file for the main app.py file. It contains: 
1) Renders appology page with an error message to the user if something goes wrong.
2) Function that checks if user is logged-in. If so h can be redirected to the requested route, if not he is redirected to the homepage.


### CSS:
**<ins>style.css</ins>** \
This file defines the overall look of the Household web application. It provides a clean, modern, and responsive user interface using a consistent color palette of navy blue and baby blue. The stylesheet handles layout design, typography, buttons, form inputs, dropdown menus, and cleaner profile cards. It also supports user interaction features such as toggling comments, form alignment, and hover effects. Media queries ensure the app is mobile-friendly, while custom elements like city autocomplete and review submission forms are styled for clarity and usability.


### HTML:
**<ins>layout.html</ins>** \
This file is the main template used throughout the Household app. It sets up the basic HTML structure including the page header, navigation bar, main content area, and footer.\
The navigation bar changes depending on whether the user is logged in or not. If user is not logged in quick access to homepage, login and registration pages is provided. If user is logged in quick access to homepage, profile, change password and logout  is provided. \
It also includes Bootstrap for responsive styling and links to the app’s custom CSS.\
Flash messages are displayed prominently to inform users of important actions or errors.\
The main content section is a placeholder where specific page content is inserted using Jinja2 blocks.\
**<ins>index.html</ins>** \
This is the homepage template users see when they first visit the Household web application. It extends the main layout.html template to maintain consistent styling and navigation.\
The page has a large header, subtitle and a central image to visually introduce the service. It clearly explains how the platform works by outlining six simple steps tailored for both customers and cleaners.\
Buttons invite users to register or log in.\
**<ins>register.html</ins>** \
This is the registration form for new users. It allows users to create an account by entering a username, password, password confirmation, name, surname, email, role (customer or cleaner), and city. The form includes city autocomplete feature powered by a JavaScript script that filters cities in Serbia as the user types. The form sends data via POST to the /register route, where server-side validation and user creation take place.\
**<ins>login.html</ins>** \
This page provides a simple login form where users enter their username and password. It submits the data via POST to the /login route, which handles authentication.\
**<ins>my_profile.html</ins>**\
This page displays the currently logged-in user's profile information, including their username, name, surname, email, user type, and city.\
If the user is a cleaner, additional details like phone number, service description,average rating, number of reviews and reviews from customers are also shown. \
All users have the option to edit their profile via a link to the edit form. \
**<ins>edit_profile.html</ins>**\
This page provides a form that allows logged-in users to update their profile information. \
Users can edit fields such as username, name, surname, email, user type (customer or cleaner), and city. \
If the user is a cleaner, additional fields for phone number and service description are also displayed. \
The city input includes an autocomplete feature based on a predefined list of Serbian cities, enhancing user experience and data consistency. \
After submission, the changes are sent via POST to the /edit_profile route for validation and updating in the database.
**<ins>change_password.html</ins>**\
This page provides a form that allows logged-in users to securely update their password. The form requires users to enter their current password, new password, and a confirmation of the new password. Upon submission, the data is sent via POST to the /change_password route.\
The change password form is separated from the edit profile form for security reasons and to prevent accidental password changes when users are updating unrelated profile information.\
**<ins>customer_home.html</ins>**\
This page is shown to logged-in users with the customer role. It displays a list of available cleaners in the same city as the user. For each cleaner, the following information is shown:\
*Username, full name, email, phone number, and service description\
*Average rating and total number of reviews\
*A toggleable section with the cleaner’s most recent comments\
*A form to submit a new review, including a numeric rating (1–5) and a comment\
*If there are no cleaners available in the user’s city, a message is displayed instead.\
A JavaScript script enables toggling visibility of the comments section for each cleaner, improving user experience by reducing clutter on the page.\
**<ins>cleaner_home.html</ins>**\
This page is displayed to logged-in users with the cleaner role. It showcases a list of other cleaners operating in the same city, allowing users to observe the local marketplace. For each cleaner, the page displays:\
*Username, full name, email, phone number, and service description\
*Average rating and number of reviews\
*A toggleable section showing the latest user comments\
*If there are no cleaners available in the user’s city, a message is displayed instead.\
Cleaners can also leave reviews for others (excluding themselves, both rating (1–5) and a comment). This feature supports scenarios where cleaners might use services offered by others for personal needs.\
A JavaScript script enables toggling visibility of the comments section for each cleaner, improving user experience by reducing clutter on the page.\
**<ins>appology.html</ins>**\
This is the error page displayed when something goes wrong in the application (e.g. incorrect login details, wrong email pattern etc.). It ensures that users receive clear feedback when their action cannot be completed. \
It uses two dynamic variables: top (a short error code or title) and bottom (a detailed explanation). These are passed from the backend using the custom apology() function defined in helpers.py. \
The page provides a clean, centered layout and includes a button that takes the user back to the homepage.  \

## Developer's personal touch
My name is Nikolina Nikolić, I am 18 years old and I come from Serbia. As a young woman, I am aware of the challenges I will face in the future. I am driven by a strong desire to contribute to society through my knowledge, education, and creativity. Whenever I see that my ideas have the potential to help or inspire others, my motivation only grows stronger.\
Everyone talks about work-life balance, but how can it truly be achieved when there is constant pressure and stress on both sides? Serbian market is facing a huge difficulty: the lack of easily accessible and reliable household services. This web application is my way of making a positive difference in people’s everyday lives.
I believe technology offers unlimited opportunities, and I am passionate about leveraging it to improve society’s well-being and create real, meaningful change.\
I hope that my web application will become long-term sustainable platform which can expand to other countries and provide more services.


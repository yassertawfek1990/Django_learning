Quizzy is a website dedicated to quizes where you can register with your email and keep track of your score.
there are 12 categories with 3 level easy medium hard and there is a random option where you can choose random category with random level.
Also you will recieve an email when you rank changes.
firstly I created a virtual environment in VSC and then installed django.
then started a new project and 3 apps
users app to handle the login and log out parts thanks to django we have already log in and log out view alsso created the register virew
I used email verification method so the user has to register his email and verify it then I created a userprofile table with the email first last name and user name that we get from the user table during registeration already and added to it a score field then we make migrations and finished the templates.
then I created a base template which has a nav bar at the top and a footer thanks to bootstarp 
then I started to work on the webpages app where I created a home view which shows 3 different levels and 3 different categories and top scores.
links were not working at this point I onnly finished the front end part thanks to bootstrap and created the views function
then created contact us and suggestions and about us pages and added their view functions that was simple and created a table for them and made migrations
then I started working on the real backend part which we have done in the Quizzy app
first I found a quiz sample from using bootstrap and made a little modifications to it 
then created the view function for it and created a result page and view function for it
I used the userprofile table to show the old score and the new score in the result table and also the old rank and the new rank
then created the categories page and its function
then I added the links to all the buttons in my templates
then I Created an API app that get requests from API to retrieve all the questions for a user by its username 
it also send post requests to add questions to the user via user name 
I added a documentation template and added both of them to the footer with quick link
I added a timer function
I added a new section where users can add questions to specific category and play from there
I created in the nav bar a sction called users questions with categories and add questions and play to button to each category
now the website is covering all the requirements mentioned in the ideas bank for the quiz project on AlX
then I have tried the website many times and had fun playing
then I deploayed the website on pythoneverywhere.com
and here is the link
https://yasser1990.pythonanywhere.com/
Thanks ALX for everything

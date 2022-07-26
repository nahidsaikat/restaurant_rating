# Restaurant Rating
## Description
Company needs internal service for its’ employees which helps them to make a decision
on lunch place. Each restaurant will be uploading menus using the system every day
over API and employees will vote for the menu before leaving for lunch.

There are an API for:
* Authentication
* Creating restaurant
* Uploading menu for restaurant (There should be a menu for each day)
* Creating employee
* Getting current day menu
* Voting for restaurant menu
* Getting results for the current day. The winner restaurant should not be the winner for 3 consecutive working days
* Logout

## Run the application 
* `git clone https://github.com/nahidsaikat/restaurant_rating.git`
* `cd restaurant_rating`
* `pipenv install`
* `pipenv shell`
* `python manage.py migrate`
* `python manage.py runserver`
* `python manage.py test`    (To run the test)

## Dependencies
* Python 3.10-*
* Django 4.0
* DRF 3.13.1

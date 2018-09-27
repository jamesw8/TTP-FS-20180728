# myPortfolio
myPortfolio aims to help you keep track of your stocks by providing all of your stocks in one place. All transaction history is also readily available.

## Instructions
* (Optional) Create a virtual environment with virtualenv
* Install requirements using `pip install -r requirements.txt`
* Run server using `gunicorn app:app` or `python app.py` for development server

## User Stories Requirements
1. A user is able to create a new account with their name, unique email, and password with a start balance of $5000.00 USD.
2. A user is able to login to their registered account with their correct email and password combination.
3. A user can invest in a specified ticker symbol for a number of shares if they have enough money and if the ticker symbol is valid.
4. A user can view all transactions they have made to date in the transactions view.
5. A user can list all of the stocks they own in their portfolio as well as their current values using IEX API.
6. A user can see performance of a stock symbol by its color (red, grey, green) in the portfolio view.

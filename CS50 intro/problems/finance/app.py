import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
#Complete the implementation of index in such a way that it displays an HTML table summarizing,
#  for the user currently logged in, which stocks the user owns,
# the numbers of shares owned,
# the current price of each stock, and
# the total value of each holding (i.e., shares times price).
# Also display the user’s current cash balance along with a grand total (i.e., stocks’ total value plus cash).

    if request.method == "GET":
        user_id = session["user_id"]
        # print(f"\n\n{user_id}\n\n\n")
        # return render_template("portfolio.html")


        stocks = db.execute("SELECT stock_name, symbol, SUM(shares) FROM transactions WHERE user_id=? GROUP BY stock_name", user_id)

        if (bool(stocks) == False):
            return render_template('portfolio.html')
        else:
            try:
                for stock in stocks:
                    stock["latest_price"] = lookup(stock["symbol"])["price"]

                for stock in stocks:
                    stock["total"] = '{:,.2f}'.format(stock['latest_price'] * stock['SUM(shares)'])

                cash = db.execute("SELECT cash FROM users WHERE id=?", user_id)[0]["cash"]
                all_stocks = db.execute("SELECT SUM(total_price) FROM(SELECT stock_name, shares*bought_price AS total_price FROM transactions WHERE user_id=?)", user_id)[0]["SUM(total_price)"]
                cash_stocks = '{:,.2f}'.format(cash + all_stocks)
                cash_format = '{:,.2f}'.format(cash)
                print(f"\n\n{cash_stocks}\n\n\n")

            except TypeError:
                return apology("unsupported operand type(s) for +: 'int' and 'NoneType'" )
            else:
                return render_template("portfolio.html", stocks=stocks, cash=cash_format, cash_stocks=cash_stocks)

    return apology("Homepage error")






@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "GET":
        return render_template("buy.html")

    """Buy shares of stock"""
    if request.method == "POST":
        symbol = request.form.get("symbol").upper()
        if not symbol:
            return apology("Please enter a symbol")
        #looking up the symbol
        item = lookup(symbol)
        if item == None:
            return apology("There was an error with looking up the stock. Ensure you've typed it correctly.")

        shares = request.form.get("shares")
        if not shares:
            return apology("Please enter a share amount you wish to buy!")
        if not shares.isdigit():
            return apology("You must enter a numeric value for shares/non negative number")
        try:
            shares = int(request.form.get("shares"))
        except ValueError:
            return apology("Apologies, shares must be an integer")
        if (shares < 1):
            return apology("Must purchase at least 1 share!")

        name = item['name']
        price = int(item['price'])
        symbol = symbol
        shares = int(shares)
        user_id = session["user_id"]
        cash = db.execute("SELECT cash FROM users WHERE id = ?", user_id)[0]["cash"]
        if (type(cash) == str):
            cash = int(cash.replace(',', ''))
        if (cash < price*shares):
            return apology("You don't have enough cash to continue this purchase.")
        new_cash = cash - (price*shares)

        #Updating the cash
        db.execute("UPDATE users SET cash = ? WHERE id = ?", new_cash, user_id)
        #adding the buy to the transactions table
        db.execute("INSERT INTO transactions (user_id, stock_name, symbol, bought_price, shares, trans_type)VALUES(?,?,?,?,?,?)",
                    user_id, name, symbol, price, shares, 'buy')
        return redirect("/")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    if request.method == "GET":
        user_id = session["user_id"]
        stocks = db.execute("SELECT * FROM transactions WHERE user_id = ?",user_id)

        print(f"\n\n{stocks[0]['trans_id']}\n\n\n")
        return render_template("history.html", stocks=stocks)

    return apology("history")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "GET":
        return render_template("quote.html")
    #displaying the stock inputted
    if request.method == "POST":
        symbol = request.form.get("symbol")
        #if not symbol:
         #   return apology("Please enter a symbol!")
        symbolup = lookup(symbol)
        if not symbolup:
            return apology("There was an error with looking up the stock. Ensure you've typed it correctly.")
        else:
            name = symbolup['name']
            price = usd(symbolup['price'])
            symbol = symbolup['symbol']
            output = name+" "+"(" + symbol + ")" + " stock is currently priced at " + price
            return render_template("quote.html", output=output)

    return apology("TODO")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        password_confirm = request.form.get("confirmation")
        cash_int = 10000
        #Error checking
        # if (db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username")) == True):
        #     return apology("Username already exists", 400)
        if (len(username)==0  or len(password)==0 or len(password_confirm) == 0):
            return apology("Please ensure all fields are filled", 400)
        if (password != password_confirm):
            return apology("Passwords do not match", 400)

        #add user to database
        hashpassword = generate_password_hash(password)
        try:
            db.execute("INSERT INTO users (username, hash, cash) VALUES(?,?,?)",username, hashpassword, cash_int)
        except ValueError:
            return apology("ValueError: UNIQUE constraint failed: users.username ")
        else:
            return redirect("/")

        # #logging the user in using a session
        # userid = db.execute("SELECT * FROM users WHERE hash = ?", hashpassword)
        # session["user_id"] = userid[0]["id"]
        # return render_template("portfolio.html")



    #default incase of error
    return apology("register error")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    user_id = session["user_id"]
    symbols = db.execute("SELECT DISTINCT symbol FROM transactions WHERE user_id=?", user_id)
    shares_has = db.execute("SELECT SUM(shares), symbol FROM transactions WHERE user_id=? GROUP BY stock_name", user_id)
    print(f'\n\n\n\n{shares_has}\n\n\n\n')

    if request.method == "GET":
        return render_template("sell.html", symbols=symbols)

    if request.method == "POST":
        symbol = request.form.get("symbol")
        shares_sell = -abs(int(request.form.get("shares")))


        symbolup = lookup(symbol)
        if not symbolup:
            return apology("There was an error with looking up the stock. Ensure you've typed it correctly.")
        else:
            name = symbolup['name']
            price = symbolup['price']
            symbol = symbolup['symbol']

        cash = db.execute("SELECT cash FROM users WHERE id=?", user_id)[0]["cash"]
        new_cash = cash - (shares_sell * price)

        # error checking
        # print(f'\n{shares_sell}\n')
        # return render_template("portfolio.html")
        for share in shares_has:
            if (share['symbol'] == symbol) and (share['SUM(shares)'] > (-shares_sell)):
                    db.execute("INSERT INTO transactions (user_id, stock_name, symbol, bought_price, shares, trans_type)VALUES(?,?,?,?,?,?)",
                    user_id, name, symbol, price, shares_sell, 'sell')
                    db.execute("UPDATE users SET cash = ? WHERE id = ?", new_cash, user_id)
                    return redirect("/")
            else:
                return apology("You do not have enough shares to perform this transaction")



Requirement for this project for setup:<br/>

-> Create a vitual environment.<br/>
== virtualenv -p python3.6 venv<br/>
-> Activate your virtual environment using this command<br/>
== source venv/bin/activate<br/>
-> Install required python libraries by using pip installer.<br/>
== pip install -r requirements.txt<br/>
-> Migrate database.<br/>
== python manage.py migrate<br/>
-> Finally, run your django runserver.<br/>
== python manage.py runserver<br/>


# JWT based authentication
--To authenticate and obtain the token. The endpoint is /api/token/ and it only accepts POST requests.<br/>
Ex - http post http://127.0.0.1:8000/api/token/ username=vitor password=root<br/>

# Please keep these things in mind while authenticating using JWT
The JWT is acquired by exchanging an username + password for an access token and an refresh token.<br/>

The access token is usually short-lived (expires in 5 min or so, can be customized though).<br/>

The refresh token lives a little bit longer (expires in 24 hours, also customizable). It is comparable to an authentication session. After it expires, you need a full login with username + password again.<br/>

--To get a new access token, you should use the refresh token endpoint /api/token/refresh/ posting the refresh token:<br/>
Ex - http post http://127.0.0.1:8000/api/token/refresh/ refresh="Put previous refresh token here"<br/>


# Post API 1 endpoint that allows users to see wallet details.
	request
	{
	    "username": "ankur1",
	    "password": "root"
	}
	response
	{
    "id": 29,
    "username": "ankur1"
	}
Ex-  http://localhost:8000/users/ <br/>


# Post API 2 endpoint that allows users to see wallet details.
	response
	{
        "id": 2,
        "balance": 40.0,
        "user_upi": "ankur@27"
    }
Ex-  http://localhost:8000/wallet_details/

# Post API 3 endpoint that allows users to be Add Amount.
    request 
    {
        "amount": ""
    }
    response
	{
	    "user_upi": "ankur@27",
	    "balance": 40.0,
	    "amount": 20,
	    "status": "Amount Added To Your Wallet Sucessfully"
	}
Ex-  http://localhost:8000/add_amount/

# Post API 4 endpoint that allows users to be Pay Amount.
    request 
    {
        "user_upi": "",
        "pay_amount": ""
    }
    response
    {
	    "sender": "ankur@27",
	    "receiver": "root@26",
	    "transaction_type": "debited",
	    "deducted_amount": 20,
	    "balance_left": 20.0
	}
Ex-  http://localhost:8000/pay_amount/ 

# Get API 5 endpoint that prints a user month wise transactions.
	response
	{
	    "user_upi": "ankur@27",
	    "user_name": "ankur",
	    "current_month_credited_amount": 60,
	    "current_month_deducted_amount": 20,
	    "wallet_balance": 40.0
	}
Ex-  http://localhost:8000/all_transactions/


# Procfile is provided to deploy on heroku


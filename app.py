# Import libraries
from flask import Flask, request, url_for, redirect, render_template

# Instantiate Flask functionality
app = Flask(__name__)

# Sample data
transactions = [
    {'id': 1, 'date': '2023-06-01', 'amount': 100},
    {'id': 2, 'date': '2023-06-02', 'amount': -200},
    {'id': 3, 'date': '2023-06-03', 'amount': 300} 
]

# Read operation: Display all transactions
@app.route("/")
def get_transactions():
    return render_template("transactions.html", transactions=transactions)

# Search feature: Search transactions with a specific maximum and minimum value.
# Route to handle the search and retrieval of transactions
@app.route("/search", methods=["GET", "POST"])
def search_transactions():

    # If the request method is a POST method
    if request.method == "POST":
        # Convert 'min_amount' and 'max_amount' values to floating-point numbers
        min = float(request.form["min_amount"]) 
        max = float(request.form["max_amount"]) 
        filtered_transactions = [
            transaction
            for transaction in transactions
            if min <= transaction["amount"] <= max
        ]
        
        # Returns the HTML template "transactions.hmtl"
        return render_template("transactions.html", transactions=filtered_transactions)
        # Returns and renders the HMTL template "search.html" as an alternative result.
    return render_template("search.html") 


# Create operation: Display add transaction form
# Route to handle the creation of a new transaction
@app.route("/add", methods=["GET", "POST"])
def add_transaction():
    if request.method == 'POST':
        try:
            # Extract the updated values from the form fields
            date = request.form['date']
            amount = float(request.form['amount'])

            # Create a new transaction object using form field values
            transaction = {
                'id': len(transactions) + 1,
                'date': date,
                'amount': int(amount)
            }

            # Append the new transaction to the transactions list
            transactions.append(transaction)

            # Redirect to the transactions list page after adding the new transaction
            return redirect(url_for("get_transactions"))

        except ValueError:
            # Handle the case where the user entered invalid numeric values
            return "Please enter valid numeric values for both 'Date' and 'Amount'."

    # If the request method is GET, render the form template to display the add transaction form
    return render_template("form.html")

# Update operation: Display edit transaction form
# Route to handle the editing of an existing transaction
@app.route("/edit/<int:transaction_id>", methods=["GET", "POST"])
def edit_transaction(transaction_id):
    # Check if the request method is POST (form submission)
    if request.method == 'POST':
        # Extract the updated values from the form fields
        date = request.form['date']            # Get the 'date' field value from the form
        amount = int(request.form['amount']) # Get the 'amount' field value from the form and convert it to a float

        # Find the transaction with the mathcing ID and update its values
        for transaction in transactions:
            if transaction['id'] == transaction_id:
                transaction['date'] = date      # Update the 'date' field of the transaction
                transaction['amount'] = amount  # Update the 'amount' field of the transaction
                break                           # Exit the loop once the transaction is found and updated

        # Redirect to the transactions list page after updating the transaction
        return redirect(url_for("get_transactions"))
    
    # If the request method is GET, find the transaction with the matching ID and render the edit form
    for transaction in transactions:
        if transaction['id'] == transaction_id:
            # Render the edit form template and pass the transaction to be edited
            return render_template("edit.html", transaction=transaction)

    # If the transaction with the specifed ID is not found, hanlde this case
    return {"mesage": "Transaction not found"}, 404


# Delete operation: Delete a transaction
# Route to handle the deletion of an existing transaction
@app.route("/delete/<int:transaction_id>")
def delete_transaction(transaction_id):
    # Find the transaction with the matching ID and remove it form the list
    for transaction in transactions:
        if transaction['id'] == transaction_id:
            transactions.remove(transaction) # Delete the transaction from the transactions list
            break # Exit the loop once the transaction is found and remove.

    # Redirect to the transactions list page after deleting the transaction
    return redirect(url_for("get_transactions"))

# Balance feature: Calculates and displays the total balance of all transactions.
# Route to handle the total balance of all transactions
@app.route("/balance")
def total_balance():
    # Initializes the 'balance' variable to accumilate the total transaction amounts.
    balance = 0

    # Intitalizes the boolean flag 'balance_flag' which becomes True if the total balance is positive
    balance_flag = False

    # Iterate through each transaction in the 'transactions' list.
    for transaction in transactions:
        # Add the transaction amount to the 'balance'.
        balance += transaction["amount"]

    # Check if the total balance is positive.
    if balance > 0:
        balance_flag = True

    # Create a formatted string for the total balance.
    total_balance = f"Total Balance: {balance}"

    # Return an HTML template, passing three variables:
    # - 'transactions' : The list of transactions (for display).
    # - 'total_balance' : The formattted total balance string.
    # - 'balance_flag': Indicates whether the balance is positive
    return render_template(
        "transactions.html",
        transactions=transactions,
        total_balance=total_balance,
        balance_flag=balance_flag,
    )

# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)

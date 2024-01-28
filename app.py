from flask import Flask, render_template, Request, redirect
import paypalrestsdk

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('landing page/index.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard/html/index.html')

@app.route('/sucess')
def sucess():
    return "Payment was successfull"

client_id = ""
client_secret= ""

# Configure PayPal
paypalrestsdk.configure({
  "mode": "sandbox", # sandbox or live
  "client_id": client_id,
  "client_secret": client_secret })

@app.route('/pay')
def pay():
    # Set up a PayPal payment
    payment = paypalrestsdk.Payment({
        "intent": "sale",
        "payer": {
            "payment_method": "paypal"},
        "redirect_urls": {
            "return_url": "http://localhost:5000/success",
            "cancel_url": "http://localhost:5000/"},
        "transactions": [{
            "item_list": {
                "items": [{
                    "name": "item",
                    "sku": "item",
                    "price": "5.00",
                    "currency": "USD",
                    "quantity": 1}]},
            "amount": {
                "total": "5.00",
                "currency": "USD"},
            "description": "This is the payment transaction description."}]})

    # Create Payment
    if payment.create():
        print("Payment created successfully")
        for link in payment.links:
            if link.rel == "approval_url":
                # Convert to str to avoid Google App Engine errors
                approval_url = str(link.href)
                print("Redirect for approval: %s" % (approval_url))
                return redirect(approval_url)
    else:
        print(payment.error)
        return "Error while creating payment"

# Add additional routes for payment execution and cancellation if needed


if __name__ == '__main__':
    app.run(debug=True)

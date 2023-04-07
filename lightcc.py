import stripe
import pycardvalidator
import requests
import os

# Set up Stripe API keys
stripe.api_key = os.environ.get("STRIPE_API_KEY")
stripe.api_version = "2020-08-27"

# Function to generate a valid credit card number
def generate_credit_card_number():
    return pycardvalidator.generate()

# Function to validate a credit card number
def validate_credit_card_number(credit_card_number):
    try:
        pycardvalidator.parseString(credit_card_number)
        return True
    except:
        return False

# Function to get credit card details
def get_credit_card_details(credit_card_number):
    try:
        response = requests.get(f'https://lookup.binlist.net/{credit_card_number}')
        data = response.json()
        credit_card_details = {}
        if 'bank' in data and 'numeric' in data['bank']:
            credit_card_details['issuing_bank_number'] = data['bank']['numeric']
        if 'country' in data and 'name' in data['country']:
            credit_card_details['country'] = data['country']['name']
        if 'scheme' in data:
            credit_card_details['card_brand'] = data['scheme'].capitalize()
        if 'type' in data:
            credit_card_details['card_level'] = data['type'].capitalize()
        if 'brand' in data:
            credit_card_details['card_type'] = data['brand'].capitalize()
        return credit_card_details
    except:
        return {'error': 'Unable to retrieve credit card details'}

# Function to process a payment using Stripe
def process_payment(card_number, exp_month, exp_year, cvc, amount):
    try:
        response = stripe.PaymentIntent.create(
            amount=amount,
            currency="usd",
            payment_method_data={
                "type": "card",
                "card": {
                    "number": card_number,
                    "exp_month": exp_month,
                    "exp_year": exp_year,
                    "cvc": cvc
                }
            },
            confirm=True
        )
        if response.status == 'succeeded':
            return {'status': 'success', 'message': 'Payment successful'}
        else:
            return {'status': 'error', 'message': 'Payment failed'}
    except stripe.error.CardError as e:
        err = e.error
        return {'status': 'error', 'message': err.message}
    except Exception as e:
        return {'status': 'error', 'message': str(e)}

# Function to test payment processing using Stripe
def test_payment():
    card_number = input("Enter your credit card number: ")
    expiration_date = input("Enter your expiration date (MM/YY): ")
    exp_month, exp_year = expiration_date.split("/")
    cvc_code = input("Enter your CVV code: ")
    amount = input("Enter the payment amount: ")

    response = process_payment(card_number, exp_month, exp_year, cvc_code, amount)

    print(response['message'])

# Test the payment function
test_payment()

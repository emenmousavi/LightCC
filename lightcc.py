import random
import requests
import pycardvalidate
from faker import Faker

def generate_credit_card_number():
    """
    Generates a random valid credit card number using the pycardvalidate library.
    """
    while True:
        fake = Faker()
        credit_card_number = fake.credit_card_number(card_type=None)
        if pycardvalidate.validate(credit_card_number):
            return credit_card_number


def validate_credit_card_number(credit_card_number):
    """
    Validates a credit card number using the https://binlist.io/ API.
    """
    # Make API call to binlist.io
    session = requests.Session()
    response = session.get(f'https://api.binlist.io/validate?format=json&credit_card_number={credit_card_number}')

    # Check if API call was successful
    if response.status_code == 200:
        # Parse JSON response
        data = response.json()

        # Check if credit card is valid
        if 'valid' in data:
            return data
        else:
            return {'error': 'Unable to validate credit card number'}
    else:
        return {'error': f'Error: {response.status_code} - {response.reason}'}


def get_credit_card_details(credit_card_number):
    """
    Gets details about a credit card using the https://binlist.io/ API.
    """
    # Make API call to binlist.io
    session = requests.Session()
    response = session.get(f'https://api.binlist.io/lookup/{credit_card_number}')

    # Check if API call was successful
    if response.status_code == 200:
        # Parse JSON response
        data = response.json()

        # Build dictionary of credit card details
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
    else:
        return {'error': f'Error: {response.status_code} - {response.reason}'}


def test_payment():
    card_number = input("Enter your credit card number: ")
    expiration_date = input("Enter your expiration date (MM/YY): ")
    cvv_code = input("Enter your CVV code: ")
    amount = "1"

    # Make payment using u24.gov.ua site
    try:
        session = requests.Session()
        response = session.post('https://donate.u24.gov.ua/payment/create',
                                data={'card[number]': card_number,
                                      'card[exp_month]': expiration_date.split("/")[0],
                                      'card[exp_year]': expiration_date.split("/")[1],
                                      'card[cvc]': cvv_code,
                                      'amount': amount},
                                headers={'User-Agent': 'Mozilla/5.0'})
        if response.status_code == 200:
            response_data = response.json()
            if response_data['paid']:
                print("Payment Successful")
            else:
                print("Payment Failed")
        else:
            print("Error Occurred: HTTP Status Code ", response.status_code)
    except Exception as e:
        print("Error Occurred: ", e)

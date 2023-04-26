from faker import Faker
import requests
import braintree
import os
from dotenv import load_dotenv

def main():
    choice = main_menu()
    if choice == '1':
        validate_credit_card_number()
    elif choice == '2':
        get_credit_card_details()
    elif choice == '3':
        process_payment()
    elif choice == '4':
        return
    else:
        print("[-] Invalid choice, please try again")

def main_menu():
    print("​🇹​​🇭​​🇮​​🇸​ ​🇵​​🇷​​🇴​​🇬​​🇷​​🇦​​🇲​ ​🇲​​🇦​​🇩​​🇪​ ​🇧​​🇾​ ❝​🇪​​🇲​​🇪​​🇳​ ​🇲​​🇴​​🇺​​🇸​​🇦​​🇻​​🇮​❝")
    print("Please choose an option:")
    print("1. Validate a credit card number")
    print("2. Get credit card details")
    print("3. Process a payment using Stripe")
    print("4. Exit")
    choice = input("Enter your choice: ")
    return choice

def validate_credit_card_number():
    credit_card_number = input("Enter the credit card number to validate: ")
    if validate(credit_card_number):
        print("[+] Valid credit card number")
    else:
        print("[-] Invalid credit card number")

def get_credit_card_details(card_number):
    url = f"https://lookup.binlist.net/{card_number}"
    response = requests.get(url)

    if response.status_code == 404:
        return "Invalid card number"

    data = response.json()
    scheme = data["scheme"]
    card_type = data["type"]
    brand = data["brand"]
    country = data["country"]["name"]

    print(f"Scheme: {scheme}")
    print(f"Type: {card_type}")
    print(f"Brand: {brand}")
    print(f"Issuing country: {country}")

    expiration_date = input("Enter the expiration date (MM/YY): ")
    if not re.match(r"^\d{2}/\d{2}$", expiration_date):
        raise ValueError("Invalid expiration date format. Please enter in MM/YY format.")

    month, year = expiration_date.split("/")
    month = int(month)
    year = int(year)

    if month > 12 or month < 1:
        raise ValueError("Invalid month. Please enter a value between 01 and 12.")

    current_year = datetime.datetime.now().year % 100
    if year < current_year or year > current_year + 10:
        raise ValueError("Invalid year. Please enter a value between {current_year} and {current_year + 10}.")

    print(f"Expiration date: {month}/{year:02}")

def process_payment():
    card_number = input("Enter your credit card number: ")
    expiration_date = input("Enter your expiration date (MM/YY): ")
    exp_month, exp_year = expiration_date.split("/")
    cvv = input("Enter your CVV code: ")
    amount = input("Enter the payment amount (Write it in cents): ")

    # Load environment variables from .env file
    load_dotenv()
    
    # Prompt the user to enter their Braintree API credentials
    while True:
        merchant_id = input("Enter your Braintree Merchant ID: ")
        public_key = input("Enter your Braintree Public Key: ")
        private_key = input("Enter your Braintree Private Key: ")
        if not(merchant_id and public_key and private_key):
            print("Error: API keys are missing or incorrect. Please enter the correct values:")
            merchant_id = input("Enter your Merchant ID: ")
            public_key = input("Enter your Public Key: ")
            private_key = input("Enter your Private Key: ")
            os.environ['MERCHANT_ID'] = merchant_id
            os.environ['PUBLIC_KEY'] = public_key
            os.environ['PRIVATE_KEY'] = private_key
        try:
            gateway = braintree.BraintreeGateway(
                braintree.Configuration(
                    environment=braintree.Environment.Sandbox,
                    merchant_id=merchant_id,
                    public_key=public_key,
                    private_key=private_key
                )
            )
            break
        except Exception as e:
            print(f"[-] Error: Failed to initialize gateway with the provided API keys. {e}")
            os.environ['MERCHANT_ID'] = ''
            os.environ['PUBLIC_KEY'] = ''
            os.environ['PRIVATE_KEY'] = ''
    
    gateway = braintree.BraintreeGateway(
        braintree.Configuration(
            environment=braintree.Environment.Sandbox,
            merchant_id=merchant_id,
            public_key=public_key,
            private_key=private_key
        )
    )

    result = gateway.transaction.sale({
        "amount": amount,
        "credit_card": {
            "number": card_number,
            "expiration_date": expiration_date,
            "cvv": cvv
        }
    })

    if result.is_success:
        print("Payment processed successfully")
    else:
        print(result.message)

def validate(card_number):
    # Luhn Algorithm
    r = [int(ch) for ch in str(card_number)][::-1]
    x = sum(r[0::2]) + sum(sum(divmod(d * 2, 10)) for d in r[1::2])
    return x % 10 == 0

if __name__ == '__main__':
    main()

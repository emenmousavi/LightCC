import stripe
import pycardvalidator
import requests
import os

# Set up Stripe API keys
stripe.api_key = os.environ.get("STRIPE_API_KEY")
stripe.api_version = "2020-08-27"

def main_menu():
    print("​🇹​​🇭​​🇮​​🇸​ ​🇵​​🇷​​🇴​​🇬​​🇷​​🇦​​🇲​ ​🇲​​🇦​​🇩​​🇪​ ​🇧​​🇾​ ❝​🇪​​🇲​​🇪​​🇳​ ​🇲​​🇴​​🇺​​🇸​​🇦​​🇻​​🇮​❝")
    print("")
    print("𝕴𝖙 𝖎𝖘 𝖔𝖓𝖑𝖞 𝖋𝖔𝖗 𝖊𝖉𝖚𝖈𝖆𝖙𝖎𝖔𝖓𝖆𝖑 𝖕𝖚𝖗𝖕𝖔𝖘𝖊!")
    print("Please choose an option:")
    print("1. Generate a valid credit card number")
    print("2. Validate a credit card number")
    print("3. Get credit card details")
    print("4. Process a payment using Stripe")
    print("5. Exit")
    choice = input("Enter your choice: ")
    return choice

def generate_credit_card_number():
    return pycardvalidator.generate()

def validate_credit_card_number():
    credit_card_number = input("Enter the credit card number to validate: ")
    try:
        pycardvalidator.parseString(credit_card_number)
        print("[+] Valid credit card number")
    except:
        print("[-] Invalid credit card number")

def get_credit_card_details():
    credit_card_number = input("Enter the credit card number to get details: ")
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
        print(credit_card_details)
    except:
        print({[-] 'error': 'Unable to retrieve credit card details'})

def process_payment():
    card_number = input("Enter your credit card number: ")
    expiration_date = input("Enter your expiration date (MM/YY): ")
    exp_month, exp_year = expiration_date.split("/")
    cvc_code = input("Enter your CVV code: ")
    amount = input("Enter the payment amount: ")

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
                    "cvc": cvc_code
                }
            },
            confirm=True
        )
        if response.status == 'succeeded':
            print([+] "Payment successful")
        else:
            print("[-] Payment failed")
    except stripe.error.CardError as e:
        err = e.error
        print(err.message)
    except Exception as e:
        print(str(e))

def main():
    while True:
        choice = main_menu()
        if choice == '1':
            print(generate_credit_card_number())
        elif choice == '2':
            validate_credit_card_number()
        elif choice == '3':
            get_credit_card_details()
        elif choice == '4':
            process_payment()
        elif choice == '5':
            break
        else:
            print("[-] Invalid choice, please try again")

if __name__ == '__main__':
    main()

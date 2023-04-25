from faker import Faker
import requests
import braintree

gateway = braintree.BraintreeGateway(
  braintree.Configuration(
    environment=braintree.Environment.Sandbox,
    merchant_id='vs927kqm6855k22h',
    public_key='43dn2btstvmknb8j',
    private_key='72ded4af049dc520ba2566e5faa1d8a2'
  )
)

def main_menu():
    print("​🇹​​🇭​​🇮​​🇸​ ​🇵​​🇷​​🇴​​🇬​​🇷​​🇦​​🇲​ ​🇲​​🇦​​🇩​​🇪​ ​🇧​​🇾​ ❝​🇪​​🇲​​🇪​​🇳​ ​🇲​​🇴​​🇺​​🇸​​🇦​​🇻​​🇮​❝")
    print("")
    print("𝕴𝖙 𝖎𝖘 𝖔𝖓𝖑𝖞 𝖋𝖔𝖗 𝖊𝖉𝖚𝖈𝖆𝖙𝖎𝖔𝖓𝖆𝖑 𝖕𝖚𝖗𝖕𝖔𝖘𝖊!")
    print("Please choose an option:")
    print("1. Validate a credit card number")
    print("2. Get credit card details")
    print("3. Process a payment using Stripe")
    print("4. Exit")
    choice = input("Enter your choice: ")
    return choice

def validate_credit_card_number():
    credit_card_number = input("Enter the credit card number to validate: ")
    if Faker().credit_card_number(card_type=None) == credit_card_number:
        print("[+] Valid credit card number")
    else:
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
        print({'error': 'Unable to retrieve credit card details'})

def process_payment():
    card_number = input("Enter your credit card number: ")
    expiration_date = input("Enter your expiration date (MM/YY): ")
    exp_month, exp_year = expiration_date.split("/")
    cvv = input("Enter your CVV code: ")
    amount = input("Enter the payment amount (Write it in cents): ")

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

def main():
    while True:
        choice = main_menu()
        if choice == '1':
            validate_credit_card_number()
            break
        elif choice == '2':
            get_credit_card_details()
            break
        elif choice == '3':
            process_payment()
            break
        elif choice == '4':
            break
        else:
            print("[-] Invalid choice, please try again")

if __name__ == '__main__':
    main()

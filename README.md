# LightCC
LightCC is a Python-based tool that generates and validates credit card numbers. It also provides functionality to test payment processing and obtain details about a given credit card.

## Requirements
LightCC requires Python 3.x and the following Python packages:
- requests
- pycardvalidate
You can install these dependencies using the following command:
    ```sh
    pip install -r requirements.txt
    ```
    
## Usage
To use LightCC, you can run the script from the command line using the following command:
    ```sh
    python lightcc.py
    ```

The script will prompt you to choose from a menu of options, including generating a random credit card number, validating a credit card number, testing payment processing, and obtaining credit card details.

## Options
- Generate a random credit card number
  - This option will generate a random credit card number that is validated using the Luhn algorithm.


- Validate a credit card number
  - This option will prompt you to enter a credit card number, which will be validated using the BINList API.

- Test payment processing
  - This option will prompt you to enter a credit card number and an amount, and then submit a payment request to a test payment processing endpoint.

- Get credit card details
  - This option will prompt you to enter a credit card number and will return details about the credit card, including the card scheme, type, brand, and issuing country.

## Credits
LightCC was developed by Amin Mousavi and is licensed under the [MIT license](https://github.com/emenmousavi/LightCC/blob/main/README.md).

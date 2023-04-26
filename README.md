# LightCC
LightCC is a Python-based tool that validates credit card numbers, tests payment processing, and obtains details about a given credit card. Please note that this tool is for educational purposes only.

## Requirements
LightCC requires Python 3.x and the following Python packages:
- requests
- braintree
- faker

You can install these dependencies using the following command:
    ```
    pip install -r requirements.txt
    ```
    
## Usage
To use LightCC, you can run the script from the command line using the following command:
    ```
    python lightcc.py
    ```

The script will prompt you to choose from a menu of options, including validating a credit card number, testing payment processing, and obtaining credit card details.

## Options

- Validate a credit card number
  - This option prompts you to enter a credit card number, which will be validated using the BINList API.

- Test payment processing
  - This option prompts you to enter a credit card number and an amount, and then submits a payment request to a test payment processing endpoint.

- Get credit card details
  - This option will prompt you to enter a credit card number and will return details about the credit card, including the card scheme, type, brand, and issuing country.

## Credits
LightCC was developed by Amin Mousavi and is licensed under the [MIT license](https://github.com/emenmousavi/LightCC/blob/main/README.md).

import json

import requests
from django.conf import settings
from django.utils.html import strip_tags


class AuthorizeNet(object):
    def __init__(self, data: dict):
        self.data = data

    def charge(self):
        """
        Charge

        :return: dict
        """

        request = {
            "createTransactionRequest": {
                "merchantAuthentication": {
                    "name": settings.MERCHANT_LOGIN['authorizenet']['test'] if settings.MERCHANT_TEST_MODE else
                    settings.MERCHANT_LOGIN['authorizenet']['live'],
                    "transactionKey": settings.MERCHANT_TRANSACTION_KEY['authorizenet'][
                        'test'] if settings.MERCHANT_TEST_MODE else settings.MERCHANT_TRANSACTION_KEY['authorizenet'][
                        'live']
                },
                "transactionRequest": {
                    "transactionType": "authCaptureTransaction",
                    "amount": f"{self.data['amount']}",
                    "currencyCode": "USD",
                    "payment": {
                        "creditCard": {
                            "cardNumber": self.data['credit_card_number'],
                            "expirationDate": f"{self.data['credit_card_year']}-{self.data['credit_card_month']}",
                            "cardCode": self.data['credit_card_cvv2']
                        }
                    },
                    "lineItems": {
                        "lineItem": {
                            "itemId": "1",
                            "name": self.data['class_type'].upper(),
                            "description": self.data['description'],
                            "quantity": "1",
                            "unitPrice": f"{self.data['amount']}",
                            "taxable": False
                        }
                    },
                    "customer": {
                        "type": "individual",
                        "email": self.data['email']
                    },
                    "billTo": {
                        "firstName": self.data['credit_card_first_name'],
                        "lastName": self.data['credit_card_last_name'],
                        "address": self.data['address'],
                        "city": self.data['city'],
                        "state": self.data['state'],
                        "zip": self.data['zipcode'],
                        "country": "US",
                        "phoneNumber": self.data['phone']
                    },
                    "customerIP": self.data['ipaddress'],
                    "retail": {
                        "marketType": "0",
                        "deviceType": "8"
                    },
                    "transactionSettings": {
                        "setting": [
                            {
                                "settingName": "duplicateWindow",
                                "settingValue": "0"
                            },
                            {
                                "settingName": "emailCustomer",
                                "settingValue": True
                            }
                        ]
                    }
                }
            }
        }

        return self.get_response('post', request)

    def get_response(self, method: str, request: dict):
        """
        Response

        :param str method: get, post
        :param dict request: data

        :return: dict | None
        """

        if method == 'post':
            response = requests.post(
                self.get_url(),
                json=request
            )

            result = json.loads(response.content)['transactionResponse']

            # Something really bad is happening
            if not result.get('responseCode'):
                message = f"An internal error has occurred which is not associated with your bank. Please give us a call at {settings.PUBLIC_BUSINESS_PHONE}"

                return {
                    'error': True,
                    'message': strip_tags(message)
                }

            # Probably declined
            elif result['responseCode'] == '2' or result['responseCode'] == '3':
                if result.get('errors') is not None:
                    message = result['errors'][0]['errorText']

                    # AVS Codes
                    if result.get('avsResultCode') == 'S':
                        message += ' The card issuing bank does not support AVS.'
                    elif result.get('avsResultCode') == 'N':
                        message += ' Address: No Match and ZIP Code: No Match.'
                    elif result.get('avsResultCode') == 'A':
                        message += ' Address: Match but ZIP Code: No Match.'
                    elif result.get('avsResultCode') == 'Z':
                        message += ' Address: No Match but ZIP Code: Match.'
                    elif result.get('avsResultCode') == 'W':
                        message += ' Address: No Match but ZIP Code: Matched 9 digits.'

                    # CVV2 Codes
                    if result.get('cvvResultCode') == 'N':
                        message += ' CVV Does NOT Match.'
                else:
                    message = 'Unknown error, please call and lets figure this out.'

                return {
                    'error': True,
                    'message': strip_tags(message)
                }

            # Transaction OK
            else:
                return {
                    'error': False,
                    'result': result
                }

    @staticmethod
    def get_url():
        """
        End point URL

        :return: str
        """

        if settings.MERCHANT_TEST_MODE:
            return 'https://apitest.authorize.net/xml/v1/request.api'
        else:
            return 'https://api.authorize.net/xml/v1/request.api'

    def manual(self):
        """
        Manual Payment

        :return: dict
        """

        request = {
            "createTransactionRequest": {
                "merchantAuthentication": {
                    "name": settings.MERCHANT_LOGIN['authorizenet']['test'] if settings.MERCHANT_TEST_MODE else
                    settings.MERCHANT_LOGIN['authorizenet']['live'],
                    "transactionKey": settings.MERCHANT_TRANSACTION_KEY['authorizenet'][
                        'test'] if settings.MERCHANT_TEST_MODE else settings.MERCHANT_TRANSACTION_KEY['authorizenet'][
                        'live']
                },
                "transactionRequest": {
                    "transactionType": "authCaptureTransaction",
                    "amount": f"{self.data['amount']}",
                    "currencyCode": "USD",
                    "payment": {
                        "creditCard": {
                            "cardNumber": self.data['credit_card_number'],
                            "expirationDate": f"{self.data['credit_card_year']}-{self.data['credit_card_month']}",
                            "cardCode": self.data['credit_card_cvv2']
                        }
                    },
                    "lineItems": {
                        "lineItem": {
                            "itemId": "1",
                            "name": 'MANUAL',
                            "description": f"{self.data['description']}",
                            "quantity": "1",
                            "unitPrice": f"{self.data['amount']}",
                            "taxable": False
                        }
                    },
                    "customer": {
                        "type": "individual",
                        "email": self.data['email']
                    },
                    "billTo": {
                        "firstName": self.data['credit_card_first_name'],
                        "lastName": self.data['credit_card_last_name'],
                        "address": self.data['address'],
                        "city": self.data['city'],
                        "state": self.data['state'],
                        "zip": self.data['zipcode'],
                        "country": "US",
                        "phoneNumber": self.data['phone']
                    },
                    "customerIP": self.data['ipaddress'],
                    "retail": {
                        "marketType": "0",
                        "deviceType": "8"
                    },
                    "transactionSettings": {
                        "setting": [
                            {
                                "settingName": "duplicateWindow",
                                "settingValue": "0"
                            },
                            {
                                "settingName": "emailCustomer",
                                "settingValue": True
                            }
                        ]
                    }
                }
            }
        }

        return self.get_response('post', request)

    def payment(self):
        """
        Payment

        :return: dict
        """

        request = {
            "createTransactionRequest": {
                "merchantAuthentication": {
                    "name": settings.MERCHANT_LOGIN['authorizenet']['test'] if settings.MERCHANT_TEST_MODE else
                    settings.MERCHANT_LOGIN['authorizenet']['live'],
                    "transactionKey": settings.MERCHANT_TRANSACTION_KEY['authorizenet'][
                        'test'] if settings.MERCHANT_TEST_MODE else settings.MERCHANT_TRANSACTION_KEY['authorizenet'][
                        'live']
                },
                "transactionRequest": {
                    "transactionType": "authCaptureTransaction",
                    "amount": f"{self.data['amount']}",
                    "currencyCode": "USD",
                    "payment": {
                        "creditCard": {
                            "cardNumber": self.data['credit_card_number'],
                            "expirationDate": f"{self.data['credit_card_year']}-{self.data['credit_card_month']}",
                            "cardCode": self.data['credit_card_cvv2']
                        }
                    },
                    "lineItems": {
                        "lineItem": {
                            "itemId": "1",
                            "name": self.data['class_type'].upper(),
                            "description": f"Student Payment for {self.data['first_name']} {self.data['last_name']}",
                            "quantity": "1",
                            "unitPrice": f"{self.data['amount']}",
                            "taxable": False
                        }
                    },
                    "customer": {
                        "type": "individual",
                        "email": self.data['email']
                    },
                    "billTo": {
                        "firstName": self.data['credit_card_first_name'],
                        "lastName": self.data['credit_card_last_name'],
                        "address": self.data['address'],
                        "city": self.data['city'],
                        "state": self.data['state'],
                        "zip": self.data['zipcode'],
                        "country": "US",
                        "phoneNumber": self.data['phone']
                    },
                    "customerIP": self.data['ipaddress'],
                    "retail": {
                        "marketType": "0",
                        "deviceType": "8"
                    },
                    "transactionSettings": {
                        "setting": [
                            {
                                "settingName": "duplicateWindow",
                                "settingValue": "0"
                            },
                            {
                                "settingName": "emailCustomer",
                                "settingValue": True
                            }
                        ]
                    }
                }
            }
        }

        return self.get_response('post', request)

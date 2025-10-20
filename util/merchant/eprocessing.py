import json

import requests
from django.conf import settings
from django.utils.html import strip_tags


class Eprocessing(object):
    def __init__(self, data: dict):
        self.data = data

    def charge(self):
        """
        Charge

        :return: dict
        """

        request = {
            "ePNAccount": settings.MERCHANT_LOGIN['epn']['test'] if settings.MERCHANT_TEST_MODE else settings.MERCHANT_LOGIN['epn']['live'],
            "RestrictKey": settings.MERCHANT_TRANSACTION_KEY['epn']['test'] if settings.MERCHANT_TEST_MODE else settings.MERCHANT_TRANSACTION_KEY['epn']['live'],
            "RequestType": "transaction",
            "TranType": "Sale",
            "Total": f"{self.data['amount']}",
            "IndustryType": "E",
            "Address": self.data['address'],
            "Zip": self.data['zipcode'],
            "CardNo": self.data['credit_card_number'],
            "ExpMonth": self.data['credit_card_month'],
            "ExpYear": self.data['credit_card_year'][-2:],
            "CVV2Type": "1",
            "CVV2": self.data['credit_card_cvv2'],
            "FirstName": self.data['credit_card_first_name'],
            "LastName": self.data['credit_card_last_name'],
            "Phone": self.data['phone'],
            "Email": self.data['email'],
            "City": self.data['city'],
            "State": self.data['state'],
            "Description": self.data['description']
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

            result = json.loads(response.content)

            # Probably declined
            if result['Success'].lower() != 'y':
                if result.get('RespText') is not None:
                    message = result['RespText']

                    if result.get('AVSText') is not None:
                        message += f" - {result['AVSText']}"
                elif result.get('AVSText') is not None:
                    message = result['AVSText']
                elif result.get('CVV2Text') is not None:
                    message = result['CVV2Text']
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

        return 'https://www.eprocessingnetwork.com/cgi-bin/epn/secure/tdbe/transact.pl'

    def payment(self):
        """
        Payment

        :return: dict
        """

        request = {
            "ePNAccount": settings.MERCHANT_LOGIN['epn']['test'] if settings.MERCHANT_TEST_MODE else settings.MERCHANT_LOGIN['epn']['live'],
            "RestrictKey": settings.MERCHANT_TRANSACTION_KEY['epn']['test'] if settings.MERCHANT_TEST_MODE else settings.MERCHANT_TRANSACTION_KEY['epn']['live'],
            "RequestType": "transaction",
            "TranType": "Sale",
            "Total": f"{self.data['amount']}",
            "IndustryType": "E",
            "Address": self.data['address'],
            "Zip": self.data['zipcode'],
            "CardNo": self.data['credit_card_number'],
            "ExpMonth": self.data['credit_card_month'],
            "ExpYear": self.data['credit_card_year'][-2:],
            "CVV2Type": "1",
            "CVV2": self.data['credit_card_cvv2'],
            "FirstName": self.data['credit_card_first_name'],
            "LastName": self.data['credit_card_last_name'],
            "Phone": self.data['phone'],
            "Email": self.data['email'],
            "City": self.data['city'],
            "State": self.data['state'],
            "Description": f"Student Payment for {self.data['first_name']} {self.data['last_name']}"
        }

        return self.get_response('post', request)

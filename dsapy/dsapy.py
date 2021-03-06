import requests
import json
from xml.etree import ElementTree as ET
from dsapy.requests.dsapy_requests import DSAPIRequests
from dsapy.utils.utils import Utils

# DSpace API in Python3 #


class DSpaceAPI(object):

    def __init__(self, username, password, api_url, content_type):
        self.__username = username
        self.__password = password
        self.__api_url = api_url
        self.__api_token = None
        self.__valid_content_types = ['json', 'xml']
        self.__content_type = content_type # default content type that should be used for requested or sent data if no other is defined
        self.__connect()

    @property
    def username(self):
        """
        Return DS API username
        :return:
        """
        return self.__username

    @property
    def password(self):
        """
        Return DS API password
        :return:
        """
        return self.__password

    @property
    def api_url(self):
        """
        Return DS API URL
        :return:
        """
        return self.__api_url

    @property
    def api_token(self):
        """
        Return DS API token
        :return:
        """
        return self.__api_token

    @api_token.setter
    def api_token(self, value):
        """
        Set DS API token
        :param str value: DS API token
        :return:
        """
        self.__api_token = value

    def __connect(self):
        """
        Sends connection request to DSpace API using provided username (email) and password,
        stores DS API token in a private variable of the dsapy object.
        :returns str
        :return: DSpace API token

        """

        try:
            # in connect we use only 'json' content type

            rqst_dict = DSAPIRequests.connect(email=self.username, password=self.password)

            try:
                print("Connecting to DSpace API...")
                result = self.send_request(rqst_dict, c_type='json')
                print("Connection request returned: ", result)
                self.api_token = result['api-token']
            except Exception as e:
                print("Failed to connect to DSpace API because of the following reason: " + str(e))
                raise e

        except Exception as e:
            raise e

    def send_request(self, rqst_dict, c_type=None):
        """
        Prepares request headers, prepares request and sends it to a given DSpace API endpoint
        with given VERB (GET, POST, PUT). Correct VERB and ACTION (ENDPOINT) passed in rqst_dict.
        Output content-type can be changed using output param (default value is used if none provided).

        :param dict rqst_dict: Dictionary containing prepared request params and data.
        :param str c_type: String containg request content-type used in 'Content-Type' and 'Accept' headers
        :return request response
        """

        # set content type to default or ad hoc one
        if c_type is None:
            content_type = self.__content_type
        else:
            content_type = c_type

        if content_type not in self.__valid_content_types:
            raise ValueError('Request content-type is not valid for DSpace API: ' + content_type)

        # try to prepare headers
        try:
            print("Creating request headers...")
            headers = Utils.prepare_headers(api_token=self.__api_token, content_type=content_type)
        except Exception as e:
            raise e

        # try to prepare request
        try:
            print("Preparing request...")
            prepared_request = self.prepare_request(rqst_dict, headers)
        except Exception as e:
            raise e

        # try to send request and return result
        try:
            print("Sending request...")
            s = requests.Session()
            result = s.send(prepared_request)
        except Exception as e:
            raise e

        try:
            print("Processing response...")
            final_result = self.__process_response(result, c_type)
        except Exception as e:
            raise e

        return final_result

    def __process_response(self, result, c_type):

        print(result.url)

        if result.status_code == requests.codes.ok:
            print("Response status code: ", result.status_code)

            if c_type is 'json':
                # print("Result is: ", json.dumps(result.text))

                if str(result.url).endswith('/login'):
                    # we have to create a json string ourselves, because DSpace API returns text/plain when logging in
                    final_result = json.loads('{"api-token":"' + result.text + '"}')
                else:
                    final_result = result.json()

            elif c_type is 'xml':
                final_result = ET.fromstring(result.text)
            else:
                raise Exception('Unknown content type ' + str(c_type))
        else:
            raise Exception(result.reason)

        return final_result

    def prepare_request(self, rqst_dict, headers):
        """
        Checks if provided VERB is valid for DSpace API and check if provided ACTION is valid (e. g. not None).
        Than prepares the request object for DSpace API.

        :param dict rqst_dict: Dictionary containing prepared request params and data.
        :param dict headers: Dictionary containing prepared request headers
        :return: prepared request object
        """

        # cache request verb, action and data from request dict containing prepared request data
        verb = str(rqst_dict['verb'])
        action = str(rqst_dict['action']).lower()
        data = rqst_dict['data']

        if verb not in ['GET', 'POST', 'PUT']:
            raise ValueError('send_request: Unknown request verb ' + str(rqst_dict))

        if action is None:
            raise ValueError('send_request: Request action is None.')

        req = requests.Request(method=verb, url=self.__api_url + '/' + action, headers=headers,
                               data=data)
        prepared = req.prepare()

        # pretty-print prepared request
        Utils.pretty_print_req(prepared)

        return prepared

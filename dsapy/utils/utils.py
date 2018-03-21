import json
import xml.etree.ElementTree as ET


class Utils(object):

    @staticmethod
    def prepare_headers(api_token, content_type):
        """
        Prepares DSpace headers based on provided DSpace API token and request content-type.

        Check if DSpace API token is None and replaces in with correct 'null' value if it is
        (this should only be true when connecting to DSpace API).
        Then, headers dictionary is created.

        Without DSpace API token some requests might not work.

        :param api_token:
        :param content_type:
        :return:
        """
        if api_token is None:
            api_token = 'null'

        headers = {'rest-dspace-token': str(api_token),
                   'accept': 'application/' + content_type,
                   'Accept-Charset': 'UTF-8',
                   'Content-Type': 'application/' + content_type}

        return headers

    @staticmethod
    def pretty_print_req(req):
        """
        Pretty prints prepared request.

        Credits: AntonioHerraizS
        (https://stackoverflow.com/questions/20658572/python-requests-print-entire-http-request-raw)

        """
        print('{}\n{}\n{}\n\n{}'.format(
            '-----------START-----------',
            req.method + ' ' + req.url,
            '\n'.join('{}: {}'.format(k, v) for k, v in req.headers.items()),
            req.body,
        ))

    @staticmethod
    def get_item_id_from_metadata(metadata):
        """
        Parses DSpace item's id from response on 'get_items_metadata' request.

        Tries to decode metadata as JSON object and parse item's id from resulting dictionary.
        If it fails to do so, method tries to parse metadata as XML using ElementTree and find item's id
        in resulting ElementTree.

        :raises Exception: if metadata is None
        :raises ValueError if metadata cannot be decoded as JSON

        :param str metadata: metadata return from request in a string

        :returns: str
        :return: DSpace item's id
        """

        if metadata is None:
            raise Exception('Item metadata cannot be None.')

        try:
            print("Trying to get item_id from JSON metadata.")
            data = json.loads(metadata)
            item_id = data['id']
        except ValueError as e:
            print("get_item_id_from_metadata: Metadata cannot be decoded as JSON.")
            print(e)

            # try XML instead
            try:
                print("Trying to get item_id from XML metadata.")
                data = ET.fromstring(metadata)
                item_id = data.find('id').text
            except Exception as e:
                print('get_item_id_from_metadata: Metadata cannot be parsed as XML Tree.')
                raise e

        return item_id

    @staticmethod
    def valid_metadata_entry(metadata_entry):
        """
        Checks if DSpace metadataEntry object is valid or not.

        DSpace metadataEntry object is a list of dictionaries. If metadata_entry is not a valid instance of a list;
        method returns False. If metadata_entry is a list, method checks if every item in a metadata_entry list
        is an instance of a dictionary. Returns False when it encounters item that is not a dictionary.
        Otherwise returns True.

        :param list metadata_entry: list of dictionaries containing DSpace item's metadata stored
        in separate dictionaries

        :returns bool
        :return: True / False
        """

        if not isinstance(metadata_entry, list):
            print('valid_metadata_entry: metadata_entry has to be an instance of a list')
            return False

        # check if metadata_entry contents is entirely made of dictionaries
        for entry in metadata_entry:
            if not isinstance(entry, dict):
                print('valid_metadata_entry: metadata_entry must contain only instances of a dictionary')
                return False

        return True

    @staticmethod
    def get_metadata_value(metadata, field_name):

        if not isinstance(metadata, list):
            print('get_metadata_value: metadata object passed to get_metadata_value has to be an instance of a list')
            raise Exception('get_metadata_value: metadata object passed to '
                            'get_metadata_value has to be an instance of a list')

        found_values = list()

        for metadata_dict in metadata:
            key = metadata_dict['key']
            value = metadata_dict['value']
            language = metadata_dict['language']

            # check if currently processed metadata field is the same as requested field
            if key == field_name:
                # check if value is not 'empty', continue to next metadata dict if it is
                if value == '':
                    continue
                else:
                    # store found values of the requested metadata field
                    found_values.append(value)

            else:
                continue
        # returns list of found values (usable for searching for singular metadata field or multiple repeating fields)
        # or an empty list
        return found_values



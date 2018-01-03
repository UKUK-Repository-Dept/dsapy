from dsapy.utils.utils import Utils
import json


class DSAPIRequests(object):

    def __init__(self):
        self.api_token = None

    @staticmethod
    def connect(email, password):
        """
        Prepares data for 'connect' request

        :param email: DSpace e-person identifier
        :param password: DSpace e-person password
        :returns: dict

        :return: Dictionary with request VERB, ACTION and DATA
        """
        data_dict = {'email': email, 'password': password}

        VERB = 'POST'
        ACTION = 'login'
        DATA = json.dumps(data_dict)

        rqst_data = {'verb': VERB, 'action': ACTION, 'data': DATA}

        return rqst_data

    @staticmethod
    def status():
        """
        Prepares data for 'status' request


        :returns: dict
        :return: Dictionary with request VERB, ACTION and DATA
        """
        data_dict = {}

        VERB = 'GET'
        ACTION = 'status'
        DATA = json.dumps(data_dict)

        rqst_data = {'verb': VERB, 'action': ACTION, 'data': DATA}

        return rqst_data

    @staticmethod
    def get_items_metadata(item_handle, item_id=None):
        """
        Prepares data for 'get_items_metadata' request

        Defaults to using DSpace item's handle, but can prepare data for request using DSpace item's id as well

        :param item_handle: DSpace item's handle
        :param item_id: DSpace item's id (defaults to None)
        :returns: dict
        :return: Dictionary with request VERB, ACTION and DATA
        """

        if item_handle is None and item_id is None:
            raise Exception('get_items_metadata: item_handle or item_id must have a value.')

        data_dict = {}
        VERB = 'GET'
        DATA = json.dumps(data_dict)

        if item_handle is None:
            ACTION = 'items/' + item_id + '/metadata'
        else:
            ACTION = 'handle/' + item_handle + '?expand=metadata'

        rqst_data = {'verb': VERB, 'action': ACTION, 'data': DATA}

        return rqst_data

    @staticmethod
    def edit_items_metadata(item_id, metadata_entry):
        """
        Prepares data for 'edit_items_metadata' request. Can only use DSpace item's id,
        DSpace doesn't provide any endpoint for editing item's metadata using item's handle.

        :param int item_id: DSpace item's id
        :param list metadata_entry: list of dictionaries containg 'key', 'value' and 'lang' keys representing item's
        metadata that are about to be changed

        :returns dict
        :return: Dictionary with request VERB, ACTION and DATA
        """

        if item_id is None:
            raise Exception('edit_items_metadata: item_id is None!')

        if metadata_entry is None:
            raise Exception('edit_items_metadata: metadata_entry is None!')

        if not Utils.valid_metadata_entry(metadata_entry):
            raise Exception('edit_items_metadata: metadata_entry is not valid!')

        print("edit_items_metadata: Metadata to edit:")
        print(metadata_entry)

        # FIXME: We only assume, that metadata entry is a JSON serializable object
        # FIXME: We have to implement XML serializable object as well
        try:
            DATA = json.dumps(metadata_entry)
        except ValueError as e:
            print("Metadata object cannot be decoded as JSON.")
            raise e

        VERB = 'PUT'
        ACTION = 'items/' + str(item_id) + '/metadata'

        rqst_data = {'verb': VERB, 'action': ACTION, 'data': DATA}

        return rqst_data


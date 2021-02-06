class BAAdaptor:
    """
    Constructor for BAAdaptor class.

    Parameters:
        self: represents this object, implicit (i.e. do not provide when calling constructor)
        api_key: the api key that should be used to connect to Watson Assistant

    Returns:
        A BAAdaptor object
    """
    def __init__(self, api_key):
        self.api_key = api_key

        #Code here to activate the IBM SDK

    """
    This function takes a message from the client and forwards it to Watson Assistant.
    It returns the response from Assistant in plain text.

    Parameters:
        message: type string

    Returns:
        string response from Assistant
    """
    def send_message(self, message):
        return "Response for: {}".format(message)

import json
from ibm_watson import AssistantV2
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

class BAAdaptor:
    """
    Constructor for BAAdaptor class.
    Parameters:
        self: represents this object, implicit (i.e. do not provide when calling constructor)
        apikey: the api key that should be used to connect to Watson Assistant
        url: the URL for the selected service instance of Watson Assistant
        version: release date of the API version
        assistant_id: unique identifier of the assistant. To find the assistant ID in the Watson Assistant user interface, open the assistant settings and click API Details.
    Returns:
        A BAAdaptor object
    """
    def __init__(self, apikey="k807A1MFQ6vbDudj63UuAmfzPSm4unFC06TqL2jAgW79", version="2020-09-24",
                 url="https://api.us-south.assistant.watson.cloud.ibm.com/instances/cdd03f40-a761-4adb-86c4-4ef7bb8dee44",
                assistant_id="df24dd6d-cb30-4950-94c8-70c7b641ba25"):
        #Activate the IBM SDK
        self.apikey = apikey
        self.version = version
        self.url = url
        self.assistant_id = assistant_id

        self.authenticator = IAMAuthenticator(self.apikey)
        self.assistant = AssistantV2(
            version=self.version,
            authenticator=self.authenticator
        )

        #Get session
        response = self.assistant.create_session(
            assistant_id=self.assistant_id
        ).get_result()

        self.session_id = response['session_id']

        self.assistant.set_service_url(self.url)

    """
    This function takes a message from the client and forwards it to Watson Assistant.
    It returns the response from Assistant in plain text.
    Parameters:
        message: type string
        confidence_threshold: controls the threshold at which we reject the response from Watson Assistant
    Returns:
        response : type depending on the response_type (only supports "text" and "options" as well as "UNDEF" as of now)
        response_type : type string; the type of response
    """
    def send_message(self, message, confidence_threshold=0.5):
#         return "Response for: {}".format(message)

        response = self.assistant.message(
            assistant_id=self.assistant_id,
            session_id = self.session_id,
            input={
                'message_type': 'text',
                'text': message
            }
        ).get_result()

        print(response)

        intent, confidence, response, response_type = self.__read_response(response)

        print(response)

        if response == '':
            response = "I'm sorry but Bindər™ is not recognizing your question, could you try rephrasing it?"
            response_type = "UNDEF"

        if confidence < confidence_threshold:
            response = "bin·dər™ Advisor doesn't understand. Please try rephrasing."
            response_type = "UNDEF"

        return response, response_type

    """
    Private helper function
    This function takes a message from the Watson Assistant.
    It returns the clean version of response.
    Parameters:
        response: type dict; from Assistant
    Returns:
        tuple of intent, confidence, text, response_type
    """
    def __read_response(self, response):
      intent = None
      confidence = 0
      text = None
      response_type = None


      # if len(response['output']['intents'])>0:
      #   intent = response['output']['intents'][0]['intent']
      #   confidence = response['output']['intents'][0]['confidence']
      #   response_type = response['output']['generic'][0]['response_type']
      #
      #   if response_type == 'text':
      #       text = response['output']['generic'][0]['text']
      #
      #   elif response_type == 'option':
      #       text = {item['label']:item['value']['input']['text'] for item in response['output']['generic'][0]['options']}

      confidence = 1
      text = response['output']['generic'][0]['text']

      return intent, confidence, text, response_type

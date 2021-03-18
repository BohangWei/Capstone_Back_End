import json
from ibm_watson import LanguageTranslatorV3
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

class LAAdaptor:
    """
    Constructor for LAAdaptor class.
    Parameters:
        self: represents this object, implicit (i.e. do not provide when calling constructor)
        apikey: the api key that should be used to connect to Language Translator
        url: the URL for the selected service instance of Language Translator
        version: release date of the API version
    Returns:
        An LAAdaptor object
    """
    def __init__(self, apikey="IOHAtZJVnwQQexRl4lY843R7U__EQ7FKmVumcHYy9gcq", version="2018-05-01", 
                 url="https://api.us-south.language-translator.watson.cloud.ibm.com/instances/7728a5f8-ee9a-4f1b-9333-ea843619f28e"):
        #Activate the IBM SDK
        self.apikey = apikey
        self.version = version
        self.url = url

        self.authenticator = IAMAuthenticator(self.apikey)
        self.language_translator = LanguageTranslatorV3(
            version=self.version,
            authenticator=self.authenticator
        )

        self.language_translator.set_service_url(self.url)

    """
    This function takes a message from the client and forwards it to Language Translator service center.
    It returns the response from LT in plain text format.
    Parameters:
        message: type string
        language: type string (specify the target language)
                  Currently supports: French, Spanish, Chinese, Korean, Japanese and Hindi.
    Returns:
        translation : translated text
    """
    def send_message(self, message, language):
#         return "Response for: {}".format(message)

        mode = 'en-'+ self.list_language()[language]

        translation = self.language_translator.translate(
            text=message,
            model_id=mode).get_result()

        translation = translation["translations"][0]["translation"]
        
         
        return translation

    """
    Helper function listing currently supported languages.
    Returns:
        language_list : dict(key: language, value: language code)
    """
    def list_language(self):
      language_list = {"English":"en","French":"fr","Spanish":"es","Chinese":"zh","Korean":"ko","Japanese":"ja","Hindi":"hi"}
      return language_list

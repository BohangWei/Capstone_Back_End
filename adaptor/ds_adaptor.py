import json
from ibm_watson import DiscoveryV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

class DSAdaptor:

    def __init__(self,
                 apikey="CRCpWPVX8KuBOo_0jw76zzl2_KlR9Kx4UwdWU0n88QOo",
                 version="2019-04-30",
                 url="https://api.us-east.discovery.watson.cloud.ibm.com/instances/c5075c20-9dfd-4e80-9a5b-497a7e6701cd",
                 environment_id="f79a2e4f-7bc2-42ac-8c17-882973120045",
                 collection_id="5830fd57-758e-4966-b1c6-4ecd79924bcb"
                ):
        #Activate the IBM SDK
        self.apikey = apikey
        self.version = version
        self.url = url
        self.environment_id = environment_id
        self.collection_id = collection_id

        self.authenticator = IAMAuthenticator(self.apikey)

        self.discovery = DiscoveryV1(
            version=self.version,
            authenticator=self.authenticator
        )

        self.discovery.set_service_url(url)


    def send_result(self, term):

        c_id, search_term = self.__extract_keyterm(term)
        found = False
        subtitle = ""
        infos = ""
        results = self.discovery.query(environment_id=self.environment_id, collection_id=c_id, filter=search_term).get_result()

        if c_id=="5830fd57-758e-4966-b1c6-4ecd79924bcb":
            if len(results["results"]) != 0:
                course = results["results"][0]

                if "subtitle" in course:
                    subtitle = "Course Name: " + course["subtitle"][0]
                if "answer" in course:
                    if len(course["answer"])!=0:
                        infos = '; '.join(course["answer"])
                    else:
                        infos = "There are no specific requirements to enter the course"
                else:
                    infos = "There are no specific requirements to enter the course"
                found = True


        elif c_id=="ba8557e9-561c-474f-aef7-7b10824de122":
            if len(results["results"]) != 0:
                if search_term.startswith("subtitle:"):
                    instructors = []
                    subtitle = "Here are the instructors who teaches/taught the course: "
                    for result in results["results"]:
                        if "title" in result:
                            instructors.append(result["title"][0])
                            infos = ', '.join(instructors)
                elif search_term.startswith("title"):
                    instructors = []
                    feedbacks = []
                    subtitle = "I found the following instructor(s) with some student feedback: "
                    for result in results["results"]:
                        if "title" in result:
                            instructor = result["title"][0]
                            infos = infos + "Instructor Name: " + instructor + "\n"
                        if "answer" in result:
                            feedback = result["answer"][0]
                            infos = infos + feedback + "\n"
                found = True
        return found, subtitle, infos

    def __extract_keyterm(self, term):
        buffer = term.split(' ')
        c_id = buffer[1]
        search_term = buffer[2]
        return c_id, search_term

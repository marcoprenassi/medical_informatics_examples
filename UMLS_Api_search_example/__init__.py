import UMLS_Api_search_example.GUI
import UMLS_Api_search_example.UMLSAPI


def runExample(api_key):
    umls_api_object = UMLS_Api_search_example.UMLSAPI.UMLSAPI(api_key=api_key)
    UMLS_Api_search_example.GUI.GUI(umls_api_object)
    # search_term = input('Insert search term: ')
    # umls_api_object.search(search_term=search_term)
    # print(umls_api_object)

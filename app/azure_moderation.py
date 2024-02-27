import os
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from azure.core.exceptions import HttpResponseError
from azure.ai.contentsafety.models import AnalyzeTextOptions
from dotenv import load_dotenv
load_dotenv()

def azure_text_moderation(mod_text):
    """This function will take the message and send it to the azure content safety api
        This will return a value 0-7 the higher the number the more severe
    """
    endpoint = os.environ["endpoint"]
    print(endpoint)
    key=os.environ["azure_token"]
    print(mod_text)
    client = ContentSafetyClient(endpoint, AzureKeyCredential(key))

    request= AnalyzeTextOptions(text=mod_text)

    try:
        response = client.analyze_text(request)
    except HttpResponseError as e:
        print("Analyze image failed.")
        if e.error:
            print(f"Error code: {e.error.code}")
            print(f"Error message: {e.error.message}")
            raise
        print(e)
        raise
    result = []
    print(response)
    for cat in response['categoriesAnalysis']:
        if cat.category == 'Hate' and cat.severity >= 2:
            # print(f"Hate severity: {response.hate_result.severity}")
            result.append({"severity": cat.severity, "type": "Hate"})
        if cat.category == 'SelfHarm' and cat.severity >= 2:
            # print(f"SelfHarm severity: {response.self_harm_result.severity}")
            result.append({"severity": cat.severity, "type": "SelfHarm"})
        if cat.category == 'Sexual' and cat.severity >= 2:
            # print(f"Sexual severity: {response.sexual_result.severity}")
            result.append({"severity": cat.severity, "type": "Sexual"})
        if cat.category == 'violence' and cat.severity >= 2:
            # print(f"Violence severity: {response.violence_result.severity}")
            result.append({"severity": cat.severity, "type": "Violence"})
    return result

# Originally there was functionality for both GCP and Azure in this bot
# Please use this module if you wish to use GCP
import os
from google.cloud import language_v1
from dotenv import load_dotenv

load_dotenv()

async def gcp_text_moderation(mod_text):
    """This function will send the message to GCP to be checked"""
    key = os.environ["gcp_key"]
    project = os.environ["gcp_project"]
    client = language_v1.LanguageServiceClient(
        client_options={"api_key": key, "quota_project_id": project}
    )
    document = language_v1.Document(content = mod_text, type_=language_v1.Document.Type.PLAIN_TEXT)
    request = language_v1.ModerateTextRequest(
        document=document,
    )
    response = client.moderate_text(request=request)
    moderate = []
    for res in response.moderation_categories:
        if res.confidence > 0.5:
            moderate.append({"name": res.name, "confidence": res.confidence})
    print(moderate)
    return moderate

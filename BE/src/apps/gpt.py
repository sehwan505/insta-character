import requests
from utils.util import config
import openai
from typing import List

# set credentials
secrete_key = config["openai_secret_key"]
openai.api_key = secrete_key

from openai.embeddings_utils import cosine_similarity, get_embedding
# function for classifcation of texts with embedding function in openai
def classfy_text(texts: List[str]):    
    labels = ['extrovert', 'introvert', "planned", "improvised"]
    model = "text-embedding-ada-002"
    label_embeddings = [(label, get_embedding(label, engine=model)) for label in labels]
    
    def label_score(review_embedding, label_embeddings):
        similaritys = {label: cosine_similarity(review_embedding, label_embedding) for label, label_embedding in label_embeddings}
        return max(similaritys, key=similaritys.get)
    
    return label_score(texts, label_embeddings)
import requests
from utils.util import config
import openai
from collections import Counter
from typing import List

# set credentials
secrete_key = config["openai_secret_key"]
openai.api_key = secrete_key

from openai.embeddings_utils import cosine_similarity, get_embedding
# function for classifcation of texts with embedding function in openai
def classfy_text(texts: List[str]):
    labels = ['extrovert', 'introvert', "judging", "perceiving", "emotional", "rational", "sensing", "intuitive"]
    model = "text-embedding-ada-002"
    label_embeddings = [(label, get_embedding(label, engine=model)) for label in labels]
    def label_score(review, label_embeddings):
        review_embedding = get_embedding(review, engine=model)
        similaritys = {label: cosine_similarity(review_embedding, label_embedding) for label, label_embedding in label_embeddings}
        return max(similaritys, key=similaritys.get)
    
    return Counter([label_score(text, label_embeddings) for text in texts])
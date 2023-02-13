import requests
from utils.util import config
import openai
from collections import Counter
from typing import List

# set credentials
openai.api_key = config["openai_secret_key"]

from openai.embeddings_utils import cosine_similarity, get_embedding
# function for classifcation of texts with embedding function in openai
def classfy_text(texts: List[str]):
    labels = [['extrovert', 'introvert'],
            ['sensing', 'intuitive'],
            ['thinking', 'feeling'],
            ['judging', 'perceiving']]
    model = "text-embedding-ada-002"
    label_embeddings = [[(label[0], get_embedding(label[0], engine=model)), (label[1], get_embedding(label[1], engine=model))] for label in labels]
    def label_score(review, label_embeddings):
        review_embedding = get_embedding(review, engine=model)
        mbti = []
        for label in label_embeddings:
            score = cosine_similarity(review_embedding, label[0][1]) - cosine_similarity(review_embedding, label[1][1])
            if score > 0:
                mbti.append(label[0][0])
            else:
                mbti.append(label[1][0])
        return mbti
    
    result = Counter([])
    for text in texts:
        result.update(label_score(text, label_embeddings))
    return get_first_char_up_to_4th(result)

# function for getting the first char in each word which have highest value in dictionary
def get_first_char_up_to_4th(d):
    return ''.join([k[0] for k, v in d.items()])[0:4].upper()
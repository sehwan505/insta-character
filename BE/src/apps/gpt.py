import requests
from utils.util import config
import openai
from collections import Counter
from typing import List
import json

# set credentials
openai.api_key = config["openai_secret_key"]

from openai.embeddings_utils import cosine_similarity, get_embedding
# function for classifcation of texts with embedding function in openai
# label을 좀 더 길게 만들어볼 필요가 있다.
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
            print(label[0][0], label[1][0], score)
            if score > 0:
                mbti.append(label[0][0])
            else:
                mbti.append(label[1][0])
        return mbti
    
    result = Counter([])
    for text in texts:
        result.update(label_score(text, label_embeddings))
    return get_mbti_from_counter(result, labels)

# function for getting the first char in each word which have highest value in dictionary
def get_mbti_from_counter(counter: Counter, labels: List[List[str]]) -> str:
    def add_more_frequent_char(result: str, s1: str, s2: str) -> str:
        if counter[s1] > counter[s2]:
            return s1[0].upper()
        else:
            return s2[0].upper()
    
    result = ""
    for s1, s2 in labels:
        result += add_more_frequent_char(result, s1, s2)
    return result


# 상황을 주는 것을 추가
def generate_description_with_3words(mbti, print_output=False):
    user_text = f"3 words which {mbti} person would use to describe themselves"
    completion = openai.Completion.create(
        engine='text-davinci-003',  
        temperature=1,           
        prompt=user_text,           # What the user typed in
        max_tokens=100,             # Maximum tokens in the prompt AND response
        n=1,                        # The number of completions to generate
        stop=None,                  # An optional setting to control response generation
    )

    return completion

def generate_react_about_given_situation(mbti, given_situation=None):
    user_text = f"if {mbti} person is in this situation, what would they say?\n {given_situation}"
    completion = openai.Completion.create(
        engine='text-davinci-003',  
        temperature=1,           
        prompt=user_text,           # What the user typed in
        max_tokens=100,             # Maximum tokens in the prompt AND response
        n=1,                        # The number of completions to generate
        stop=None,                  # An optional setting to control response generation
    )

    return completion

def classfy_text_with_completion(texts: List[str]):
    user_text = "\nClassify user's mbti type with these tweets\n MBTI type:"
    user_text += "\n".join(texts)
    completion = openai.Completion.create(
        engine='text-davinci-003',
        temperature=0,           
        prompt=user_text,          
        max_tokens=60,
        top_p=1
    )
    mbti_types = ["INFP", "INFJ", "INTP", "INTJ", "ISTP", "ISTJ", "ISFJ", "ISFP", "ENFP", "ENFJ", "ENTP", "ENTJ", "ESTP", "ESTJ", "ESFJ", "ESFP"]
    for mbti in mbti_types:
        if mbti in completion['choices'][0]['text']:
            return mbti
    return "not clear"

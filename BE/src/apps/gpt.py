import requests
from utils.util import config
import openai

# set credentials
secrete_key = 'YOUR_SECRETE_KEY'
openai.api_key = secrete_key

# Upload file
openai.File.create(file=open("training.jsonl"),
                   purpose="classifications")

# function call classfication function of openai api
def classfy_text(text):
    response = openai.Classification.create(
        search_model="ada",
        model="curie:ft-xlnet-base-cased",
        query=text,
        examples=[
            ["", "positive"],
            ["", "negative"],
            ["", "neutral"],
        ],
        file=openai.File.retrieve("YOUR_FILE_ID"),
        labels=["positive", "negative", "neutral"],
        label="positive",
        examples_context="text",
        max_examples=1000,
        return_prompt_text=True,
    )
    return response
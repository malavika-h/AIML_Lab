from django.shortcuts import render
import requests
import json
from django.http import JsonResponse
import torch
from transformers import AutoTokenizer, AutoModelWithLMHead
from newspaper import fulltext
from goose3 import Goose
from requests import get
from newspaper import Article
import requests
from newsdataapi import NewsDataApiClient

# tokenizer = AutoTokenizer.from_pretrained("mrm8488/t5-base-finetuned-summarize-news")
# model = AutoModelForSeq2SeqLM.from_pretrained("mrm8488/t5-base-finetuned-summarize-news")
tokenizer=AutoTokenizer.from_pretrained('flax-community/t5-base-cnn-dm')
model=AutoModelWithLMHead.from_pretrained('flax-community/t5-base-cnn-dm', return_dict=True)

countries = { 'au': 'Australia', 
'be': 'Belgium', 'ca': 'Canada', 
'ch': 'Switzerland', 'cn': 'China',
'de': 'Germany', 'eg': 'Egypt', 'fr': 'France', 
'gb': 'United Kingdom', 'hk': 'Hong Kong', 'hu': 'Hungary', 
'id': 'Indonesia', 'ie': 'Ireland',
'il': 'Israel', 'in': 'India',
'it': 'Italy', 'jp': 'Japan',
'kr': 'South Korea', 'lt': 'Lithuania',
'lv': 'Latvia','mx': 'Mexico', 'my': 'Malaysia', 
'nl': 'Netherlands', 'no': 'Norway', 'nz': 'New Zealand',
'ph': 'Philippines', 'pl': 'Poland',
'pt': 'Portugal', 'ro': 'Romania',
'rs': 'Serbia', 'ru': 'Russia',
'sa': 'Saudi Arabia', 'se': 'Sweden',
'sg': 'Singapore','sk': 'Slovakia', 'th': 'Thailand',
'tr': 'Turkey','ua': 'Ukraine', 'us': 'United States',
've': 'Venezuela', 'za': 'South Africa'}

api = NewsDataApiClient(apikey="pub_26427ca5bbdf746716578bc143d47ae5f1c48")

def index(req):
    allNews = api.news_api(language='en')
    print(type(allNews))
    res = allNews
    i=0
    for r in res['results']:
        if r['creator'] == None: r['creator'] = 'Unknown'
        if r['image_url'] == None: r['image_url'] = 'Unknown'
        if r['description'] == None: r['description'] = 'Unknown'
        if r['content'] == None: 
            r['content'] = 'Unknown'
        else:
            t = summarize(r['content'])
            r['content'] = t
    return render(req, 'index.html', {'res': res, 'cou': countries.items()})

# def summarize(text, max_length=3000):
#   input_ids = tokenizer.encode(text, return_tensors="pt", add_special_tokens=True)
#   generated_ids = model.generate(input_ids=input_ids, num_beams=2, max_length=max_length,  repetition_penalty=2.5, length_penalty=1.0, early_stopping=True)
#   preds = [tokenizer.decode(g, skip_special_tokens=True, clean_up_tokenization_spaces=True) for g in generated_ids]
#   return preds[0]

def summarize(text):
   #input_ids = tokenizer.encode(text, truncation=True, return_tensors='pt')
   inputs=tokenizer.encode("summarize: " +text, return_tensors='pt', max_length=3000, truncation=True)
   #generated_ids = model.generate(input_ids=input_ids, num_beams=4, max_length=75, early_stopping=True)
   output = model.generate(inputs, min_length=80, max_length=100)
   #preds = tokenizer.decode(generated_ids[0], skip_special_tokens=True, clean_up_tokenization_spaces=True)
   preds = tokenizer.decode(output[0], skip_special_tokens=True)
   return str(preds)

def query(req):
    searchRes = {}
    if req.GET:
        query = req.GET.get('query').lower()
        queryNews = api.news_api(q=query, language='en')
        searchRes = queryNews
        for r in searchRes['results']:
            if r['creator'] == None: r['creator'] = 'Unknown'
            if r['image_url'] == None: r['image_url'] = 'Unknown'
            if r['description'] == None: r['description'] = 'Unknown'
            if r['content'] == None: 
                r['content'] = 'Unknown'
            else:
                t = summarize(r['content'])
                r['content'] = t
        return render(req,'index.html', {'res': searchRes, 'cou': countries.items()})

def getCategory(req, ct):
    searchRes = {}
    catNews = api.news_api(category=ct, language='en')
    searchRes = catNews
    for r in searchRes['results']:
            if r['creator'] == None: r['creator'] = 'Unknown'
            if r['image_url'] == None: r['image_url'] = 'Unknown'
            if r['description'] == None: r['description'] = 'Unknown'
            if r['content'] == None: 
                r['content'] = 'Unknown'
            else:
                t = summarize(r['content'])
                r['content'] = t
    return render(req,'index.html', {'res': searchRes, 'cou': countries.items()})

def getCountry(req, cid):
    searchRes = {}
    countriesNews = api.news_api(country=cid, language='en')
    searchRes = countriesNews
    for r in searchRes['results']:
            if r['creator'] == None: r['creator'] = 'Unknown'
            if r['image_url'] == None: r['image_url'] = 'Unknown'
            if r['description'] == None: r['description'] = 'Unknown'
            if r['content'] == None: 
                r['content'] = 'Unknown'
            else:
                t = summarize(r['content'])
                r['content'] = t
    return render(req,'index.html', {'res': searchRes, 'cou': countries.items()})

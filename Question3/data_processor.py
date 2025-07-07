import pandas as pd
import os
import re
from config import RAW_DATA_PATH, PROCESSED_DATA_PATH
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import string
import csv

def clean_text(text):
    text = text.lower()
    text = re.sub(f'[{string.punctuation}]', '', text)
    return text

def extract_keywords(text):
    words = text.split()
    stop_words = set(stopwords.words('english'))
    words = [w for w in words if w not in stop_words]
    lemmatizer = WordNetLemmatizer()
    words = [lemmatizer.lemmatize(w) for w in words]
    return words

def process_data():
    df = pd.read_csv(RAW_DATA_PATH)
    df = df.dropna(subset=['title'])
    df['clean_title'] = df['title'].apply(clean_text)
    df['keywords'] = df['clean_title'].apply(extract_keywords)
    df.to_csv(PROCESSED_DATA_PATH, index=False)
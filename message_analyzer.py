from transformers import pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re
from proxies.LLM_proxy.gpt_chat import GPTChat
import os
from dotenv import load_dotenv

class MessageAnalyzer:
    def __init__(self):
        load_dotenv()
        self.chatgpt = GPTChat()

    def analyze_commit_message(self, commit, diff):
        commit_message = commit.message.strip()
        commit_data = dict()
        commit_data["message"] = commit_message
        response = self.chatgpt.ask_gpt_about_commit(diff, commit_data)
        return response

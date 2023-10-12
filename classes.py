import pandas as pd
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

class LyricsSearch:
    def __init__(self, csv_path):
        self.df = pd.read_csv(csv_path)
        self.vectorizer = TfidfVectorizer()
        self.all_sentences, self.song_info = self.prepare_data()
        self.tfidf_matrix = self.vectorizer.fit_transform(self.all_sentences)
        
    def prepare_data(self):
        all_sentences = []
        song_info = []
        for _, row in self.df.iterrows():
            sentences = self.split_lyrics(row['lyrics'])
            all_sentences.extend(sentences)
            song_info.extend([(row['singer'], row['song'])] * len(sentences))
        return all_sentences, song_info
    
    @staticmethod
    def split_lyrics(lyrics):
        sentences = re.split('[?.!]', lyrics)
        sentences = [s.strip() for s in sentences if s]
        return sentences
    
    def find_sentence_for_word(self, query):
        query_vector = self.vectorizer.transform([query])
        cosine_similarities = cosine_similarity(query_vector, self.tfidf_matrix).flatten()
        
        sorted_indices = np.argsort(cosine_similarities)[::-1]
        
        for idx in sorted_indices:
            lyrics = self.all_sentences[idx]
            lines = lyrics.split("\n")
            
            for line in lines:
                if query.lower() in line.lower():
                    singer, song = self.song_info[idx]
                    print(f"Singer: {singer}")
                    print(f"Song: {song}")
                    print(f"Sentence: {line}")
                    return
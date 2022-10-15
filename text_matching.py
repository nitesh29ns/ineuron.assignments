import numpy as np
import pandas as pd
import re
import nltk
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import CountVectorizer
from nltk.corpus import stopwords

cv = CountVectorizer(ngram_range=(1,3))
lemmatizer = WordNetLemmatizer()
stopwords = stopwords.words('english')

data = pd.read_csv("string_matching.xlsx")
data.drop(columns=['Unnamed: 10','Unnamed: 11','Unnamed: 12'], inplace=True)


# Extracting all the text from public study columns
public = []
for i in data['Public Title of Study']:
    text = re.sub('[^a-zA-z0-9]',' ', i)
    public.append(text.lower())

# Extracting all the text from scientific study columns
scientific = []
for i in data['Scientific Title of Study']:
        text = re.sub('[^a-zA-z0-9]',' ', i)
        scientific.append(text.lower())

# extracting all the causes
causes = []
for i in data['List of Causes']:
    if type(i) == str:
        causes.append(i.lower())

# combinding pubic and scientific column text
studys = []
for item1, item2 in zip(public, scientific):
    studys.append([item1+','+item2])

# deleting stopwords from the causes
corpus = []
for i in range(len(causes)):
    text = causes[i]
    text = text.split()
    words = [word for word in text if word not in stopwords]
    print(words)
    corpus.append(" ".join(words))


"""
This class return the dictionary containing causes_names as keys and values is list containing tuples with first element 
is index of the text present in the data and second element is who much % matched of text is matched with the causes.

"""
matched_data = {}
class text_matching:
    def cause(self, data:list):
        for i in  range(len(data)):
            text = data[i]
            cv.fit_transform([text])
            self.string_matching()
            matched_data[text] = self.matched
        
        return matched_data
            
    def string_matching(self,data=studys):
        self.matched = []
        for item in range(len(data)):
            array = cv.transform(data[item]).toarray()[0]
            a = len(cv.transform(data[item]).toarray()[0])
            same = 0
            for i in array :
                if i != 0:
                    same = same+1
            per_match = same/a*100
            if per_match != 0.0:
                #print(f"index {item} : {per_match}")
                self.matched.append((item, "%.2f" % per_match))   

test = text_matching()
test.cause(corpus)

print(matched_data)

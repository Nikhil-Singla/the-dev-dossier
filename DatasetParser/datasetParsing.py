import pandas as pd
import os
import glob
import nltk
import re
import contractions
import string

from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from bs4 import BeautifulSoup

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import Perceptron, LogisticRegression
from sklearn.svm import LinearSVC
from sklearn.naive_bayes import MultinomialNB

from sklearn.metrics import precision_score, recall_score, f1_score, accuracy_score

from bs4 import BeautifulSoup

nltk.download('wordnet', quiet=True)
nltk.download('stopwords', quiet=True)
nltk.download('punkt_tab', quiet=True)

absoluteSourcePath =  os.path.dirname(__file__)
# Finds out the path to the source code location

subFolder = os.path.join(absoluteSourcePath, "China")
# Subfolder named Chine with the dataset inside in the same location as the script

regexForDirectory = os.path.join(subFolder, "China_*.parquet")
# print(regexForDirectory), this one gets the general path into the regex for getting all dataset files

allFiles = glob.glob(regexForDirectory)  # Get all files from the global directory.
# print(allFiles), we get ALL the files into this variable

allFiles = allFiles[:20]
print(len(allFiles))

datasetFile = pd.concat([pd.read_parquet(f, engine='fastparquet') for f in allFiles], ignore_index=True)
# Used to get the dataset file name which contains the columns
# Shape = (1000000, 19)

useLessColumnList = ["postid", "application_name", "in_reply_to_postid", "in_reply_to_accountid", "follower_count", "reposted_accountid", "reposted_postid", "account_mentions"]
# Get out the useful column headings in the dataset
# usefulColumns = ["post_text", "post_language", "post_time", "accountid", "following_count", "account_creation_date", "is_repost", "hashtags", "urls", "account_profile_description", "is_control"]

inputData = datasetFile.drop(useLessColumnList, axis=1).reset_index(drop=True)
# New Shape = (1000000, 11)

print('\nThree sample reviews, along with their ratings include: \n')
print(inputData.sample(10, random_state=10), "\n")
# Getting a sample of 3 reviews to confirm workings
# TO DO: Process data to remove unknown characters and spaces, etc, Perform Contractions, Remove stopwords, perform lemmatization

allLangs = inputData['post_language'].unique()
print("Total languages are: ", allLangs)

inputData.replace(['NONE', None, ''], pd.NA, inplace=True)
inputData.dropna(inplace=True)


lemmWords = WordNetLemmatizer()
stopWords = set(stopwords.words("english"))

def clean_text(inText):
    if not isinstance(inText, str):
        return ""

    inText = BeautifulSoup(inText, "html.parser").get_text()
    inText = contractions.fix(inText)   # Removing and fixing contractions

    inText = re.sub(f"[{re.escape(string.punctuation)}]", "", inText)   # Trying to remove excess punctuations

    inText = re.sub(r'\s+', ' ', inText).strip()  # Leaving only one extra space.

    inText = inText.casefold()  # Using the lowercase that accounts for different languages and not just english 

    tokenizedList = word_tokenize(inText)  # Tokenization

    tokenizedList = [lemmWords.lemmatize(oneWord) for oneWord in tokenizedList if oneWord not in stopWords]  # Lemmatize and removing stopwords

    return " ".join(tokenizedList)

if 'post_text' in inputData.columns:
    inputData['post_text'] = inputData['post_text'].apply(clean_text)

inputData.reset_index(drop=True, inplace=True)

print("Data preprocessing complete. Sample processed data:\n")
print(inputData.sample(10, random_state=10))
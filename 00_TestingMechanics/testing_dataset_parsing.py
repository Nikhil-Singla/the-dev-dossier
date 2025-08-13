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

from bs4 import BeautifulSoup, MarkupResemblesLocatorWarning
import warnings

warnings.filterwarnings("ignore", category=MarkupResemblesLocatorWarning)

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

inputData.replace(['NONE', None, ''], pd.NA, inplace=True)
inputData.dropna(axis=0, how='any', inplace=True)

allLangs = inputData['post_language'].unique()
print("Total languages are: ", allLangs)

lemmWords = WordNetLemmatizer()
stopWords = set(stopwords.words("english"))

def clean_text(inText):
    if not isinstance(inText, str):
        return ""

    inText = BeautifulSoup(inText, "html.parser").get_text()
    if len(inText) > 1:
        try:
            inText = contractions.fix(inText)   # Removing and fixing contractions
        except IndexError:
            pass

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

X = inputData['post_text']
y = inputData['is_control']           

X_train_text, X_test_text, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

vectorizer = TfidfVectorizer(max_features=5_000)
X_train = vectorizer.fit_transform(X_train_text)
X_test  = vectorizer.transform(X_test_text)

models = {
    'LogisticRegression': LogisticRegression(max_iter=1_000),
    'LinearSVC':          LinearSVC(),
    'MultinomialNB':      MultinomialNB(),
    'Perceptron':         Perceptron(),
}

# Train & evaluate
for name, clf in models.items():
    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_test)
    
    print(f"=== {name} ===")
    print("  Accuracy: ", accuracy_score(y_test, y_pred))
    print("  Precision:", precision_score(y_test, y_pred))
    print("  Recall:   ", recall_score(y_test, y_pred))
    print("  F1:       ", f1_score(y_test, y_pred))
    print()

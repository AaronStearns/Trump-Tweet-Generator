# short script that ingests all Trump tweets from 2016 to 2018 and
# partially cleans them and splits them up into 2 word n-grams, then pushes 
# words into arrays based on matching keys
# For example: { 'middle': ['of', 'class', 'east', 'income', 'class']}

import os, json, random

os.chdir('/CHANGE/TO/YOUR/DIRECTORY/NAME')

tweets = open("tweets2016to2018.json")


tweetData = json.load(tweets)

tweetText = []

# some tweets saved main body of tweet text under 
# dict key 'text' instead of 'full_text'
def getTweetText():
    for i in range(0, len(tweetData) - 1):
        if "full_text" in tweetData[i]:
            tweetText.append(tweetData[i]['full_text'])
        elif "text" in tweetData[i]:
            tweetText.append(tweetData[i]['text'])
        else:
            continue
        
getTweetText()

############################################################

tweetWords = []

# strip certain punctuation and push individual words into tweetWords[]
def combineTweets():
    # choosing these 8 punctuation characters to remove for now
    table = str.maketrans("!?().,-\"", 8 * " ")
    for tweet in tweetText:
        # split each tweet at the word level with .split()
        for word in tweet.split():
            eachWord = word.translate(table).replace(" ", "")
            tweetWords.append(eachWord)

combineTweets()

# joining all tweet words and stripping any additional whitespace
joinedTweetWords = ' '.join(tweetWords).strip()

order = 2

theNgrams = []

def makeNGrams():
    splitText = joinedTweetWords.split()
    for i in range(0, len(splitText) - 1):
        # iterate over splitText and create n-grams
        gram = splitText[i : i + order]
        theNgrams.append(gram)
        
makeNGrams()

# d moved to outside of function - now storing values properly        
d = {}

def createArrays():
    for k, v in theNgrams:
        # takes the first item in each array of theNgrams and finds 
        d.setdefault(k, []).append(v)

createArrays()

# randomly sample one of these 4 words to kick off markov chain
# this could be changed to randomly sample any
# word from the entire corpus
commonWords = ["I", "America", "Democrats", "The"]

fullString = random.sample(commonWords, 1)

# iters for number of markov iterations
def markov(iters):
    for i in range(0, iters):
        # hard coding last val in array, but will change to use variable ('order' - length) 
        possibilities = d.get(fullString[-1][0])
        # TODO: write while loop to search for first variable 
        # without "@" or "#" or "&amp" or "https://..."
        # while:
        #   continue:
        if random.sample(possibilities, 1)[0][0] != "@" or "#" or "&amp" or "https://...":
            nextWord = random.sample(possibilities, 1)
        fullString.append(nextWord)
    print(fullString)
    
# generate tweet of length 14     
markov(14)

#TODO:
# cross-reference tweetWords with a dictionary and 
# reject non-words, words with spelling errors, URLs, @people, emojis, and hashtags


# dict structure:
#testObj = {"hate": 
#            {"sentiment": -5, 
#             "partOfSpeech": ["verb", "noun"]}
#            }
            
            

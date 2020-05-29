from django.shortcuts import render
import requests
from django.http import HttpResponse
# Create your views here.
import nltk
nltk.download('punkt')
from textblob import TextBlob
from googletrans import Translator
translator = Translator()
from urllib.request import urlopen
import json
import re


def analysis(data):

    text = data

    sentence = text.replace('।','.')
    
    sentence = sentence.split('.')
    

    en_sent = translator.translate(text).text
    en_split = en_sent.split('.')
    
    polarity_data = []
    sentence_data = []
    rating = 0

    for i, val in enumerate(en_split):
        tb = TextBlob(val)
        # print("Polarity of Sentence [" + str(i+1) + "] = ", end="")
        sentiment = tb.sentiment.polarity
        # print(sentence[i] ,sentiment, end="")
        
        polarity_data.append(round(sentiment*100))
        
        rating+=sentiment
        
        try:
        #    sentence_data.append(sentence[i]+' '+str(round(sentiment*100)))
           data_obj = {'text':sentence[i],'score':str(round(sentiment*100))}
        except IndexError:
            data_obj = {'text':'','score':''}
        
        sentence_data.append(dict(data_obj))
       
    # sentence_data.pop()
    if len(en_split)==1:
        # rating = len(en_split)
        rating = round((rating/(len(en_split)))*100)
    else:
        rating = round((rating/(len(en_split)-1))*100)
    
    
    return sentence_data,polarity_data,rating

def analyser(request):
    sdata,pdata,rating='','',0
    if request.method == 'POST':
        parsed = request.POST['indata']
        
        
        # parsed = parsed+'।'


        sdata,pdata,rating = analysis(parsed)

 
    return render(request,"index.html",{'sdata': sdata, 'pdata': pdata, 'rating': rating})


def analysisYoutube(data):

    text = data

    sentence = text.replace('।','.')
    
    sentence = sentence.split('.')
    

    en_sent = translator.translate(text).text
    en_split = en_sent.split('.')
    
    polarity_data = []
    sentence_data = []
    rating = 0
    leng_div= 1

    for i, val in enumerate(en_split):
        tb = TextBlob(val)
        # print("Polarity of Sentence [" + str(i+1) + "] = ", end="")
        sentiment = tb.sentiment.polarity
        # print(sentence[i] ,sentiment, end="")
        
        polarity_data.append(round(sentiment*100))
        
        if round(sentiment*100)==0:
            leng_div+=0
        else:
            leng_div+=1

        rating+=sentiment
        
        try:
        #    sentence_data.append(sentence[i]+' '+str(round(sentiment*100)))
           data_obj = {'text':sentence[i],'score':str(round(sentiment*100))}
        except IndexError:
            data_obj = {'text':'','score':''}
        
        sentence_data.append(dict(data_obj))
       
    # sentence_data.pop()
    if len(en_split)==1:
        # rating = len(en_split)
        rating = round((rating/(leng_div))*100)
    else:
        rating = round((rating/(leng_div-1))*100)
    
    
    return sentence_data,polarity_data,rating


def fetchComments(videoId):
    # Get the dataset
    url = 'https://www.googleapis.com/youtube/v3/commentThreads?key={{YOUR_API_KEY}}&textFormat=plainText&part=snippet&videoId='+videoId
    response = urlopen(url)

    # Convert bytes to string type and string type to dict
    string = response.read().decode('utf-8')
    json_obj = json.loads(string)

    to_serve=''
    for i in range(len(json_obj['items'])):
        halfParse= json_obj['items'][i]
        data = halfParse['snippet']['topLevelComment']['snippet']['textOriginal']
        to_serve+=data
        print(data)
    return(to_serve)

def remove_emoji(string):
    emoji_pattern = re.compile("["
                           u"\U0001F600-\U0001F64F"  # emoticons
                           u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                           u"\U0001F680-\U0001F6FF"  # transport & map symbols
                           u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           u"\U00002702-\U000027B0"
                           u"\U000024C2-\U0001F251"
                           "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', string)

def social(request):
    sdata,pdata,rating='','',0
    parsed = 'W8bYzadPilA'
    # parse the link
    if request.method == 'POST':
        parsed = request.POST['videoId']

        comments = fetchComments(parsed)

        comments = remove_emoji(comments)

        sdata,pdata,rating = analysisYoutube(comments)

    # fetch API
    
    # parse data
    # evalute ratings from data
    # return data object and ratings to page
    vid_link = 'src="https://www.youtube.com/embed/"'+parsed
    
    return render(request,"social.html",{'sdata': sdata, 'videolink': parsed, 'rating': rating})

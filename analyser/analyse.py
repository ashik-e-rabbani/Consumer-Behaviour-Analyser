import nltk

nltk.download('punkt')
from textblob import TextBlob
from googletrans import Translator
translator = Translator()

def analysis(data):

    text = data

    sentence = text.split('।')

    en_sent = translator.translate(text).text
    en_split = en_sent.split('.')
    en_split = en_split.pop()
    all_data = []
    polarity_data = []
    sentence_data = []

    for i, val in enumerate(en_split):
        tb = TextBlob(val)
        # print("Polarity of Sentence [" + str(i+1) + "] = ", end="")
        sentiment = tb.sentiment.polarity
        # print(sentence[i] ,sentiment, end="")
        polarity_data.append(round(sentiment*100))
        sentence_data.append(sentence[i])
        

        # if (sentiment > 0):
            
        #     # print("\t\t(Positive sentence)")

        # elif (sentiment < 0):
            
        #     # print("\t\t(Negative sentence)")

        # else:
        #     # print("\t\t(It\'s Neutral)")
    all_data.append(sentence_data)
    all_data.append(polarity_data)
    return all_data

    






#   for i, val in enumerate(sentence):
#       print("Sentence [" + str(i+1) + "] = " + val)

  # for i, val in enumerate(sentence):
  #     token = nltk.word_tokenize(val)
  #     print("\nWords of Sentence [" + str(i+1) + "] = ", end="")
  #     for j in token:
  #         print(j + ", ", end="")

  # print("\n")

  
   
      

parsed = 'আমি সয়তানকে ভালোবাসি না । কিন্তু আজো বিয়া করতে পারি নাই। সে খুব ভালো । মেয়েটা খারাপ না কিন্তু।'
analysis_data = analysis(parsed)

print(analysis_data)
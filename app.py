from flask import Flask, render_template, url_for
import re 
import tweepy 
import random
import matplotlib.pyplot as plt
from tweepy import OAuthHandler 
from textblob import TextBlob 
    
class TwitterClient(object):
    def __init__(self):    #Initialization 
    
        consumer_key = '#########'
        consumer_secret = '#########'
        access_token = '#########'
        access_token_secret = '#########'
  
        # Authentication from keys
        try:  
            self.auth = OAuthHandler(consumer_key, consumer_secret) 
            self.auth.set_access_token(access_token, access_token_secret) 
            self.api = tweepy.API(self.auth)     # tweepy API object (to fetch tweets)
        except: 
            print("Error : Authentication Failed") 
  
    def return_clean_tweet(self, tweet):     # Removes links and special characters using regex 
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split()) 
  
    def return_sentiment(self, tweet): 
       
        analysis = TextBlob(self.return_clean_tweet(tweet)) 

        #Sentiment Names
        if analysis.sentiment.polarity > 0.5: 
            return 'Highly Positive Tweets'
        elif analysis.sentiment.polarity > 0: 
            return 'Somewhat Positive Tweets'
        elif analysis.sentiment.polarity == 0: 
            return 'Neutral Tweets'
        elif analysis.sentiment.polarity > -0.5: 
            return 'Somewhat Negative Tweets'
        else:
            return 'Highly Negative Tweets'
        
  
    def get_tweets(self, query, count = 10): #returns list of produced tweets

        tweets = [] #store parsed tweets
  
        try: 
            tweets_produced = self.api.search(q = query, count = count) # list of produced tweets
  
            for tweet in tweets_produced : 
                parsed_tweet = {} 
                parsed_tweet['text'] = tweet.text             #Dictionary to store Tweet Text and Sentiment
                parsed_tweet['sentiment'] = self.return_sentiment(tweet.text) 
  
                if tweet.retweet_count > 0:    #add repeated tweet only once
                    if parsed_tweet not in tweets: 
                        tweets.append(parsed_tweet) 
                else: 
                    tweets.append(parsed_tweet) 
            return tweets 
  
        except tweepy.TweepError as e:   #any error 
            print("Error : " + str(e)) 
  

def main(): 
    #PRINT OUTPUT
    print("TWITTER SENTIMENTAL ANALYSIS\n\n")
    print("Enter Topic of Analysis - ")
    topic=input()
    print("The Result is as follows -> \n\n")

    api = TwitterClient() #twitterclient class object
    tweets = api.get_tweets(query=topic, count=300) 
  
    # Highly Positive tweets  
    hptweets = [tweet for tweet in tweets if tweet['sentiment'] == 'Highly Positive Tweets'] 
    print("Highly Positive tweets : {} %".format(100*len(hptweets)/len(tweets))) 
    
    # Somewhat Positive tweets  
    sptweets = [tweet for tweet in tweets if tweet['sentiment'] == 'Somewhat Positive Tweets'] 
    print("Somewhat Positive Tweets : {} %".format(100*len(sptweets)/len(tweets))) 
    
    # Highly Negative tweets  
    hntweets = [tweet for tweet in tweets if tweet['sentiment'] == 'Highly Negative Tweets'] 
    print("Highly Negative Tweets : {} %".format(100*len(hntweets)/len(tweets))) 
    
    # Somewhat Negative Tweets 
    sntweets = [tweet for tweet in tweets if tweet['sentiment'] == 'Somewhat Negative Tweets'] 
    print("Somewhat Negative Tweets : {} %".format(100*len(sntweets)/len(tweets))) 
    
    # Neutral Tweets 
    nrtweets = [tweet for tweet in tweets if tweet['sentiment'] == 'Neutral Tweets'] 
    print("Neutral Tweets : {} %".format(100*(len(tweets) -(len(hptweets)+len(sptweets)+len(hntweets)+len(sntweets)))/len(tweets))) 
    
    # Display Tweets 
    
    print("\n\nHighly Positive Tweets:\n") 
    for tweet in hptweets[:5]: 
        print(tweet['text']) 
        
    print("\n\nSomewhat Positive Tweets:\n") 
    for tweet in sptweets[:5]: 
        print(tweet['text']) 
        
    print("\n\nHighly Negative Tweets:\n") 
    for tweet in hntweets[:5]: 
        print(tweet['text']) 
   
    print("\n\nSomewhat Negative Tweets:\n") 
    for tweet in sntweets[:5]: 
        print(tweet['text']) 
        
    
    print("\n\nNeutral Tweets:\n") 
    for tweet in nrtweets[:5]: 
        print(tweet['text'])     
    
    
    # Creating lists of Tweets to display in PieChart 
    hptweets_list=list()
    for tweet in hptweets: 
        value=tweet['text']
        hptweets_list.append(value)
    
    sptweets_list=list()
    for tweet in sptweets: 
        value=tweet['text']
        sptweets_list.append(value)
  
    hntweets_list=list()
    for tweet in hntweets: 
        value=tweet['text']
        hntweets_list.append(value)
     
    sntweets_list=list()
    for tweet in sntweets: 
        value=tweet['text']
        sntweets_list.append(value)
  
    nrtweets_list=list()
    for tweet in nrtweets: 
        value=tweet['text']
        nrtweets_list.append(value)
        
    #FIGURES      
    fig = plt.figure(figsize=(5, 5))
    labels = 'Highly Positive', 'Somewhat Postive','Highly Negative','Somewhat Negative', 'Neutral'
    sizes = [len(hptweets_list),len(sptweets_list),len(hntweets_list),len(sntweets_list),len(nrtweets_list)] 
    plt.pie(sizes, labels=labels, autopct='%1.1f%%',shadow=True, startangle=90) # Counter Clockwise
    plt.axis('equal')  # Equal ratio - circle
    plt.show()

app= Flask(__name__)

@app.route('/')
def index():
    main()
    return render_template("index.html")

if __name__ == "__main__":
    app.run()
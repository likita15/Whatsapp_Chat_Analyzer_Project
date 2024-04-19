from urlextract import URLExtract
from wordcloud import WordCloud
from collections import Counter
import pandas as pd
import re

def fetch_stat(selected_user , df):
    if selected_user != "Overall":
       df = df[df['user']== selected_user]
        
    #fetching invidual user number of messages:
    num_message = df['message'].shape[0]

    #fetching the message words :
    nwords = []
    for i in df['message']:
        nwords.extend(i.split())

    #fetching the number of media:
    num_media_messages = df[df['message']=='<Media omitted>\n'].shape[0]

    
    links = []
    extractor = URLExtract()
    for  i  in df['message']:
        links.extend(extractor.find_urls(i))
    
    return num_message , nwords  , num_media_messages , links


def most_busy_users(df):
    
    x = df['user'].value_counts().head()
    return x 

def percentage_of_user(df):
   x = round((df['user'].value_counts()/df.shape[0])*100,2).reset_index().rename({'index':'name','user':'percent'})
   return x 
   

def create_word_cloud(selected_user , df):
    if selected_user != 'Overall':
        df = df[df['user']==selected_user]
   

    #word filtration:
    new_df = df[df['user']!='group_notification']
    new_df = new_df[new_df['message']!='<Media omitted>\n']
    


    wc = WordCloud(width = 300 , height = 300 , min_font_size = 10 , background_color='white')
   
    x = new_df['message'].str.cat(sep = " ")
   
    df_wc = wc.generate(x)
    return df_wc

def most_common_words(selected_user , df):
    if selected_user != 'Overall':
        df = df[df['user']==selected_user]

    new_df = df[df['user']!='group_notification']
    new_df = new_df[new_df['message']!='<Media omitted>\n']
    f  = open('stop_hinglish.txt','r')
    stop_words = f.read()

    words = []
    for message in new_df['message']:
        for word in message.lower().split(" "):
            if word not in stop_words:
                words.append(word)
    
    for i in range(len(words)):
        words[i] = words[i].replace('\n' ,"")
    
    df = pd.DataFrame(Counter(words).most_common(20))
    return df
def emoji_helper(selected_user , df):
    if selected_user != 'Overall':
        df = df[df['user']==selected_user]

    
    
    def extract_emojis(message):
        emoji_pattern = re.compile("["
                            u"\U0001F600-\U0001F64F"  # emoticons
                            u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                            u"\U0001F680-\U0001F6FF"  # transport & map symbols
                            u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                            "]+", flags=re.UNICODE)
        return emoji_pattern.findall(message)

    emojis = []
    for message in df['message']:
        emojis.extend(extract_emojis(message))

    df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
    df.rename(columns={0:'Emojis' , 1:'no._of_times_used'},inplace=True)
    return df 

    

    
def get_monthly_timeline(selected_user , df):
    if selected_user != 'Overall':
        df = df[df['user']==selected_user]
   
    timeline = df.groupby(['year','month_num','month']).count()['message'].reset_index()
    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i]+ "-"+str(timeline['year'][i]))
    timeline['time'] = time

    return timeline

def get_daily_timeline_month(selected_user , df):
    if selected_user != 'Overall':
       df = df[df['user']==selected_user]
    timeline = df.groupby('only_date').count()['message'].reset_index()
    return timeline
    
def get_week_activity_map(selected_user , df):
    if selected_user != 'Overall':
       df = df[df['user']==selected_user]
    activity = df['day_name'].value_counts().reset_index()
    return activity
def get_month_activity_map(selected_user , df):
    if selected_user != 'Overall':
       df = df[df['user']==selected_user]
    df = df['month'].value_counts().reset_index()
    return df
def heatmap(selected_user , df):
    if selected_user != 'Overall':
       df = df[df['user']==selected_user]
    pivot_df = df.pivot_table(index='day_name', columns='period', values='message', aggfunc='count').fillna(0)
    return pivot_df

    
   


    

    
   


    
    
   


        

        
    

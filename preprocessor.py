import re
import pandas as pd


def call_the_preprocessor(data):
   
    pattern_in_24_hrs = '\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s'
   


    if len(re.findall(pattern_in_24_hrs , data)) == 0:
        return  process_for_meridem(data)
    else:
        return process_24_hrs(data)

        



def process_24_hrs(data):
    pattern = "\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s"
    date_list = re.findall(pattern, data)
    message_list = re.split(pattern, data)[1:]
    df = pd.DataFrame({"user_message": message_list, "message_date": date_list})
    df["date_list"] = pd.to_datetime(df["date_list"], format="%d/%m/%Y, %H:%M - ")
    df.rename(columns={"date_list": "date"}, inplace=True)
    users = []
    messages = []
    for message in df["user_message"]:
        entry = re.split("([\w\W]+?):\s", message)
        if entry[1:]:
            users.append(entry[1])
            messages.append(entry[2])
        else:
            users.append("group_notification")
            messages.append(entry[0])


    df["user"] = users
    df["message"] = messages
    df.drop(columns=["user_message"], inplace=True)

    # extracting year
    df["year"] = df["date"].dt.year
    df['month_num'] = df['date'].dt.month

    # extracting month:
    df["month"] = df["date"].dt.month_name()

    df["day"] = df["date"].dt.day

    df["hour"] = df["date"].dt.hour
    df["minute"] = df["date"].dt.minute

    return df 



def process_for_meridem(data):
    pattern = "\d{1,2}/\d{1,2}/\d{4},\s\d{1,2}:\d{2}\s[ap]m"
    date_list = re.findall(pattern , data)
    for i in range(len(date_list)):
         date_list[i] = date_list[i].replace('\u202f' , ' ') 
    meridiem = []
    for i  in range(len(date_list)):
        meridiem.append(re.findall('[ap]m' , date_list[i])[0])
    new_date_list = re.findall("\d{1,2}/\d{1,2}/\d{4},\s\d{1,2}:\d{2}",data)
    df = pd.DataFrame({'date_list':new_date_list})
    df['date_list']=pd.to_datetime(df['date_list'],format = '%d/%m/%Y, %H:%M')
    pattern_for_filtering_string = "\d{1,2}/\d{1,2}/\d{4},\s\d{1,2}:\d{2}\s[ap]m\s-\s"
    message_list = re.split(pattern_for_filtering_string , data)[1:]
    df['user_message'] = message_list


    users = []
    messages = []
    for message in df['user_message']:
        entry = re.split('([\w\W]+?):\s',message)
        if entry[1:]:
            users.append(entry[1])
            messages.append(entry[2])
        else:
            users.append("group_notification")
            messages.append(entry[0])
    df['user'] = users
    df['message'] = messages
    df.drop(columns = ['user_message'],inplace = True)

    df["year"] = df["date_list"].dt.year

    df['month_num'] = df['date_list'].dt.month


    df["month"] = df["date_list"].dt.month_name()

    df["day"] = df["date_list"].dt.day
    
    df['only_date'] = df['date_list'].dt.date
    df["hour"] = df["date_list"].dt.hour
    df['day_name'] = df['date_list'].dt.day_name()
    df["minute"] = df["date_list"].dt.minute

    df['meridiem'] = meridiem
    period = []
    df[['day_name' , 'hour']]['hour']
    for hour in df[['day_name' , 'hour']]['hour']:
        if hour == 23:
            period.append(str(hour) + "-" + str('00'))
        elif hour == '0':
            period.append(str('00') + "-"+ str(hour+1))
        else:
            period.append(str(hour) + "-" + str(hour+1))
    df['period'] = period
    
    

    return df 

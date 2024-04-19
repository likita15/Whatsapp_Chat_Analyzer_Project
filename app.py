import plotly.express as px
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

import preprocessor as pre
import helper as hel

# link = r"C:\Users\aditya\Desktop\Developement\Data Analysis\whatsapp_chat_analyzer\uno.txt"
# f = open(link,'r',encoding = 'utf-8')
# data = f.read()

st.sidebar.title('Whatsapp Chat Analyzer')

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
   bytes_data = uploaded_file.getvalue()

   data = bytes_data.decode("utf-8")
   
   
   df  = pre.call_the_preprocessor(data) 
   if df.shape[0]!=0:

   
   

      user_list = df['user'].unique().tolist()

      user_list.remove('group_notification')
      user_list.sort()
      user_list.insert(0,'Overall')
      selected_user = st.sidebar.selectbox("Show analysis wrt" , user_list)

      if st.sidebar.button("Show Analysis"):
         number_of_messages , number_of_words ,num_media_message , no_links_shared = hel.fetch_stat(selected_user,df)
         col1 , col2 , col3 , col4 = st.columns(4)

         with col1: 
            st.header(":red[Messages]")
            st.subheader(number_of_messages)
         with col2: 
            
            st.header(":red[Words]")
            st.subheader(len(number_of_words))
         with col3: 
            st.header(":red[Media]")
            st.subheader(num_media_message)
         with col4: 
            st.header(":red[Links]")
            st.subheader(len(no_links_shared))

         #monthly-timeline:
         st.header('Monthly-Timeline')
         timeline = hel.get_monthly_timeline(selected_user , df)
         
         data = pd.DataFrame({
            'time': timeline['time'].values,
            'No_of_message': timeline['message'].values
         })
         
         
         st.line_chart(data , x="time", y="No_of_message",color = ['#af28fa'])


         #Daily Timelines:
         st.header('Daily-Timeline')
         timeline = hel.get_daily_timeline_month(selected_user , df)
         data = pd.DataFrame({
            'Day': timeline['only_date'].values,
            'No_of_message': timeline['message'].values
         })
         
         
         st.line_chart(data , x="Day", y="No_of_message",color = ['#ff7c1f'])

         #activity map:
         col1 , col2 = st.columns(2)
         with col1:
            st.subheader('Most Busy Day')

            x = hel.get_week_activity_map(selected_user,df)
            data = pd.DataFrame({
            'day_name': x['day_name'].values,
            'Activity_value_per_Day': x['count'].values
            })
            st.bar_chart(data,x = 'day_name',y = 'Activity_value_per_Day',color = "#ff5d51" , width = 0.5 , height = 600)

         with col2:
            st.subheader('Most Busy month')

            x = hel.get_month_activity_map(selected_user,df)
         
            data = pd.DataFrame({
            'month_name': x['month'].values,
            'Activity value per month': x['count'].values
            })
            st.bar_chart(data,x = 'month_name',y = 'Activity value per month',color = "#d200ff" , width = 0.5 , height = 600)





      


         if selected_user == 'Overall':
            st.title('Most Busy Users')
            x = hel.most_busy_users(df)
            
            col1 , col2 = st.columns(2)
            with col1:
               

               
               x = hel.most_busy_users(df)
               data = {
               'Users': x.index,
               'Messages': x.values
               }
               chart_data = pd.DataFrame(data)
               chart_data.set_index('Users', inplace=True)


               st.bar_chart(chart_data,color = "#51ffcb" , width = 0.5 , height = 600)

            with col2:
               new_df = hel.percentage_of_user(df)
               st.dataframe(new_df)

         
         try:
            df_wc  = hel.create_word_cloud(selected_user,df)
            st.title('Word Cloud')
            
            fig , ax = plt.subplots()
            plt.axis('off')
            ax.imshow(df_wc)
            st.pyplot(fig)
         except :
            st.header('No words for clouds')

         


      
         

         st.title('Most common word')
         try:

            most_common_df = hel.most_common_words(selected_user , df)
            
            st.dataframe(most_common_df)

            data = {
            'words': most_common_df[0].values,
            'numbers': most_common_df[1].values
            }
            chart_data = pd.DataFrame(data)
            chart_data.set_index('words', inplace=True)

            plt.xticks(rotation = 'vertical')

            st.bar_chart(chart_data,color = "#ee82ee" , width = 0.5 , height = 600)
         except:
            st.header(':red[No Words Found]')
      

         emoji_data = hel.emoji_helper(selected_user ,df)
         if emoji_data.shape[0] !=0:
            st.header(':violet[Emoji Analysis]')
            col1 , col2 = st.columns(2)
            with col1:
                  
                  data = {
                     
                  'emojis': emoji_data['Emojis'].values,
                  'numbers': emoji_data['no._of_times_used'].values
               }
                  chart_data = pd.DataFrame(data)
                  chart_data.set_index('numbers', inplace=True)

                  

                  st.bar_chart(chart_data,color = "#46C7A7" , width = 0.5 , height = 600)
         else:
            st.header(':violet[No Emojis used]')

         with col2:
            st.dataframe(emoji_data)
         
         
         st.title('Heatmap')

         
         
         pivot_df = hel.heatmap(selected_user, df)
      

         
         new_pivot_values = list(pivot_df.values)
         
         for i in range(len(new_pivot_values)):
            new_pivot_values[i] = list(new_pivot_values[i])
         
         data = new_pivot_values
         index_values = list(pivot_df.columns)
         columns_values = list(pivot_df.index)
         st.set_option('deprecation.showPyplotGlobalUse', False)
         plt.figure(figsize=(15, 8))


         sns.heatmap(data, annot=True, cmap='coolwarm', yticklabels=columns_values, xticklabels=index_values)
         plt.title('Heatmap')
         plt.xlabel('time_in_Hour')
         plt.ylabel('Days_in_weeks')

         # Display heatmap in Streamlit
         st.pyplot()

   else:
      st.header(':red[No Data Found]')
   
         
         
    
     



      


      

         
      
            
            

   
   




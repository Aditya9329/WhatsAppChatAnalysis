import numpy as np 
import pandas as pd 
import re 
from . import text_preparation
from urlextract import URLExtract
from Analysis import helper






class TextPreparation:
    def __init__(self):
        pass 


    def read_file(self,text):
        global control_df
        """
            Getting text and then split the 
            text and then i get  user and msg as list of string
        """
        self.user= []
        self.t = r'([\w\W]*?):\s'
        self.user_msg = []

        self.text    = text
        self.pattern = '\d{1,2}\/\d{1,2}\/\d{4}\,\s\d{1,2}:\d{1,2}\s-\s'
        self.msg_and_name = re.split(self.pattern,self.text)[1:]
        self.dates   = re.findall(self.pattern,self.text)

        self.df = pd.DataFrame({'msg':self.msg_and_name,'dates':self.dates})

        for e in range(len(self.df['msg'])):
            data = re.split(self.t,self.df['msg'][e])  
            if data[1:]:
                self.user.append(data[1])
                self.user_msg.append(data[2])
            else:
                self.user.append('Notification')
                self.user_msg.append(data[0])

        # converting dates into datetime format
        self.df['dates'] = pd.to_datetime(self.df['dates'],format='%d/%m/%Y, %H:%M - ')
        

        # print(self.df)
        # print(self.user)
        # pd.set_option('display.max_colwidth', 40)
        self.df['user'] = self.user 
        self.df['message'] = self.user_msg
        self.df['year']  = self.df['dates'].dt.year
        self.df['month'] = self.df['dates'].dt.month_name()
        self.df['day']  = self.df['dates'].dt.day_name()
        self.df.drop(columns='msg',inplace=True)

       
        # TextPreparation.read_file.dataframe = self.df  
        control_df= self.df
        
        self.n_user = self.df['user'].unique().tolist()
        return str(self.df.to_html(classes='table table-striped', justify='center',border=2,col_space=5)),self.n_user#converting to html format or tabular data


    
    def GetParticular(self,srch_user):
        self.srch_user=srch_user
        user_messages=[]
        collect_links=[]
        total_words=[]
        global control_df
        total_msg=0
        for (u,m) in zip(control_df['user'],control_df['message']):
            if u == srch_user:
                user_messages.append(m)
                collect_links.append(m)
                total_msg+=1
            else:
                pass
        print("Control DF-User",control_df['user'])
        #Time to extract the urls shared by particular one
        url_extractor = URLExtract()
        urls  = url_extractor.find_urls(str(collect_links))

    
        return total_msg,srch_user,user_messages,len(urls)

    # counting number of words 
    # calling this function from views.py
    def Total_words(self,user_messages):
        self.user_messages = user_messages
        words = 0
        words = len(str(self.user_messages).split())
        print(self.user_messages)
        print("total words = ",words)
        return words


    def get_visualization_for_most_active(self):
        global control_df
        print("Hello visual is running",control_df)
        x = control_df['user'].value_counts().head(20)
        name = x.index
        count = x.values
        # temp1  as name
        temp1 = list(name)
        temp2 = list(count)
        temp1.reverse()
        temp2.reverse()
        return temp1,temp2


    def get_most_active_month(self):
        global control_df
        monthVSmsg = control_df['month'].value_counts()
        x = monthVSmsg.index
        y = monthVSmsg.values
        return x,y
    

    def most_active_days(self):
        global control_df
        active_days = control_df['day'].value_counts()
        x_active  = active_days.index
        y_active  =active_days.values
        
        return x_active,y_active
    # total number of urls in group
    def count_urls(self):
        
        global control_df
        url_collect=[]
        for e in control_df['message']:
            url_collect.append(e)
        
        url_exractor = URLExtract()
        urls = url_exractor.find_urls(str(url_collect))
        num_urls = len(urls)
        return num_urls

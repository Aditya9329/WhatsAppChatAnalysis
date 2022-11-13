from msilib.schema import File

from django.shortcuts import render
from django.http import HttpResponse
from django.core.files import File
from .import forms
import re 
import pandas as pd 
from .utils import get_plot, get_plot_bar

from Text_Preparation import text_preparation
# Create your views here.
def home(request):
    if request.method =='POST':
        uploaded_file = forms.File(request.POST,request.FILES)
        if uploaded_file.is_valid():
            # Getting file data directly from form field
            file = request.FILES.get('upload_file').read() 
            #Getting whole dataframe
            df,user= text_preparation.TextPreparation().read_file(str(file))
            #creating the attribute of the object of function home
            home.dataframe = df
            
            # print(home.__dict__)
            res = render(request,'info.html',{'df':df,'user':user})
            return res 
    else:
        form =forms.File()
        res = render(request,'index.html',{'form':form})
        return res




# Analysis for particular user
def Analyzer(request):
   
    if request.method=='POST':
        selected_user = request.POST.get('user')
        num_of_msg,name,user_messages,links= text_preparation.TextPreparation().GetParticular(selected_user)
        # text_preparation.TextPreparation().GetParticular(selected_user)
        print(selected_user)
        print(num_of_msg,name)
    
        # print(home.__dict__)
        # Calculate the number of words 
        total_words = text_preparation.TextPreparation().Total_words(user_messages)
        # show visual for  most active user
        active_name,count = text_preparation.TextPreparation().get_visualization_for_most_active()
        chart = get_plot(active_name,count)
        #show most active month
        month, msg =  text_preparation.TextPreparation().get_most_active_month()
        chart2 = get_plot_bar(month,msg)
        #presenting analysis of most active days
        active_day_x,active_day_y =text_preparation.TextPreparation().most_active_days()
        chart3 = get_plot(active_day_x,active_day_y)
        res = render(request,'analysis.html',{'msg':num_of_msg,'name':name,'user_messages':user_messages,'total_words':total_words,'links':links,'chart':chart,'chart2':chart2,
        'chart3':chart3})
        return res
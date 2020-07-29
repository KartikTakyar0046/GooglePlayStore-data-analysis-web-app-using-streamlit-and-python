import streamlit as st
from PIL import Image
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
local_css("style.css")
st.markdown('<style>h1{color: red;}</style>', unsafe_allow_html=True)
image = Image.open('pic7.jpg')
st.image(image, use_column_width=True)

user_reviews = pd.read_csv("googleplaystore_user_reviews.csv")
playstore_data = pd.read_csv("googleplaystore.csv")

st.title("Google Play Store Data Analysis")
st.markdown('<i class="material-icons">Let us find the insights and visualise the dataset of googleplaystore in detail......</i>', unsafe_allow_html=True)

if st.checkbox('Show dimensions of the datasets'):
    st.write('-> Dimentions of google_playstore dataset: {}'.format(playstore_data.shape))
    st.write('-> Dimentions of user_review dataset: {}'.format(user_reviews.shape))
    st.write('-> Unique Stores: {}'.format(len(playstore_data['App'].unique())))

#removing missing values and duplicates
user_reviews.dropna(inplace=True)
playstore_data= playstore_data.drop_duplicates(subset='App')
playstore_data.dropna(inplace=True,subset=['Type','Content Rating','Current Ver','Android Ver'])

if st.checkbox('Statistics of Ratings of apps'):
    st.write(user_reviews.describe())
    playstore_data.fillna(0,inplace=True)
    playstore_data[playstore_data['Rating'] == 0].head()
    st.write(playstore_data.describe())
    rating = playstore_data[playstore_data['Rating'] != 0 ]
    st.write("After removing the missing values in ratings")
    st.write(rating.describe())
    sns.kdeplot(shade=True,data=rating['Rating'])
    st.pyplot()
    from scipy.stats import kurtosis, skew
    x = np.random.normal(0, 2, 10000)
    st.write( '-> Excess kurtosis of  distribution: {}'.format( kurtosis(rating['Rating']) ))
    st.write( '-> Skewness of distribution: {}'.format( skew(rating['Rating']) ))

df1 = user_reviews['Sentiment'].value_counts()
df1 = df1.reset_index()
def bar_plot(x,y,y_label,title,color):
    objects = x.values
    y_pos = np.arange(len(objects))
    plt.figure(figsize=(10,5))
    bar = plt.bar(x,y,color=color)
    plt.xticks(y_pos, objects)
    plt.ylabel(y_label)
    plt.title(title)
    return bar

if st.checkbox('Bar plot on sentiments:'):
    bar_plot(x = df1['index'],y = df1['Sentiment'],y_label = 'Sentiment_Freq',title = 'Bar Plot on Sentiment', color = 'r')
    st.pyplot()

if st.checkbox('Bar charts on category,installs,type,content rating and genre'):
    list_1 = ['Category', 'Installs', 'Type',
            'Content Rating']
    def bar_plot(x,y,y_label,x_label,title,color,ax):
        bar = sns.barplot(x = x,y=y,ax=ax,orient='h')
        plt.ylabel(y_label)
        plt.xlabel(x_label)
        plt.title(title)
        for i, v in enumerate(x.values):
            ax.text(v + 3, i + .25, str(v), color='black', fontweight='bold')
        return bar
    fig = plt.figure(figsize=(14,18))
    fig.subplots_adjust(hspace=0.4, wspace=0.4)
    i = 1
    for names in list_1:
        ax1 = fig.add_subplot(2, 2, i)
        df2 = playstore_data[names].value_counts()
        df2 = df2.reset_index()
        bar_plot(x = df2[names],y = df2['index'],x_label = 'Freq',title = 'Bar Chart On {}'.format(names),color='red',ax=ax1,y_label=names)
        i += 1
    st.pyplot()

    list_2 = ['Genres']
    def bar_plot(x,y,y_label,x_label,title,color,ax=None):
        plt.figure(figsize=(5,8))
        bar = sns.barplot(x = x,y=y,orient='h')
        plt.ylabel(y_label)
        plt.xlabel(x_label)
        plt.title(title)
        for i, v in enumerate(x.values):
            bar.text(v + 3, i + .25, str(v), color='black', fontweight='bold')
        return bar
    df2 = playstore_data['Genres'].value_counts()
    df2 = df2.reset_index()
    df2 = df2[df2['Genres'] > 100]
    bar_plot(x = df2['Genres'],y = df2['index'],x_label = 'Freq',title = 'Bar Chart On Genre',color='red',y_label='Genre')
    st.pyplot()

if st.checkbox('Apps with 1 billion downloads'):
    st.write(playstore_data[playstore_data['Installs'] == '1,000,000,000+']['App'])


df2 = playstore_data['Genres'].value_counts()
df2 = df2.reset_index()
df2 = df2[df2['Genres'] > 100]
genres=  list(df2['index'][1:10])
d = pd.DatetimeIndex(playstore_data['Last Updated'])
playstore_data['year'] = d.year
playstore_data['month'] = d.month

if st.checkbox('10 Apps with 100 million installs and Rating >= 4.5 and Year = 2018 in'):
    for i in genres:
        play = playstore_data[(playstore_data['Installs'] != '1,000,000,000+') & (playstore_data['Genres'] == i) & (playstore_data['Rating'] >= 4.5) & (playstore_data['year'] == 2018)]['App']

        if st.checkbox('>>> {}'.format(i)):
            st.write('--------------------------------------------------')
            st.write(play[0:10])
    st.write("")

if st.checkbox('Free vs Paid apps'):
    size=[8895,753]
    sentiment = ['Free', 'Paid']
    colors = ['g', 'pink']
    plt.pie(size, labels=sentiment, colors=colors, startangle=180, autopct='%.1f%%')
    plt.title('% Free vs Paid Apps')
    plt.show()
    st.pyplot()

if st.checkbox('Number of apps not been updated since:'):
    st.write('-> year 2016 :{}'.format(len(playstore_data[playstore_data['year'] < 2016])))
    st.write('-> year 2015 :{}'.format(len(playstore_data[playstore_data['year'] < 2015])))
    st.write('-> year 2014 :{}'.format(len(playstore_data[playstore_data['year'] < 2014])))

if st.checkbox('Analysis on paid apps'):
    paided = playstore_data[playstore_data['Type'] == 'Paid']
    df3 = paided['Category'].value_counts()
    df3 = df3.reset_index()
    df3 = df3[:10]
    plt.figure(figsize=(10,5))
    plt.pie(x = list(df3['Category']), labels=list(df3['index']), autopct='%1.0f%%', pctdistance=0.8, labeldistance=1.2)
    plt.title('% Distribution of Paided Apps Categories')
    st.pyplot()

if st.checkbox('Top rated paid apps with installs 1,000,000+'):
    paided = playstore_data[playstore_data['Type'] == 'Paid']
    st.write(paided[(paided['Rating'] > 4.7) & (paided['Installs'] == '100,000+') ]['App'])

image = Image.open('pic8.jfif')
st.image(image, use_column_width=True)

#Imports

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from PIL import Image
import plotly.express as px
import altair as alt
from bokeh.plotting import figure


#import plotly.figure_factory as ff


#Functions 
@st.cache(suppress_st_warning=True)
def count_word(df, ref_col, liste):
    keyword_count = dict()
    for s in liste: keyword_count[s] = 0
    for liste_keywords in df[ref_col].str.split('|'):
        if type(liste_keywords) == float and pd.isnull(liste_keywords): continue
        for s in liste_keywords: 
            if pd.notnull(s): keyword_count[s] += 1
    # convert the dictionary in a list to sort the keywords  by frequency
    keyword_occurences = []
    for k,v in keyword_count.items():
        keyword_occurences.append([k,v])
    keyword_occurences.sort(key = lambda x:x[1], reverse = True)
    return keyword_occurences, keyword_count

def count_rows(rows): 
    return len(rows)

@st.cache(suppress_st_warning=True)
def artistpie(artistname):
    if artistname in artists:
        mask=stream_hist['artistName'].str.contains(artistname)
        res=stream_hist[mask]
        fig = px.pie(res, values='msPlayed', names='trackName', color_discrete_sequence=px.colors.sequential.RdBu)
        fig.update_traces(textposition='inside', textinfo='percent+label')
        fig.show()

@st.cache(suppress_st_warning=True)
def songpie(song):
    mask = stream_hist['trackName'].str.contains(song)
    res=stream_hist[mask]
    fig = px.pie(res, values='msPlayed', names='trackName',hole=0.3,color_discrete_sequence=px.colors.sequential.RdBu)
    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.show()

@st.cache(suppress_st_warning=True)
def songSearch(string):
    search = stream_hist['trackName'].str.contains(string)
    res=stream_hist[search]
    return res

@st.cache(suppress_st_warning=True)
def artistSearch(string):
    search = stream_hist['artistName'].str.contains(string)
    res=stream_hist[search]
    return res

def artistSongcount(artistname):
    fig, ax = plt.subplots()
    ax=sns.countplot(stream_hist.loc[stream_hist['artistName']==artistname]['trackName'])
    ax.set_xticklabels(ax.get_xticklabels(),rotation=90)
    plt.title(artistname+' songs count')
    plt.show()

st.set_option('deprecation.showPyplotGlobalUse', False)


#Dataframe

stream_hist1=pd.read_json('StreamingHistory0.json')
stream_hist2=pd.read_json('StreamingHistory1.json')
stream_hist=pd.concat([stream_hist1,stream_hist2],ignore_index=True)


#Data pre-processing

stream_hist['songInfo']=stream_hist['artistName']+' - '+stream_hist['trackName']
df=stream_hist.groupby(['artistName','trackName'])['msPlayed'].agg('sum')
df1=stream_hist.groupby(['artistName'])['msPlayed'].agg('sum')
df2=stream_hist.groupby(['songInfo'])['msPlayed'].agg('sum')
stream_hist.isnull().sum()
artists = stream_hist['artistName'].unique().tolist()
len(artists)
#Creation of artists list

artists = stream_hist['artistName'].unique().tolist()
songs=stream_hist['trackName'].unique().tolist()




#top 25 most listened
most_listened = stream_hist.groupby(['trackName','artistName']).size().sort_values(ascending=False)[:25]
most_listened.head(25)

st.title('Spotify data viz app')

st.write('Welcome in my musical world!')
st.image('https://jouretnuit.paris/wp-content/uploads/2016/10/spotify-banniere.png')

st.header('One of my favourite songs')
st.write(" [Rihanna - Te amo](https://www.youtube.com/watch?v=Oe4Ic7fHWf8)")
st.video('https://www.youtube.com/watch?v=Oe4Ic7fHWf8')




with st.sidebar:
    st.title('Presentation')
    col1, col2, col3 = st.columns(3)
    col2.image(Image.open('image0.jpeg'))
    st.info('Kadidia Coulibaly,')
    icon_size = 20


    st.title('Links')
    st.write("[Linkedin](https://www.linkedin.com/in/kadidia-coulibaly-b2383b217/)")
    st.write("[Github](https://github.com/ckmaguy/MySpotify-Data-Viz)")
    st.write("[Spotify profil](https://open.spotify.com/user/maguycoul?si=5cf564998dfd42d1)")

    


#Search tools 
def searchTools():
    st.header('Search by artist name')
    artist = st.text_input('Name of the artist', 'Artist Name')
    st.write('Here are the results for', artist)
    result=artistSearch(artist)
    st.write(result)
    #if len(result)>0:
    #    st.subheader(artist +' count graph ')
    #    st.pyplot(artistSongcount(artist))

    st.header('Song search')
    song = st.text_input('song', 'string')
    st.write('Here are the results for', song)
    st.write(songSearch(song))

searchTools()


#Top30 plot

def top30plot():
    st.header('Top 30 songs')
    st.write('Let\'s see the songs that I listen to the most:' )
    fig, ax = plt.subplots()
    plt.title('Top30 Songs')
    ax=sns.barplot(x=df2.nlargest(30).index,y=df2.nlargest(30).values)
    ax.set_xticklabels(ax.get_xticklabels(),rotation=90)
    plt.show()
    st.pyplot(fig)

top30plot()


#Most popular artists

def topArtists():
    st.header('What about my favourite artists ?')
    st.write('Here\'s the top 25 ! ')

    keyword_occurences, dum = count_word(stream_hist, 'artistName', artists)
    trunc_occurences = keyword_occurences[0:25]

    trunc_occurences = keyword_occurences[0:25]

    fig, ax = plt.subplots()
    y_axis = [i[1] for i in trunc_occurences]
    x_axis = [k for k,i in enumerate(trunc_occurences)]
    x_label = [i[0] for i in trunc_occurences]
    plt.xticks(rotation=90, fontsize = 15)
    plt.yticks(fontsize = 15)
    plt.xticks(x_axis, x_label)
    plt.ylabel("No. of occurences", fontsize = 24, labelpad = 0)
    ax.bar(x_axis, y_axis, align = 'center', color='orange')
    plt.title("Popularity of Artists",bbox={'facecolor':'k', 'pad':5},color='w',fontsize = 30)
    plt.show()
    st.pyplot(fig)

topArtists()

#Tab to see distribution of songs/artist
def graphTab():
    st.header('Graph Tab')
    st.caption('Code')
    with st.expander("See code"):
        with st.echo():
            t1, t2, t3,t4 = st.tabs(["Khalid", "Justin Bieber", "Ne-Yo","Your choice"])
            with t1:
                st.header("Khalid")
                st.pyplot(artistSongcount("Khalid"))
            with t2:

                st.header("Justin Bieber")
                st.pyplot(artistSongcount("Justin Bieber"))
            with t3:
                st.header("Ne-Yo")
                st.pyplot(artistSongcount("Ne-Yo"))
            artists.sort()
        
    

    t1, t2, t3,t4 = st.tabs(["Khalid", "Justin Bieber", "Ne-Yo","Your choice"])
    with t1:
        st.header("Khalid")
        st.pyplot(artistSongcount("Khalid"))
    with t2:
        st.header("Justin Bieber")
        st.pyplot(artistSongcount("Justin Bieber"))
    with t3:
        st.header("Ne-Yo")
        st.pyplot(artistSongcount("Ne-Yo"))

    artists.sort()
    with t4:
        st.header('We can also use a slider to make graphs:')
        A = st.select_slider(

            'Select an artist',

            options=artists)
        st.write('My artist choice is', A)
        st.pyplot(artistSongcount(A))

graphTab()

#Pie with artist name
def artistPie():
    st.header('Let\'s make a pie with the artist of your choice:')

    artist = st.text_input('Name', 'Name')
    st.pyplot(artistpie(artist))



#Tab to see internal st graph

def stGraphs():
    st.header('Internal streamlit plots')
    tab1, tab2, tab3 = st.tabs(["Line chart", 'Area Chart', "Altair chart"])



    with tab1:
        st.header("Line chart")
        st.line_chart(stream_hist.head(50),x='artistName',y='msPlayed')



    with tab2:

        st.header('Area Chart')
        st.write('Artists list : ',artists[:50])
        st.area_chart(stream_hist.head(50),x=artists,y='msPlayed')



    with tab3:

        st.header("Altair chart")
        c=alt.Chart(stream_hist.head(50)).mark_circle().encode(
        x='trackName',y='msPlayed',size='artistName',color='artistName',tooltip=['trackName','msPlayed','artistName'])
        st.altair_chart(c,use_container_width=True)
stGraphs()

def songPie():
    st.header('Let\'s make a pie with a song search:')
    song = st.text_input('song name', 'song name')
    st.pyplot(songpie(song))

def pies():
    col1, col2 = st.columns(2)

    with col1:
        st.header("Artist pie")
        artistPie()
    with col2:
        st.header("Songs pie")
        songPie()

pies()

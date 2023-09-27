import streamlit as st 
import pandas as pd 
import preprocess,functions
import plotly.express as px
import plotly.figure_factory as ff
import matplotlib.pyplot as plt 
import seaborn as sns

data = pd.read_csv('athlete_events.csv')
regions_data= pd.read_csv('noc_regions.csv') 

df=preprocess.preproc(data,regions_data)
st.sidebar.title('Olympics Analysis')
st.sidebar.image('https://upload.wikimedia.org/wikipedia/commons/5/5c/Olympic_rings_without_rims.svg')
user_menu=st.sidebar.radio(
    'Select an Option',
    ('Medal Tally','Overall Analysis','Country-wise Analysis','Athlete-wise Analysis')
)

#st.dataframe(df)

if user_menu == 'Medal Tally':
    st.sidebar.header('Medal Tally')
    years,countries = functions.year_contry_list(df)

    selected_year = st.sidebar.selectbox("Select Year",years)
    selected_country = st.sidebar.selectbox("Select Country",countries)
    medal=functions.fetch_medal(df,selected_year,selected_country) 
    if selected_year == 'Overall' and selected_country == 'Overall':
        st.title('Overall Tally') 
    if selected_year != 'Overall' and selected_country == 'Overall':
        st.title('Medal tally in '+ str(selected_year)) 
    if selected_year == 'Overall' and selected_country != 'Overall':
        st.title('Medal tally of '+ selected_country) 
    if selected_year != 'Overall' and selected_country != 'Overall':
        st.title('Medal tally of '+ selected_country +' in '+str(selected_year))
    st.table(medal) 

if user_menu == 'Overall Analysis':
    editions=df['Year'].unique().shape[0]-1 
    cities=df['City'].unique().shape[0] 
    sports=df['Sport'].unique().shape[0]
    events=df['Event'].unique().shape[0] 
    athletes=df['Name'].unique().shape[0]
    nations=df['NOC'].unique().shape[0] 

    st.title('Top Statistics')

    col1,col2,col3=st.columns(3)
    with col1: 
        st.header("Editions")
        st.title(editions)
    with col2:
        st.header('Cities')
        st.title(cities)
    with col3:
        st.header("Sports")
        st.title(sports) 

    col1,col2,col3=st.columns(3)
    with col1:
        st.header('Events')
        st.title(events)
    with col2:
        st.header('Athletes')
        st.title(athletes)
    with col3:
        st.header('Nations')
        st.title(nations) 

    nations_overtime=functions.data_overtime(df,'NOC')
    fig=px.line(nations_overtime,x='Year',y='count') 
    st.title('Participating Nations over the years')
    st.plotly_chart(fig)  

    events_overtime=functions.data_overtime(df,'Event')
    fig1=px.line(events_overtime,x='Year',y='count') 
    st.title('Number of events over the years')
    st.plotly_chart(fig1) 

    athletes_overtime=functions.data_overtime(df,'Name')
    fig1=px.line(athletes_overtime,x='Year',y='count') 
    st.title('Number of Athletes over the years')
    st.plotly_chart(fig1) 


    st.title("No of events over the time(Every Sport)")
    fig,ax=plt.subplots(figsize=(15,15))
    x=df.drop_duplicates(['Year','Sport','Event'])
    ax=sns.heatmap(x.pivot_table(index='Sport',columns='Year',values='Event',aggfunc='count').fillna(0).astype(int))
    st.pyplot(fig) 

    st.title('Most successful Athletes')
    sport_list=df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0,'Overall')

    selected_sport=st.selectbox('Select a Sport',sport_list)
    x=functions.most_successful(df,selected_sport)
    st.table(x) 


if user_menu == 'Country-wise Analysis':
    
    st.sidebar.title('Country-wise Analysis')
    countries=df['region'].dropna().unique().tolist() 
    countries.sort() 
    #countries.insert(0,'Overall')  
    selected_con = st.sidebar.selectbox("Select a Country",countries)
    #selected_con=st.selectbox('Select a Country',countries) 
    medals_ycwise=functions.yearwise_medaltally(df,selected_con)
    st.title('Year wise medals of '+selected_con)
    fig=px.line(medals_ycwise,x='Year',y='Medal') 
    st.plotly_chart(fig) 

    st.title('Excels of each sport by '+selected_con)
    pt=functions.country_event_hm(df,selected_con)
    fig,ax=plt.subplots(figsize=(15,15))
    ax=sns.heatmap(pt)
    st.pyplot(fig) 

    st.title('Top 10 Athletes from '+selected_con)
    top_athletes=functions.most_successful_athletes_regions(df,selected_con)
    st.table(top_athletes)



if user_menu == 'Athlete-wise Analysis':

    athletes=df.drop_duplicates(subset=['Name','region'])
    x1=athletes['Age'].dropna() 
    x2=athletes[athletes['Medal']=='Gold']['Age'].dropna()
    x3=athletes[athletes['Medal']=='Silver']['Age'].dropna()
    x4=athletes[athletes['Medal']=='Bronze']['Age'].dropna() 
    
    st.title('Distribution of Age')
    fig=ff.create_distplot([x1,x2,x3,x4],['Overall Age','Gold Medalist','Silver Medalist','Bronze Medalist'],show_hist=False,show_rug=False)
    fig.update_layout(autosize=False,width=1000,height=600)
    st.plotly_chart(fig)

    sports=df['Sport'].unique()[:30].tolist()
    x=[]
    name=[]
    for i in sports:
        t=athletes[athletes['Sport']==i]
        x.append(t[t['Medal']=='Gold']['Age'].dropna())
        name.append(i) 
    fig1=ff.create_distplot(x,name,show_hist=False,show_rug=False)
    fig1.update_layout(autosize=False,width=1000,height=600) 
    st.title('Distribution of Age wrt Sport(Gold Medal)')
    st.plotly_chart(fig1) 
    
    st.title('Weight Vs Height Distribution')
    selected_sport=st.selectbox('Select a Sport',sports)
    wvh=functions.weight_v_height(df,selected_sport)
    fig,ax=plt.subplots()
    ax=sns.scatterplot(data=wvh,x='Weight',y='Height',hue='Medal',style='Sex',s=50)
    #fig2.update_layout(autosize=False,width=1000,height=600) 
    st.title('Weight Vs Height of '+selected_sport) 
    st.pyplot(fig) 
    
    st.title('Participation of Men and Women Over the Years')
    men=athletes[athletes['Sex']=='M'].groupby('Year')['Name'].count().reset_index()
    women=athletes[athletes['Sex']=='F'].groupby('Year')['Name'].count().reset_index() 
    final=men.merge(women,on='Year',how='left')
    final.fillna(0,inplace=True)
    final.rename(columns={'Name_x':'Male','Name_y':'Female'},inplace=True) 
    fig=px.line(final,x='Year',y=['Male','Female'])
    fig.update_layout(autosize=False,width=1000,height=600)
    st.plotly_chart(fig)




    
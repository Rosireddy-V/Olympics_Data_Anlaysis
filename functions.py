def func(df):
    medal_tally=df.drop_duplicates(subset=['Team','NOC','Games','City','Sport','Event','Medal'])
    medal_tally=medal_tally.groupby('region').sum()[['Gold','Silver','Bronze']].sort_values('Gold',ascending=False).reset_index()
    medal_tally['total']=medal_tally['Gold']+medal_tally['Silver']+medal_tally['Bronze']
    
    return medal_tally 

def year_contry_list(df):
    years=df['Year'].unique().tolist()
    years.sort()
    years.insert(0,'Overall') 

    countries=df['region'].dropna().unique().tolist() 
    countries.sort() 
    countries.insert(0,'Overall') 

    return years,countries 

def fetch_medal(df,year,country):
    medal_tally=df.drop_duplicates(subset=['Team','NOC','Games','City','Sport','Event','Medal'])
    flag=0 
    if year=='Overall' and country == 'Overall':
        tempdf=medal_tally 
    if year == 'Overall' and country != 'Overall':
        flag=1
        tempdf=medal_tally[medal_tally['region']==country]  
    if year !='Overall' and country == 'Overall':
        tempdf=medal_tally[medal_tally['Year']==year] 
    if year !='Overall' and country!='Overall':
        tempdf=medal_tally[(medal_tally['Year']==year)&(medal_tally['region']==country)]
    
    if flag==1:
        x= tempdf.groupby('Year').sum()[['Gold','Silver','Bronze']].sort_values('Year').reset_index()
    else:
        x= tempdf.groupby('region').sum()[['Gold','Silver','Bronze']].sort_values('Gold',ascending=False)

    x['total']=x['Gold']+x['Silver']+x['Bronze']
    
    return x 

def data_overtime(df,col):
    data_over_years=df.drop_duplicates(['Year',col])['Year'].value_counts().reset_index().sort_values('Year')
    return data_over_years


def most_successful(df,sport):
    temp_df= df.dropna(subset=['Medal'])

    if sport != 'Overall':
        temp_df=temp_df[temp_df['Sport']==sport] 
    x=temp_df['Name'].value_counts().reset_index().merge(df,how='outer').dropna(subset=['Medal'])[['Name','count','Sport','region']].drop_duplicates(subset=['Name']).head(15)
    x=x.dropna(subset=['count'])
    x['count']=x['count'].astype(int)
    return x

def yearwise_medaltally(df,country):
    y=df.dropna(subset=['Medal'])
    y.drop_duplicates(subset=['Team','NOC','Games','Year','Season','City','Sport','Event','Medal'],inplace=True)
    if country!='Overall':
        y=y[y['region']==country]
    f=y.groupby('Year')['Medal'].count().reset_index() 

    return f

def country_event_hm(df,country):
    y=df.dropna(subset=['Medal'])
    y.drop_duplicates(subset=['Team','NOC','Games','Year','Season','City','Sport','Event','Medal'],inplace=True)
    z=y[y['region']==country] 
    pt=z.pivot_table(index='Sport',columns='Year',values='Medal',aggfunc='count').fillna(0).astype(int) 
    
    return pt 

def most_successful_athletes_regions(df,country):
    temp_df= df.dropna(subset=['Medal'])
    temp_df=temp_df[temp_df['region']==country] 
    x=temp_df['Name'].value_counts().reset_index().merge(df,how='outer').dropna(subset=['Medal'])[['Name','count','Sport']].drop_duplicates(subset=['Name'])
    x=x.dropna(subset=['count'])
    x['count']=x['count'].astype(int)
    return x.head(10)

def weight_v_height(df,sport):
    athletes=df.drop_duplicates(subset=['Name','region'])
    athletes['Medal'].fillna('No Medal',inplace=True)
    tdf=athletes[athletes['Sport']==sport]

    return tdf 



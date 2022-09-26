import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import hydralit_components as hc
from plotly.offline import init_notebook_mode, iplot
from PIL import Image
from streamlit_metrics import metric, metric_row


st.set_page_config(
    page_title="Suicides Dashboard",
    page_icon=":collision:",
    layout='wide'
)

#reading the csv file,
#filling na values of suicides with 0
df=pd.read_csv(r"who_suicide.csv")
df["suicides_no"].fillna(0,inplace=True)
df.info()



##################################
    
over_theme = {'txc_inactive': 'white','menu_background':'rgb(128,0,0)', 'option_active':'white'}
   #i used this menu_data below to make it easier if i want to add more pages later on 
menu_data = [

    {'label': 'Visuals'},
    ]


menu_id = hc.nav_bar(
    menu_definition=menu_data,
    override_theme=over_theme,
    sticky_nav=True,
    sticky_mode='sticky'
)
    
   
if menu_id == 'Visuals':
    st.write('')
    st.title(' Suicides Dashboard ')
    
    
    col1, col2 = st.columns(2)
    col1.metric("Total Nb. of Suicides", df["suicides_no"].sum())
    col2.metric("Country with Highest Nb. of Suicides", "Russian Federation", "+ 1.5M")
    



    year_list = sorted(df["year"].unique())

    selected_min_time, selected_max_time = st.select_slider(
        label = "Select Time Period",
        options = year_list,
        value = (min(year_list), max(year_list)),
    )
    
    country_list = df["country"].unique()

    selected_region = st.multiselect(
        label = "Select Countries",
        options = country_list,
        default = country_list
    )




## What is the total number of suicides among males and females between 1979 and 2016 ###
    st.header("What is the total number of suicides among males and females between 1979 and 2016?")

    suicides = df.groupby('year').suicides_no.sum()
    df2 = pd.DataFrame(df.groupby(['year','sex']).suicides_no.sum())
    df2 = df2.unstack()

# a line graph that shows the number of suicides among males and females between year 1979 and 2016
    fig0= px.line(
              df2,
              x=df2.index,
              y=df2.suicides_no.male,
              color_discrete_sequence=["blue"] * len(df2),
              title="Total Number of Suicides between 1979 and 2016",
              labels={
                     "index": "Year",
                     "y": "Number of Suicides",
                 },
              )
        
    fig0.add_scatter(x=df2.index, y=df2.suicides_no.female, name="Female")
     
    # to show the legends
    fig0['data'][0]['showlegend'] = True
    fig0['data'][0]['name'] = 'Male'
    fig0=go.Figure(fig0)

    st.plotly_chart(fig0,use_container_width=True)


#PLOT 2
    st.header("What is the Suicide Distribution amongst the genders in the top 10 countries with the highest number of suicides? ")
    df_gen=pd.DataFrame(df.groupby(['country','sex'])['suicides_no'].sum()).reset_index()
    df_gen=pd.merge(df_gen,pd.DataFrame(df_gen.groupby(['country'])['suicides_no'].sum()).reset_index(),on=['country'])
    df_gen.rename(columns={'suicides_no_x':'gender_suicides','suicides_no_y':'total_suicides'},inplace=True)
    df_gen.sort_values(by=['total_suicides'],ascending=False,inplace=True)
    df_gen.head()
    df_gen_m=df_gen[df_gen['sex']=="male"]
    df_gen_fm=df_gen[df_gen['sex']=="female"]
    trace1 = go.Bar(
        x=df_gen_m['country'].head(10),
        y=df_gen_m['gender_suicides'].head(10),
        name='Male Suicides'
    )
    trace2 = go.Bar(
        x=df_gen_fm['country'].head(10),
        y=df_gen_fm['gender_suicides'].head(10),
        name='Female Suicides'
    )

    data = [trace1, trace2]
    layout = go.Layout(
        barmode='group',
        title='Suicide Distribution amongst the Genders in top 10 countries having max. suicides'
    )

    fig = go.Figure(data=data, layout=layout)
    st.plotly_chart(fig,use_container_width=True)

#PLOT 3
    st.header("What is the Suicide Distribution amongst the genders in the least 10 countries with the highest number of suicides? ")

    traceA = go.Bar(
        x=df_gen_m['country'].tail(10),
        y=df_gen_m['gender_suicides'].tail(10),
        name='Male Suicides'
    )
    traceB = go.Bar(
        x=df_gen_fm['country'].tail(10),
        y=df_gen_fm['gender_suicides'].tail(10),
        name='Female Suicides'
    )

    data = [traceA, traceB]
    layout = go.Layout(
        barmode='group',
        title='Suicide Distribution amongst the Genders in top 10 countries having least number of suicides'
    )

    fig1 = go.Figure(data=data, layout=layout)
    st.plotly_chart(fig1,use_container_width=True)



#PLOT 4
    st.header("What is the age group that has the highest number of suicides ?")
    suicide_age = df.groupby('age').suicides_no.sum()
    suicide_age = pd.DataFrame(suicide_age)

    #Creating a temporary dataframe and merging two tables to sort the index of 'suicide_age'
    tempdf = pd.DataFrame(range(6), 
                      index = ['5-14 years', '15-24 years', '25-34 years', '35-54 years', '55-74 years', '75+ years'])
    suicide_age = pd.merge(tempdf, suicide_age, left_index = True, right_index = True, how = 'inner')
    suicide_age.drop(columns = 0, inplace = True)
    fig2= px.line(
                  suicide_age,
                  x=suicide_age.index,
                  y=suicide_age.suicides_no,
                  color_discrete_sequence=["green"] * len(df2),
                  title="Distribution of Suicides by Age",
                  labels={
                         "index": "Age",
                         "suicides_no": "Number of Suicides",
                     },
                  )
    fig2=go.Figure(fig2)
    st.plotly_chart(fig2,use_container_width=True)

    st.subheader("Summary")
    container1 = st.container()
    container1.write('This dashboard helps you understand the distribution of suicides among age groups, countries, and gender.')
    container2 = st.container()
    container2.write("Link of the Suicides Dataset: https://www.kaggle.com/datasets/szamil/who-suicide-statistics ")

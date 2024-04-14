import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import pymysql
import plotly.express as px
import requests 
import json
from PIL import Image

#DataFrame Creation
#Mysql con
mydb = pymysql.connect(host='127.0.0.1', user='root', password='Prajith581998@', database='phonepe_data')
cursor = mydb.cursor()

#Aggregated_insurance_df
cursor.execute("SELECT * FROM aggregated_insurance;")
mydb.commit()
table7 = cursor.fetchall()

Aggregated_insurance= pd.DataFrame(table7,columns = ("States", "Years", "Quarter", "Transaction_type",
                                                 "Transaction_count","Transaction_amount"))

#aggregated_transaction_df
cursor.execute(" SELECT * FROM aggregated_transaction")
mydb.commit()
table1=cursor.fetchall()

Aggregated_transaction=pd.DataFrame(table1,columns=("States","Years","Quarter","Transaction_type",
                                                    "Transaction_count","Transaction_amount"))

#aggregated_user table
cursor.execute(" SELECT * FROM aggregated_user")
mydb.commit()
table2=cursor.fetchall()

Aggregated_user=pd.DataFrame(table2,columns=("States","Years","Quarter","Brands",
                                             "Transaction_count","Percentage"))

#map_insurance table
cursor.execute("SELECT * FROM map_insurance")
mydb.commit()
table8 = cursor.fetchall()

Map_insurance = pd.DataFrame(table8,columns = ("States", "Years", "Quarter", "Districts",
                                               "Transaction_count","Transaction_amount"))

#map_transaction table
cursor.execute(" SELECT * FROM map_transaction")
mydb.commit()
table3=cursor.fetchall()

Map_transaction=pd.DataFrame(table3,columns=("States","Years","Quarter","Districts",
                                             "Transaction_count","Transaction_amount"))

#map_user table
cursor.execute(" SELECT * FROM map_user")
mydb.commit()
table4=cursor.fetchall()

Map_user=pd.DataFrame(table4,columns=("States","Years","Quarter","Districts",
                                      "RegisteredUsers","AppOpens"))

#top_insurance table
cursor.execute("SELECT * FROM top_insurance")
mydb.commit()
table9 = cursor.fetchall()

Top_insurance = pd.DataFrame(table9,columns = ("States", "Years", "Quarter", "Pincodes",
                                               "Transaction_count", "Transaction_amount"))

#top_transaction table
cursor.execute(" SELECT * FROM top_transaction")
mydb.commit()
table5=cursor.fetchall()

Top_transaction=pd.DataFrame(table5,columns=("States","Years","Quarter","Pincodes",
                                             "Transaction_count","Transaction_amount"))

#top_user table
cursor.execute(" SELECT * FROM top_user")
mydb.commit()
table6=cursor.fetchall()

Top_user=pd.DataFrame(table6,columns=("States","Years","Quarter",
                                      "Pincodes","RegisteredUsers"))

def Transaction_count_amount(df,yr):
    year=df[df['Years']== yr]
    year.reset_index(drop=True,inplace=True)
    group_year=year.groupby("States")[['Transaction_count','Transaction_amount']].sum()
    group_year.reset_index(inplace = True)

    col1,col2=st.columns(2)
    with col1:
        fig_count=px.bar(group_year,x='States',y='Transaction_count',title=f"{yr} Transaction_Count",
                        color_discrete_sequence=px.colors.sequential.Electric, height=500, width=500)
        st.plotly_chart(fig_count)
    
    with col2:
        fig_amount=px.bar(group_year,x='States',y='Transaction_amount',title=f"{yr} Transaction_Amount",
                        color_discrete_sequence=px.colors.sequential.Oryel, height=500, width=500)
        st.plotly_chart(fig_amount)
    
    col1,col2=st.columns(2)
    with col1:
        url="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        response=requests.get(url)
        coordinate=json.loads(response.content)
        state_names=[]
        for i in coordinate["features"]:
            state_names.append(i['properties']['ST_NM'])
        state_names.sort()
        
        fig_geo_count=px.choropleth(group_year, geojson=coordinate, locations="States",featureidkey="properties.ST_NM",
                                    color="Transaction_count",color_continuous_scale="ylorrd",height=500,width=500,
                                    range_color=(group_year["Transaction_count"].min(),group_year["Transaction_count"].max()),
                                    hover_name="States", title= f"{yr} TRANSACTION COUNT",fitbounds="locations")
        fig_geo_count.update_geos(visible= False)
        st.plotly_chart(fig_geo_count)

    with col2:
        fig_geo_amount=px.choropleth(group_year, geojson=coordinate, locations="States",featureidkey="properties.ST_NM",
                                color="Transaction_amount",color_continuous_scale="ylgnbu",height=500,width=500,
                                range_color=(group_year["Transaction_amount"].min(),group_year["Transaction_amount"].max()),
                                hover_name="States", title= f"{yr} TRANSACTION AMOUNT",fitbounds="locations")
        fig_geo_amount.update_geos(visible= False)
        st.plotly_chart(fig_geo_amount)

    return year

def Transaction_count_amount_Q(df,quarter):
    year=df[df['Quarter']== quarter]
    year.reset_index(drop=True,inplace=True)
    group_year=year.groupby("States")[['Transaction_count','Transaction_amount']].sum()
    group_year.reset_index(inplace = True)

    col1,col2=st.columns(2)
    with col1:
        fig_count=px.bar(group_year,x='States',y='Transaction_count',title=f"{year['Years'].min()} YEAR {quarter} QUARTER Transaction_Count",
                        color_discrete_sequence=px.colors.sequential.Electric, height=500, width=500)
        st.plotly_chart(fig_count)
    with col2:
        fig_amount=px.bar(group_year,x='States',y='Transaction_amount',title=f"{year['Years'].min()} YEAR {quarter} QUARTER Transaction_Amount",
                        color_discrete_sequence=px.colors.sequential.Oryel, height=500, width=500)
        st.plotly_chart(fig_amount)

    col1,col2=st.columns(2)
    with col1:
        url="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        response=requests.get(url)
        coordinate=json.loads(response.content)
        state_names=[]
        for i in coordinate["features"]:
            state_names.append(i['properties']['ST_NM'])
        state_names.sort()

        fig_geo_count=px.choropleth(group_year, geojson=coordinate, locations="States",featureidkey="properties.ST_NM",
                                    color="Transaction_count",color_continuous_scale="ylorrd",height=500,width=500,
                                    range_color=(group_year["Transaction_count"].min(),group_year["Transaction_count"].max()),
                                    hover_name="States", title= f"{year['Years'].min()} YEAR {quarter} QUARTER  TRANSACTION COUNT",fitbounds="locations")
        fig_geo_count.update_geos(visible= False)
        st.plotly_chart(fig_geo_count)
    
    with col2:
        fig_geo_amount=px.choropleth(group_year, geojson=coordinate, locations="States",featureidkey="properties.ST_NM",
                                color="Transaction_amount",color_continuous_scale="ylgnbu",height=500,width=500,
                                range_color=(group_year["Transaction_amount"].min(),group_year["Transaction_amount"].max()),
                                hover_name="States", title= f"{year['Years'].min()} YEAR {quarter} QUARTER  TRANSACTION AMOUNT",fitbounds="locations")
        fig_geo_amount.update_geos(visible= False)
        st.plotly_chart(fig_geo_amount)

    return year

def Agg_tran_type(df,state):
    year=df[df['States']== state]
    year.reset_index(drop=True,inplace=True)
    group_year=year.groupby("Transaction_type")[['Transaction_count','Transaction_amount']].sum()
    group_year.reset_index(inplace = True)
    
    col1,col2=st.columns(2)
    with col1:
        fig_pie_1=px.pie(data_frame=year,names="Transaction_type",values="Transaction_amount",
                        width=500,title=f"{state.upper()} TRANSACTION AMOUNT",
                        color_discrete_sequence=px.colors.sequential.Cividis,hole= 0.3)
        st.plotly_chart(fig_pie_1)
    with col2:    
        fig_pie_2=px.pie(data_frame=year,names="Transaction_type",values="Transaction_count",
                        width=600,title=f"{state.upper()} TRANSACTION COUNT",
                        color_discrete_sequence=px.colors.sequential.Bluyl_r,hole= 0.3)
        st.plotly_chart(fig_pie_2)

#Agg_user
def Agg_user_plot1(df,year):
    agg_user=df[df["Years"]==year]
    agg_user.reset_index(drop=True,inplace=True)
    agg_userg=pd.DataFrame(agg_user.groupby("Brands")["Transaction_count"].sum())
    agg_userg.reset_index(inplace=True)

    fig_bar1=px.bar(agg_userg,x="Brands",y="Transaction_count",title=f"{year} BRANDS & TRANSACTION COUNT",
                    width=800,color_discrete_sequence=px.colors.sequential.Oryel_r,hover_name="Brands")
    st.plotly_chart(fig_bar1)

    return agg_user

#Agg_user_p2
def Agg_user_plot2(df,quarter):
    agg_user_q=df[df["Quarter"]==quarter]
    agg_user_q.reset_index(drop=True,inplace=True)
    agg_user_qg=pd.DataFrame(agg_user_q.groupby("Brands")["Transaction_count"].sum())
    agg_user_qg.reset_index(inplace=True)

    fig_bar1=px.bar(agg_user_qg,x="Brands",y="Transaction_count",title= f"{quarter} QUARTER-BRANDS & TRANSACTION COUNT",
                        width=800,color_discrete_sequence=px.colors.sequential.Jet,hover_name="Brands")
    st.plotly_chart(fig_bar1)

    return agg_user_q

#Agg_user_p3
def Agg_user_plot3(df,state):
    agg_user_qs=df[df["States"]==state]
    agg_user_qs.reset_index(drop=True,inplace=True)

    fig_line1=px.line(agg_user_qs,x="Brands",y="Transaction_count",hover_data="Percentage",
                    title=f"{state.upper()}-BRANDS & TRANSACTION COUNT & PERCENTAGE",width=800,markers=True)
    st.plotly_chart(fig_line1)

#Map_insurance_districts
def Map_insur_dist(df,state):
    year=df[df['States']== state]
    year.reset_index(drop=True,inplace=True)
    group_year=year.groupby("Districts")[['Transaction_count','Transaction_amount']].sum()
    group_year.reset_index(inplace = True)

    col1,col2=st.columns(2)
    with col1:
        fig_bar_1=px.bar(group_year,x="Transaction_amount",y="Districts",orientation="h",height=500,
                        title=f"{state.upper()}-DISTRICT & TRANSACTION AMOUNT",color_discrete_sequence=px.colors.sequential.Oryel_r)
        st.plotly_chart(fig_bar_1)
    with col2:
        fig_bar_2=px.bar(group_year,x="Transaction_count",y="Districts",orientation="h",height=500,
                        title=f"{state.upper()}-DISTRICT & TRANSACTION COUNT",color_discrete_sequence=px.colors.sequential.Sunsetdark)
        st.plotly_chart(fig_bar_2)

#map_user_plot1
def map_user_plot1(df,year):
    map_user=df[df["Years"]==year]
    map_user.reset_index(drop=True,inplace=True)

    map_userg=map_user.groupby("States")[["RegisteredUsers","AppOpens"]].sum()
    map_userg.reset_index(inplace=True)

    fig_line1=px.line(map_userg,x="States",y=["RegisteredUsers","AppOpens"],
                        title=f"{year}-REGISTERED USERS & APPOPENS",width=900,height=750,markers=True)
    st.plotly_chart(fig_line1)

    return map_user

#map_user_plot2
def map_user_plot2(df,quarter):
    map_userq=df[df["Quarter"]==quarter]
    map_userq.reset_index(drop=True,inplace=True)
    map_userqg=map_userq.groupby("States")[["RegisteredUsers","AppOpens"]].sum()
    map_userqg.reset_index(inplace=True)

    fig_line2=px.line(map_userqg,x="States",y=["RegisteredUsers","AppOpens"],
                        title=f"{df['Years'].min()}-{quarter} QUARTER-REGISTERED USERS & APPOPENS",width=900,
                        height=750,markers=True,color_discrete_sequence=px.colors.sequential.Blackbody)
    st.plotly_chart(fig_line2)

    return map_userq

#map_user_plot3
def map_user_plot3(df,states):
    map_userqs=df[df["States"]==states]
    map_userqs.reset_index(drop=True,inplace=True)

    col1,col2=st.columns(2)
    with col1:
        fig_bar1=px.bar(map_userqs,x="RegisteredUsers",y="Districts",orientation="h",
                        title=f"{states.upper()}-REGISTERED USERS",height=800,color_discrete_sequence=px.colors.sequential.Agsunset)
        st.plotly_chart(fig_bar1)
    with col2:
        fig_bar2=px.bar(map_userqs,x="AppOpens",y="Districts",orientation="h",
                        title=f"{states.upper()}-APPOPENS",height=800,color_discrete_sequence=px.colors.sequential.Bluered)
        st.plotly_chart(fig_bar2)

#top_insur_plot1
def top_insur_plot1(df,state):
    top_insur=df[df["States"]==state]
    top_insur.reset_index(drop=True,inplace=True)

    col1,col2=st.columns(2)
    with col1:
        fig_bar1=px.bar(top_insur,x="Quarter",y="Transaction_amount",hover_data="Pincodes",
                        title="TRANSACTION AMOUNT",height=500,width=600,color_discrete_sequence=px.colors.sequential.Oryel_r)
        st.plotly_chart(fig_bar1)
    with col2:
        fig_bar2=px.bar(top_insur,x="Quarter",y="Transaction_count",hover_data="Pincodes",
                        title="TRANSACTION COUNT",height=500,width=600,color_discrete_sequence=px.colors.sequential.Agsunset)
        st.plotly_chart(fig_bar2)

#top_user_plot1
def top_user_plot1(df,year):
    top_user=df[df["Years"]==year]
    top_user.reset_index(drop=True,inplace=True)
    top_userg=pd.DataFrame(top_user.groupby(["States","Quarter"])["RegisteredUsers"].sum())
    top_userg.reset_index(inplace=True)

    fig_bar1=px.bar(top_userg,x="States",y="RegisteredUsers",color="Quarter",
                        title=f"{year}-REGISTERED USERS",height=800,width=750,
                        color_discrete_sequence=px.colors.sequential.Jet,hover_name="States")
    st.plotly_chart(fig_bar1)

    return top_user

#top_user_plot2
def top_user_plot2(df,state):
    Top_user_YS=df[df["States"]==state]
    Top_user_YS.reset_index(drop=True,inplace=True)

    fig_bar1=px.bar(Top_user_YS,x="Quarter",y="RegisteredUsers",title="REGISTERED USERS-PINCODES-QUARTER",
                    width=850,height=700,color="RegisteredUsers",hover_data="Pincodes",
                    color_continuous_scale=px.colors.sequential.Burg_r)
    st.plotly_chart(fig_bar1)

#topchart_transaction_amount
def topchart_transaction_amount(table_name):
        mydb = pymysql.connect(host='127.0.0.1', user='root', password='Prajith581998@', database='phonepe_data')
        cursor = mydb.cursor()
        #plot1
        query1=f'''SELECT States, SUM(Transaction_amount) as Transaction_amount 
                FROM {table_name}
                GROUP BY states 
                ORDER BY Transaction_amount DESC 
                LIMIT 10'''
        cursor.execute(query1)
        t1=cursor.fetchall()
        mydb.commit()

        df1=pd.DataFrame(t1,columns=("States","Transaction_amount"))
        col1,col2=st.columns(2)
        with col1:
            fig_bar1=px.bar(df1,x="States",y="Transaction_amount",title="TOP 10-TRANSACTION AMOUNT",
                            height=500,width=600,color_discrete_sequence=px.colors.sequential.Oryel_r,hover_name="States")
            st.plotly_chart(fig_bar1)

        #plot2
        query2=f'''SELECT States, SUM(Transaction_amount) as Transaction_amount 
                FROM {table_name}
                GROUP BY states 
                ORDER BY Transaction_amount
                LIMIT 10'''
        cursor.execute(query2)
        t2=cursor.fetchall()
        mydb.commit()

        df2=pd.DataFrame(t2,columns=("States","Transaction_amount"))
        with col2:
            fig_bar2=px.bar(df2,x="States",y="Transaction_amount",title="LAST 10-TRANSACTION AMOUNT",
                            height=500,width=600,color_discrete_sequence=px.colors.sequential.Aggrnyl,hover_name="States")
            st.plotly_chart(fig_bar2)

        #plot3
        query3=f'''SELECT States, AVG(Transaction_amount) as Transaction_amount 
                FROM {table_name}
                GROUP BY states 
                ORDER BY Transaction_amount'''
        cursor.execute(query3)
        t3=cursor.fetchall()
        mydb.commit()

        df3=pd.DataFrame(t3,columns=("States","Transaction_amount"))

        fig_bar3=px.bar(df3,x="Transaction_amount",y="States",title="AVERAGE-TRANSACTION AMOUNT",orientation="h",
                        height=700,width=800,color_discrete_sequence=px.colors.sequential.algae_r,hover_name="States")
        st.plotly_chart(fig_bar3)

#topchart_transaction_count
def topchart_transaction_count(table_name):
        mydb = pymysql.connect(host='127.0.0.1', user='root', password='Prajith581998@', database='phonepe_data')
        cursor = mydb.cursor()
        #plot1
        query1=f'''SELECT States, SUM(Transaction_count) as Transaction_count 
                FROM {table_name}
                GROUP BY states 
                ORDER BY Transaction_count DESC 
                LIMIT 10'''
        cursor.execute(query1)
        t1=cursor.fetchall()
        mydb.commit()

        df1=pd.DataFrame(t1,columns=("States","Transaction_count"))
        col1,col2=st.columns(2)
        with col1:
            fig_bar1=px.bar(df1,x="States",y="Transaction_count",title="TOP 10-TRANSACTION COUNT",
                            height=500,width=600,color_discrete_sequence=px.colors.sequential.Cividis_r,hover_name="States")
            st.plotly_chart(fig_bar1)

        #plot2
        query2=f'''SELECT States, SUM(Transaction_count) as Transaction_count 
                FROM {table_name}
                GROUP BY states 
                ORDER BY Transaction_count
                LIMIT 10'''
        cursor.execute(query2)
        t2=cursor.fetchall()
        mydb.commit()

        df2=pd.DataFrame(t2,columns=("States","Transaction_count"))
        with col2:
            fig_bar2=px.bar(df2,x="States",y="Transaction_count",title="LAST 10-TRANSACTION COUNT",
                            height=500,width=600,color_discrete_sequence=px.colors.sequential.Blues_r,hover_name="States")
            st.plotly_chart(fig_bar2)

        #plot3
        query3=f'''SELECT States, AVG(Transaction_count) as Transaction_count 
                FROM {table_name}
                GROUP BY states 
                ORDER BY Transaction_count'''
        cursor.execute(query3)
        t3=cursor.fetchall()
        mydb.commit()

        df3=pd.DataFrame(t3,columns=("States","Transaction_count"))

        fig_bar3=px.bar(df3,x="Transaction_count",y="States",title="AVERAGE-TRANSACTION COUNT",orientation="h",
                        height=700,width=800,color_discrete_sequence=px.colors.sequential.amp_r,hover_name="States")
        st.plotly_chart(fig_bar3)

#topchart_registeredusers
def topchart_registeredusers(table_name,state):
        mydb = pymysql.connect(host='127.0.0.1', user='root', password='Prajith581998@', database='phonepe_data')
        cursor = mydb.cursor()
        #plot1
        query1=f'''SELECT Districts, SUM(RegisteredUsers) as RegisteredUsers 
                FROM {table_name}
                where States= '{state}'
                GROUP BY Districts 
                ORDER BY RegisteredUsers DESC 
                LIMIT 10'''
        cursor.execute(query1)
        t1=cursor.fetchall()
        mydb.commit()

        df1=pd.DataFrame(t1,columns=("Districts","RegisteredUsers"))
        col1,col2=st.columns(2)
        with col1:
            fig_bar1=px.bar(df1,x="Districts",y="RegisteredUsers",title="TOP 10-REGISTERED USERS",
                            height=500,width=600,color_discrete_sequence=px.colors.sequential.Oryel_r,hover_name="Districts")
            st.plotly_chart(fig_bar1)

        #plot2
        query2=f'''SELECT Districts, SUM(RegisteredUsers) as RegisteredUsers 
                FROM {table_name}
                where States= '{state}'
                GROUP BY Districts 
                ORDER BY RegisteredUsers 
                LIMIT 10'''
        cursor.execute(query2)
        t2=cursor.fetchall()
        mydb.commit()

        df2=pd.DataFrame(t2,columns=("Districts","RegisteredUsers"))
        with col2:
            fig_bar2=px.bar(df2,x="Districts",y="RegisteredUsers",title="LAST 10-REGISTERED USERS",
                            height=500,width=600,color_discrete_sequence=px.colors.sequential.Aggrnyl,hover_name="Districts")
            st.plotly_chart(fig_bar2)

        #plot3
        query3=f'''SELECT Districts, AVG(RegisteredUsers) as RegisteredUsers 
                FROM {table_name}
                where States= '{state}'
                GROUP BY Districts 
                ORDER BY RegisteredUsers'''
        cursor.execute(query3)
        t3=cursor.fetchall()
        mydb.commit()

        df3=pd.DataFrame(t3,columns=("Districts","RegisteredUsers"))

        fig_bar3=px.bar(df3,x="RegisteredUsers",y="Districts",title="AVERAGE-REGISTERED USERS",orientation="h",
                        height=700,width=800,color_discrete_sequence=px.colors.sequential.algae_r,hover_name="Districts")
        st.plotly_chart(fig_bar3)

#topchart_appopens
def topchart_appopens(table_name,state):
        mydb = pymysql.connect(host='127.0.0.1', user='root', password='Prajith581998@', database='phonepe_data')
        cursor = mydb.cursor()
        #plot1
        query1=f'''SELECT Districts, SUM(AppOpens) as AppOpens 
                FROM {table_name}
                where States= '{state}'
                GROUP BY Districts 
                ORDER BY AppOpens DESC 
                LIMIT 10'''
        cursor.execute(query1)
        t1=cursor.fetchall()
        mydb.commit()

        df1=pd.DataFrame(t1,columns=("Districts","AppOpens"))
        col1,col2=st.columns(2)
        with col1:
            fig_bar1=px.bar(df1,x="Districts",y="AppOpens",title="TOP 10-APPOPENS",
                            height=500,width=600,color_discrete_sequence=px.colors.sequential.Oryel_r,hover_name="Districts")
            st.plotly_chart(fig_bar1)

        #plot2
        query2=f'''SELECT Districts, SUM(AppOpens) as AppOpens 
                FROM {table_name}
                where States= '{state}'
                GROUP BY Districts 
                ORDER BY AppOpens 
                LIMIT 10'''
        cursor.execute(query2)
        t2=cursor.fetchall()
        mydb.commit()

        df2=pd.DataFrame(t2,columns=("Districts","AppOpens"))
        with col2:
            fig_bar2=px.bar(df2,x="Districts",y="AppOpens",title="LAST 10-APPOPENS",
                            height=500,width=600,color_discrete_sequence=px.colors.sequential.Aggrnyl,hover_name="Districts")
            st.plotly_chart(fig_bar2)

        #plot3
        query3=f'''SELECT Districts, AVG(AppOpens) as AppOpens 
                FROM {table_name}
                where States= '{state}'
                GROUP BY Districts 
                ORDER BY AppOpens'''
        cursor.execute(query3)
        t3=cursor.fetchall()
        mydb.commit()

        df3=pd.DataFrame(t3,columns=("Districts","AppOpens"))

        fig_bar3=px.bar(df3,x="AppOpens",y="Districts",title="AVERAGE-APPOPENS",orientation="h",
                        height=700,width=800,color_discrete_sequence=px.colors.sequential.algae_r,hover_name="Districts")
        st.plotly_chart(fig_bar3)

#topchart_transaction_count
def topchart_transactioncount(table_name):
        mydb = pymysql.connect(host='127.0.0.1', user='root', password='Prajith581998@', database='phonepe_data')
        cursor = mydb.cursor()
        #plot1
        query1=f'''SELECT Brands, sum(Transaction_count) as Transaction_count 
                FROM {table_name}
                GROUP BY Brands
                ORDER BY Transaction_count DESC
                LIMIT 10'''
        cursor.execute(query1)
        t1=cursor.fetchall()
        mydb.commit()

        df1=pd.DataFrame(t1,columns=("Brands","Transaction_count"))
        col1,col2=st.columns(2)
        with col1:
            fig_bar1=px.bar(df1,x="Brands",y="Transaction_count",title="TOP 10-TRANSACTION COUNT",
                            height=500,width=600,color_discrete_sequence=px.colors.sequential.Oryel_r,hover_name="Brands")
            st.plotly_chart(fig_bar1)

        #plot2
        query2=f'''SELECT Brands, sum(Transaction_count) as Transaction_count 
                FROM {table_name}
                GROUP BY Brands
                ORDER BY Transaction_count
                LIMIT 10'''
        cursor.execute(query2)
        t2=cursor.fetchall()
        mydb.commit()

        df2=pd.DataFrame(t2,columns=("Brands","Transaction_count"))
        with col2:
            fig_bar2=px.bar(df2,x="Brands",y="Transaction_count",title="LAST 10-TRANSACTION COUNT",
                            height=500,width=600,color_discrete_sequence=px.colors.sequential.Aggrnyl,hover_name="Brands")
            st.plotly_chart(fig_bar2)


#Streamlit part
st.set_page_config(layout="wide")
st.title(":blue[PhonePe]")
with st.sidebar:
    select=option_menu("Menu",['Home','Data Exploration','Top Charts'])

if select == 'Home':
    col1,col2=st.columns(2)
    with col1:
        st.video(r'C:\Users\ELCOT\Desktop\New vs\home-fast-secure-v3.mp4')
    with col2:
        st.header("India's Digital Wallet & Online Payment App")
        st.subheader("Simple, Fast & Secure")
        st.write("***One app for all things money***")
        st.write("***Pay whenever you like, wherever you like***")
        st.write("***Find all your favourite apps on PhonePe Switch***")
        st.write("****Transfer money, pay bills, make easy payments at stores and invest smartly - all on the app you trust!****")
        st.download_button("Download the App","https://www.phonepe.com/app-download/")

    col3,col4=st.columns(2)
    with col3:
        st.header("PhonePe for Business")
        st.subheader("Accelerate business growth with PhonePe Payment Gateway")
        st.write("***Using PhonePe to accept payments as a merchant?***")
        st.write("***Manage your accounts & store listing, increase customer walk-ins and grow your business with our business app***")
        st.write("***Handle large-scale transactions with dynamic routing ensuring 100% uptime***")
        st.download_button("Download PhonePe for Business","https://www.phonepe.com/app-download/")
    with col4:
        st.image(Image.open(r"C:\Users\ELCOT\Desktop\New vs\phonepe photo bussiness.png"))

elif select == 'Data Exploration':
    tab1,tab2,tab3=st.tabs(['Aggregated Analysis','Map Analysis','Top Analysis'])

    with tab1:
        view1=st.selectbox('Select Method',['Aggregated Insurance','Aggregated Transaction','Aggregated User'])

        if view1 == 'Aggregated Insurance':
            col1,col2=st.columns(2)
            with col1:
                years=st.slider("Select The Year_AI",Aggregated_insurance["Years"].min(),
                                Aggregated_insurance["Years"].max(),Aggregated_insurance["Years"].min())
            Tran_Y=Transaction_count_amount(Aggregated_insurance,years)

            col1,col2=st.columns(2)
            with col1:
                quarters=st.slider("Select The Quarter_AI",Tran_Y["Quarter"].min(),
                                   Tran_Y["Quarter"].max(),Tran_Y["Quarter"].min())
            Transaction_count_amount_Q(Tran_Y,quarters)

        elif view1 == 'Aggregated Transaction':
            col1,col2=st.columns(2)
            with col1:
                years=st.slider("Select The Year_AT",Aggregated_transaction["Years"].min(),
                                Aggregated_transaction["Years"].max(),Aggregated_transaction["Years"].min())
            Agg_Tran_Y=Transaction_count_amount(Aggregated_transaction,years)

            col1,col2=st.columns(2)
            with col1:
                states=st.selectbox("Select The State_AT",Agg_Tran_Y["States"].unique())
            Agg_tran_type(Agg_Tran_Y,states)

            col1,col2=st.columns(2)
            with col1:
                quarters=st.slider("Select the Quarter_AT",Agg_Tran_Y["Quarter"].min(),
                                   Agg_Tran_Y["Quarter"].max(),Agg_Tran_Y["Quarter"].min())
            Agg_Tran_YQ=Transaction_count_amount_Q(Agg_Tran_Y,quarters)

            col1,col2=st.columns(2)
            with col1:
                states=st.selectbox("Select The State",Agg_Tran_YQ["States"].unique())
            Agg_tran_type(Agg_Tran_YQ,states)

        elif view1 == 'Aggregated User':
            col1,col2=st.columns(2)
            with col1:
                years=st.slider("Select The Year_AU",Aggregated_user["Years"].min(),
                                Aggregated_user["Years"].max(),Aggregated_user["Years"].min())
            Agg_User_Y=Agg_user_plot1(Aggregated_user,years)

            col1,col2=st.columns(2)
            with col1:
                quarters=st.slider("Select The Quarter_AU",Agg_User_Y["Quarter"].min(),
                                   Agg_User_Y["Quarter"].max(),Agg_User_Y["Quarter"].min())
            Agg_User_YQ= Agg_user_plot2(Agg_User_Y,quarters)

            col1,col2=st.columns(2)
            with col1:
                states=st.selectbox("Select The State_AU",Agg_User_YQ["States"].unique())
            Agg_user_plot3(Agg_User_YQ,states)

    with tab2:
        view2=st.selectbox('Select Method',['Map Insurance','Map Transaction','Map User'])
        if view2 == 'Map Insurance':
            col1,col2=st.columns(2)
            with col1:
                years=st.slider("Select The Year_MI",Map_insurance["Years"].min(),
                                Map_insurance["Years"].max(),Map_insurance["Years"].min())
            Map_insur_Y=Transaction_count_amount(Map_insurance,years)

            col1,col2=st.columns(2)
            with col1:
                states=st.selectbox("Select The State_MI",Map_insur_Y["States"].unique())
            Map_insur_dist(Map_insur_Y,states)

            col1,col2=st.columns(2)
            with col1:
                quarters=st.slider("Select the Quarter_MI",Map_insur_Y["Quarter"].min(),
                                   Map_insur_Y["Quarter"].max(),Map_insur_Y["Quarter"].min())
            Map_insur_YQ=Transaction_count_amount_Q(Map_insur_Y,quarters)

            col1,col2=st.columns(2)
            with col1:
                states=st.selectbox("Select The State",Map_insur_YQ["States"].unique())
            Map_insur_dist(Map_insur_YQ,states)


        elif view2 == 'Map Transaction':
            col1,col2=st.columns(2)
            with col1:
                years=st.slider("Select The Year_MT",Map_transaction["Years"].min(),
                                Map_transaction["Years"].max(),Map_transaction["Years"].min())
            Map_tran_Y=Transaction_count_amount(Map_transaction,years)

            col1,col2=st.columns(2)
            with col1:
                states=st.selectbox("Select The State_MT",Map_tran_Y["States"].unique())
            Map_insur_dist(Map_tran_Y,states)

            col1,col2=st.columns(2)
            with col1:
                quarters=st.slider("Select the Quarter_MT",Map_tran_Y["Quarter"].min(),
                                   Map_tran_Y["Quarter"].max(),Map_tran_Y["Quarter"].min())
            Map_tran_YQ=Transaction_count_amount_Q(Map_tran_Y,quarters)

            col1,col2=st.columns(2)
            with col1:
                states=st.selectbox("Select The State",Map_tran_YQ["States"].unique())
            Map_insur_dist(Map_tran_YQ,states)

        elif view2 == 'Map User':
            col1,col2=st.columns(2)
            with col1:
                years=st.slider("Select The Year_MU",Map_user["Years"].min(),
                                Map_user["Years"].max(),Map_user["Years"].min())
            Map_user_Y=map_user_plot1(Map_user,years)

            col1,col2=st.columns(2)
            with col1:
                quarters=st.slider("Select the Quarter_MU",Map_user_Y["Quarter"].min(),
                                   Map_user_Y["Quarter"].max(),Map_user_Y["Quarter"].min())
            Map_user_YQ=map_user_plot2(Map_user_Y,quarters)
            
            col1,col2=st.columns(2)
            with col1:
                states=st.selectbox("Select The State_MU",Map_user_YQ["States"].unique())
            map_user_plot3(Map_user_YQ,states)


    with tab3:
        view3=st.selectbox('Select Method',['Top Insurance','Top Transaction','Top User'])

        if view3 == 'Top Insurance':
            col1,col2=st.columns(2)
            with col1:
                years=st.slider("Select The Year_TI",Top_insurance["Years"].min(),
                                Top_insurance["Years"].max(),Top_insurance["Years"].min())
            Top_insur_Y=Transaction_count_amount(Top_insurance,years)

            col1,col2=st.columns(2)
            with col1:
                states=st.selectbox("Select The State_TI",Top_insur_Y["States"].unique())
            top_insur_plot1(Top_insur_Y,states)

            col1,col2=st.columns(2)
            with col1:
                quarters=st.slider("Select the Quarter_TI",Top_insur_Y["Quarter"].min(),
                                   Top_insur_Y["Quarter"].max(),Top_insur_Y["Quarter"].min())
            Top_insur_YQ=Transaction_count_amount_Q(Top_insur_Y,quarters)

        if view3 == 'Top Transaction':
            col1,col2=st.columns(2)
            with col1:
                years=st.slider("Select The Year_TT",Top_transaction["Years"].min(),
                                Top_transaction["Years"].max(),Top_transaction["Years"].min())
            Top_tran_Y=Transaction_count_amount(Top_transaction,years)

            col1,col2=st.columns(2)
            with col1:
                states=st.selectbox("Select The State_TT",Top_tran_Y["States"].unique())
            top_insur_plot1(Top_tran_Y,states)

            col1,col2=st.columns(2)
            with col1:
                quarters=st.slider("Select the Quarter_TT",Top_tran_Y["Quarter"].min(),
                                   Top_tran_Y["Quarter"].max(),Top_tran_Y["Quarter"].min())
            Top_tran_YQ=Transaction_count_amount_Q(Top_tran_Y,quarters) 

        elif view3 == 'Top User':
            col1,col2=st.columns(2)
            with col1:
                years=st.slider("Select The Year_TU",Top_user["Years"].min(),
                                Top_user["Years"].max(),Top_user["Years"].min())
            Top_user_Y=top_user_plot1(Top_user,years)

            col1,col2=st.columns(2)
            with col1:
                states=st.selectbox("Select The State_TU",Top_user_Y["States"].unique())
            top_user_plot2(Top_user_Y,states)


elif select == 'Top Charts':
    question=st.selectbox("Select the Question",
                          ["1.States with Highest & Lowest of Transaction Amount & Transaction Count of Aggregated Insurance",
                           "2.States with Highest & Lowest of Transaction Amount & Transaction Count of Map Insurance",
                           "3.States with Highest & Lowest of Transaction Amount & Transaction Count of Top Insurance",
                           "4.States with Highest & Lowest of Transaction Amount & Transaction Count of Aggregated Transaction",
                           "6.States with Highest & Lowest of Transaction Amount & Transaction Count of Top Transaction",
                           "7.States with Highest & Lowest of Transaction Count of Aggregated User",
                           "8.Districts with Highest & Lowest of RegisteredUsers of Map User",
                           "9.Districts with Highest & Lowest of AppOpens of Map User",
                           "10.Mobile Brands with Highest & Lowest of Transaction Count"])

    if question == "1.States with Highest & Lowest of Transaction Amount & Transaction Count of Aggregated Insurance":
        st.subheader("TRANSACTION AMOUNT")
        topchart_transaction_amount("aggregated_insurance")
        st.subheader("TRANSACTION COUNT")
        topchart_transaction_count("aggregated_insurance")

    elif question == "2.States with Highest & Lowest of Transaction Amount & Transaction Count of Map Insurance":
        st.subheader("TRANSACTION AMOUNT")
        topchart_transaction_amount("map_insurance")
        st.subheader("TRANSACTION COUNT")
        topchart_transaction_count("map_insurance")

    elif question == "3.States with Highest & Lowest of Transaction Amount & Transaction Count of Top Insurance":
        st.subheader("TRANSACTION AMOUNT")
        topchart_transaction_amount("top_insurance")
        st.subheader("TRANSACTION COUNT")
        topchart_transaction_count("top_insurance")

    elif question == "4.States with Highest & Lowest of Transaction Amount & Transaction Count of Aggregated Transaction":
        st.subheader("TRANSACTION AMOUNT")
        topchart_transaction_amount("aggregated_transaction")
        st.subheader("TRANSACTION COUNT")
        topchart_transaction_count("aggregated_transaction")

    elif question == "5.States with Highest & Lowest of Transaction Amount & Transaction Count of Map Transaction":
        st.subheader("TRANSACTION AMOUNT")
        topchart_transaction_amount("map_transaction")
        st.subheader("TRANSACTION COUNT")
        topchart_transaction_count("map_transaction")

    elif question == "6.States with Highest & Lowest of Transaction Amount & Transaction Count of Top Transaction":
        st.subheader("TRANSACTION AMOUNT")
        topchart_transaction_amount("top_transaction")
        st.subheader("TRANSACTION COUNT")
        topchart_transaction_count("top_transaction")

    elif question == "7.States with Highest & Lowest of Transaction Count of Aggregated User":
        st.subheader("TRANSACTION COUNT")
        topchart_transaction_count("aggregated_user")

    elif question == "8.Districts with Highest & Lowest of RegisteredUsers of Map User":
        states=st.selectbox("Select the State",Map_user["States"].unique())
        st.subheader("REGISTERED USERS")
        topchart_registeredusers("map_user",states)

    elif question == "9.Districts with Highest & Lowest of AppOpens of Map User":
        states=st.selectbox("Select the State",Map_user["States"].unique())
        st.subheader("APPOPENS")
        topchart_appopens("map_user",states)

    elif question == "10.Mobile Brands with Highest & Lowest of Transaction Count":
        st.subheader("TRANSACTION COUNTS")
        topchart_transactioncount("aggregated_user")

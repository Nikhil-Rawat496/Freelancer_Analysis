#streamlit after jupyter analysis for freelancer earning
#''streamlit run freelancer_dashboard.py''     to run streamlit file using terminal
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st

# data loading
def load_data():
    df = pd.read_csv('freelancer_earnings.csv')
    return df


# defining function for fill null values of column
def fill_null(df,dtype):
    # if you want to fill null values in original df then use inplace=True and don't return df.

    # print error and return if user give wrong data type or which is not int64 ,float64 and object
    if dtype not in('int64','float64','object'):
        print("[ERROR] Un-accepted Data type!")
        return df
    
    # dtypes: object, float64, 
    # loop for all columns and filling values according to col data type
    for col in df.select_dtypes(include = dtype):
        if df[col].dtype == 'object':
            mode = df[col].mode()[0]
            df[col] = df[col].fillna(mode) # filling mode for object 
        else : #dtype in('int64','float64'):
            mean = df[col].mean()
            df[col] = df[col].fillna(mean) # mean of col for numeric
           
    #new df returning after filling null values
    return df


# filter data 
def filter_data(df):
    st.sidebar.header("Filters")
    
    # filter by job category
    category = df['Job_Category'].unique()
    selected_category = st.sidebar.multiselect("Select category", category, default=category, placeholder='Select job category')

    # region filter
    region = df['Client_Region'].unique()
    selected_region = st.sidebar.multiselect("Filter Region", region, default=region, placeholder='Select region')
    
    filtered_df = df[
        (df['Job_Category'].isin(selected_category)) &
        (df['Client_Region'].isin(selected_region))           
    ]
    return filtered_df

def KPI_for_analysis(df):
    st.subheader("Over all Analysis")
    #KPI for data
    total_freelancer = df['Freelancer_ID'].nunique()
    total_earnings = df['Earnings_USD'].sum() #total income of freelanceres
    
    total_jobs = df['Job_Category'].count()

    platforms = df['Platform'].nunique()
    # unique() return unique values array
    #nunique() return unique values count

    kpi1, kpi2, kpi3, kpi4 = st.columns(4) 
    with kpi1:
        st.metric(label='Total Freelancer', value=total_freelancer)
    with kpi2:
        st.metric(label='Total Earning', value=total_earnings)
    with kpi3:
        st.metric(label='Total Jobs', value=total_jobs)
    with kpi4:
        st.metric(label='Total Platforms', value=platforms)
    

#function for bar and line plot
def bar_plot(data, x, y, rotation=None, xlabel=None, ylabel=None):
    fig, ax = plt.subplots()
    sns.barplot(data=data, x=x, y=y, ax=ax)
    plt.xticks(rotation=rotation)
    
    if xlabel is not None:
        ax.set_xlabel(xlabel)
    else:
        ax.set_xlabel('')
        
    if ylabel is not None:
        ax.set_ylabel(ylabel)
    else:
        ax.set_ylabel('')
        
    st.pyplot(fig)
    
    
    
def line_plot(data, x, y, marker=None, rotation=None, xlabel=None, ylabel=None):
    fig, ax= plt.subplots()
    sns.lineplot(data=data, x=x, y=y, marker=marker, ax=ax)
    #if user want rotation default=None
    plt.xticks(rotation=rotation)
    
    
    if xlabel is not None:
        ax.set_xlabel(xlabel)
    else:
        ax.set_xlabel('')
        
    if ylabel is not None:
        ax.set_ylabel(ylabel)
    else:
        ax.set_ylabel('')
        
    st.pyplot(fig)
   
   
   
    
def job_category_plot(df):
    st.subheader("Avg Earnings by job category") #heading for the chrt

    category_earning = df.groupby('Job_Category').agg({'Earnings_USD':'mean'})
    category_earning.rename(columns= {'Earnings_USD':'Avg_earning'}, inplace=True)

    bar_plot(category_earning, category_earning.index, 'Avg_earning', 45, ylabel='Avg Earning')
    
    

    
def experience_pie_plot(df):
    f_distribution, e_distribution = st.columns(2)

    with f_distribution:
        st.subheader('Freelancer Distribution')
        earning_distribution = df.groupby('Experience_Level').agg({'Earnings_USD':'sum', 'Freelancer_ID':'count'})
        explode = (0,0,0.1) #highlight the third part
        fig, ax=plt.subplots()
        
        plt.pie(data=earning_distribution, x='Freelancer_ID', labels=earning_distribution.index, explode=explode, autopct='%1.1f%%')
        st.pyplot(fig)

    with e_distribution:
        st.subheader("Earning Distribution")
        fig, ax=plt.subplots()
        plt.pie(data=earning_distribution, x=earning_distribution['Earnings_USD'],explode=explode, labels=earning_distribution.index, autopct='%1.1f%%')
        st.pyplot(fig) # to show figure
        
def jobrate_and_earning_scatter(df):
    st.subheader('Job success with earning')
    job_effect_earning = df.groupby(df['Job_Success_Rate'].astype(int)).agg({'Earnings_USD':'sum'})

    fig, ax=plt.subplots()
    sns.scatterplot(data=job_effect_earning, x=job_effect_earning.index, y='Earnings_USD', hue=job_effect_earning.index)
    plt.legend(bbox_to_anchor=(1,1))
    st.pyplot(fig)

def platform_plots(df):
    platform_d1, platform_d2= st.columns(2)
    with platform_d1:
        st.subheader('Hourly rate in platform')
        platform_earning = df.groupby('Platform').agg({'Hourly_Rate':'mean', 'Earnings_USD':'sum'}) 
        line_plot(platform_earning, 'Platform', 'Hourly_Rate', 'o')
        
    with platform_d2:
        st.subheader('Income in millions')
        line_plot(platform_earning, 'Platform', 'Earnings_USD', 'o')

def region_plots(df):
    region_pay, region_rate = st.columns(2)
    with region_pay:
        st.subheader('Region payment in millions')
        region_payment =df.groupby('Client_Region').agg({'Earnings_USD':'sum', 'Client_Rating':'mean'})

        bar_plot(region_payment, 'Client_Region', 'Earnings_USD', 45)

    with region_rate:
        st.subheader('Avg rating gived by clients to  freelancers by region')
        bar_plot(region_payment, 'Client_Region', 'Client_Rating', 45)

def payment_type_bar_plot(df):
    st.subheader('Payment in millions')
    payment_type = df.groupby('Payment_Method').agg({'Earnings_USD':'sum'})
    bar_plot(payment_type, 'Payment_Method', 'Earnings_USD')
       
def rating_and_rehire_plot(df):
    st.subheader('Rating effect rehire rate ')
    rating_and_rehire = df.groupby(df['Client_Rating'].astype(int)).agg({'Client_Rating':'count', 'Rehire_Rate':'mean'})

    bar_plot(rating_and_rehire, rating_and_rehire.index, 'Rehire_Rate') 


def marketing_spend_plots(df):
    st.subheader('Marketing spend effect on earnings')
    
    marketing_spend = df.groupby('Marketing_Spend').agg({'Earnings_USD':'sum', 'Job_Success_Rate':'mean'})
    line_plot(marketing_spend, 'Marketing_Spend', 'Earnings_USD', xlabel='Marketing Spend', ylabel='Total earnings')


    st.subheader('marketing spend effect on job rate')
    line_plot(marketing_spend, 'Marketing_Spend', 'Job_Success_Rate', xlabel='Marketing spend', ylabel='Job Success Rate')

def payment_on_duration_plots(df):
    st.subheader('Payment difference on job duration')
    payment_on_duration  =df.groupby('Job_Duration_Days').agg({'Earnings_USD':'sum', 'Hourly_Rate':'mean'})
    
    line_plot(payment_on_duration.head(20), 'Job_Duration_Days', 'Earnings_USD', 'o', xlabel='Job Duration Days', ylabel='Total earnings')

    st.subheader('Hourly rate in job duration')
    line_plot(payment_on_duration.head(20), 'Job_Duration_Days', 'Hourly_Rate', 'o', xlabel='Job Duration Days', ylabel='Avg hourly rate')

        
    
#main starts from here
#page layout   
st.set_page_config(layout='wide')

# Set the title of the app
st.title("Freelancer Earnings Analysis")

st.markdown("In this project we alanylize freelancers earnings from gived data. Data given in csv file which holding multiple platforms freelancers data to analyze. also we using streamlit to show analysis on app/web page. Using filters to filter data according to user choice and show them into graphs.")

# Reading file and loading data 
df = load_data()

dtype = 'int64'  # dtype to fill null values in dataframe col.
df = fill_null(df, dtype)

filtered_df = filter_data(df)
# filtered data frame copy of df 

if not filtered_df.empty:     #if applied filters 
    
    KPI_for_analysis(filtered_df)
  
    job_category_plot(filtered_df)
   
    experience_pie_plot(filtered_df)
   
    jobrate_and_earning_scatter(filtered_df)
   
    platform_plots(filtered_df)
    
    region_plots(filtered_df)
    
    payment_type_bar_plot(filtered_df)
    
    rating_and_rehire_plot(filtered_df)
    
    marketing_spend_plots(filtered_df)
    
    payment_on_duration_plots(filtered_df)
    
    #button to download filtered data
    st.download_button(label='Download Filtered Data', data=filtered_df.to_csv(index=False), file_name='Filtered_data.csv', mime='text/csv')
   
else:
    df = load_data()
    
    KPI_for_analysis(df)

    job_category_plot(df)
       
    experience_pie_plot(df)
   
    jobrate_and_earning_scatter(df)
   
    platform_plots(df)
    
    region_plots(df)
   
    payment_type_bar_plot(df)
   
    rating_and_rehire_plot(df)
    
    marketing_spend_plots(df)
   
    payment_on_duration_plots(df)
    
    
   
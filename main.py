import pandas as pd
import numpy as np
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

pd.options.display.float_format = '{:,.2f}'.format
# Create locators for ticks on the time axis
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()
df_yearly = pd.read_csv('data/annual_deaths_by_clinic.csv')
# parse_dates avoids DateTime conversion later
df_monthly = pd.read_csv('data/monthly_deaths.csv', 
                      parse_dates=['date'])
print(f"Any yearly dublicate? {df_yearly.duplicated().values.any()}")
print(f"Any monthly dublicate? {df_monthly.duplicated().values.any()}")
#calculate the percentage of women giving birth who die throught 1840s
percent_deaths_yearly=df_yearly['deaths'].sum()/df_yearly['births'].sum()*100
print(f"Percentage of women giving birth who die throught 1840s: {percent_deaths_yearly:.2f}%")
#Create a Matplotlib chart that visualise the Total Number of Births 🤱 and Deaths 💀 over Time
def total_births_deaths():
    plt.figure(figsize=(12,6), dpi=110)
    font1 = {'family':'serif','color':'blue','size':20}
    font2 = {'family':'serif','color':'darkred','size':15}
    ax1 = plt.gca() # get current axis
    ax2 = ax1.twinx()
    ax1.set_xlabel('Year')
    ax1.set_ylabel('deaths per year', fontdict=font1)
    ax2.set_ylabel('births per year', fontdict=font2)
    ax1.plot(df_monthly.date, df_monthly.deaths, color='skyblue')
    ax2.plot(df_monthly.date, df_monthly.births, color='red')
    plt.title('Total Number of Monthly Births and Deaths', fontdict=font1)
    plt.savefig('images/total_births_deaths.png')
    plt.show()
def yearly_births_deaths_clinic():
        line=px.line(df_yearly
                 , x='year'
                 , y=['births']
                 , title='Total Number of Yearly Births by Clinic'
                 ,color='clinic')
        line.update_layout(xaxis_title='Year', yaxis_title='Births and Deaths')
        line.write_image('images/yearly_births_deaths_clinic.png')
        line.show()
        line2=px.line(df_yearly
                 , x='year'
                 , y=['deaths']
                 , title='Total Number of Yearly Deaths by Clinic'
                 ,color='clinic')
        line2.update_layout(xaxis_title='Year', yaxis_title='Births and Deaths')
        line2.write_image('images/yearly_births_deaths_clinic2.png')
        line2.show()
yearly_births_deaths_clinic()
   



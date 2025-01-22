import pandas as pd
import numpy as np
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from scipy import stats

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
#avarage of deths per clinic
df_yearly['pct_deaths'] = df_yearly['deaths'] / df_yearly['births']
df_clinic1 = df_yearly[df_yearly['clinic'] == 'clinic 1']
avg = df_clinic1.deaths.sum() / df_clinic1.births.sum() * 100
print(f"Average deaths per year in clinic 1: {avg:.2f}%")
df_clinic2 = df_yearly[df_yearly['clinic'] == 'clinic 2']
avg = df_clinic2.deaths.sum() / df_clinic2.births.sum() * 100
print(f"Average deaths per year in clinic 2: {avg:.2f}%")
def yearly_pct_deaths():
    line=px.line(df_yearly
                 , x='year'
                 , y=['pct_deaths']
                 , title='Proportion of Yearly Deaths by Clinic'
                 ,color='clinic')
    line.update_layout(xaxis_title='Year', yaxis_title='Percentage of Deaths')
    line.write_image('images/yearly_pct_deaths.png')
    line.show()
# the effect of handwashing on the proportion of monthly deaths
df_monthly['pct_deaths'] = df_monthly['deaths'] / df_monthly['births']
#avarage rate after handwashing and before handwashing
handwashing_start = pd.to_datetime('1847-06-01')
before_handwashing = df_monthly[df_monthly.date < handwashing_start]
after_handwashing = df_monthly[df_monthly.date >= handwashing_start]
bw_rate = before_handwashing.deaths.sum() / before_handwashing.births.sum() * 100
aw_rate = after_handwashing.deaths.sum() / after_handwashing.births.sum() * 100
print(f"Average monthly deaths before handwashing: {bw_rate:.2f}%")
print(f"Average monthly deaths after handwashing: {aw_rate:.2f}%")
#Calculate a Rolling Average of the Death Rate 6-month
roll_df = before_handwashing.set_index('date').rolling(window=6).mean()
def after_and_before_handwashing():
     plt.figure(figsize=(10, 4), dpi=110)
     plt.title('Proportion of Monthly Deaths by Clinic, with Handwashing Start')
     ax=plt.gca()
    
     bw_line= plt.plot(before_handwashing.date
                       , before_handwashing.pct_deaths
                       , color='skyblue'
                       , label='before handwashing')
     aw_line= plt.plot(after_handwashing.date
                       , after_handwashing.pct_deaths
                       , color='red'
                       , label='after handwashing')
     ma_line= plt.plot(roll_df.index
                       , roll_df.pct_deaths
                       , color='darkred'
                       , label='6m rolling average')
     # , label='6m rolling average')
     plt.legend()
     ax.xaxis.set_major_locator(mdates.YearLocator())
     ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
     ax.set_xlim([df_monthly.date.min(), df_monthly.date.max()])
     plt.xlabel('Year')
     plt.ylabel('Percentage of Monthly Deaths')
     plt.savefig('images/after_and_before_handwashing.png')
     plt.show()
#average percentage of monthly deaths before handwashing (i.e., before June 1847)
avrg_before_handwashing=before_handwashing.pct_deaths.mean()*100
print(f"Average percentage of monthly deaths before handwashing: {avrg_before_handwashing:.2f}%")
#average percentage of monthly deaths after handwashing (i.e., after June 1847)
avrg_after_handwashing=after_handwashing.pct_deaths.mean()*100
print(f"Average percentage of monthly deaths after handwashing: {avrg_after_handwashing:.2f}%")
#handwashing reduce the average chance of dying in childbirth in percentage terms
print(f"Change in percentage of monthly deaths after handwashing: {avrg_before_handwashing-avrg_after_handwashing:.2f}%")
#lower chances of dying after handwashing compared to before
times=avrg_before_handwashing/avrg_after_handwashing
print(f"Ratio of average monthly deaths before and after handwashing: {times:.2f}")
#add a column to df_monthly that shows if a particular date was before or after the start of handwashing.
df_monthly['washing_hands'] = np.where(df_monthly['date'] < handwashing_start, 'NO', 'Yes')
def box_washing_hands():
    plt.figure(figsize=(10, 4), dpi=110)
    box= px.box(df_monthly
                ,x='washing_hands'
                , y='pct_deaths'
                ,color='washing_hands'
                , title='How Have the Stats Changed with Handwashing?')
                # , title='How Have the Stats Changed with Handwashing?')
    box.update_layout(xaxis_title='Washing Hands?', yaxis_title='Percentage of Monthly Deaths')
    box.write_image('images/box_washing_hands.png')
    box.show()
def Histogram_Monthly_Distribution_Outcomes():
     fig = px.histogram(df_monthly
                        ,x='pct_deaths'
                        ,marginal='box'
                        ,nbins=30
                        ,opacity=0.6
                        ,color='washing_hands'
                        ,title='Distribution of Monthly Death Rate by Handwashing'
                        ,barmode='overlay'
                        ,histnorm='percent'
                        )
     
     fig.update_layout(xaxis_title='Proportion of Monthly Deaths'
                       , yaxis_title='Count')
     
     fig.write_image('images/Histogram_Monthly_Distribution_Outcomes.png')
     fig.show()
'''Use Seaborn's .kdeplot() to create two kernel density estimates
 of the pct_deaths, one for before handwashing and one for after.'''  
def KDE_Monthly_Distribution_Outcomes():
     plt.figure(figsize=(10, 4), dpi=110)
     sns.kdeplot(before_handwashing.pct_deaths, 
                 shade=True, 
                 label='before handwashing',
                 clip=(0,1),  # Ensure it starts from 0
                 bw_adjust=0.5)  # Adjust bandwidth for smoothing
     sns.kdeplot(after_handwashing.pct_deaths, 
                 shade=True, 
                 label='after handwashing',
                 clip=(0,1),  # Ensure it starts from 0
                 bw_adjust=0.5)  # Adjust bandwidth for smoothing
     plt.title('Estimated PDF of Monthly Death Rate by Handwashing')
     plt.xlabel('Proportion of Monthly Deaths')
     plt.ylabel('Density')
     plt.legend()
     plt.xlim(0, 0.4)  # Set x-axis limits
     plt.ylim(0, None)  # Set y-axis limits to start from 0
     plt.savefig('images/KDE_Monthly_Distribution_Outcomes.png')
     plt.show()  
#Use T-test to calculate the p-value for the null hypothesis that the two distributions are identical.
t_stat, p_value = stats.ttest_ind(a=before_handwashing.pct_deaths, 
                                  b=after_handwashing.pct_deaths)
print(f'p-palue is {p_value:.10f}')
print(f't-statstic is {t_stat:.4}')
'''This code performs a t-test on the pct_deaths before 
and after handwashing and prints the p-value and t-statistic. 
If the p-value is small (e.g., less than 0.05), 
it suggests that handwashing had a significant effect on reducing deaths.'''



     









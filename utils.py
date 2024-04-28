import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Plotting functions
def plot_source_distribution(data):
    plt.figure(figsize=(10, 6))
    sns.countplot(data=data, x='Industry')
    plt.title('Distribution of Subscriptions by Industry')
    return plt 
    st.pyplot(plt)

def plot_source_pie_chart(data):
    plt.figure(figsize=(8, 8))
    data['Source'].value_counts().plot.pie(autopct='%1.1f%%')
    plt.title('Source Distribution')
    plt.ylabel('')  # Hide the y-label as it's not necessary
    return plt
    st.pyplot(plt)
    
def plot_frequency_histogram(data):
    plt.figure(figsize=(10, 6))
    sns.histplot(data=data, x='Frequency', bins=20, kde=True)
    plt.title('Histogram of Newsletter Frequencies per Week')
    plt.xlabel('Frequency of Newsletter per Week')
    plt.ylabel('Count of Subscriptions')
    return plt
    st.pyplot(plt)
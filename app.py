import streamlit as st
import mysql.connector
from mysql.connector import Error
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

from utils import plot_source_distribution, plot_source_pie_chart, plot_frequency_histogram
# Set the aesthetics for seaborn plots
sns.set_theme(style="whitegrid")

# Database configuration
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '**********',
    'database': 'newsletter_app'
}

# Database config for docker file
db_config = {
    'host': os.getenv('DATABASE_HOST', 'localhost'),
    'user': os.getenv('DATABASE_USER', 'root'),
    'password': os.getenv('DATABASE_PASSWORD', 'password'),
    'database': os.getenv('DATABASE_DB', 'mydatabase')
}

# Connect to MySQL database
def create_db_connection():
    connection = None
    try:
        connection = mysql.connector.connect(**db_config)
        print("MySQL Database connection successful")
    except Error as e:
        print(f"The error '{e}' occurred")
    return connection

# Create or check table existence
def create_subscription_table(connection):
    create_table_query = """
    CREATE TABLE IF NOT EXISTS sub_users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        email VARCHAR(255) NOT NULL UNIQUE,
        industry VARCHAR(50),
        source VARCHAR(50),
        subcategory VARCHAR(50),
        frequency INT
    );
    """
    cursor = connection.cursor()
    try:
        cursor.execute(create_table_query)
        connection.commit()
        print("Table checked/created successfully")
    except Error as e:
        print(f"The error '{e}' occurred")

# Check if the email already exists in the database
def check_email_exists(connection, email):
    query = "SELECT COUNT(*) FROM sub_users WHERE email = %s"
    cursor = connection.cursor()
    try:
        cursor.execute(query, (email,))
        # If count is 0, return False, otherwise return True
        return cursor.fetchone()[0] > 0
    except Error as e:
        print(f"The error '{e}' occurred")
        return False

# Insert new subscription into the table
def insert_subscription(connection, email, industry, source, subcategory, frequency):
    insert_query = """
    INSERT INTO sub_users (email, industry, source, subcategory, frequency)
    VALUES (%s, %s, %s, %s, %s);
    """
    cursor = connection.cursor()
    try:
        cursor.execute(insert_query, (email, industry, source, subcategory, frequency))
        connection.commit()
        print("Subscription inserted successfully")
    except Error as e:
        print(f"The error '{e}' occurred")

# Retrieve all subscriptions for admin dashboard
def get_all_subscriptions(connection):
    query = "SELECT email, industry, source, subcategory, frequency FROM sub_users"
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return pd.DataFrame(result, columns=['Email', 'Industry', 'Source', 'Subcategory', 'Frequency'])
    except Error as e:
        print(f"The error '{e}' occurred")
        return pd.DataFrame()



# Streamlit UI
def main():
    st.sidebar.title("Navigation")
    choice = st.sidebar.selectbox("Choose a view", ["Subscribe", "Admin Dashboard", "Statistics"])

    conn = create_db_connection()
    create_subscription_table(conn)

    if choice == "Subscribe":
        st.title("Newsletter Subscription Manager")

        with st.form("subscription_form"):
            email = st.text_input("Email Address")
            industry = st.selectbox("Industry/Sector", ['Consumer Health', 'Beauty', 'Tech'])
            source = st.selectbox("Source", ['Social Media', 'News'])
            subcategory = st.selectbox("Subcategory", ['New Product Releases', 'Mergers and Acquisitions'])
            frequency = st.slider("Frequency of Newsletter per Week", 1, 50, 1)
            submit_button = st.form_submit_button("Submit Subscription")

        if submit_button:
            if check_email_exists(conn, email):
                st.error("You have already subscribed. To manage your subscription, contact support.")
            else:
                insert_subscription(conn, email, industry, source, subcategory, frequency)
                st.success("Your subscription has been successfully registered!")

    elif choice == "Admin Dashboard":
        st.title("Admin Dashboard")
        df = get_all_subscriptions(conn)
        st.dataframe(df)  # Display the table in the dashboard

    elif choice == "Statistics":
        st.title("Statistics")
        df = get_all_subscriptions(conn)
        if not df.empty:
            st.pyplot(plot_source_distribution(df))
            st.pyplot(plot_source_pie_chart(df))
            st.pyplot(plot_frequency_histogram(df))  # Plot the histogram of frequencies
        else:
            st.write("No subscription data available to display statistics.")

if __name__ == "__main__":
    main()
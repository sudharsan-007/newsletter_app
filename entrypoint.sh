#!/bin/bash

# Start MySQL
service mysql start

# Ensure MySQL is fully started before continuing
sleep 10

# Start the Streamlit app
streamlit run newsletter_app.py

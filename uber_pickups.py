import streamlit as st
import pandas as pd
import numpy as np

# Every good app has a title, so let's add one:
st.title('Uber pickups in NYC')

DATE_COLUMN = 'date/time'
DATA_URL = ('https://s3-us-west-2.amazonaws.com/'
            'streamlit-demo-data/uber-raw-data-sep14.csv.gz')


@st.cache_data
def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
    return data


# Create a text element and let the reader know the data is loading.
data_load_state = st.text('Loading data...')
# Load 10,000 rows of data into the dataframe.
data = load_data(10000)
# Notify the reader that the data was successfully loaded.
# data_load_state.text('Loading data...done!')
data_load_state.text("Done! (using st.cache_data)")

# Draw a histogram
st.subheader('Number of pickups by hour')
hist_values = np.histogram(data[DATE_COLUMN].dt.hour, bins=24, range=(0, 24))[0]
st.bar_chart(hist_values)
st.table(hist_values)

# Plot data on a map
# Add a subheader for the section:
st.subheader('Map of all pickups')
# Use the st.map() function to plot the data:
st.map(data)

# Filter results with a slider
# In the last section, when you drew the map, the time used to filter results was hardcoded into the script,
# but what if we wanted to let a reader dynamically filter the data in real time? Using Streamlit's widgets you can.
# Let's add a slider to the app with the st.slider() method.
hour_to_filter = st.slider('hour', 0, 23, 17)  # min: 0h, max: 23h, default: 17h
# Use the slider and watch the map update in real time.

# Uber pickups was 17:00
# hour_to_filter = 17
filtered_data = data[data[DATE_COLUMN].dt.hour == hour_to_filter]
st.subheader(f'Map of all pickups at {hour_to_filter}:00')
st.map(filtered_data)

# Use a button to toggle data
# Sliders are just one way to dynamically change the composition of your app.
# Let's use the st.checkbox function to add a checkbox to your app. We'll use this checkbox to show/hide
# the raw data table at the top of your app.
if st.checkbox('Show raw data'):
    st.subheader('Raw data')
    st.write(data)


# Share your app

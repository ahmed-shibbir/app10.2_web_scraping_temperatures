import requests
import selectorlib
import os
from datetime import datetime
import pandas as pd
from matplotlib import pyplot as plt

import streamlit as st


URL = "http://programmer100.pythonanywhere.com/"


def scrape(url):
    response = requests.get(URL)
    if response.status_code == 200:
        # print(response)
        html = response.text
        # print(html)
        return html


# print(html)

def extracted(html):
    extractor = selectorlib.Extractor.from_yaml_file("extract.yaml")
    # print(extractor)
    data = extractor.extract(html)
    print(data)
    value = data["temperature"]
    # value = extractor.extract(html)["temperature"]

    # print(value)
    return value


html = scrape(URL)
extracted_value = extracted(html=html)

print(extracted_value)


def create_file():
    # Open the file in append mode and write the header only if it's empty
    with open('temperatures.txt', 'a') as file:
        # Check if the file is empty (has no content)
        is_empty = os.stat('temperatures.txt').st_size == 0
        if is_empty:
            # file.write('Temperature\n')  # Write the column header
            # Write the column header with a tab separator
            file.write('Date\tTemperature\n')


# Call create_file function to create the file with the header (if it doesn't exist)
create_file()

# Get the current date
# current_date = datetime.now()#.strftime("%Y-%m-%d")
current_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

with open("temperatures.txt", "a") as file:
    # file.write(extracted + "\n")
    file.write(f"{current_date}\t{extracted_value}\n")

df = pd.read_csv("temperatures.txt", sep="\t")
print(df)
x_series = df["Date"]
print(x_series)
y_series = df["Temperature"]
print(y_series)

# plt.figure(figsize=(10, 6))  # Adjust the figure size as needed
# plt.plot(df['Date'], df['Temperature'], marker='o', linestyle='-')
# plt.title('Temperature Over Time')
# plt.xlabel('Date')
# plt.ylabel('Temperature')
# plt.grid(True)
#
# # Show the graph
# plt.tight_layout()
# plt.show()

st.title('Temperature Over Time')
st.write('Line Chart with Date and Time on x-axis')

# Create Series for x (DateTime) and y (Temperature)
x = df['Date']
y = df['Temperature']

# Create a line graph using st.line_chart()
st.line_chart(pd.concat([x, y], axis=1).set_index('Date'))

# Show the graph in the Streamlit app
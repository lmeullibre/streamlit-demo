# complex_app.py
import streamlit as st
import pandas as pd
import numpy as np
import io
import datetime
import random

def generate_file(approx_size_mb, file_type, columns, missing_rate=0):
    """Generate a file of approximately the desired size."""
    num_rows = int(approx_size_mb * 1e6 / 50)  # rough estimation
    df = generate_random_data(num_rows, columns, missing_rate)
    buffer = io.BytesIO()

    if file_type == "CSV":
        csv_buffer = io.StringIO()
        df.to_csv(csv_buffer, index=False)
        buffer.write(csv_buffer.getvalue().encode())
        mime_type = "text/csv"
        file_extension = "csv"
    elif file_type == "Excel":
        df.to_excel(buffer, index=False)
        mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        file_extension = "xlsx"
    elif file_type == "JSON":
        json_buffer = io.StringIO()
        df.to_json(json_buffer, orient="records", lines=True)
        buffer.write(json_buffer.getvalue().encode())
        mime_type = "application/json"
        file_extension = "json"

    return buffer.getvalue(), mime_type, file_extension

def generate_random_data(num_rows, columns, missing_rate=0):
    """Generate a dataframe with diverse types of random data."""
    data_types = {
        'Integer': np.random.randint(0, 10000, size=num_rows),
        'Float': np.random.randn(num_rows),
        'String': ["".join(np.random.choice(list('ABCDEFGHIJKLMNOPQRSTUVWXYZ'), 5)) for _ in range(num_rows)],
        'Date': [datetime.date(2000, 1, 1) + (datetime.date(2023, 1, 1) - datetime.date(2000, 1, 1)) * random.random() for _ in range(num_rows)],
        'Boolean': np.random.choice([True, False], num_rows)
    }

    df = pd.DataFrame({col: data_types[col] for col in columns})

    # Introduce missing values
    if missing_rate > 0:
        mask = np.random.choice([True, False], size=df.shape, p=[missing_rate, 1-missing_rate])
        df = df.mask(mask)

    return df

st.title("Complex File Generator App")

file_type = st.selectbox("Select a file type", ["CSV", "Excel", "JSON"])
desired_size = st.slider("Select desired file size (MB)", 1, 100)
columns = st.multiselect("Select columns for your file", ['Integer', 'Float', 'String', 'Date', 'Boolean'], default=['Integer', 'Float', 'String'])
missing_rate = st.slider("Percentage of Missing Values", 0, 100, 0) / 100

chosen_color = st.color_picker("Pick a color for good luck!")
if chosen_color in ['#0000FF', '#0000ff', '#0000FE', '#0000fe', '#0100FF', '#0100ff']: # approximate values for blue
    jokes = [
        "Why did the two 4s skip lunch? They already 8!",
        "Why don’t scientists trust atoms? Because they make up everything!",
        "What do you call fake spaghetti? An impasta!",
        "Did you hear about the mathematician who’s afraid of negative numbers? He'll stop at nothing to avoid them!"
    ]
    st.sidebar.write(f"Joke of the day: {random.choice(jokes)}")

# ... [rest of your Streamlit code for file generation]

if st.button("Generate File"):
    file_data, mime_type, file_extension = generate_file(desired_size, file_type, columns, missing_rate)
    
    st.download_button(
        label=f"Download {desired_size}MB {file_type}",
        data=file_data,
        file_name=f"data_{desired_size}mb.{file_extension}",
        mime=mime_type
    )
    
    # Preview the first 5 rows of the generated data
    df_preview = generate_random_data(5, columns, missing_rate)
    st.write(df_preview)

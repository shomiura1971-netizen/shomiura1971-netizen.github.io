import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Interactive Tool", page_icon="🔧", layout="wide")

st.title("Interactive Tool")
st.markdown("---")

# --- Sidebar ---
st.sidebar.header("Settings")
tool_choice = st.sidebar.selectbox(
    "Select a tool:",
    ["Unit Converter", "Text Analyzer", "Random Data Generator"],
)

# --- Unit Converter ---
if tool_choice == "Unit Converter":
    st.header("Unit Converter")
    category = st.selectbox("Category", ["Length", "Weight", "Temperature"])

    col1, col2 = st.columns(2)

    if category == "Length":
        units = {"Meter": 1.0, "Kilometer": 0.001, "Centimeter": 100.0, "Mile": 0.000621371, "Foot": 3.28084}
        with col1:
            from_unit = st.selectbox("From", list(units.keys()))
            value = st.number_input("Value", value=1.0, format="%.4f")
        with col2:
            to_unit = st.selectbox("To", list(units.keys()))
            result = value / units[from_unit] * units[to_unit]
            st.metric(label=f"Result ({to_unit})", value=f"{result:.4f}")

    elif category == "Weight":
        units = {"Kilogram": 1.0, "Gram": 1000.0, "Pound": 2.20462, "Ounce": 35.274}
        with col1:
            from_unit = st.selectbox("From", list(units.keys()))
            value = st.number_input("Value", value=1.0, format="%.4f")
        with col2:
            to_unit = st.selectbox("To", list(units.keys()))
            result = value / units[from_unit] * units[to_unit]
            st.metric(label=f"Result ({to_unit})", value=f"{result:.4f}")

    elif category == "Temperature":
        with col1:
            from_unit = st.selectbox("From", ["Celsius", "Fahrenheit", "Kelvin"])
            value = st.number_input("Value", value=0.0, format="%.2f")
        with col2:
            to_unit = st.selectbox("To", ["Celsius", "Fahrenheit", "Kelvin"])
            # Convert to Celsius first
            if from_unit == "Fahrenheit":
                celsius = (value - 32) * 5 / 9
            elif from_unit == "Kelvin":
                celsius = value - 273.15
            else:
                celsius = value
            # Convert from Celsius to target
            if to_unit == "Fahrenheit":
                result = celsius * 9 / 5 + 32
            elif to_unit == "Kelvin":
                result = celsius + 273.15
            else:
                result = celsius
            st.metric(label=f"Result ({to_unit})", value=f"{result:.2f}")

# --- Text Analyzer ---
elif tool_choice == "Text Analyzer":
    st.header("Text Analyzer")
    text = st.text_area("Enter text to analyze:", height=200, placeholder="Type or paste your text here...")

    if text:
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Characters", len(text))
        col2.metric("Characters (no spaces)", len(text.replace(" ", "")))
        col3.metric("Words", len(text.split()))
        col4.metric("Lines", len(text.splitlines()))

        st.subheader("Character Frequency")
        freq = {}
        for ch in text.lower():
            if ch.isalpha():
                freq[ch] = freq.get(ch, 0) + 1
        if freq:
            df = pd.DataFrame(
                sorted(freq.items(), key=lambda x: x[1], reverse=True),
                columns=["Character", "Count"],
            )
            st.bar_chart(df.set_index("Character"))

# --- Random Data Generator ---
elif tool_choice == "Random Data Generator":
    st.header("Random Data Generator")

    col1, col2 = st.columns(2)
    with col1:
        rows = st.slider("Number of rows", 10, 500, 100)
    with col2:
        cols = st.slider("Number of columns", 1, 10, 3)

    distribution = st.selectbox("Distribution", ["Normal", "Uniform", "Exponential"])

    if st.button("Generate"):
        if distribution == "Normal":
            data = np.random.randn(rows, cols)
        elif distribution == "Uniform":
            data = np.random.rand(rows, cols)
        else:
            data = np.random.exponential(1.0, size=(rows, cols))

        col_names = [f"Col_{i+1}" for i in range(cols)]
        df = pd.DataFrame(data, columns=col_names)

        st.subheader("Generated Data")
        st.dataframe(df, use_container_width=True)

        st.subheader("Statistics")
        st.dataframe(df.describe(), use_container_width=True)

        st.subheader("Distribution Chart")
        st.line_chart(df)

        csv = df.to_csv(index=False)
        st.download_button("Download CSV", csv, "generated_data.csv", "text/csv")

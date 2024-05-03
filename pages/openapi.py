import streamlit as st
import os
from openai import OpenAI
import altair as alt
import json
import pandas as pd


# Set up OpenAI client
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# Define function to generate visualization specification from natural language prompt
@st.cache_data
def generate_visualization_spec(prompt, data, model_name="gpt-3.5-turbo"):
    chat_completion = client.chat.completions.create(
        messages=[
            {"role": "system", "content": "You are a visualization assistant that generates JSON specifications for charts based on natural language prompts and provided data."},
            {"role": "user", "content": f"Data: {data}\n\nPrompt: {prompt}"},
        ],
        model=model_name,
        temperature=0.7,
        max_tokens=1024,
    )
    return chat_completion.choices[0].message.content

# Define function to render visualization from JSON specification
def render_visualization(spec_json):
    spec = json.loads(spec_json)
    if "chart_type" in spec:
        chart_type = spec["chart_type"]
        data = pd.DataFrame(spec["data"])

        if chart_type == "bar":
            x = spec["x"]
            y = spec["y"]
            sort_order = spec.get("sort_order", None)
            tooltip = spec.get("tooltip", None)

            chart = alt.Chart(data).mark_bar().encode(
                x=alt.X(x, title=spec.get("x_title", x)),
                y=alt.Y(y, title=spec.get("y_title", y), sort=sort_order),
                tooltip=tooltip
            )
        else:
            # Add support for other chart types here
            st.warning(f"Chart type '{chart_type}' is not supported.")
            return
    else:
        st.warning("Invalid chart specification format.")
        return

    return st.altair_chart(chart, use_container_width=True)


# Streamlit app
def main():
    st.title("Chat2Plot")
    st.write("Enter a natural language prompt and upload data to generate a visualization.")

    prompt = st.text_area("Prompt","Create a bar chart showing the total sales for each product category across all regions in the year 2022. Sort the categories in descending order of sales, and include data labels displaying the sales value for each category.")
    data = st.file_uploader("Upload data", type=["csv", "json"])

    if data is not None:
        data_content = data.getvalue().decode("utf-8")

    if prompt and data:
        with st.spinner("Generating visualization specification..."):
            visualization_spec = generate_visualization_spec(prompt, data_content)
        st.write("Generated visualization specification:")
        st.code(visualization_spec, language="json")
        render_visualization(visualization_spec)

if __name__ == "__main__":
    main()
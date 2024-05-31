import streamlit as st
from scrapy_spider import run_spider
import pandas as pd
from io import BytesIO
import openai

# Function to summarize data using OpenAI
def summarize_data(openai_api_key, data):
    openai.api_key = openai_api_key
    summaries = []
    for item in data:
        text_to_summarize = item['Content']
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Summarize the following text."},
                {"role": "user", "content": text_to_summarize}
            ]
        )
        summary = response['choices'][0]['message']['content']
        summaries.append({
            'URL': item['URL'],
            'Summary': summary
        })
    return summaries

# Set up the Streamlit app
st.title("Web Scraping and Summarization AI Agent 🕵️‍♂️")
st.caption("This app allows you to scrape multiple websites, summarize the data using OpenAI API, and export results to Excel")

# Get OpenAI API key from user
openai_api_key = st.text_input("OpenAI API Key", type="password")

# Get the URLs of the websites to scrape
urls = st.text_area("Enter the URLs of the websites you want to scrape, separated by commas")

if urls and openai_api_key:
    url_list = [url.strip() for url in urls.split(",")]

    if st.button("Scrape and Summarize"):
        with st.spinner("Scraping..."):
            results = run_spider(url_list)
        
        if results:
            with st.spinner("Summarizing..."):
                summarized_results = summarize_data(openai_api_key, results)
            
            # Display summaries
            st.write("## Summarized Results")
            for summary in summarized_results:
                st.write(f"### {summary['URL']}")
                st.write(f"**Summary:** {summary['Summary']}")
                st.write("---")

            # Create a DataFrame and export to Excel
            df = pd.DataFrame(summarized_results)
            output = BytesIO()
            df.to_excel(output, index=False)
            output.seek(0)

            st.download_button(
                label="Download Excel",
                data=output,
                file_name="scraping_summarized_results.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
            st.success("Scraping and summarization completed. You can download the results.")
        else:
            st.error("No results to display. Please enter valid URLs.")







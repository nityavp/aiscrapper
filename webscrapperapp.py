import streamlit as st
import requests
from bs4 import BeautifulSoup
from scrapegraphai.graphs import SmartScraperGraph
import pandas as pd
from io import BytesIO

# Set up the Streamlit app
st.title("Web Scraping AI Agent 🕵️‍♂️")
st.caption("This app allows you to scrape multiple websites using OpenAI API and export results to Excel")

# Get OpenAI API key from user
openai_access_token = st.text_input("OpenAI API Key", type="password")

if openai_access_token:
    model = st.radio(
        "Select the model",
        ["gpt-3.5-turbo", "gpt-4"],
        index=0,
    )
    graph_config = {
        "llm": {
            "api_key": openai_access_token,
            "model": model,
        },
    }
    
    # Get the URLs of the websites to scrape
    urls = st.text_area("Enter the URLs of the websites you want to scrape, separated by commas")
    # Get the user prompts
    prompts = st.text_area("Enter the prompts for each website, separated by commas (in the same order as the URLs)")
    
    # Function to get HTML content
    def get_html_content(url):
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            st.error(f"Error fetching {url}: {e}")
            return None
    
    # Create SmartScraperGraph objects for each URL and prompt
    if urls and prompts:
        url_list = [url.strip() for url in urls.split(",")]
        prompt_list = [prompt.strip() for prompt in prompts.split(",")]
        
        if len(url_list) != len(prompt_list):
            st.error("The number of URLs and prompts must be equal.")
        else:
            smart_scrapers = [
                SmartScraperGraph(prompt=prompt, source=url, config=graph_config)
                for url, prompt in zip(url_list, prompt_list)
            ]
            
            # Scrape the websites
            if st.button("Scrape"):
                results = []
                for i, (url, prompt) in enumerate(zip(url_list, prompt_list)):
                    if url:
                        # Use the requests and BeautifulSoup to get HTML content
                        html_content = get_html_content(url)
                        if html_content:
                            soup = BeautifulSoup(html_content, 'html.parser')
                            cleaned_html_content = str(soup)
                            # Assuming smart_scrapers[i].run() processes the cleaned_html_content
                            result = smart_scrapers[i].run(html_content=cleaned_html_content)
                            results.append(result)
                
                # Create a DataFrame and export to Excel
                if results:
                    df = pd.DataFrame(results)
                    output = BytesIO()
                    df.to_excel(output, index=False)
                    output.seek(0)
                    
                    st.download_button(
                        label="Download Excel",
                        data=output,
                        file_name="scraping_results.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )
                    st.success("Scraping completed. You can download the results.")
                else:
                    st.error("Please enter valid URLs and prompts.")

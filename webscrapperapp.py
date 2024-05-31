import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
from io import BytesIO

# Set up the Streamlit app
st.title("Web Scraping AI Agent 🕵️‍♂️")
st.caption("This app allows you to scrape multiple websites and export results to Excel")

# Get the URLs of the websites to scrape
urls = st.text_area("Enter the URLs of the websites you want to scrape, separated by commas")
# Get the user prompts
prompts = st.text_area("Enter the prompts for each website (keywords to search for), separated by commas (in the same order as the URLs)")

if urls and prompts:
    url_list = [url.strip() for url in urls.split(",")]
    prompt_list = [prompt.strip() for prompt in prompts.split(",")]

    if len(url_list) != len(prompt_list):
        st.error("The number of URLs and prompts must be equal.")
    else:
        if st.button("Scrape"):
            results = []
            for url, prompt in zip(url_list, prompt_list):
                try:
                    response = requests.get(url)
                    response.raise_for_status()
                    soup = BeautifulSoup(response.content, "html.parser")

                    # Extract text content based on the prompt (simple keyword search example)
                    elements = soup.find_all(text=lambda text: text and prompt.lower() in text.lower())

                    result = {
                        "URL": url,
                        "Prompt": prompt,
                        "Matches": [element.strip() for element in elements]
                    }
                    results.append(result)
                except Exception as e:
                    st.error(f"Error processing {url}: {e}")

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
                st.error("No results to display. Please enter valid URLs and prompts.")




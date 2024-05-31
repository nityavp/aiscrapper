import streamlit as st
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
    
    if urls and prompts:
        url_list = [url.strip() for url in urls.split(",")]
        prompt_list = [prompt.strip() for prompt in prompts.split(",")]
        
        if len(url_list) != len(prompt_list):
            st.error("The number of URLs and prompts must be equal.")
        else:
            # Create SmartScraperGraph objects for each URL and prompt
            smart_scrapers = [
                SmartScraperGraph(prompt=prompt, source=url, config=graph_config)
                for url, prompt in zip(url_list, prompt_list)
            ]
            
            # Scrape the websites
            if st.button("Scrape"):
                results = []
                for i, scraper in enumerate(smart_scrapers):
                    try:
                        result = scraper.run()
                        results.append(result)
                    except Exception as e:
                        st.error(f"Error processing {url_list[i]}: {e}")
                
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



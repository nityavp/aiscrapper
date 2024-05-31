import streamlit as st
from scrapy_spider import run_spider
import pandas as pd
from io import BytesIO

# Set up the Streamlit app
st.title("Web Scraping Agent 🕵️‍♂️")
st.caption("This app allows you to scrape multiple websites and export results to Excel")

# Get the URLs of the websites to scrape
urls = st.text_area("Enter the URLs of the websites you want to scrape, separated by commas")

if urls:
    url_list = [url.strip() for url in urls.split(",")]

    if st.button("Scrape and Export"):
        with st.spinner("Scraping..."):
            try:
                results = run_spider(url_list)
                st.write("Scraping completed successfully.")  # Debug print
                st.write(results)  # Debug print to show results
            except Exception as e:
                st.error(f"An error occurred while scraping: {e}")
                results = None
        
        if results:
            # Create a DataFrame and export to Excel
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
            st.error("No results to display. Please enter valid URLs.")








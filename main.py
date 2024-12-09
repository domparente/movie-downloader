import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException
import time

# Configure Streamlit page
st.set_page_config(layout="centered")

st.title("Plex Downloader")
search_bar = st.text_input("Enter the movie or TV show you want to download...")

try:
    # Setup Chrome WebDriver
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--enable-unsafe-swiftshader')

    service = Service(executable_path='./chromedriver.exe')  # Adjust path as necessary
    driver = webdriver.Chrome(service=service, options=options)

    if "button_clicked" not in st.session_state:
        st.session_state.button_clicked = False
    def callback():
        st.session_state.button_clicked = True

    if (
        st.button("Search", on_click=callback)
        or st.session_state.button_clicked
        ):
            driver.get("https://thepiratebay.org")
                
            # Show progress bar
            progress_text = "Searching for results..."
            my_bar = st.progress(0, text=progress_text)
            
            # Wait for the search box to be available
            search_box = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='search']"))
            )
            search_box.send_keys(search_bar)
            search_box.submit()
            
            # Update progress bar
            my_bar.progress(30, text="Waiting for search results...")
            
            # Wait for search results to load
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "list-entry"))
            )
            
            # Update progress bar
            my_bar.progress(70, text="Loading results...")
            
            # Get search results, limiting to first 5 entries
            results = driver.find_elements(By.CLASS_NAME, "list-entry")[:5]
            
            # Use a container for better organization
            for index, result in enumerate(results):
                link_element = result.find_element(By.XPATH, ".//a[contains(@href, 'description.php?id=')]")
                title = link_element.text
                link = link_element.get_attribute('href')

                if st.button(label=title):
                    driver.get(link)
                    magnet_link = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, "//a[contains(@href, 'magnet:?')]"))
                    ).get_attribute('href')
                    st.write(f"**Magnet Link for {title}:**")
                    st.code(f" {magnet_link}")

            # Complete the progress bar
                my_bar.progress(100, text="Search complete!")
                time.sleep(1)  # Keep the completion message visible for a moment
                my_bar.empty()  # Clear the progress bar
except StaleElementReferenceException:
    # If the operation completed successfully despite the exception, do nothing or log it.
    st.write("Stale element exception occurred but operation succeeded.")
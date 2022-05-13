import streamlit as st
from PIL import Image
import home

#--------------------------
#PAGE CONFIG
st.set_page_config(
    page_title="Speckle Comments to Notion",
    page_icon="💬"
)
#--------------------------


#--------------------------
#SIDEBAR
#import logo
logo = Image.open("app-logo.png")

st.sidebar.image(logo,caption="Connects your Speckle Comments to Notion Database")
#sidebar title
st.sidebar.title("Speckle Comments to Notion")

#page names as a list
pages = ["Home", "App"]
#radio for the page navigation
nav = st.sidebar.radio(label="Navigation", options=pages, index=0)
#--------------------------

#--------------------------
#CONTAINERS
about_app = st.container()
hack_inspiration = st.container()
what_it_does = st.container()
how_to_use = st.container()
#--------------------------

#HOMEPAGE
if nav == pages[0]:
    home.homePage()

#INPUTS PAGE
if nav == pages[1]:
    #once the code is done, i'll import it here.
    st.title(pages[1])
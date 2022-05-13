#--------------------------
# IMPORT LIBRARIES
import streamlit as st
#--------------------------

"""#--------------------------
#PAGE CONFIG
st.set_page_config(
    page_title="Speckle Comments to Notion",
    page_icon="💬"
)
#--------------------------"""
def homePage():
    #--------------------------
    #CONTAINERS
    header = st.container()
    about_app = st.container()
    hack_inspiration = st.container()
    how_to_use = st.container()
    #--------------------------

    #--------------------------
    #PAGE TITLE
    with header:
        st.title("Speckle Comments 💬 to Notion📄")
    #--------------------------

    #--------------------------
    #ABOUT APP
    with about_app.expander("About this app🔽", expanded=True):
        st.markdown(
            """
            This app sends your Speckle comments into a given Notion database and assigns Speckle attributes as properties of Notion pages.
            Our main aim was to create a bidirectional link between two applications so we can leverage the best out of both.
            For now it only works one way, from Speckle to Notion. Take a look 👀
            """
        )
    #--------------------------

    #--------------------------
    with hack_inspiration:
        st.subheader("Inspiration 🌹")
        st.markdown(
            """
            Recently added **Comments** feature on Speckle has broken new grounds but since it's still being developed, it has its own limitations.
            One limitation we saw was assigning statuses to comments and tracking of them. We thought, "*Notion is really flexible and powerful in this area,
            and its used by a lot of architecture offices, maybe we can track their status there. Why not integrate the two?*".

            Vision was to create a bidirectional link between the two so when a comment is being archived in Notion, it would also be archived in Speckle.
            But we couldn't make it there **yet**.
            """
        )
    #--------------------------

    #--------------------------
    #HOW TO USE
    with how_to_use:
        st.subheader("How to use🤔")
        st.markdown(
            """
            If you want to learn how to use it, take a look at the video below👇
            """
        )
        st.video("https://youtu.be/6N854BoPWII",)
    #--------------------------
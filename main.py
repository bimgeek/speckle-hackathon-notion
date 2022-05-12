from gql import gql
from specklepy.api.credentials import get_account_from_token
from specklepy.api.client import SpeckleClient
import streamlit as st

#--------------------------
#PAGE CONFIG
st.set_page_config(
    page_title="Speckle Comments to Notion",
    page_icon="💬"
)
#--------------------------

#--------------------------
#CONTAINERS
header = st.container()
input = st.container()
viewer = st.container()
report = st.container()
graphs = st.container()
#--------------------------

#--------------------------
#HEADER
#Page Header
with header:
    st.title("Speckle Comments - Notion Integration 💬")
#About info
with header.expander("About this app🔽", expanded=True):
    st.markdown(
        """Speckle Hackathon project. Our main was to create a bidirectional link with Speckle and Notion.
        Speckle comments are limited at the moment and Notion is really flexible to assign attributes to page objects.
        Maybe Notion can be used to track Speckle Comments?
        """
    )
#--------------------------

#--------------------------
#INPUTS
with input:
    st.subheader("Inputs")

    #-------
    #Columns for inputs
    serverCol, tokenCol = st.columns([1,3])
    #User Input boxes
    speckleServer = serverCol.text_input("Server URL", "speckle.xyz", help="Speckle server to connect.")
    speckleToken = tokenCol.text_input("Speckle token", "c3ec1797cca318cc2fd96822dad37cc6f9823c52ca", help="If you don't know how to get your token, take a look at this [link](https://speckle.guide/dev/tokens.html)👈")
    #-------

    #-------
    #CLIENT
    client = SpeckleClient(host=speckleServer)
    #Get account from Token
    account = get_account_from_token(speckleToken, speckleServer)
    #Authenticate
    client.authenticate_with_account(account)
    #-------

    #-------
    #Streams List👇
    streams = client.stream.list()
    #Get Stream Names
    streamNames = [s.name for s in streams]
    #Dropdown for stream selection
    sName = st.selectbox(label="Select your stream", options=streamNames, help="Select your stream from the dropdown")
    #SELECTED STREAM ✅
    stream = client.stream.search(sName)[0]
    #Stream Branches 🌴
    branches = client.branch.list(stream.id)
    #Stream Commits 🏹
    commits = client.commit.list(stream.id, limit=100)
    #-------
#--------------------------

#--------------------------
#Query code for receiving comments
query = gql(
    """
    query{comments(streamId:"1a3d717f57") {
    items {
    id
    authorId
    text
    data
    archived
    screenshot}}}
    """
)
# Making query to Speckle
gql_result = client.execute_query(query=query)
#--------------------------

st.write(gql_result)
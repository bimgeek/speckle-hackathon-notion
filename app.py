#--------------------------
# IMPORT LIBRARIES
# Streamlit for UI
import streamlit as st
#Gql for GraphQL queries
from gql import gql
#SpecklePy stuff
from specklepy.api.credentials import get_account_from_token
from specklepy.api.client import SpeckleClient
#json when dealing with received objects
import json
# Notion API requests
import requests
#pandas for dealing with dictionaries
import pandas as pd
import base64
#--------------------------

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
speckle_inputs = st.container()
notion_inputs = st.container()
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
        """*Description will be updated.*
        Speckle Hackathon project. Our main goal was to create a  link between Speckle and Notion.
        Speckle comments are limited at the moment and Notion is really flexible to assign attributes to page objects.
        Maybe Notion can be used to track Speckle Comments?
        """
    )
    st.markdown(
        """
        ###### How to use it
        """
    )
    st.markdown(
        """
        video/text explaining how to use the app.
        """
    )
#--------------------------

#--------------------------#--------------------------#--------------------------#--------------------------
#🔹SPECKLE INPUTS
with speckle_inputs:
    st.subheader("🔹Speckle")

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
    #🔽DROPDOWN for stream selection🔽
    sName = st.selectbox(label="Select your stream", options=streamNames, help="Select your stream from the dropdown")
    #✅SELECTED STREAM ✅
    stream = client.stream.search(sName)[0]
    #Stream Branches 🌴
    #branches = client.branch.list()
    #Stream Commits 🏹
    #commits = client.commit.list(stream.id, limit=100)
    #-------
#--------------------------

#--------------------------
#CACHE
@st.cache

# Function for receiving comments🛠
def get_comments(stream):
    query = gql(
        """{
        comments(streamId:\""""
        + stream.id + 
        """\") {
            items {
            text
            id
            authorId
            createdAt
            data
            archived
            screenshot
            }
        }
        }"""
    )
    # Making query to Speckle
    comments = client.execute_query(query=query)
    return comments
#--------------------------

#get user info
def get_user_info(authorId):
    query = gql(
        """{
        user(id: \""""
        + authorId + 
        """\") {
            name
            }
        }"""
    )

    try:
        user_name = client.execute_query(query=query)
        return user_name['user']['name']
    except:
        return authorId
#--------------------------

# archive comment
def archiveSpeckleComment(streamId, commentId):
    query = gql(
        """mutation {
            commentArchive(
                streamId:\""""
                + streamId + 
                """\"
                commentId:\""""
                + commentId + 
                """\"
                archived:true)
            }"""
    )
    client.execute_query(query)
    st.write('Archive comment: ' + commentId)
    
#--------------------------

#--------------------------#--------------------------#--------------------------#--------------------------

#--------------------------#--------------------------#--------------------------#--------------------------
#--------------------------
# NOTION ⬛ INPUTS
with notion_inputs:
    st.subheader('Notion ⬛')
    notion_token = st.text_input('Notion Integration Token', 'secret_P6HNSC8hX5gaQVkLSm5XlzR1KD61OMJDltOnVPWEE3Z', help='Learn how to get your Notion Token')
    notion_db_id = st.text_input('Database Id 🆔', '26d224183bfc488181a37cd2d74be1bf', help='Learn more about how to get your database id')
#--------------------------

#--------------------------
#HEADERS
headers = {
    "Accept": "application/json",
    "Notion-Version": "2022-02-22",
    "Content-Type": "application/json",
    "Authorization": "Bearer "+notion_token
}
#--------------------------

#--------------------------
#🔨NOTION FUNCTIONS 🔨
#CACHE NOTION
#@st.cache
# Database Query
def queryDatabase(databaseId, headers):
    url = f"https://api.notion.com/v1/databases/{databaseId}/query"
    res = requests.request("POST", url, headers=headers)
    data = res.json()
    return res , data

# Get list of Issues already in Notion
def getExistingIssueIds(jsonData):
    existingIssuesIds = dict()
    pages = jsonData['results']
    for p in pages:
        props = p['properties']
        id = props['Id']['rich_text'][0]['plain_text']
        issue_id = p['id']
        status_name = props['Status']['select']['name']
        status_color = props['Status']['select']['color']
        existingIssuesIds[id] = (issue_id, status_name, status_color)
    return existingIssuesIds


# Define page layout
def definePage(databaseId, comment_info, author, status_name, status_color):
    payload = {
        "parent": {
        "type": "database_id",
        "database_id": databaseId
        },
        "properties": {
            "Author Id": {
                "id": "%3Dazv",
                "type": "rich_text",
                "rich_text": [
                    {
                        "type": "text",
                        "text": {
                            "content": author,
                            "link": None
                        },
                        "annotations": {
                            "bold": False,
                            "italic": False,
                            "strikethrough": False,
                            "underline": False,
                            "code": False,
                            "color": "default"
                        },
                        "plain_text": author,
                        "href": None
                    }
                ]
            },
            "Id": {
                "id": "Ker%7B",
                "type": "rich_text",
                "rich_text": [
                    {
                        "type": "text",
                        "text": {
                            "content": comment_info['id'],
                            "link": None
                        },
                        "annotations": {
                            "bold": False,
                            "italic": False,
                            "strikethrough": False,
                            "underline": False,
                            "code": False,
                            "color": "default"
                        },
                        "plain_text": comment_info['id'],
                        "href": None
                    }
                ]
            },
            "Status": {
                "id": "VlA%5B",
                "type": "select",
                "select": {
                    "id": "1",
                    "name": status_name,
                    "color": status_color
                }
            },
            "Camera Position": {
                "id": "xd%3C%5C",
                "type": "rich_text",
                "rich_text": []
            },
            "Created At": {
                "id": "%7B%3Ai%60",
                "type": "date",
                "date": {
                    "start": comment_info['createdAt']
                }
            },
            "Name": {
                "id": "title",
                "type": "title",
                "title": [
                    {
                        "type": "text",
                        "text": {
                            "content": comment_info['text'],
                            "link": None
                        },
                        "annotations": {
                            "bold": False,
                            "italic": False,
                            "strikethrough": False,
                            "underline": False,
                            "code": False,
                            "color": "default"
                        },
                        "plain_text": comment_info['text'],
                        "href": None
                    }
                ]
            }
        },
        # "cover": {
        # "type": "external",
        # "external": {"url": n_page_cover }
        # }
    }
    return payload

# Create a Page 📄
def createPage(databaseId, headers, comment_info, author):
    url = "https://api.notion.com/v1/pages"
    payload = definePage(databaseId=databaseId, comment_info=comment_info, author=author, status_name='Not started', status_color='red')

    response = requests.post(url, json=payload, headers=headers)
    st.write('Create comment: ' + comment_info['id'])
    #st.write(response.text)

# Update a Page 📄
def updatePage(databaseId, headers, comment_info, author, page_info):
    url = f"https://api.notion.com/v1/pages/{page_info[0]}"
    payload = definePage(databaseId=databaseId, comment_info=comment_info, author=author, status_name=page_info[1], status_color=page_info[2])
    
    response = requests.patch(url, json=payload, headers=headers)
    st.write('Update comment: ' + comment_info['id'])
    #st.write(response.text)


#💬COMMENTS 💬
#💬Get Comments From Stream💬
comments = get_comments(stream=stream)
comment_info_list = comments['comments']['items']

#TODO: Get screenshot
n_page_cover = comments['comments']['items'][0]['screenshot']
# sc_result = str(comments['comments']['items'][0]['screenshot'])
# sc_base64 = sc_result.split(',')[1]
# n_page_cover = base64.urlsafe_b64decode(sc_base64)

# Get pages already in Notion database
res, jsonData = queryDatabase(databaseId=notion_db_id, headers=headers)

# Get Ids of existing issues and pages
issueIds = getExistingIssueIds(jsonData)
st.write('Number of comments: ' + str(len(comment_info_list)))

# Go through comment list from Speckle
# If comment already in Notion then update else create new
for com in comment_info_list:
    user = get_user_info(com['authorId'])
    if com['id'] in issueIds:
        if issueIds[com['id']][1] == 'Archived':
            archiveSpeckleComment(streamId=stream.id, commentId=com['id'])
        else:
            updatePage(databaseId=notion_db_id, headers=headers, comment_info=com, author=user, page_info=issueIds[com['id']])
    else:
        createPage(databaseId=notion_db_id, headers=headers, comment_info=com, author=user)
#n_db_res, n_db_data = queryDatabase(databaseId=notion_db_id, headers=headers)
#st.write(n_db_data['results'][0])
#--------------------------
#--------------------------#--------------------------#--------------------------#--------------------------

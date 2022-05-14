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
#imagehandler to upload image as url to notion
from imageHandler import uploadImage, downloadImage
#--------------------------

#--------------------------
#CONTAINERS
header = st.container()
speckle_inputs = st.container()
notion_inputs = st.container()
run = st.container()
#--------------------------

#--------------------------
#HEADER
#Page Header
with header:
    st.title("App 💬")
#--------------------------

#--------------------------#--------------------------#--------------------------#--------------------------
#🔹SPECKLE INPUTS
with speckle_inputs:
    st.subheader("Speckle🔹")

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
            resources{
                resourceId
            }
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

#--------------------------
# NOTION ⬛ INPUTS
with notion_inputs:
    st.subheader('Notion📄')
    notion_token = st.text_input('Notion Integration Token', 'secret_P6HNSC8hX5gaQVkLSm5XlzR1KD61OMJDltOnVPWEE3Z', help='Learn how to get your Notion Token')
    notion_db_id = st.text_input('Database Id 🆔', '26d224183bfc488181a37cd2d74be1bf', help='Learn more about how to get your database id')
#--------------------------

#--------------------------
#RUN BUTTON 🏃‍♂️💨
#if button clicked run app otherwise don't
with run:
    run_app = st.button("RUN 🚀")
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
        # If existing page doesn't contain an Id just skip
        try:
            id = props['Id']['rich_text'][0]['plain_text']
        except:
            continue

        issue_id = p['id']
        status_name = props['Status']['select']['name']
        status_color = props['Status']['select']['color']
        existingIssuesIds[id] = (issue_id, status_name, status_color)
    return existingIssuesIds


# Define page layout
def definePage(databaseId, comment_info, author, status_name, status_color, img_url):
    # Join cam postion into comma separated string
    camPos = ",".join([str(pos) for pos in [comment_info["data"]["camPos"]]])

    # Construct embed link
    commitURL = comment_info["resources"][0]["resourceId"]
    embedUrl = f"https://speckle.xyz/embed?stream={stream.id}&commit={commitURL}&c={camPos}"

    # define page payload
    payload = {
        "children":[{
            "object": "block",
            "id": "a7e10d37-4652-4573-a62a-3f3b3a2a648f",
            "has_children": False,
            "archived": False,
            "type": "embed",
            "embed": {
                "caption": [],
                "url": embedUrl
            }
            }],
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
                "rich_text": [
                    {
                        "type": "text",
                        "text": {
                            "content": camPos,
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
                        "plain_text": camPos,
                        "href": None
                    }
                ]
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
        "cover": {
        "type": "external",
        "external": {"url": img_url }
        }
            
    }
    return payload

# Create a Page 📄
def createPage(databaseId, headers, comment_info, author):
    url = "https://api.notion.com/v1/pages"

    img_path = downloadImage(img_string=comment_info['screenshot'], img_name=comment_info['id'])
    image = uploadImage(img_path=img_path)
    payload = definePage(databaseId=databaseId, comment_info=comment_info, author=author, status_name='Not started', status_color='red', img_url=image['link'])

    response = requests.post(url, json=payload, headers=headers)
    st.write('Created comment: ' + comment_info['id'])
    #st.write(response.text)

# Update a Page 📄
def updatePage(databaseId, headers, comment_info, author, page_info):
    url = f"https://api.notion.com/v1/pages/{page_info[0]}"
    payload = definePage(databaseId=databaseId, comment_info=comment_info, author=author, status_name=page_info[1], status_color=page_info[2], img_url=None)
    
    response = requests.patch(url, json=payload, headers=headers)
    st.write('Updated comment: ' + comment_info['id'])
    #st.write(response.text)

if run_app:
    #💬COMMENTS 💬
    #💬Get Comments From Stream💬
    comments = get_comments(stream=stream)
    comment_info_list = comments['comments']['items']

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
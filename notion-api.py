#--------------------------
#IMPORT LIBRARIES
import json
import requests
import streamlit as st
#--------------------------

#--------------------------
#NOTION INFO
#this can be a streamlit input
notion_token = "secret_P6HNSC8hX5gaQVkLSm5XlzR1KD61OMJDltOnVPWEE3Z"
#this also can be a streamlit input
notion_db_id = "22fd1e9048ec4f7fbf7e1695822a1181"
#--------------------------

st.title("Notion API Exercise 🤺")

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
#NOTION FUNCTIONS
# Database Query
def queryDatabase(databaseId, headers):
    url = f"https://api.notion.com/v1/databases/{databaseId}/query"
    res = requests.request("POST", url, headers=headers)
    data = res.json()
    return res , data

# Database retrieve
def retrieveDatabase(databaseId, headers):
    url = f"https://api.notion.com/v1/databases/{databaseId}"
    res = requests.request("GET", url, headers=headers)
    data = res.json()
    return res , data

#Create a Page
def createPage(notion_db_id, headers):
    url = "https://api.notion.com/v1/pages"
    payload = {
        "parent": {
        "type": "database_id",
        "database_id": "22fd1e90-48ec-4f7f-bf7e-1695822a1181"
        },
        "properties": {
            "Status": {
                "id": "_o%3Df",
                "type": "select",
                "select": {
                    "id": "1",
                    "name": "Not started",
                    "color": "red"
                }
            },
            "Name": {
                "id": "title",
                "type": "title",
                "title": [
                    {
                        "type": "text",
                        "text": {
                            "content": "Created via Python",
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
                        "plain_text": "Created via Python",
                        "href": None
                    }
                ]
            }
        }
    }

    response = requests.post(url, json=payload, headers=headers)
    st.write(response.text)

createPage(notion_db_id=notion_db_id, headers=headers)

#--------------------------

res,data = queryDatabase(notion_db_id, headers)
st.write(res.status_code)
st.json(data)
import streamlit as st
import requests

url = "https://api.notion.com/v1/blocks/3799e2368ba941f0a0146f7ce67736bd/children?page_size=100"

headers = {
    "Accept": "application/json",
    "Notion-Version": "2022-02-22",
    "Authorization": "Bearer secret_P6HNSC8hX5gaQVkLSm5XlzR1KD61OMJDltOnVPWEE3Z"
}

response = requests.get(url, headers=headers)

st.write(response.json())

import requests

url = "https://api.notion.com/v1/blocks/3799e2368ba941f0a0146f7ce67736bd/children?page_size=100"

headers = {
    "Accept": "application/json",
    "Notion-Version": "2022-02-22",
    "Authorization": "Bearer secret_P6HNSC8hX5gaQVkLSm5XlzR1KD61OMJDltOnVPWEE3Z"
}

response = requests.get(url, headers=headers)

print(response.text)
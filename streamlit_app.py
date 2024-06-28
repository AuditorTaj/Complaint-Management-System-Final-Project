import streamlit as st
import requests

API_URL = "http://localhost:8000"

def signup(username, password):
    response = requests.post(f"{API_URL}/users/", json={"username": username, "password": password})
    return response.json()

def login(username, password):
    response = requests.post(f"{API_URL}/token", data={"username": username, "password": password})
    return response.json()

def create_complaint(token, title, description):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.post(f"{API_URL}/complaints/", json={"title": title, "description": description}, headers=headers)
    return response.json()

st.title("Complaint Management System")

if "token" not in st.session_state:
    st.session_state["token"] = None

if st.session_state["token"] is None:
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Sign Up"):
        user = signup(username, password)
        st.write(user)

    if st.button("Log In"):
        token = login(username, password)
        st.session_state["token"] = token["access_token"]

if st.session_state["token"]:
    st.write("Logged in")
    title = st.text_input("Complaint Title")
    description = st.text_area("Complaint Description")

    if st.button("Submit Complaint"):
        complaint = create_complaint(st.session_state["token"], title, description)
        st.write(complaint)

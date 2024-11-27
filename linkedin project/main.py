import json
import pandas as pd 
import streamlit as st
from few_shot import FewShotPosts
from post_generator import generate_post  

# Initialize the FewShotPosts class and load posts data
fs = FewShotPosts()

# Load posts data
fs.load_posts("data/processed_posts.json")

length_options = ["Short", "Medium", "Long"]
language_options = ["English","Hinglish"]

def main():
    st.title("Linkedin Post Generator")
    
    col1, col2, col3 = st.columns(3)
    # Ensure tags are loaded
    if fs.get_tags():
        # Display tag options in selectbox
        
        with col1:
            selected_tag = st.selectbox("Title", options = list(fs.get_tags()))
    else:
        st.write("No tags available")


    with col2:
        selected_len = st.selectbox("Length", options = length_options)

    with col3:
        selected_lan = st.selectbox("Language", options = language_options)
    
    if st.button("Generate"):
        post = generate_post(selected_len,selected_lan,selected_tag)
        st.write(post)

if __name__ == "__main__":
    main()



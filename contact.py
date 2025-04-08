import streamlit as st 

def contact_page():
    st.title("Contact Author of app.")

    st.markdown("Author: Nikhil Rawat. Second year student of BCA (Bachelor of Computer Application) when he create this app as project to test skills and knowledge in data analysis")
    
    github = 'https://github.com/Nikhil-Rawat496?tab=repositories'
    
    linkedIN = 'https://www.linkedin.com/in/nikhil-rawat-13443529b/'
    
    st.write(f'LinkedIN: [Nikhil Rawat]({linkedIN})')
    st.write(f'GitHub: [Nikhil Rawat]({github})')

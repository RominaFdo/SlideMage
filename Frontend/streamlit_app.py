import streamlit as st
import requests
import os
from io import BytesIO

API_URL = os.getenv("API_URL", "http://127.0.0.1:8000")

# Page configuration
st.set_page_config(
    page_title="SlideMage",
    page_icon="🧙",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
    .main-header {
        text-align: center;
        color: #1f77b4;
        margin-bottom: 2rem;
        background: linear-gradient(45deg, #1f77b4, #ff00bc);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        
    }
    .stButton > button {
        background-color: #1f77b4;
        color: white;
        border-radius: 20px;
        border: none;
        padding: 0.5rem 2rem;
        font-weight: bold;
    }
    .success-message {
        background-color: #d4edda;
        color: #155724;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="main-header">SlideMage - AI Presentation Generator</h1>', unsafe_allow_html=True)
st.markdown("---")

# Sidebar with information
with st.sidebar:
    st.header("ℹ️ About SlideMage")
    st.write("SlideMage uses AI to automatically generate professional presentations from topics or documents.")
    st.write("**Features:**")
    st.write("• Topic-based generation")
    st.write("• Document upload support")
    st.write("• AI-powered content creation")
    st.write("• Professional slide design")

# Main interface
col1, col2 = st.columns([1, 1])

with col1:
    st.header("Generate from Topic")
    topic = st.text_input(
        "Enter a topic:", 
        placeholder="e.g., Climate Change, Ancient Rome, Machine Learning",
        help="Enter any topic you'd like to create a presentation about"
    )
    
    if st.button("🚀Generate from Topic", key="topic_btn"):
        if not topic.strip():
            st.error("Please enter a topic!")
        else:
            with st.spinner(f"Creating presentation about '{topic}'..."):
                try:
                    response = requests.post(
                        f"{API_URL}/generate_slides", 
                        data={"topic": topic},
                        timeout=60
                    )
                    
                    if response.status_code == 200:
                        st.success("✅ Presentation generated successfully!")
                        
                        # Download button
                        st.download_button(
                            label="Download Presentation",
                            data=response.content,
                            file_name=f"{topic.replace(' ', '_')}_slides.pptx",
                            mime="application/vnd.openxmlformats-officedocument.presentationml.presentation"
                        )
                    else:
                        st.error(f"❌ Error generating presentation: {response.text}")
                        
                except requests.exceptions.Timeout:
                    st.error("⏱Request timed out. Please try again.")
                except requests.exceptions.ConnectionError:
                    st.error("Cannot connect to the API. Make sure the backend is running.")
                except Exception as e:
                    st.error(f"❌ An error occurred: {str(e)}")

with col2:
    st.header("Generate from Document")
    uploaded_file = st.file_uploader(
        "Upload your document:",
        type=["txt", "pdf", "docx"],
        help="Upload a text file, PDF, or Word document"
    )
    
    if uploaded_file and st.button("🚀 Generate from Document", key="doc_btn"):
        with st.spinner(f"Processing '{uploaded_file.name}'..."):
            try:
                files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
                response = requests.post(
                    f"{API_URL}/upload_doc",
                    files=files,
                    timeout=60
                )
                
                if response.status_code == 200:
                    st.success("✅ Presentation generated from document!")
                    
                    # Download button
                    st.download_button(
                        label="Download Presentation",
                        data=response.content,
                        file_name=f"{uploaded_file.name}_slides.pptx",
                        mime="application/vnd.openxmlformats-officedocument.presentationml.presentation"
                    )
                else:
                    st.error(f"❌ Error processing document: {response.text}")
                    
            except requests.exceptions.Timeout:
                st.error("Request timed out. Please try again.")
            except requests.exceptions.ConnectionError:
                st.error("Cannot connect to the API. Make sure the backend is running.")
            except Exception as e:
                st.error(f"❌ An error occurred: {str(e)}")

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #666;'>Built with ❤️ using FastAPI, Streamlit, and AI</div>",
    unsafe_allow_html=True
)
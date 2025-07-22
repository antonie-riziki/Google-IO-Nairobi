import streamlit as st 
import sys
import tempfile
import os


from streamlit_option_menu import option_menu



sys.path.insert(1, './modules')

from upload_file_rag import get_qa_chain, query_system
from toc_summary import generate_toc_summary
from gemini_image_models import get_image_description



page_config = {"page_title":"GDG IO Nairobi 2025", "page_icon":":desktop computer:", "layout":"centered"}
st.set_page_config(**page_config)


with st.sidebar:
	selected = option_menu(
		menu_title = 'Menu',
		options = ['Rags to Riches 😅', 'GemVision 🖼'],
		icons = ['speedometer', 'chat-dots', 'currency-bitcoin', 'activity'],
		menu_icon = 'cast',
		default_index = 0
		)


st.image('https://linktr.ee/og/image/gdgnairobi.jpg', width=700)


# col1, col2 = st.columns(2)

# with col1:
# def reset_conversation():
#   st.session_state.conversation = None
#   st.session_state.chat_history = None


# with st.sidebar:
#     pass
#     # if st.button(label="", icon=":material/quick_reference_all:", on_click=reset_conversation):
#     #     with st.spinner("Refreshing chat... Please wait."):
#     #         st.success("Chat refreshed successfully!")


if selected=="Rags to Riches 😅":
    uploaded_files = st.file_uploader('Upload a File (PDF/CSV)', accept_multiple_files=True)

    if uploaded_files:
        for uploaded_file in uploaded_files:

            suffix = os.path.splitext(uploaded_file.name)[1]
            with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp_file:
                temp_file.write(uploaded_file.getbuffer())
                temp_path = temp_file.name

            col1, col2 = st.columns(2)


            # Initialize QA chain from saved file
            qa_chain = get_qa_chain(temp_path)

            with col1:

                # Initialize session state for chat history
                if "messages" not in st.session_state:
                    st.session_state.messages = [{"role": "assistant", "content": "How may I help you?"}]

                # Display chat history
                for message in st.session_state.messages:

                    with st.chat_message(message["role"]):
                        st.markdown(message["content"])


                if prompt := st.chat_input("How may I help?", key='RAG chat'):
                    # Append user message
                    st.session_state.messages.append({"role": "user", "content": prompt})
                    with st.chat_message("user"):
                        st.markdown(prompt)

                    # Generate AI response
                    chat_output = query_system(prompt, qa_chain)
                    
                    # Append AI response
                    with st.chat_message("assistant"):
                        st.markdown(chat_output)

                    st.session_state.messages.append({"role": "assistant", "content": chat_output})

            with col2: 
                with st.expander('', expanded=True):
                    st.markdown("""
                            <style>
                            .scroll-box {
                                max-height: 650px;
                                overflow-y: scroll;
                                padding: 10px;
                                
                                
                            }
                            </style>
                        """, unsafe_allow_html=True)

                    pdf_summary = generate_toc_summary(temp_path)
                    st.markdown(f'<div class="scroll-box">{pdf_summary}</div>', unsafe_allow_html=True)

# =================================== End of Rags to Riches Section =======================================#

# =================================== Image Generation Section ============================================ #
if selected=="GemVision 🖼":
    uploaded_file = st.file_uploader('Upload Your Drip', type=['jpg', 'jpeg', 'png', 'webp', 'bitmap', 'gif'])

    if uploaded_file is not None:

        user_image = Image.open(uploaded_file)


    image_description_text = get_image_description(user_image)

    col1, col2 = st.columns(2)

    with col11:
        st.image(uploaded_file)
        # generate_speech(roast_text) # Remember to uncomment this line for presentation

    with col12:
        

        st.markdown("""
                <style>
                .scroll-box {
                    max-height: 450px;
                    overflow-y: scroll;
                    padding: 10px;
                    border: 1px solid #ccc;
                    border-radius: 8px;
                    
                }
                </style>
            """, unsafe_allow_html=True)

        # Then display the formatted Markdown content in a scrollable box
        st.markdown(f'<div class="scroll-box">{image_description_text}</div>', unsafe_allow_html=True)




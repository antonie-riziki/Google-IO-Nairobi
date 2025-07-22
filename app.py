import streamlit as st 
import sys
import tempfile
import os


from streamlit_option_menu import option_menu



sys.path.insert(1, './modules')

from upload_file_rag import get_qa_chain, query_system
from toc_summary import generate_toc_summary



page_config = {"page_title":"GDG IO Nairobi 2025", "page_icon":":desktop computer:", "layout":"centered"}
st.set_page_config(**page_config)


with st.sidebar:
	selected = option_menu(
		menu_title = 'Menu',
		options = ['Home', 'Chatbot', 'Document Chat', 'Image Gen'],
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


if selected=="Home":
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
                                max-height: 450px;
                                overflow-y: scroll;
                                padding: 10px;
                                border: 1px solid #ccc;
                                border-radius: 8px;
                                
                            }
                            </style>
                        """, unsafe_allow_html=True)

                    pdf_summary = generate_toc_summary(temp_path)
                    st.markdown(f'<div class="scroll-box">{pdf_summary}</div>', unsafe_allow_html=True)


if selected=="Chatbot":
    st.write('This is the chatbot')




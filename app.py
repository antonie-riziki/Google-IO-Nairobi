import streamlit as st 
import sys
import tempfile
import os



sys.path.insert(1, './modules')

from upload_file_rag import get_qa_chain, query_system






st.image('https://res.cloudinary.com/startup-grind/image/fetch/c_scale,w_2560/c_crop,h_650,w_2560,y_0.57_mul_h_sub_0.57_mul_650/c_crop,h_650,w_2560/c_fill,dpr_2.0,f_auto,g_center,q_auto:good/https://res.cloudinary.com/startup-grind/image/upload/c_fill%2Cdpr_2.0%2Cf_auto%2Cg_center%2Cq_auto:good/v1/gcs/platform-data-goog/chapter_banners/devfest19%2520main.JPG', width=700)


# col1, col2 = st.columns(2)

# with col1:
def reset_conversation():
  st.session_state.conversation = None
  st.session_state.chat_history = None


with st.sidebar:
    pass
    # if st.button(label="", icon=":material/quick_reference_all:", on_click=reset_conversation):
    #     with st.spinner("Refreshing chat... Please wait."):
    #         st.success("Chat refreshed successfully!")

uploaded_files = st.file_uploader('Upload a File', accept_multiple_files=True)

if uploaded_files:
    for uploaded_file in uploaded_files:

        suffix = os.path.splitext(uploaded_file.name)[1]
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp_file:
            temp_file.write(uploaded_file.getbuffer())
            temp_path = temp_file.name

        # Initialize QA chain from saved file
        qa_chain = get_qa_chain(temp_path)

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




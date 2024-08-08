import streamlit as st
import document_processor
import embeddings
import model
import time
from html_chat_template import css, bot_template, user_template
from html_input_template import input_text_style, header_style
from dotenv import load_dotenv


def submit():
    st.session_state.submit_input = True
    st.session_state.user_question = st.session_state.user_input 
    st.session_state.user_input = ""
    #clear_input_field()       
    
    
def handle_userinput(user_question):
    response = st.session_state.conversation({'question': user_question})
    st.session_state.chat_history = response['chat_history'] 

    for i, message in enumerate(st.session_state.chat_history):
        if i % 2 == 0:
            st.write(user_template.replace(
                "{{MSG}}", message.content), unsafe_allow_html=True)
        else:
            st.write(bot_template.replace(
                "{{MSG}}", message.content), unsafe_allow_html=True)
            
                                       
def main():
    load_dotenv()
    st.set_page_config(page_title="Chat with multiple PDFs", page_icon=":books:")
    st.write(css, unsafe_allow_html=True)
    
    if "conversation" not in st.session_state:
        st.session_state.conversation = None
        
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = None   
          
    if "submit_input" not in st.session_state:
        st.session_state.submit_input = False
        
    if "user_question" not in st.session_state:   
        st.session_state.user_question = "" 
               
    
    header_container = st.container()
    chat_container = st.container()
    input_container = st.container()
    
    
    with header_container:
        header_styles = header_style.get('style')
        st.markdown(header_styles, unsafe_allow_html=True)
        st.header("Chat with AI Doc-Master 💻:books:")
        
        
    
    with input_container:
        text_column, button_column = st.columns([4, 1])
        input_text_styles = input_text_style.get('style')
        st.markdown(input_text_styles, unsafe_allow_html=True)
        with text_column:
            user_input = st.text_input("", key='user_input', on_change=submit, placeholder="Ask a question about your documents")
        with button_column:
            send_button = st.button('send', key='send_button')
    
        if send_button or st.session_state.submit_input:
            print('yes')
            print (st.session_state.user_question) 
            if st.session_state.user_question != "":
                print (st.session_state.user_question)
                with chat_container:
                    handle_userinput(st.session_state.user_question)
    
    
    with st.sidebar:
        st.subheader("File Manager")
        uploaded_docs = st.file_uploader("Upload your PDFs here and click on 'Compute'", accept_multiple_files=True)
        model_name = st.selectbox("Select your prefered LLM", ["OpenAI", "HuggingFace", "LaMini"])
        if st.button("Compute"):
            with st.spinner("Training model on your document(s)"):
                raw_text = document_processor.get_pdf_text(uploaded_docs)
                text_chunks = document_processor.get_text_chunks(raw_text)
                vector_database = embeddings.get_vector_database(text_chunks, model_name)
                st.session_state.conversation = model.chatbot(vector_database, model_name)
                st.write('Training Completed')
                
    
    
if __name__ == '__main__':
    main()
    
        
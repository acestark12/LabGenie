import streamlit as st
from dotenv import load_dotenv
from PyPDF2 import PdfReader
import nltk
from nltk.corpus import stopwords 
import os
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.schema.messages import HumanMessage, SystemMessage, AIMessage
#from dotenv import load_dotenv

st.set_page_config(page_title="Chat with your own report", page_icon=":books:")

def get_answer_from_gpt(question,messages):
    messages.append(HumanMessage(content=question))
    answer=chat.invoke(messages).content
    messages.append(AIMessage(content=answer))
    return answer

def get_keywords(pdf_doc):
    reader = PdfReader(pdf_doc)
    keywords=[]
    for page in reader.pages:
        text = page.extract_text()
        tokens = nltk.word_tokenize(text)
        stop_words = set(stopwords.words('english'))
        filtered_text = [word for word in tokens if not word.lower() in stop_words]
        for word in filtered_text:
            if word.isalpha():
                keywords.append(word.lower())
        keywords=list(set(keywords))        
    return keywords

def main():
    load_dotenv()
    if "chat_history" not in st.session_state:
        st.session_state.chat_history=[
        SystemMessage(content="You're a helpful assistant that describes health realted terms in short, its healthy level in body and tips to keep it balanced in body."),
    ]
    if "previous_messages" not in st.session_state:
        st.session_state.previous_messages = []

    if "keywords" not in st.session_state:
        st.session_state.keywords=[]
    
    if "definition" not in st.session_state:
        st.session_state.definition=""
 
    st.header("Your report's key definitions :heavy_exclamation_mark:")
    
    with st.sidebar:
        st.subheader("Your Report")
        file_uploaded = st.file_uploader("Upload your report here and click on 'Process'")
        if st.button("Process"):
            keywords=get_keywords(file_uploaded)
            kw_str=''
            for word in keywords:
                st.write(word)
                kw_str=kw_str+word+', '
            query=[SystemMessage(content="""You are a helpful assistant that identifies the terms directly or indirectly related to protiens,
                                 enzymes and hormones found in body from the list of words provided,
                                 and defines them in short, mentions its healthy level in body in terms of medical units and tips to keep it balanced."""),
                                 HumanMessage(content=kw_str)]
            st.session_state.definition=chat.invoke(query).content

            
    if st.session_state.definition:
        st.write(st.session_state.definition)
    
    st.header("Chat with LabGenie 🧞")
    for message in st.session_state.previous_messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    if prompt:=st.chat_input("I am your LabGenie. How may I help you?"):
        with st.chat_message("user"):
            st.markdown(prompt)
        st.session_state.previous_messages.append({"role":"user","content":prompt})
        st.session_state.chat_history.append(HumanMessage(content=prompt))
        ai_response=chat.invoke(st.session_state.chat_history).content
        st.session_state.chat_history.append(AIMessage(content=ai_response))

        response=f"Genie:{ai_response}"
        with st.chat_message("assistant"):
            st.markdown(response)
        st.session_state.previous_messages.append({"role":"assistant","content":response})

if __name__ == "__main__":
       
    os.environ['OPENAI_API_KEY']='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'
    chat=ChatOpenAI()    
    main() 

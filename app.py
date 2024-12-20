import streamlit as st
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings,HuggingFaceInstructEmbeddings
# from langchain.llms import HuggingFaceHub
from langchain.vectorstores import FAISS
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI
from htmlTemplates import css,bot_template,user_template
from pdfgen import PDF

# https://github.com/alejandro-ao/ask-multiple-pdfs/blob/main/app.py

def get_pdf_text(pdf_docs):
    text = "" 
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text

def get_text_chunks(text):
    text_splitter = CharacterTextSplitter(
        separator="\n\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    chunks = text_splitter.split_text(text)
    return chunks

def get_vectorstore(text_chunks):
    #embeddings = OpenAIEmbeddings()
    # More info on embeddings
    # https://huggingface.co/spaces/mteb/leaderboard
    embeddings = HuggingFaceInstructEmbeddings(model_name="hkunlp/instructor-xl")
    vectorstore = FAISS.from_texts(texts=text_chunks,embedding=embeddings)
    return vectorstore

def get_conversation_chain(vectorstore):

    llm = ChatOpenAI()

    # llm = HuggingFaceHub(model_name="TMElyralab/lyraLLaMA")
    # llm = HuggingFaceHub(repo_id="TMElyralab/lyraLLaMA", huggingfacehub_api_token="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")
    memory = ConversationBufferMemory(memory_key='chat_history',return_messages=True)
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(),
        memory=memory
    )
    return conversation_chain
    

def handle_userinput(user_question):
    response = st.session_state.conversation({'question': user_question})
    # st.write(response)
    st.session_state.chat_history = response['chat_history']

    # pdf = PDF('P','mm','Letter')
    # pdf.set_auto_page_break(auto = True,margin = 15)

    for i,message in enumerate(st.session_state.chat_history):
        if i % 2 == 0:
            st.write(user_template.replace("{{MSG}}",message.content),unsafe_allow_html=True)
            # pdf.print_chapter(i,'Chapter',message.content)
            with open('chp1.txt','w') as f:
                f.write(message.content)


        else:
            st.write(bot_template.replace("{{MSG}}",message.content),unsafe_allow_html=True)
            with open('chp2.txt','w') as f:
                f.write(message.content)
    
    
    
        
def generate_pdf():

    pdf = PDF('P','mm','Letter')
    pdf.set_auto_page_break(auto = True,margin = 15)

    pdf.print_chapter(1,'What is Covered','chp1.txt')
    pdf.print_chapter(2,'What is not Covered','chp2.txt')

    pdf.output('MyCoverage.pdf')


        

def main():
    load_dotenv()
    st.set_page_config(page_title="Chat with multiple PDFs",page_icon=":books:")

    st.write(css,unsafe_allow_html=True)

    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = None
    # if "pdf" not in st.session_state:
    #     st.session_state.pdf = None

    st.header("Chat with multiple PDFs :books:")
    user_question = st.text_input("Ask a question about your documents:")
    if user_question:
        handle_userinput(user_question)


    if st.button("Generate pdf"):
        with st.spinner("Processing"):
            generate_pdf()
            
            
    
    with st.sidebar:
        st.subheader("Your documents")
        pdf_docs = st.file_uploader("Upload your PDF documents and click on Process",accept_multiple_files=True)
        if st.button("Process"):
            with st.spinner("Processing"):
                #Get pdf text
                raw_text = get_pdf_text(pdf_docs)
                #st.write(raw_text)
                #create chunks
                text_chunks = get_text_chunks(raw_text)
                #st.write(text_chunks)
                #create vector store
                vectorstore = get_vectorstore(text_chunks)
                #create conversation chain
                st.session_state.conversation = get_conversation_chain(vectorstore)
    


if __name__ == '__main__':
    main()
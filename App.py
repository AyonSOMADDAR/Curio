import re
import streamlit as st
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os
import pandas as pd
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import google.generativeai as genai
from langchain.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()
os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
conversation_df = pd.DataFrame(columns=["Timestamp", "Name", "User_Input", "Response"])
feedback=pd.DataFrame(columns=["Name", "Feedback"])

def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text

def get_text_chunks(text):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=1000)
    chunks = text_splitter.split_text(text)
    return chunks

def get_vector_store(text_chunks):
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    vector_store = FAISS.from_texts(text_chunks, embedding=embeddings)
    vector_store.save_local("faiss_index")

def get_conversational_chain():
    prompt_template = """
    Your name is "Curio". user will input his details, please answer keeping the details {AboutStudent} in mind.
    Answer in the format of a teacher
    Rating: \n {rating}\n
    Name: \n {name} \n
    Context:\n {context}?\n
    Question: \n{question}\n
    AboutStudent: \n{AboutStudent}\n
    Answer:
    """

    model = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0.3)

    prompt = PromptTemplate(template=prompt_template, input_variables=["rating","context", "question", "name","AboutStudent"])
    chain = load_qa_chain(model, chain_type="stuff", prompt=prompt)

    return chain



def take_quiz(name,rating):
    
    question_prompt='''Generate a Short question based on the {context} and {rating} of the student and the previous chats that has occured. 
    It has to be a short question which is easy to evaluate.
    # '''
    chain=get_conversational_chain()
    df=pd.read_csv('conversation_history.csv')
    df.columns=['Timestamps','Name','User_Input','Response']
    df=df[df.Name==name]
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    new_db = FAISS.load_local("faiss_index", embeddings)
    history=df['User_Input'].tolist()+df['Response'].tolist()
    docs = new_db.similarity_search(history)
    result = chain({"rating":rating,"input_documents": docs, "question": question_prompt, "name": name, "AboutStudent": []}, return_only_outputs=True)
    # print(result['output_text'])
    response=result['output_text']
    # st.write()
    st.write(result['output_text'])
    answer=[]
    if st.button('answer'):
        answer=st.text_input("Give an answer")
        st.write(answer)
        st.write("--------")
    

    evaluation_parameter=f'''
    Evaluate in short andstudent based on  {answer} returning score(ranging from 0 to 10) and detailed performance analysis.
    Highlight missed questions with corrective explanations.
    Offer personalized feedback addressing knowledge gaps, strengths, and learning opportunities.
    '''
    

    evaluation= chain({"rating":rating,"input_documents": [], "question": evaluation_parameter, "name": name, "AboutStudent": answer}, return_only_outputs=True)

    feedback.loc[len(feedback)] = [name, evaluation]
    feedback.to_csv("feedback_history.csv", index=False, mode='a',  header=not os.path.exists("feedback_history.csv"))

    return rating



def student_info(name,rating):
    
    # Generate greeting message using language model
    
    with st.sidebar:
        answers=[]
        model = get_conversational_chain()
        on=st.toggle("Profile Playground")
        if on:
            
            prompt = """
            Generate a good and descriptive user greeting given the following inputs: 
            Ask some questions related to capturing student information like Name, Age, Gender, Learning History:, Learning Styles, Accessibility Needs, Areas of Interest, Preferred Modalities
            Name: \n {name} \n
            make sure the questions are concise.
            Answer: 
            """
            # response = model(prompt)
            response = model({"rating":rating,"input_documents": [], "question": prompt, "name": name, "AboutStudent":[]}, return_only_outputs=True)
            st.write(response["output_text"])
            answers=st.text_input("Answer here")
            

    
    greet="Generate a greeting message as per the information you under about the user. If user information is not available, simple greet generally"
    greeting = model({"rating":rating,"input_documents": [], "question": greet, "name":name, "AboutStudent":answers})
    st.write(greeting["output_text"])
    
    

def user_input(user_question, name, answers,rating):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    new_db = FAISS.load_local("faiss_index", embeddings)
    docs = new_db.similarity_search(user_question)
    chain = get_conversational_chain()
    try:
        response = chain({"rating":rating,"input_documents": docs, "question": user_question, "name": name, "AboutStudent": answers}, return_only_outputs=True)
        st.write("Reply: ", response["output_text"])
    
    except:
        st.write("Sorry, I couldn't generate a response for that.")
        response = {"output_text": "Sorry, I couldn't generate a response for that."}

    if st.button("Regenerate"):
            with st.spinner("regenerating...."):
                #template update
                chain = get_conversational_chain()
                response = chain({"rating":rating,"input_documents": docs, "question": user_question, "name": name, "context":new_db, "AboutStudent": answers}, return_only_outputs=True)
                st.write("Regenerated Reply: ", response["output_text"])
                
    conversation_df.loc[len(conversation_df)] = [timestamp, name, user_question, response["output_text"]]
    conversation_df.to_csv("conversation_history.csv", index=False, mode='a',  header=not os.path.exists("conversation_history.csv"))


    return answers


    
def main():
    st.set_page_config("Chat PDF")
    st.header("Curio")
    rating =0
    with st.sidebar:
        st.title("Details")
        name = st.text_input("Enter your name")
        if st.button("Take Quiz"):
            rating=take_quiz(name,rating)
            
    
    answers=student_info(name,rating)
       

    user_question = st.text_input("Ask a Question")
    if user_question:
        user_input(user_question, name, answers,rating)
        df=pd.read_csv('conversation_history.csv')
        df.columns=['Timestamps','Name','User_Input','Response']
        conversation_df.to_csv("conversation_history.csv", index=False, mode='a',  header=not os.path.exists("conversation_history.csv"))
        with st.sidebar:
            st.write(df[df['Name'] == name])
            
    with st.sidebar:
        on=st.toggle("Upload Document")
        if on:
            st.title("Menu:")
            pdf_docs = st.file_uploader("Upload your PDF Files and Click on the Submit & Process Button", accept_multiple_files=True)
            if st.button("Submit & Process"):
                with st.spinner("Processing..."):
                    raw_text = get_pdf_text(pdf_docs)
                    text_chunks = get_text_chunks(raw_text)
                    get_vector_store(text_chunks)
                    st.success("Done")
     

if __name__ == "__main__":
    main()

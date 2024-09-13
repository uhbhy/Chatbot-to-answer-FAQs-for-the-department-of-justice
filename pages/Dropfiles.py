import streamlit as st
import io
import pdfplumber
import docx2txt
import time
from deep_translator import GoogleTranslator
from openai import OpenAI

def questionfunc(api_key,question,raw_text):
    # Initialize OpenAI client
    client = OpenAI(api_key=api_key)    
    # Define the system message template
    system_message = ("You are a highly experienced legal expert with extensive knowledge in Indian law, including contract law, corporate law, civil litigation,"
                      "constitutional law, and statutory interpretation. You have been provided with a [text_excerpt], and your task is to analyze"
                      "and interpret its contents based on the [question] posed to you by a customer. You will carefully consider the relevant clauses, provisions"
                      "under Indian statutes, case law, and legal principles contained within the document. Provide clear, precise, and legally sound explanations,"
                      "while avoiding unnecessary legal jargon, so that the customer can fully understand the legal implications under Indian law. When addressing"
                      "the customer’s questions: 1. Ensure your answers are accurate and based strictly on the document provided, as well as relevant Indian laws such"
                      "as the Indian Contract Act, 1872; Companies Act, 2013; Code of Civil Procedure, 1908; Constitution of India, and other pertinent legislation."
                      "2. Where applicable, refer to specific sections, clauses, or legal terms from the document or Indian statutes. 3. If certain information is"
                      "unclear or incomplete, indicate the need for further clarification or additional legal advice. 4. When needed, explain legal terms or concepts"
                      "in simple language without compromising on accuracy or professionalism, considering the context of Indian law.")
     
    # Create the user message for few-shot prompting
    user_message_tuning=(f"""text: It is hereby enacted, in accordance with the provisions of the Indian Majority Act, 1875, that every person domiciled in India shall be deemed to have attained the age of majority upon the completion of eighteen years, and not before, except in cases where a personal law applicable to such persons prescribes otherwise. Notwithstanding any custom or usage to the contrary, no marriage shall be deemed lawful unless the contracting parties have attained the age prescribed under the Prohibition of Child Marriage Act, 2006, being eighteen years for females and twenty-one years for males, respectively.
                             question: What is the Indian Majority Act of 1875?
                         """)
                                     
    #Create assistant response for user_message_tuning
    assistant_message_tuning=("According to the Indian Majority Act of 1875, any person living in India is considered an adult once they turn 18, unless a specific personal law says otherwise. For marriages, regardless of any traditions or customs, it’s illegal unless both people meet the legal age requirements set by the Prohibition of Child Marriage Act of 2006: 18 years old for women and 21 years old for men.")
    
    #input question submitted by user 
    user_message=(f"text_excerpt: {raw_text} \n question: {question} ")
    # Call OpenAI API to generate options
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_message_tuning},
            {"role": "assistant", "content":assistant_message_tuning},
            {"role": "user", "content": user_message}
        ],
        temperature=0.35,
        n=1,
        max_tokens=1000,
        top_p=0.5,
        frequency_penalty=0,
        presence_penalty=0
    )
    # Extract the response content
    result=response.choices[0].message.content
    return result

def explainfunc(api_key,raw_text):
    # Initialize OpenAI client
    client = OpenAI(api_key=api_key)
    # Define the system message template
    system_message = (  "You are a retired and very experienced lawyer, who lives in a Village in India and helps people who have little knowledge of English"
                        "to understand Legal contracts and documents that they are signing in a very simple, moderately concise and easy to understand way"
                        "so that people don't get scammed or mislead into signing something against their interests.")                     
    # Create the user message for few-shot prompting
    user_message_tuning=("""
                         Given Text:
                         Document 1
                         AGREEMENT

                        This Agreement is made and entered into on the __ day of , 20, by and between:

                        Party A: [Name], having its registered office at [Address], hereinafter referred to as "First Party",
                        Party B: [Name], having its registered office at [Address], hereinafter referred to as "Second Party".

                        WHEREAS:

                        The First Party is engaged in the business of [describe business].
                        The Second Party is engaged in the business of [describe business].
                        Both Parties desire to enter into a business relationship on the terms and conditions set forth herein.
                        NOW, THEREFORE, in consideration of the mutual promises and covenants contained herein, the Parties hereby agree as follows:

                        1. Scope of Work
                        The First Party agrees to provide [services/products] as per the specifications and terms set out in Annexure A. The Second Party agrees to [obligations of the second party].

                        2. Term of Agreement
                        This Agreement shall commence on the date mentioned above and shall remain in effect for a period of [duration], unless terminated earlier in accordance with the provisions of this Agreement.

                        3. Consideration
                        The First Party agrees to compensate the Second Party an amount of ₹[Amount] for the services/products provided under this Agreement. Payment terms are detailed in Annexure B.

                        4. Confidentiality
                        Both Parties agree to maintain the confidentiality of proprietary information exchanged during the course of the business relationship, as specified in Annexure C.

                        5. Termination
                        Either Party may terminate this Agreement upon [days] written notice to the other Party in the event of a material breach of this Agreement or for any reason as described in Annexure D.
                        """)
    #Create assistant response for user_message_tuning
    assistant_message_tuning=("""
                                This agreement is a contract between two parties, referred to as the "First Party" and the "Second Party," who are entering into a business relationship. Here's a breakdown of the key sections:

                                Parties Involved:
                                First Party: The name and address of Party A are specified.
                                Second Party: The name and address of Party B are specified.
                                Recitals ("Whereas" Clauses):
                                These clauses explain the background:

                                The First Party and Second Party are each engaged in their respective businesses.
                                They wish to work together under this agreement.
                                Main Terms of the Agreement:
                                Scope of Work:

                                The First Party will provide specific services or products, which are described in detail in Annexure A.
                                The Second Party's responsibilities or obligations are also outlined here.
                                Term of Agreement:

                                The agreement will start on the specified date and will last for a certain period (the duration is mentioned).
                                It may be terminated earlier if either party follows the conditions set out in the agreement.
                                Consideration (Payment):

                                The First Party will pay the Second Party a specific amount (₹[Amount]) for the services or products.
                                The exact payment terms are listed in Annexure B.
                                Confidentiality:

                                Both parties must keep any proprietary information they exchange during the course of business confidential.
                                Further details on confidentiality are provided in Annexure C.
                                Termination:

                                Either party can end the agreement by giving a certain number of days' written notice.
                                Termination can occur if there's a material breach (a serious violation of the agreement) or for reasons stated in Annexure D.
                                Annexures:
                                Annexure A: This will include the detailed description of the services or products that the First Party is supposed to provide.
                                Annexure B: Contains the payment terms (e.g., payment schedule, mode of payment).
                                Annexure C: Covers the specific confidentiality obligations for both parties.
                                Annexure D: Lists the specific conditions under which the agreement can be terminated and the process to do so.
                                """)
    #Create the user message for generating itinerary
    user_message=(f"Given Text: {raw_text}")

    # Call OpenAI API to generate options
    response = client.chat.completions.create(
        model="gpt-4ko",
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_message_tuning},
            {"role": "assistant", "content":assistant_message_tuning},
            {"role": "user", "content": user_message}
        ],
        temperature=0.35,
        n=1,
        max_tokens=1000,
        top_p=0.5,
        frequency_penalty=0,
        presence_penalty=0
    )

    # Extract the response content
    result=response.choices[0].message.content
    return result

def main():
    api_key=""
    st.sidebar.title("MENU")
    st.sidebar.image("logo.jpeg", use_column_width=True)
    st.sidebar.markdown("<hr>",unsafe_allow_html=True)
    st.subheader("Drop Files Here")
    raw_files=st.file_uploader('Upload your files', type=['txt','docx','pdf'], accept_multiple_files=True)
    #Reading File Data
    if raw_files is not None:
        raw_text = ""  # Initialize an empty string to accumulate text from all documents
        for uploaded_file in raw_files:  # Loop through each uploaded file
            if uploaded_file.type == "text/plain":
                try:
                    text = str(uploaded_file.read(), "utf-8")
                    raw_text += text  # Concatenate the text from the current document
                except:
                    st.error(".txt file fetching problem!\ncheck your file again and try re-uploading")
            elif uploaded_file.type == "application/pdf":
                try:
                    pdf_reader = pdfplumber.open(uploaded_file)
                    for page_num in range(len(pdf_reader.pages)):
                        page = pdf_reader.pages[page_num]
                        raw_text += page.extract_text()  # Concatenate the text from the current page
                except:
                    st.error(".pdf file fetching problem!\ncheck your file again and try re-uploading")
            elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
                try:
                    raw_text += docx2txt.process(uploaded_file)  # Concatenate the text from the current document
                except:
                    st.error(".docx file fetching problem!\ncheck your file again and try re-uploading")
            else:
                st.error("Please Upload a File to continue!")

    st.markdown("<hr>",unsafe_allow_html=True)
    st.info("What do you want to do with your document?")
    menu=["Ask a question","Explain","Translate"]
    choice=st.selectbox("",menu)
    st.markdown("<hr>",unsafe_allow_html=True)
    if choice=="Ask a question":
        question=st.text_area("Enter your question")
        if st.button("Submit"):
            response1=questionfunc(api_key,question,raw_text)
            st.info(response1)
    if choice=="Explain":
        response2=explainfunc(api_key,raw_text)
        st.info(response2)
    if choice=="Translate":
        target_lang = st.selectbox("Choose Language", ["Tamil", "Hindi"])
        display_target_lang=target_lang
        if target_lang == "Tamil":
            target_lang = 'ta'
        elif target_lang=="Hindi":
            target_lang = 'hi'
        
        if st.button("Translate"):
            if len(raw_text) < 3:
                st.warning("Sorry! You need to provide a text with at least 3 characters")
            else:
                my_bar = st.progress(0)
                message_slot = st.empty()
                message_slot.text('Translating...')

                for value in range(50):
                    time.sleep(0.01)
                    my_bar.progress(value + 1)

                if my_bar.progress(100):
                    message_slot.empty()  # Clear the "Translating..." message
                    st.success("Your Text Has Been Translated successfully!")
                    
                translator = GoogleTranslator(source="auto", target=target_lang)
                translated_text = translator.translate(raw_text)
                st.info("Original text: "+raw_text)
                st.warning("language selected is: "+display_target_lang)
                st.info("Translated text: "+translated_text)
        

if __name__=="__main__":
    main()

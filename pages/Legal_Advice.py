import streamlit as st
from openai import OpenAI

def advice_func(api_key,question):
    # Initialize OpenAI client
    client = OpenAI(api_key=api_key)    
    # Define the system message template
    system_message = ("""Assume you are an experienced legal advisor specializing in Indian law, known for giving clear, concise, and practical legal advice. 
                      A customer comes to you seeking help with understanding a legal document or navigating a legal situation.
                            Begin by asking for relevant details about their situation or the specific legal document they need help with.
                            Once you have the necessary information, provide straightforward, easy-to-understand advice, avoiding complex legal jargon.
                            Ensure your response includes practical steps or actions they can take, and highlight any key points or potential pitfalls they should be aware of.
                            Offer additional resources or suggestions if applicable, and encourage them to seek further professional help if their situation requires it.
                        For example, if a customer is confused about a property lease agreement, guide them through the main clauses, their rights and responsibilities, 
                      and any important terms they need to be aware of. Provide your advice in a manner that is both approachable and informative.""")
     
    # Create the user message for few-shot prompting
    user_message_tuning=("""If a previous owner of a land had allowed a neighbour or neighbour to walk or drive over his land in a shortcut 
                         and this has been going on for say a decade or so can I as the new owner stop them now from using the shortcut? Or can the neighbour or neighbours 
                         claim a legal right of way against me?""")
                                     
    #Create assistant response for user_message_tuning
    assistant_message_tuning=(""" Here's the text as a single string:
                              "In India, if a previous owner allowed a neighbor to use land as a shortcut for a significant period, 
                              the new owner might face some legal challenges in stopping this use.
                               Here’s a breakdown of the situation: 1. Right of Way (Easement) Prescriptive Easement: If the neighbor has been 
                              using the land continuously, openly, and without permission for a long time (typically over 20 years), they might claim a 
                              prescriptive easement. This means they could argue that they have acquired a legal right of way through adverse possession. 
                              Types of Easements: Easements can be express (written agreement) or implied (based on continuous use). If the previous owner 
                              had allowed the use informally and there was no written agreement, the neighbor might still claim an implied right. 2. Legal
                               Action Consultation with a Lawyer: Before taking any action, consult with a lawyer to understand the specifics of your case.
                               They can help determine if the neighbor’s use might qualify as an easement and the best course of action. Seek Court Relief: 
                              If the neighbor is claiming a right of way and you wish to contest it, you may need to seek a declaration from the court. 
                              The court will evaluate whether the neighbor’s claim is valid based on the history of use and other factors. 3. Practical 
                              Considerations Negotiation: Sometimes, negotiating with the neighbor and reaching an agreement can be more practical than 
                              legal battles. You might agree on terms for their continued use or seek compensation. Documentation: Ensure all agreements or 
                              disputes are documented to avoid future complications. In summary, if a neighbor has been using your land for a long period, 
                              they might claim a right of way through prescriptive easement. It’s important to consult with a legal expert to understand your rights and options.""")
    
    #input question submitted by user 
    user_message=(question)
    # Call OpenAI API to generate options
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_message_tuning},
            {"role": "assistant", "content":assistant_message_tuning},
            {"role": "user", "content": user_message}
        ],
        temperature=0.4,
        n=1,
        max_tokens=1000,
        top_p=0.55,
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
    st.title("Ask for any kind of Legal Advice...")
    raw_text=st.text_area("Explain Your Problem Here...")
    if(st.button("Submit")):
        response=advice_func(api_key, raw_text)
        st.success(response)

if __name__=="__main__":
    main()

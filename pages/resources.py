import streamlit as st
from openai import OpenAI

def cite_func(api_key,excerpt):
    # Initialize OpenAI client
    client = OpenAI(api_key=api_key)    
    # Define the system message template
    system_message = ("""Assume you are a legal expert well-versed in Indian laws. I will provide you with an excerpt from a legal document or text. Your task is to:
                      Read the provided excerpt carefully.Identify which specific Indian law is being referenced in the excerpt.Specify the particular section or provision
                       of that law mentioned in the excerpt.Provide a brief explanation of the relevance of this section or provision in the context of the excerpt.For example,
                       if the excerpt discusses the rights of tenants under a lease agreement, you would identify the relevant property law and cite the specific section related
                       to tenant rights.""")
     
    # Create the user message for few-shot prompting
    user_message_tuning=("""ny paid employment; or
                            (c) has been convicted of an offence which, in the opinion of the Central
                            Government, involves moral turpitude; or
                            (d) has acquired such financial or other interest as is likely to affect prejudicially
                            his functions as a Member; or
                            (e) has so abused his position as to render his continuance in office prejudicial
                            to the public interest; or
                            (f) has become physically or mentally incapable of acting as a Member.
                            (2) Notwithstanding anything contained in sub-section (1), no Member shall be
                            removed from his office on the grounds specified in clauses (d) and (e) of that sub-section
                            unless the Supreme Court, on a reference being made to it in this behalf by the Central
                            Government, has, on an inquiry, held by it in accordance with such procedure as may be
                            prescribed in this behalf by the Supreme Court, reported that the Member, ought on such
                            ground or grounds to be removed""")
                                     
    #Create assistant response for user_message_tuning
    assistant_message_tuning=("The excerpt is from the New Delhi International Arbitration Centre Act, 2019, here’s the analysis: "
         "Specific Indian Law Referenced: New Delhi International Arbitration Centre Act, 2019 "
         "Particular Section or Provision: The excerpt corresponds to Section 12 of the New Delhi International Arbitration Centre Act, 2019. "
         "Relevance of the Section or Provision: Section 12 deals with the conditions and procedure for the removal of members from the New Delhi International Arbitration Centre. "
         "It lists various grounds for removal, including involvement in paid employment, conviction of an offense involving moral turpitude, acquisition of prejudicial interests, abuse of position, or physical/mental incapability. "
         "The provision ensures that members are not removed arbitrarily and sets out a procedure involving the Supreme Court to determine the validity of the removal on certain grounds. "
         "This ensures fairness and due process in the removal process.")
    
    #input question submitted by user 
    user_message=(excerpt)
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

def main():
    api_key=""
    st.sidebar.title("MENU")
    st.sidebar.image("logo.jpeg", use_column_width=True)
    st.sidebar.markdown("<hr>",unsafe_allow_html=True)
    st.title("Enter text to get citations....")
    raw_text=st.text_area("Explain text Here...")
    if(st.button("Submit")):
        response=cite_func(api_key, raw_text)
        st.success(response)

if __name__=="__main__":
    main()

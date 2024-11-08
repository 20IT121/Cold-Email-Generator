from utils import clean_text
from portfolio import Portfolio
from chains import Chain

import streamlit as st
from langchain_community.document_loaders import WebBaseLoader
from urllib.parse import quote

base_url = "https://jobs.nike.com/job/R-42566"
query_param = "from=job search funnel"

encoded_query = quote(query_param, safe='')
full_url = f"{base_url}?{encoded_query}"


def streamlit_app(llm, portfolio, clean_text):
    print("In the appp")
    st.title("📧 Cold Email generator")
    url_input = st.text_input ("Enter your url: " , value = full_url)
    submit_button = st.button("Submit")

    if submit_button :
        try :
            print("In the try block")
            loader = WebBaseLoader([url_input])
            print(1)
            data = clean_text(loader.load().pop().page_content)
            print(2)
            portfolio.load_portfolio()
            print(3)
            jobs = llm.extract_jobs(data)
            print(4)
            skills = jobs.get('skills', [])
            print(5)
            links = portfolio.query_links(skills)
            print(6)
            email = llm.write_email(skills, links)
            print(email)
            st.code(email, language='markdown')
    
# THis loop will take care if there are multiple jobs in the url , it will generate cold email for every job listed
            # for job in jobs: 
            #     print("In the for loop")
            #     skills = job.get('skills', [])
            #     links = portfolio.query_links(skills)
            #     email = llm.write_email(skills, links)
            #     print(email)
            #     st.code(email, language='markdown')
        
        except Exception as e:
            print("in the error")
            st.error(f"Error Occured: {str(e)}")

if __name__ == "__main__":
    chain = Chain()
    portfolio = Portfolio()
    st.set_page_config(layout  = 'wide' , page_title = 'Cold email generator' , page_icon = '📧')
    streamlit_app(chain, portfolio, clean_text)
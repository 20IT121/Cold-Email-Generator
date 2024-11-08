import os
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from dotenv import load_dotenv
from langchain_core.exceptions import OutputParserException

load_dotenv()

class Chain:
    def __init__(self):
        self.llm = ChatGroq(
        model_name="llama-3.1-70b-versatile",
        temperature=0,
        groq_api_key="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"
        )
    
    def extract_jobs(self , cleaned_text):
        prompt_template = PromptTemplate.from_template(
        """
        ### SCRAPED TEXT FROM WEBSITE: {page_data}
        #### INSTRUCTION:
        The scraped text is from the career's page of a website.
        Your job is to extract the job postings and return them in JSON format containing the following keys: role, experience, skills and description* Only return the valid JSON.
        ### VALID JSON (NO PREAMBLE):
        """
        )

        chain_extract = prompt_template | self.llm
        res = chain_extract.invoke(input  = {'page_data' : cleaned_text})
        
        try:
            json_parser = JsonOutputParser()
            json_res = json_parser.parse(res.content)
        except OutputParserException as e:
            raise OutputParserException("Context too big. Unable to parse jobs")
        
        return res if isinstance(res, list) else [res] # it checks if res is a list it will return res else it will return res encloses list
    
    def write_email (self, jobs, links):
        prompt_email = PromptTemplate.from_template(
        """
        ### JOB_DESCRIPTION
        {job_description}

        ### INSTRUCTION:
        You are Mohan, a business development executive at AtliQ. AtliQ is an AI & Software Consulting the seamless integration of business processes through automated tools.
        Over our experience, we have empowered numerous enterprises with tailored solutions, fostering process optimization, cost reduction, and heightened overall efficiency.
        Your job is to write a cold email to the client regarding the job mentioned above describing the capabilities in fulfilling their needs.
        Also add the most relevant ones from the following links to showcase Atliq's portofolio : {link_list}
        Remember you are Mohan, BDE at AtliQ.
        Do not provide a preamble.
        ### EMAIL (NO PREAMBLE):
        """
        )
        chain_email = prompt_email | self.llm
        res = chain_email.invoke({
            'job_description' : str(jobs) ,
            'link_list' : links
        })

        return res.content
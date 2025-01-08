import os
from screenshot import find_images_in_directory
from crewai import Agent, Task, Crew
from crewai.process import Process
from dotenv import load_dotenv
from crewai_tools import VisionTool
from filereader_assign import FileReaderTool   #using custom function
        

#checking for image's existence in cwd(current working directory):
images_url=find_images_in_directory('.')

vision_tool = VisionTool()  #vision tool by crewai
file_reader_tool = FileReaderTool()   #custom code for file reading

load_dotenv()
# loading the keys from .env file
os.environ["OPENAI_API_KEY"]=os.getenv("OPENAI_API_KEY")
os.environ["OPENAI_MODEL_NAME"]=os.getenv("OPENAI_MODEL_NAME")

class User_ask:
    '''
    section of input from the user end
    '''
    def user_info(self):
        user_q=input("which stock you want to check today? : ")
        return user_q

class Crew_stuff:
    '''
    crewai_initiate: responsible for extracting ticker name of the stock.
    crewai_summary: responsible for using vision capability and summarization.
    '''
    def crewai_initiate(self,user_q):
        user_query=f"user wants to know the stock of {user_q}."
        info_agent = Agent(
            role="Information extraction and analysis Agent",
            goal="""You need to extract the information from the text provided to you. And as per analysis,
            return the answer in the format asked. Also, you need to write the final content in a file. """,
            backstory="""
                You are given a couple of screenshots in the working directory. And you need to extract the data from it then perform the task.
            """,
            verbose=True
        )

        task_assign = Task(
            description=f"""User's query is: {user_query}. Extract the company name that user is asking from this query. 
            And use the listed stock name or listed stock ticker name of this company in further processing, like netflix name is NFLX, apple name is AAPL, here AAPL and NFLX are listed stock name of these companies.
            Strictly adhere by this stock name of the company for the further process.
            In the output, it should provide the company name and the field in which it works.
            You can use the following output format:
            <output>
            Company name: ___Provide the exact company stock name given by user in query________,
            Area of work: _________
            </output>
            """,
            expected_output="Quick summary of the information present in that screenshot. And write it in company_info.txt file.",
            output_file="company_info.txt",
            agent=info_agent
        )

        crew = Crew(
            agents=[info_agent],
            tasks=[task_assign],
            process=Process.sequential
        )

        result=crew.kickoff()
        return result

    
    
    ## summarization section
    def crewai_summary(self):

        arguments = {
            "filename": "example.md",  # Specify the filename
            "directory": ".",    # Specify the directory for this filename
        }

        file_content = file_reader_tool._run(**arguments) #custom code for file content extraction

        summary_agent = Agent(
            role="Stock summarization and analysis agent",
            goal="""You need to extract the information from those screenshots and analyze them. You also need to read the information from the txt file provided. And as per analysis,
            return the summzarized answer. Also, you need to write the final content in a file. """,
            backstory="""
                This txt file contains stock info of the company. It was extracted via scraping.
            """,
            tools=[vision_tool],
            verbose=True
        )
        task_summary = Task(
            description=f"""Analyze the screenshots provided to you and read the text present in txt file provided as well and analyze the text. 
            As per the analysis, tell me which screenshot contains the exact information of the company stocks that user has asked for. 
            You need to access the screenshots in the same directory I am running this script.
            The screenshots are provided under the variable {images_url}.
            If the screenshot is not having that company name, then write no matched screenshots.
            You need to assess all the screenshots present in that directory with .png extension.
            Your second task includes, provide me summary of the stock info present in file and provide some recommendation to the user for this stock as per market trend. The file content you can find here: {file_content}.
            If you didn't find something relevant you can write in the fields as not completely relevant info.
            In the output you should provide Company stock name, screenshot name, Stock summary. You need to adhere by the following format:
            <output>
            Company stock name: ___________,
            Screenshot name: _____________,
            Stock summary: ___________
            </output>
            """,
            expected_output="Brief overview of the information present in the file. And write it in summary.md file.",
            output_file="summary.md",
            agent=summary_agent
        )

        crew = Crew(
            agents=[summary_agent],
            tasks=[task_summary],
            process=Process.sequential
        )

        result1=crew.kickoff()
        print("##################")  # behaves like a bookmark for output visualization, you can trace it in the output on console
        return result1
    
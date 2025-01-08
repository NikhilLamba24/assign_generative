from scrape_assign import Assign
from crewprocess import User_ask, Crew_stuff


def initiate_and_scrape():
    '''
    responsible for:
    1. Crew initiation for user query.
    2. Handling tabs and scraping for the interested stock ticker.
    3. Summarization of the stock.
    Consideration: try to run it with google chrome installed on your desktop. 
                   For more info, refer to comments before exception section in assing.py.
    '''
    try:
        # initiate the query from user
        user_ask_instance = User_ask()
        user_info = user_ask_instance.user_info()

        crew_instance = Crew_stuff()  #crew stuff class initialization

        # Crew initiation with user information
        crew_initiation_result = crew_instance.crewai_initiate(user_info)
        print("crew init result: ",crew_initiation_result)

        # Scraping process as per user query
        assign_instance = Assign()
        assign_instance.task_scrape()

        # Generate the crew summary
        crew_summary = crew_instance.crewai_summary()
        print("summarization response: ",crew_summary)

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    initiate_and_scrape()


import os
import time
from crewai import Crew
from langchain_groq import ChatGroq
from agents import personalize_email_agent, ghostwriter_agent # For Agent import
from tasks import PersonalizeEmailTask # For Tasks to get Imported
from dotenv import load_dotenv
load_dotenv()
from langchain_openai import ChatOpenAI
import csv

email_template = """
Hey [Name]!

I am a recent CS Masters grad from Illinois Tech, Chicago and actively looking for entry level job opportunities. 
I have recently relocated to San Jose, CA, and am actively seeking new opportunities.

I am attaching my resume for your review.I am proficient in Python, SQL, ML and have 3 years of Software Engineering experience at Accenture 
and currently working as an AI Engineer Intern at a startup.

Looking to explore roles in Software Development, Data Science, and Machine Learning.
I have attached my resume for your review. I would love to learn more about any potential opportunities at [Company Name] 
and how I might be a good fit for your team.

Thank you in advance for your time, and I look forward to hearing from you.

Best,
Aditya Kolluru
"""

# 1. Create Agent - Done
# 2. If tool then Create Tool - currently for this NO
# 3. Create Tasks - Done
# 4. Set up the crew 
# 5. Kickoff the crew

# Creatign agents done and now tasks
tasks = PersonalizeEmailTask()

personalize_email_tasks = []
ghostwrite_email_tasks = []

# Path to the CSV file containing client information
csv_file_path = 'data/clients_small.csv'

# Open the CSV file
with open(csv_file_path, mode='r', newline='') as file:
    # Create a CSV reader object
    csv_reader = csv.DictReader(file)

    # Iterate over each row in the CSV file
    for row in csv_reader:
        # Access each field in the row
        recipient = {
            'first_name': row['first_name'],
            'last_name': row['last_name'],
            'email': row['email'],
            'Company': row['Company'],
            'last_conversation': row['last_conversation']
        }

        # Create a personalize_email task for each recipient
        personalize_email_task = tasks.personalize_email(
            agent=personalize_email_agent,
            recipient=recipient,
            email_template=email_template
        )

        # Create a ghostwrite_email task for each recipient
        ghostwrite_email_task = tasks.ghostwrite_email(
            agent=ghostwriter_agent,
            draft_email=personalize_email_task,
            recipient=recipient
        )

        # Add the task to the crew
        personalize_email_tasks.append(personalize_email_task)
        ghostwrite_email_tasks.append(ghostwrite_email_task)

# Crew Setup

crew = Crew(
    agents=[personalize_email_agent, ghostwriter_agent],
    tasks = [*personalize_email_tasks,*ghostwrite_email_tasks],
    # max_rpm=29
)

# Kick Off the Crew
start_time = time.time()
result = crew.kickoff()
end_time = time.time()
time_spent = end_time - start_time
print(f"Crew kickoff total time spent running is {time_spent} seconds.")
print("Crew usage", crew.usage_metrics)
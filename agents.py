import os
from crewai import Agent # For crewAI
from langchain_groq import ChatGroq  # For Model

# For Tasks Import

# MODEL
llm = ChatGroq(
    groq_api_key = os.getenv("GROQ_API_KEY"),
    model="mixtral-8x7b-32768"
)

# AGENTS
"""
We have 2 agents 
1. Personalize email
2. Ghost write the personlize email
"""
# Agent1:
personalize_email_agent = Agent(
    role="Email Personalizer",
    goal=f"""
        Personalize template emails for reciepients using their information.
        Given a template email and recipient information (name, email, company, last conversation), 
        personalize the email by incorporating the recipient's details 
        into the email while maintaining the core message and structure of the original email. 
        This involves updating the introduction, body, and closing of the email to make 
        it more personal and engaging for each recipient.
        """,
    backstory="""
            As an Email personalizer, you are responsible for customizing template emails for individual recipients 
            based on their information and previous interactions.
            """,
    verbose = True,
    llm = llm,
    allow_delegation=True
    # max_iter = 2
    )

ghostwriter_agent = Agent(
    role="Ghostwriter",
    goal=f"""
        Revise draft emails to adopt the Ghostwriter's writing style.

        Use an informal, engaging, and slightly sales-oriented tone, mirroring the Ghostwriter's final email communication style.
        """,
    backstory = """
                As a Ghostwriter, you are responsible for revising draft emails to match the Ghostwriter's writing style, focusing 
                on clear, direct communication with a little friendly/professional and approachable tone.
                """,
    verbose=True,
    allow_delegation=False
    # max_iter = 2
)
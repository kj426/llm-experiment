from crewai import Crew

from models import ResumeData
from agents import query_classifier_agent, jobrole_industry_researcher_agent, work_culture_researcher_agent
from tasks import query_classification_task, jobrole_industry_research_task, work_culture_research_task
from resume_extractor import get_structured_data_from_resume_path

def classify_input(user_input):
    crew = Crew(agents=[query_classifier_agent], tasks=[query_classification_task])
    result = crew.kickoff(inputs={"query": user_input})
    return result




def start_chat_app(profile: ResumeData):
    print("Welcome to the Career Chatbot! Type 'exit' to quit.")
    while True:
        user_input = input("You: ")

        if user_input.lower() == "exit":
            print("Goodbye!")
            break

        category = classify_input(user_input)
        print(f"Classified as: {category.raw}, {type(category.raw)}")

        if category.raw == "Job Role/Industry":
            crew = Crew(agents=[jobrole_industry_researcher_agent], tasks=[jobrole_industry_research_task])
            result = crew.kickoff(inputs={"query": user_input, "profile": profile.model_dump()})
            print(result.raw)
        elif category.raw == "Work Culture":
            crew = Crew(agents=[work_culture_researcher_agent, jobrole_industry_researcher_agent],
                        tasks=[work_culture_research_task, jobrole_industry_research_task])
            result = crew.kickoff(inputs={"query": user_input, "profile": profile.model_dump()})
            print(result.raw)
        else:
            print("I didn't understand. Please rephrase.")


if __name__ == "__main__":
    resume_data = get_structured_data_from_resume_path("/home/karthik/Downloads/Karthik_Jayanthi_Resume.pdf")
    start_chat_app(resume_data)
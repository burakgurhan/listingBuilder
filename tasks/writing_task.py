from crewai import Task
from crewai.project import task
from agents.editor_agent import EditorAgent

class WritingTask:
    def __init__(self):
        pass
    
    
    def create_writing_task(self):        
        return Task(
            name="Writing Task",
    description="""
    Take the report from the Research Agent and generate an SEO-optimized product title and description.  
    Follow these guidelines:  

    ### Title Requirements:
    - Must be exactly **80 characters** (no more, no less).  
    - Should be **SEO-friendly** and include relevant keywords from the report.  
    - Must be clear, engaging, and **easy for customers to understand**.  

    ### Description Requirements:
    - Must be exactly **4 paragraphs** each paragraph has maximum 3 sentence. (no more, no less).  
    - Use best keywords from the report. Use keywords naturally.
    - Must not exceed 400 words. (no more, no less).  
    - Should be **SEO-optimized** and naturally incorporate important keywords.  
    - Must provide a compelling yet concise overview of the product. 
    - Should highlight key features, benefits, and unique selling points.
    - Focus on the product's value proposition and how it meets customer needs in one paragraph. 
    - Ensure clarity and readability for potential buyers.  
    - **Only use information from the research report** (do not add external context).  
    - Do not include Brand name in the title.

    The final output should be well-structured and formatted for easy processing.  
    """,
    expected_output="""
    A dictionary containing the SEO-optimized title and description:
    {
        "title": "Exactly 80-character product title...",
        "description": "Exactly 4 paragraphs product description..."
    }
    """,
    agent=EditorAgent().create_editor_agent()
    )

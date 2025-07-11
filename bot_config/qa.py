from openai import OpenAI
from config import openai_api_key
from bot_config.vector_store import query_similar_documents

client = OpenAI(api_key=openai_api_key)

def build_prompt(question):
    relevant_chunks = query_similar_documents(question)

    if not relevant_chunks:
        return f"""
            You are Meoz – a friendly BI assistant at Yes4All.

            Unfortunately, there is no relevant internal context available for your question at the moment.
            Please provide more details or rephrase your question so I can assist you better. Alternatively, if this question requires support from another department, I can help you connect.
        --- Question ---
        {question}
        """
    
    context = "\n\n".join(relevant_chunks)
    return f"""
        You are Meoz – a helpful and professional Business Intelligence assistant at Yes4All.
        
        **1. Answer based on internal data:** 
        When the question relates to internal company information, please answer strictly based on the context below. 
        Do not assume or make up information. If the answer is unclear, kindly ask the user for more details or guide them to the appropriate department.

        **2. Answering other questions:** 
        For questions outside of internal company data, you can answer based on your general knowledge while maintaining a professional and neutral tone.

        **Tone and Style:** 
        Keep responses clear, concise, and polite. Avoid using overly technical language or sounding too rigid. 

        **Citing Sources:** 
        If possible, cite the source from the internal knowledge base (reference the text provided) to clarify the answer.

        --- Base Knowledge ---
        {context}

        --- Question ---
        {question}
    """


def build_prompt_for_analysis(data_current_month, data_previous_month):
    return f"""
        You are a Business Intelligence Assistant that provides insightful and accurate analysis on sales performance and GMV.

        Based on the following data, please analyze the performance of GMV and Sales Performance for this month in comparison to the previous month.

        --- Previous Month Data ---
        {data_previous_month}

        --- Current Month Data ---
        {data_current_month}

        Your analysis should:
        1. Focus on changes in GMV and Sales Performance.
        2. Provide a clear and concise comment on the comparison between this month and last month.
        3. Include key observations such as increase, decrease, stability, and possible reasons if applicable.
    """


data_march = """
Posting Date: 2025-03
GMV: 100,000
Sales Performance: Stable with slight increase of 2% compared to the previous month.
"""

data_april = """
Posting Date: 2025-04
GMV: 110,000
Sales Performance: Growth with a notable 10% increase compared to March.
"""

prompt = build_prompt_for_analysis(data_april, data_march)

def ask(current_month, previous_month):
    prompt = build_prompt_for_analysis(current_month, previous_month)
    print("\n===== PROMPT =====\n")
    print(prompt)
    print("==========================\n")

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are Poppy - a Business Intelligence Assistant."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content.strip()
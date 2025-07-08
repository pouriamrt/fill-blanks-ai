import os
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

def generate_question(topic_name: str):
    prompt = ChatPromptTemplate.from_template("""
    Write a single, interesting {topic} sentence. Hide one key word with ____.
    Then provide the answer with four choices (separated by comma with a space) and a short hint. Format:
    Sentence: ...
    Choices: ...
    Answer: ...
    Hint: ...
    """)
    llm = ChatOpenAI(model="gpt-4.1", openai_api_key=OPENAI_API_KEY, temperature=0.9)
    out = llm.invoke(prompt.format(topic=topic_name))
    try:
        lines = [l.strip() for l in out.content.split('\n') if l.strip()]
        s = [l.replace("Sentence:","").strip() for l in lines if l.lower().startswith("sentence:")][0]
        c = [l.replace("Choices:","").strip() for l in lines if l.lower().startswith("choices:")][0]
        a = [l.replace("Answer:","").strip() for l in lines if l.lower().startswith("answer:")][0]
        h = [l.replace("Hint:","").strip() for l in lines if l.lower().startswith("hint:")][0]
        return s, c, a, h
    except Exception as e:
        raise Exception(f"Failed to parse LLM response: {out.content}")

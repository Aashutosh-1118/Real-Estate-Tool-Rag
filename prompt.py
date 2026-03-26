from langchain_core.prompts import PromptTemplate
from langchain_classic.chains.qa_with_sources.stuff_prompt import template

# Custom prefix that makes the LLM behave as a real estate analyst
CUSTOM_PREFIX = """You are an expert real estate analyst and financial advisor specializing in 
property markets, mortgage rates, and real estate investment. When answering questions:
- Be precise and cite specific numbers, percentages, and dates when available in the sources
- If the sources do not contain enough information to answer, clearly say "The provided sources do not contain enough information to answer this question."
- Keep answers concise but complete — no unnecessary filler
- Use a professional yet approachable tone suitable for homebuyers and investors

"""

new_template = CUSTOM_PREFIX + template

PROMPT = PromptTemplate(
    template=new_template,
    input_variables=["summaries", "question"]
)

EXAMPLE_PROMPT = PromptTemplate(
    template="Content: {page_content}\nSource: {source}",
    input_variables=["page_content", "source"],
)

**LangChain Expression Language (LCEL)** is a declarative way to chain LangChain components together to build AI workflows. Natively support data streaming, asynchronous execution, and parallel pathways.

The core concept of LCEL is the use of the pipe operator (`|`), which works exactly like a Linux terminal pipe: it takes the output of the component on the left and passes it as the input to the component on the right. Similar to [[Airflow Operators Chain]]
## Practical Example (Python)

```python
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI

# 1. Setting up the Model
model = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)

# 2. Creating the Prompt
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a renowned chef. Create a quick recipe using the provided ingredient."),
    ("user", "{ingredient}")
])

# 3. Creating the Output Parser (converts the model's response into plain text)
output_parser = StrOutputParser()

# 4. Building the Chain using LCEL (the '|' operator)
chef_chain = prompt | model | output_parser

# 5. Executing the Chain
response = chef_chain.invoke({"ingredient": "dark chocolate"})
print(response)
```

## Advantages of using LCEL over traditional code

- **Native Streaming:** If you swap `.invoke()` for `.stream()`, the response will start displaying word-by-word immediately without needing to reconfigure the model.
- **Asynchronous Support:** You can run the chain in a non-blocking manner using the `.ainvoke()` method.
- **Automated Parallelism:** If you have multiple pathways that rely on the same data (for example, fetching information from two different vector databases), LangChain automatically executes them in parallel to reduce latency.

"""ai_utils.py

Utility functions for interacting with AI models to verify LaTeX code.
"""


from openai import OpenAI
from utils.config_utils import get_api_key
from utils.litex_utils import convert_litex_latex

API_KEY = get_api_key()


def generate_prompt(row: dict[str, str]) -> str | None:
    """
    Generate a prompt to verify if the LaTeX code solves the given topic.

    :param row: A dictionary containing 'description' and 'solution' keys.
    :return: A formatted prompt string.
    :raises ValueError: If Litex conversion fails.
    """
    topic = row["description"]
    litex_code = row["solution"]
    try:
        latex_code_converter_result = convert_litex_latex(litex_code)
        if not latex_code_converter_result["success"]:
            return None
    except Exception as e:
        return None
    latex_code = latex_code_converter_result["message"]
    return f"""
You are a knowledgeable assistant skilled in evaluating LaTeX code for mathematical and logical correctness.
For those basic math conceptions, if the LaTeX code is translating the conceptions only, please consider it as solving the topic.
For those obvious math problems, if the LaTeX code is directly providing the final answer or solution to the problem, even it was problem itself, please consider it as solving the topic.
For those easy math algebra problems, if the LaTeX code is solving for a variable or simplifying an expression, please consider it as solving the topic.
For those polynomial transformation or simplification problems, if the LaTeX code is transforming the polynomial to another form, please consider it as solving the topic.

Topic: 
{topic}

LaTeX code:
```
{latex_code}
```

Is the LaTeX code trying to prove or solve the given topic above?
You can answer "Yes" or "No" only. "Yes" means the LaTeX code is indeed trying to prove or solve the topic, while "No" indicates it does not.
    """.strip()


def get_agent_list() -> list[str]:
    """
    Map model names to agent identifiers.

    :param model: Model name string.
    :return: Corresponding agent identifier.
    """
    return ["qwen-max-latest", "qwen-plus-latest", "deepseek-v3.1"]


def ask_agent(info: tuple[str, str]):
    """
    Ask a specific agent (model) to process the prompt.

    :param client: The API client instance.
    :param model: Model name string.
    :param prompt: The prompt string to be processed.
    :return: The agent's response content.
    """
    (model, prompt) = info

    client = OpenAI(
        api_key=API_KEY,
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    )

    completion = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": "You are a knowledgeable assistant skilled in evaluating LaTeX code for mathematical and logical correctness.",
            },
            {"role": "user", "content": prompt},
        ],
    )
    return completion

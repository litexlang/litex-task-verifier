"""ai_utils.py

Utility functions for interacting with AI models to verify LaTeX code.
"""


from openai import OpenAI
from utils.config_utils import get_api_key
from utils.litex_utils import convert_litex_latex

API_KEY = get_api_key()


def generate_prompt(row: dict[str, str]) -> list[dict[str, str]] | None:
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
    prompt = [{"role": "system", "content": "You are a knowledgeable assistant skilled in evaluating LaTeX code for mathematical and logical correctness. You should follow the user's instructions carefully and provide accurate assessments based on the provided LaTeX code and topic. you should answer \"Yes\" or \"No\" only."}]
    prompt.append({"role": "user", "content": "Consider this restrict: You should answer \"Yes\" if the LaTeX code is clearly and unambiguously attempting to describe or solve the given topic."})
    prompt.append({"role": "user", "content": "Consider this restrict: You should answer \"Yes\" if the LaTeX code is using different symbol to describe the vars in the topic, like \"x\", \"y\", \"z\" or other math symbol but still represent the same calculation relationship between numbers and vars."})
    prompt.append({"role": "user", "content": "Consider this restrict: You should answer \"Yes\" if the LaTeX code is translating the conceptions only for those basic math conceptions."})
    prompt.append({"role": "user", "content": "Consider this restrict: You should answer \"Yes\" if the LaTeX code is directly providing the final answer or solution to the problem, even it was problem itself for those obvious math problems. "})
    prompt.append({"role": "user", "content": "Consider this restrict: You should answer \"Yes\" if the LaTeX code is solving for a variable or simplifying an expression for those easy math algebra problems. "})
    prompt.append({"role": "user", "content": "Consider this restrict: You should answer \"Yes\" if the LaTeX code is transforming the polynomial to another form for those polynomial transformation or simplification problems."})
    prompt.append({"role": "user", "content": "Consider this restrict: You must answer \"No\" if the same answer shown both before and after the $\\Rightarrow$ symbol."})

    prompt.append({"role": "user", "content": f"Here is the topic and the LaTeX code:\nTopic:\n{topic}\n\nLaTeX code:\n```\n{latex_code}\n```"})
    prompt.append({"role": "user", "content": "Is the LaTeX code describe the topic? Answer \"Yes\" or \"No\" only."})

    return prompt


def get_agent_list() -> list[str]:
    """
    Map model names to agent identifiers.

    :param model: Model name string.
    :return: Corresponding agent identifier.
    """
    return ["qwen-max-latest", "qwen-plus-latest", "Pro/deepseek-ai/DeepSeek-V3.1"]


def ask_agent(info: tuple[str, list[dict[str, str]]]):
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
        base_url="http://35.220.164.252:3888/v1/",
    )

    completion = client.chat.completions.create(
        model=model,
        messages=prompt, # type: ignore
    )
    return completion

"""verifier.py

Verification utility using multiple LLMs to check if LaTeX code solves a given topic.
"""

from volcenginesdkarkruntime import Ark
from utils.litex_utils import litex_latex_converter
from utils.config_utils import get_api_key
import pylitex


VOLCENGINE_API_KEY = get_api_key()


def _prompt_generator(row: dict[str, str]) -> str:
    """
    Generate a prompt to verify if the LaTeX code solves the given topic.

    :param row: A dictionary containing 'description' and 'solution' keys.
    :return: A formatted prompt string.
    :raises ValueError: If Litex conversion fails.
    """
    topic = row["description"]
    litex_code = row["solution"]
    try:
        latex_code_converter_result = litex_latex_converter(litex_code)
        if not latex_code_converter_result["success"]:
            raise ValueError(
                f"Litex conversion error: {latex_code_converter_result['message']}"
            )
    except Exception as e:
        raise ValueError(f"Error processing Litex code: {e}")
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


def verify_semantic(row: dict[str, str]):
    """
    Verify if the LaTeX code solves the given topic using multiple LLMs.

    :param row: A dictionary containing 'description', 'solution', and 'expect' keys.
    :return: A dictionary with the original data and the verification results.
    """
    prompt = _prompt_generator(row)

    client = Ark(api_key=VOLCENGINE_API_KEY, timeout=1800)
    resp_deepseek_r1 = client.chat.completions.create(
        model="deepseek-r1-250528",
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
    )
    answer_deepseek_r1 = resp_deepseek_r1.choices[0].message.content.strip()  # type: ignore

    resp_kimi = client.chat.completions.create(
        model="kimi-k2-250905",
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
    )
    answer_kimi = resp_kimi.choices[0].message.content.strip()  # type: ignore

    resp_doubao = client.chat.completions.create(
        model="doubao-seed-1-6-thinking-250715",
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
    )
    answer_doubao = resp_doubao.choices[0].message.content.strip()  # type: ignore

    answers = [answer_deepseek_r1, answer_doubao, answer_kimi]
    answer = "Yes" if "Yes" in answers else "No"

    print(
        "Except:",
        row["expect"],
        "\tAnswer:",
        answer,
        "\tDeepseek-R1:",
        answer_deepseek_r1,
        "\tDoubao:",
        answer_doubao,
        "\tKimi:",
        answer_kimi,
    )
    return {
        "title": row["title"],
        "description": row["description"],
        "solution": row["solution"],
        "collaboration_title": row["collaboration_title"],
        "expect": row["expect"],
        "actual": answer,
        "deepseek_r1": answer_deepseek_r1,
        "doubao": answer_doubao,
        "kimi": answer_kimi,
    }


def verify_grammar(row: dict[str, str]):
    """
    Verify if the LaTeX code is grammatically correct.

    :param row: A dictionary containing 'description' and 'solution' keys.
    :return: A dictionary with the original data and the grammar verification results.
    """
    result = pylitex.run(row["solution"])
    return {
        "title": row["title"],
        "description": row["description"],
        "solution": row["solution"],
        "collaboration_title": row["collaboration_title"],
        "output": result["message"],
        "success": result["success"],
    }

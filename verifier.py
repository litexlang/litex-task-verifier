"""verifier.py

Functions to verify LaTeX code against given topics and check for grammatical correctness.
"""

from utils.ai_utils import ask_agent, generate_prompt, get_agent_list
import pylitex

VOTING_ROUND = 2


def verify_semantic(row: dict[str, str]):
    """
    Verify if the Litex code solves the given topic using multiple LLMs.

    :param row: A dictionary containing 'description', 'solution', and 'expect' keys.
    :return: A dictionary with the original data and the verification results.
    """
    prompt = generate_prompt(row)
    if prompt is None:
        return {
            "title": row["title"],
            "description": row["description"],
            "solution": row["solution"],
            "collaboration_title": row["collaboration_title"],
            "expect": row["expect"],
            "actual": "No",
        }

    else:
        results = []
        for i in range(VOTING_ROUND):  # Two rounds of voting
            for model in get_agent_list():
                result = ask_agent((model, prompt))
                results.append(result)

        answers = [result.choices[0].message.content for result in results]  # type: ignore
        answer = "Yes" if "Yes" in answers else "No"

        print(
            "Except:",
            row["expect"],
            "\tAnswers:",
            answers,
            "\tAnswer:",
            answer,
        )
        return {
            "title": row["title"],
            "description": row["description"],
            "solution": row["solution"],
            "collaboration_title": row["collaboration_title"],
            "expect": row["expect"],
            "actual": answer,
        }


def verify_grammar(row: dict[str, str]):
    """
    Verify if the Litex code is grammatically correct.

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

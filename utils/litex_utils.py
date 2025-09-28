"""litex_utils.py

Utilities for interacting with Litex, including converting Litex code to LaTeX format.
"""

import re
import subprocess
import pylitex


LITEX_PATH = "litex"  # Adjust if litex is not in PATH


def extract_document_content(tex: str) -> str | None:
    """
    Return the content between \\begin{claim} and \\begin{proof}.

    :param tex: The full LaTeX claim as a string.
    :return: The content inside the document environment, or None if not found.
    """
    pattern = re.compile(r"\\begin\{claim\}(.*?)\\begin\{proof\}", re.DOTALL)
    m = pattern.search(tex)
    if not m:
        return None
    return m.group(1).strip()


def convert_litex_latex(litex_code: str) -> dict:
    """
    Convert a Litex file to LaTeX format using the Litex Core.

    :param litex_code: The Litex code as a string.
    :return: The LaTeX formatted string.
    """

    try:
        result = pylitex.convert_to_latex(litex_code.replace("\r\n", "\n"))
        claim_content = extract_document_content(result["message"])
        if claim_content is not None:
            return {"success": True, "message": (result["message"])}
        else:
            return {
                "success": False,
                "message": "No claim environment found in the LaTeX output.",
            }
    except subprocess.CalledProcessError as e:
        return {"success": False, "message": e.stderr}
    except FileNotFoundError:
        return {
            "success": False,
            "message": "Litex command not found. Please ensure Litex is installed and in your PATH.",
        }

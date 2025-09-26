"""litex_utils.py

Utilities for interacting with Litex, including converting Litex code to LaTeX format.
"""

from utils.tmp_hasher import store_string
import re
import subprocess


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

    :param litex_file_path: Path to the Litex file.
    :return: The LaTeX formatted string.
    """
    file_path = store_string(litex_code, prefix="litex_", suffix=".lix")

    try:
        result = subprocess.run(
            [LITEX_PATH, "-latex", file_path],
            capture_output=True,
            text=True,
            check=True,
        )
        claim_content = extract_document_content(result.stdout)
        if claim_content is not None:
            return {"success": True, "message": (result.stdout)}
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

"""litex_utils.py

Utilities for interacting with Litex, including converting Litex code to LaTeX format.
"""

from utils.tmp_hasher import store_string
import re
import subprocess


LITEX_PATH = "litex"  # Adjust if litex is not in PATH


def extract_document_content(tex: str) -> str:
    """
    Return the content between \\begin{document} and \\end{document}.

    This uses a non-greedy DOTALL regex and strips leading/trailing whitespace.
    Raises ValueError if no document environment is found.

    :param tex: The full LaTeX document as a string.
    :return: The content inside the document environment.
    :raises ValueError: If no document environment is found.
    """
    pattern = re.compile(r"\\begin\{document\}(.*?)\\end\{document\}", re.DOTALL)
    m = pattern.search(tex)
    if not m:
        raise ValueError("No document environment found")
    return m.group(1).strip()


def litex_latex_converter(litex_code: str) -> dict:
    """
    Convert a Litex file to LaTeX format using the Litex REPL.

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
        return {"success": True, "message": extract_document_content(result.stdout)}
    except subprocess.CalledProcessError as e:
        return {"success": False, "message": e.stderr}
    except FileNotFoundError:
        return {
            "success": False,
            "message": "Litex command not found. Please ensure Litex is installed and in your PATH.",
        }

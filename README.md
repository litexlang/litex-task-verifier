# Litex Task Verifier

A comprehensive Python utility for verifying Litex code solutions through dual verification modes: semantic analysis using multiple Large Language Models (LLMs) with enhanced dual-round voting, and grammar validation using pylitex.

## Overview

This tool provides two verification approaches: (1) **Semantic Verification** - converts Litex code to LaTeX and uses multiple AI models (Qwen Max, Qwen Plus, and DeepSeek V3.1) to evaluate whether the mathematical expressions correctly solve given problems, employing dual-round voting for enhanced reliability; (2) **Grammar Verification** - validates Litex syntax correctness using pylitex compilation.

## Features

- **Multi-LLM Verification**: Uses three different AI models for robust evaluation
- **Dual Verification Modes**: Semantic verification (content correctness) and grammar verification (syntax correctness)
- **Litex to LaTeX Conversion**: Automatically converts Litex code to LaTeX format
- **Grammar Checking**: Built-in Litex grammar verification using pylitex
- **Dual-Round Voting**: Enhanced reliability through 6-vote system (2 rounds × 3 models)
- **Batch Processing**: Supports processing multiple test cases via CSV files
- **Multiprocessing**: Parallel processing for improved performance
- **Configuration Management**: JSON-based configuration for API keys and settings

## Project Structure

```
litex-task-verifier/
├── README.md
├── requirements.txt         # Python dependencies
├── verifier.py              # Main verification logic
├── config.json.template     # Template for configuration
├── test/
│   ├── benchmark_test.py   # Benchmark testing script
│   ├── test.csv            # Test data input
│   └── test_with_results.csv # Test results output
├── utils/
│   ├── ai_utils.py         # AI model interaction utilities
│   ├── config_utils.py     # Configuration utilities
│   ├── csv_utils.py        # CSV handling utilities
│   ├── litex_utils.py      # Litex processing utilities
│   └── tmp_hasher.py       # Temporary file hashing
└── config.json              # Configuration file (created after setup)
```

## Installation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/litexlang/litex-task-verifier.git
   cd litex-task-verifier
   ```

2. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

   The required dependencies are:

   - `openai` (for AI model access)
   - `pylitex >= 0.2.0` (for Litex grammar verification and LaTeX conversion)

3. **Configure API access**:
   ```bash
   cp config.json.template config.json
   # Edit config.json and add your API key
   ```

## Configuration

Create a `config.json` file in the project root:

```json
{
  "api_key": "your_api_key_here"
}
```

**Note**: The `config.json` file is ignored by git to protect your API keys.

## Usage

### Basic Verification

```python
from verifier import verify_semantic, verify_grammar

# Test data format
test_data = {
    "title": "Problem Title",
    "description": "Mathematical problem description",
    "solution": "claim:\n    forall a, b R:\n        a + b = b + a\n    prove:\n        a + b = b + a",
    "collaboration_title": "Collaboration info",
    "expect": "TRUE"  # Expected result
}

# Semantic verification (checks if solution addresses the problem)
semantic_result = verify_semantic(test_data)
print("Semantic verification:", semantic_result)
# Returns: {'title': '...', 'description': '...', 'solution': '...', 
#          'collaboration_title': '...', 'expect': '...', 'actual': 'Yes'}

# Grammar verification (checks Litex syntax correctness)
grammar_result = verify_grammar(test_data)
print("Grammar verification:", grammar_result)
# Returns: {'title': '...', 'description': '...', 'solution': '...', 
#          'collaboration_title': '...', 'output': '...', 'success': True}
```

**Note**: If Litex to LaTeX conversion fails during semantic verification, the function returns `"No"` for the `actual` field to handle invalid syntax gracefully.

### Batch Processing

```bash
# Process CSV file with test cases
python test/benchmark_test.py
```

Or use it programmatically:

```python
import multiprocessing as mp
from utils.csv_utils import load_csv_dicts, export_csv_dicts
from verifier import verify_semantic, verify_grammar

# Load test data
test_data = load_csv_dicts("test/test.csv")

# Semantic verification with multiprocessing
with mp.Pool(processes=40) as pool:
    semantic_results = pool.map(verify_semantic, test_data)

# Grammar verification with multiprocessing  
with mp.Pool(processes=40) as pool:
    grammar_results = pool.map(verify_grammar, test_data)

# Export results
export_csv_dicts("test/test_with_results.csv", results, write_mode="w")
```

### Running Benchmark Tests

To run the benchmark test and see detailed performance metrics:

```bash
python test/benchmark_test.py
```

This will:

- Process all test cases in `test/test.csv`
- Generate results in `test/test_with_results.csv`
- Display detailed performance metrics and missed cases
- Show overall system accuracy

### CSV Input Format

Your input CSV should contain these columns:

- `title`: Problem title
- `description`: Problem description
- `solution`: Litex code solution
- `collaboration_title`: Additional context
- `expect`: Expected verification result ("TRUE" or "FALSE")

### Output Format

#### Semantic Verification (`verify_semantic`)
Returns a dictionary with:
- All original input fields
- `actual`: Final verification result ("Yes" or "No")

#### Grammar Verification (`verify_grammar`)
Returns a dictionary with:
- All original input fields
- `output`: Litex compilation output/error messages
- `success`: Boolean indicating if Litex code compiled successfully

## API Models Used

- **Qwen Max**: `qwen-max-latest`
- **Qwen Plus**: `qwen-plus-latest`  
- **DeepSeek V3.1**: `deepseek-v3.1`

### Voting Mechanism

The tool uses an enhanced dual-round voting system where:

- Each of the 3 models is queried twice (2 rounds), generating 6 total responses
- Each model provides a "Yes" or "No" answer per round
- If any of the 6 responses is "Yes", the final result is "Yes"
- Only if all 6 responses are "No", the final result is "No"
- This approach favors inclusion and significantly reduces false negatives
- The dual-round system improves reliability by accounting for model response variability

## Utilities

### Verification Functions (`verifier.py`)

```python
from verifier import verify_semantic, verify_grammar

# Semantic verification - checks if Litex code solves the given problem
result = verify_semantic(test_data)

# Grammar verification - checks if Litex code is syntactically correct
result = verify_grammar(test_data)
```

### Configuration Utils (`utils/config_utils.py`)

```python
from utils.config_utils import load_config, get_api_key

# Load configuration
config = load_config()

# Get API key
api_key = get_api_key()

# Custom config file
custom_config = load_config("custom_config.json")
```

### CSV Utils (`utils/csv_utils.py`)

```python
from utils.csv_utils import load_csv_dicts, export_csv_dicts

# Load CSV data
data = load_csv_dicts("input.csv")

# Export results
export_csv_dicts("output.csv", results, write_mode="w")
```

### Litex Utils (`utils/litex_utils.py`)

```python
from utils.litex_utils import convert_litex_latex, extract_document_content

# Convert Litex code to LaTeX using pylitex
result = convert_litex_latex(litex_code)
# Returns: {"success": True, "message": "latex_output"} or {"success": False, "message": "error"}

# Extract claim content from LaTeX
claim_content = extract_document_content(latex_tex)
# Returns the content between \begin{claim} and \begin{proof}
```

## Benchmark Results

The tool has been extensively tested on a dataset of 449 test cases (360 positive cases expecting "TRUE" and 89 negative cases expecting "FALSE"). Here are the performance metrics:

### Overall System Performance

- **True Positive Rate**: 356/360 = 98.89% (correctly identified valid solutions)
- **True Negative Rate**: 89/89 = 100% (correctly identified invalid solutions)  
- **False Negative Rate**: 4/360 = 1.11% (missed valid solutions)
- **False Positive Rate**: 0/89 = 0% (no false positives)
- **Overall Accuracy**: 445/449 = 99.11%

### Key Insights

- The **dual-round voting system significantly improves accuracy** compared to single-round approaches
- **Perfect specificity**: No false positives across the combined system
- **Enhanced robustness**: Dual-round voting reduces model response variability impact
- **Combined system achieves 99.11% accuracy**, demonstrating excellent performance
- The system maintains its conservative approach, preferring to miss some valid solutions rather than approve invalid ones
- **Improved false negative rate**: Reduced to 1.11% with dual-round voting

### Missed Cases Analysis

The system missed 4 true positive cases:
- inequality antisymmetry
- multiplication sign rules negative × negative = positive
- mixed number conversion
- Non-Negative Subtraction

These cases represent edge cases in mathematical reasoning that require further prompt engineering.

## Performance

The tool supports multiprocessing for batch operations:

```python
import multiprocessing as mp

with mp.Pool(processes=40) as pool:
    results = pool.map(verify_semantic, test_cases)
```

## Error Handling

The verifier includes comprehensive error handling for:

- Litex to LaTeX conversion failures using `pylitex.convert_to_latex()`
- Missing or invalid claim environments in LaTeX output
- API communication errors
- Configuration file issues
- Invalid input data
- Subprocess errors and file system issues
- Improved exception handling with graceful error recovery

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

No License now.

## Support

For issues and questions, please open an issue on GitHub or contact the development team.

## Changelog

### Recent Updates

- **Enhanced Dual-Round Voting**: Implemented 2-round voting system for improved reliability (6 total votes)
- **Improved Accuracy**: Achieved 99.11% overall accuracy with enhanced voting mechanism
- **Model Update**: Transitioned to Qwen Max, Qwen Plus, and DeepSeek V3.1 for optimal performance
- **Pylitex Integration**: Updated to use `pylitex >= 0.2.0` for improved Litex to LaTeX conversion
- **Enhanced Error Handling**: Improved conversion failure handling with claim environment validation
- **Reduced False Negatives**: Decreased false negative rate to 1.11%
- **Configuration Simplification**: Streamlined config.json structure with unified API key field
- **Multiprocessing Optimization**: Fixed multiprocessing issues for stable parallel processing
- **Comprehensive Testing**: Added detailed benchmark analysis with missed case reporting
- **Litex Utils Enhancement**: Added `extract_document_content()` for better LaTeX processing

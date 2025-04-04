from typing import List, Dict, Any
import json

def get_code_analyzer_prompt(user_input: str) -> str:
    return f"""
You are a specialized code requirements analyzer. Your job is to analyze user requests for code generation
and output a structured JSON specification that will be used by a code generator.

Parse the following user request and provide a JSON output with these fields:
- task_type: The general programming task (e.g., "data_processing", "web_scraping", "api_integration", etc.)
- language: The programming language to use
- libraries: List of suggested libraries needed
- inputs: Expected inputs and their data types
- outputs: Expected outputs and their data types
- requirements: List of specific requirements to implement
- edge_cases: Edge cases to consider in the implementation
- code_structure: Suggested code structure (classes, functions, etc.)

USER REQUEST: {user_input}

Output your analysis as a valid JSON object only, without any commentary:
"""


def get_code_generator_prompt(analysis: Dict[str, Any]) -> str:
    return f"""
You are an expert code generator. Based on the following analysis, write clean, efficient, 
and well-documented code that meets all the specified requirements.

REQUIREMENTS:
```json
{json.dumps(analysis, indent=2)}
```

INSTRUCTIONS:
1. Use {analysis.get('language', 'Python')} as the programming language.
2. Include proper error handling and input validation.
3. Add comprehensive documentation and comments.
4. Follow best practices for {analysis.get('language', 'Python')} code style.
5. Consider all specified edge cases.

Begin your response with only the code - do not include any other explanations before the code itself.
"""

def get_human_eval_analyzer_prompt(x: Dict[str, Any]) -> str:
    entry_point = x["entry_point"]
    prompt = x["prompt"]
    return f"""
You are a specialized code requirements analyzer. Analyze the following Python function '{entry_point}' and provide a structured JSON specification.

FUNCTION TO IMPLEMENT:
{prompt}

ENTRY POINT: {entry_point}

Provide a JSON output with these fields:
- task_type: The type of programming task
- entry_point: The name of the function to implement ('{entry_point}')
- inputs: Expected inputs and their data types (from function signature)
- outputs: Expected output and its data type (from function signature)
- requirements: List of specific requirements extracted from the docstring
- examples: List of example inputs and outputs from the docstring
- edge_cases: Edge cases to consider based on the function description
- validation_needs: Input validation requirements

Output your analysis as a valid JSON object only, without any commentary:
"""

def get_human_eval_generator_prompt(user_input: Dict[str, Any], analysis: Dict[str, Any]) -> str:
    entry_point = user_input["entry_point"]
    prompt = user_input["prompt"]
    return f"""
You are an expert Python programmer. Implement the function '{entry_point}'.
Only output the function body with proper indentation. Do not include the function definition or docstring.

ENTRY POINT: {entry_point}

FUNCTION TO IMPLEMENT:
{prompt}

ANALYSIS:
```json
{json.dumps(analysis, indent=2)}
```

Requirements:
1. Implement the function body for '{entry_point}'
2. Use proper indentation (4 spaces)
3. Do not include the function definition or docstring
4. Do not include any explanations or comments
5. Follow the function signature exactly
6. Handle all edge cases from the analysis
7. Implement the logic that satisfies all examples in the docstring

Begin your response with only the implementation:
"""

def get_mbpp_analyzer_prompt(x: Dict[str, Any]) -> str:
    problem = x["text"]
    
    return f"""
You are a specialized code requirements analyzer. Analyze the following Python programming problem and provide a structured JSON specification.

PROBLEM STATEMENT:
{problem}

Provide a JSON output with these fields:
- task_type: The type of programming task
- inputs: Expected inputs and their data types based on the problem statement
- outputs: Expected output and its data type based on the problem statement
- requirements: List of specific requirements extracted from the problem statement
- examples: List of example test cases and expected outputs
- edge_cases: Edge cases to consider based on the problem description
- validation_needs: Input validation requirements
- function_signature: Suggested function signature (name, parameters)

Output your analysis as a valid JSON object only, without any commentary:
"""

def get_mbpp_generator_prompt(user_input: Dict[str, Any], analysis: Dict[str, Any]) -> str:
    problem = user_input["text"]
    
    return f"""
You are an expert Python programmer. Implement a solution to the following programming problem.
The solution should be a complete Python function that passes all the test cases.

PROBLEM STATEMENT:
{problem}

ANALYSIS:
```json
{json.dumps(analysis, indent=2)}
```

Requirements:
1. Implement a complete Python function that solves the problem
2. Use proper indentation (4 spaces)
3. Make sure your solution passes all the provided test cases
4. Handle all edge cases identified in the analysis
5. Follow best practices for Python coding style
6. Use appropriate function signature as suggested in the analysis

Begin your response with only the implementation:
"""

def get_ds1000_analyzer_prompt(x) -> str:
    """
    Create a prompt for analyzing DS1000 problems.
    
    DS1000 is a benchmark for data science code generation with 
    problems from libraries like Pandas, Numpy, Matplotlib, etc.
    """

    return f"""
You are a specialized data science code analyzer. Analyze the following data science programming problem and provide a structured JSON specification.

PROBLEM STATEMENT:
{x}



Provide a JSON output with these fields:
- task_type: The type of data science task (e.g., "data_manipulation", "visualization", "statistics", etc.)
- library: Main library being used (e.g., "pandas", "numpy", "matplotlib", etc.)
- inputs: Available variables and their data types from the code context
- outputs: Expected output and its data type based on the problem statement
- requirements: List of specific requirements extracted from the problem statement
- constraints: Any constraints or specific conditions that must be met
- domain_knowledge: Relevant data science concepts needed to solve this problem
- solution_approach: High-level approach to solving the problem

Output your analysis as a valid JSON object only, without any commentary:
"""

def get_ds1000_generator_prompt(user_input:str, analysis ) -> str:
    """
    Create a prompt for generating code solutions for DS1000 problems 
    based on the analysis.
    """
    return f"""
You are an expert data science programmer. Implement a solution to the following data science problem.
Your solution should integrate with the provided code context.

PROBLEM STATEMENT:
{user_input}

ANALYSIS:
{analysis}

Requirements:
1. Implement a complete solution that addresses the problem
2. Your code must work within the given code context - do not modify existing variables
3. Follow the conventions of the main library included in the library section of the analysis
4. Use efficient and idiomatic approaches specific to the library
5. Ensure your solution handles all specified requirements
6. Comment your code to explain complex operations
7. Focus on readability and maintainability

Begin your response with only the implementation (code that should be inserted at the position indicated in the problem):
"""
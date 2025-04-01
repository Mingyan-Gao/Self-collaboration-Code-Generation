#!/usr/bin/env python
import json
import gzip
import concurrent.futures
import argparse
from tqdm import tqdm

# Import the self collaboration framework's session and roles.
from session import Session
from roles.rule_descriptions_actc import TEAM, ANALYST, PYTHON_DEVELOPER, TESTER

# The system prompt from ds1000_direct_gemini.
SYSTEM_PROMPT = (
    "Write a short code following the given format and indentation. "
    "Place the executable code between <code> and </code> tags, without any other non-executable things."
)

def main():
    parser = argparse.ArgumentParser(
        description="Run self collaboration framework on ds1000 dataset, combining the system prompt with each task prompt."
    )
    parser.add_argument(
        '--dataset_path',
        type=str,
        default='data/ds1000.jsonl.gz',
        help='Path to the ds1000 dataset file (gzip JSONL format)'
    )
    parser.add_argument(
        '--output_path',
        type=str,
        default='data/selfcol-{model}-ds1000-answers.jsonl',
        help='Output file path pattern (use {model} to include the model name)'
    )
    parser.add_argument('--model', type=str, default='gemini-2.0-flash')
    parser.add_argument('--max_round', type=int, default=2)
    parser.add_argument('--max_tokens', type=int, default=1024)
    parser.add_argument('--majority', type=int, default=1)
    parser.add_argument('--temperature', type=float, default=0.0)
    parser.add_argument('--top_p', type=float, default=0.95)
    args = parser.parse_args()

    # Load the ds1000 dataset (each line is a JSON record)
    with gzip.open(args.dataset_path, 'rt') as f:
        ds1000 = [json.loads(line) for line in f]

    responses = []

    def process_problem(problem):
        problem_id = int(problem['metadata']['problem_id'])
        prompt = problem['prompt']
        # Combine the system prompt with the original prompt for the session.
        full_requirement = SYSTEM_PROMPT + "\n" + prompt
        try:
            session = Session(
                TEAM, ANALYST, PYTHON_DEVELOPER, TESTER,
                requirement=full_requirement,
                model=args.model,
                majority=args.majority,
                max_tokens=args.max_tokens,
                temperature=args.temperature,
                top_p=args.top_p,
                max_round=args.max_round,
                before_func="",  # No additional pre-processing for ds1000
                task_id=problem_id
            )
            # Run the self collaboration framework.
            code, session_history = session.run_analyst_coder()
        except Exception as e:
            print(f"Task {problem_id} failed: {e}")
            code = "error"
        # Return output matching the ds1000_direct_gemini.py format.
        return {'id': problem_id, 'code': code, 'metadata': problem['metadata']}

    # Process problems concurrently.
    with concurrent.futures.ThreadPoolExecutor(max_workers=32) as executor:
        futures = [executor.submit(process_problem, p) for p in ds1000]
        for future in tqdm(concurrent.futures.as_completed(futures), total=len(futures)):
            responses.append(future.result())

    # Sort responses by problem id.
    responses.sort(key=lambda x: x['id'])
    # Format output filename (if pattern includes {model}).
    output_filename = args.output_path.format(model=args.model) if '{model}' in args.output_path else args.output_path

    # Write out each response as a JSON line.
    with open(output_filename, 'w') as f:
        for resp in responses:
            f.write(json.dumps(resp) + "\n")

if __name__ == "__main__":
    main()

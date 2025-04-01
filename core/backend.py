import openai
from openai import OpenAI
import time
import os
import google.generativeai as genai



def call_chatgpt(prompt, model='code-davinci-002', stop=None, temperature=0., top_p=1.0,
        max_tokens=128, echo=False, majority_at=None):
    
    client = OpenAI()
    num_completions = majority_at if majority_at is not None else 1
    num_completions_batch_size = 10

    completions = []
    for i in range(20 * (num_completions // num_completions_batch_size + 1)):
        try:
            requested_completions = min(num_completions_batch_size, num_completions - len(completions))

            response = client.chat.completions.create(
            model=model,
            messages=prompt,
            max_tokens=max_tokens,
            temperature=temperature,
            top_p=top_p,
            n=requested_completions
            )
            completions.extend([choice.message.content for choice in response.choices])
            if len(completions) >= num_completions:
                return completions[:num_completions]
        except openai.RateLimitError as e:
            time.sleep(min(i**2, 60))
    raise RuntimeError('Failed to call GPT API')

def call_gemini(prompt, model='gemini-2.0-flash', stop=None, temperature=0.5,top_p=1.0, max_tokens=128, echo=False, majority_at=None):

    genai.configure(api_key="") #Replace with your api key.

    model_genai = genai.GenerativeModel(model)

    num_completions = majority_at if majority_at is not None else 1
    completions = []

    for i in range(20 * num_completions):  # Attempt up to 20 times for retries
        try:
            for _ in range(num_completions):
                response = model_genai.generate_content(
                    contents=prompt,
                    generation_config=genai.GenerationConfig(
                        temperature=temperature,
                        top_p=top_p,
                        max_output_tokens=max_tokens,
                    ),
                )
                completions.append(response.text)

            return completions[:num_completions] #Return the correct number of completions.

        except Exception as e: # Catch all exceptions, including rate limit errors.
            print(f"Error calling Gemini API: {e}")
            time.sleep(min(i**2, 60)) # Exponential backoff with a maximum of 60 seconds.

    raise RuntimeError('Failed to call Gemini API after multiple retries.')
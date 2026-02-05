import os
import google.generativeai as genai
import instructor
from .models import GeneratedProject
from .prompts import SYSTEM_PROMPTS, DEFAULT_SYSTEM_PROMPT
from dotenv import load_dotenv

load_dotenv()

def get_gemini_client():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY environment variable is not set.")
    
    genai.configure(api_key=api_key)
    # Using instructor with Gemini provider
    return instructor.from_gemini(
        client=genai.GenerativeModel(
            model_name="gemini-2.5-flash",
        ),
        mode=instructor.Mode.GEMINI_JSON,
    )

def generate_project_code(selected_features: list[str]) -> GeneratedProject:
    client = get_gemini_client()
    
    feature_prompts = []
    for feature in selected_features:
        prompt = SYSTEM_PROMPTS.get(feature, f"Implement the feature: {feature}")
        feature_prompts.append(f"- {feature}: {prompt}")
    
    user_content = "Please generate the code for the following features:\n" + "\n".join(feature_prompts)
    
    response = client.chat.completions.create(
        messages=[
            {"role": "system", "content": DEFAULT_SYSTEM_PROMPT},
            {"role": "user", "content": user_content}
        ],
        response_model=GeneratedProject,
    )
    
    return response

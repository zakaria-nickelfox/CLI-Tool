import os
import json
from pathlib import Path
from typing import Dict

# Paths
RULES_FILE = Path(__file__).parent / "rules.json"

# Default fallbacks in case rules.json is missing or corrupt
DEFAULT_SYSTEM_PROMPT_FALLBACK = (
    "You are an expert Django architect. Your goal is to generate a professional, production-ready "
    "Django project structure based on selected features. All code must be Python/Django."
)

SYSTEM_PROMPTS_FALLBACK = {
    "Mail services": "Implement a Django mail service.",
    "Notification": "Implement a notification system for Django.",
    "RBAC": "Implement RBAC in Django.",
    "Upload documents": "Implement file upload in Django.",
    "Error handling (global)": "Implement global error handling.",
    "Logging system(mail,database,file)": "Configure a robust logging system."
}

def load_rules():
    if not RULES_FILE.exists():
        return DEFAULT_SYSTEM_PROMPT_FALLBACK, SYSTEM_PROMPTS_FALLBACK
    
    try:
        with open(RULES_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            
            default_prompt = data.get("default_system_prompt", DEFAULT_SYSTEM_PROMPT_FALLBACK)
            
            # Extract prompts and flows for each feature
            feature_data = data.get("features", {})
            refined_prompts = {}
            for name, details in feature_data.items():
                prompt_text = details.get("prompt", "")
                flow_text = details.get("flow", "")
                # Combine prompt and flow for the AI
                combined = f"{prompt_text}\nExpected Flow:\n{flow_text}" if flow_text else prompt_text
                refined_prompts[name] = combined
                
            return default_prompt, refined_prompts
    except Exception as e:
        print(f"Warning: Could not load {RULES_FILE}, using defaults. Error: {e}")
        return DEFAULT_SYSTEM_PROMPT_FALLBACK, SYSTEM_PROMPTS_FALLBACK

# Load them once or dynamically - let's export them as properties for compatibility
DEFAULT_SYSTEM_PROMPT, SYSTEM_PROMPTS = load_rules()

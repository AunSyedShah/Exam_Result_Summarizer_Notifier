#!/usr/bin/env python3
"""
Test script to verify Hugging Face LLM integration.
Run this to test if your HF API key and model selection work correctly.
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_hf_integration():
    """Test Hugging Face API integration."""
    
    print("=" * 60)
    print("🧪 Hugging Face LLM Integration Test")
    print("=" * 60)
    
    # Check API key
    api_key = os.getenv('HF_API_KEY', '')
    print(f"\n1️⃣  HF_API_KEY: {'✅ Set' if api_key else '❌ Not set (will use mock feedback)'}")
    if api_key:
        masked_key = api_key[:20] + '...' if len(api_key) > 20 else api_key
        print(f"   Key: {masked_key}")
    
    # Check model selection
    model_choice = os.getenv('HF_MODEL', 'mistral').lower()
    print(f"\n2️⃣  HF_MODEL: {model_choice}")
    
    available_models = {
        'llama-3.3': 'meta-llama/Llama-3.3-70B-Instruct',
        'mistral': 'mistralai/Mistral-7B-Instruct-v0.2',
        'zephyr': 'HuggingFaceH4/zephyr-7b-beta',
        'deepseek-r1': 'deepseek-ai/DeepSeek-R1',
        'flan-t5': 'google/flan-t5-base',
    }
    
    if model_choice in available_models:
        print(f"   ✅ Model: {available_models[model_choice]}")
    else:
        print(f"   ❌ Unknown model: {model_choice}")
        print(f"   Available: {', '.join(available_models.keys())}")
        return False
    
    # Test import
    print(f"\n3️⃣  Testing imports...")
    try:
        from huggingface_hub import InferenceClient
        print("   ✅ huggingface_hub imported successfully")
    except ImportError as e:
        print(f"   ❌ Failed to import huggingface_hub: {e}")
        print("   Run: uv sync")
        return False
    
    # Test LLM service
    print(f"\n4️⃣  Testing LLM Service...")
    try:
        sys.path.insert(0, os.path.dirname(__file__))
        from app.services.llm_service import get_llm_service
        
        service = get_llm_service()
        print(f"   ✅ LLM Service initialized")
        
        # Try generating feedback
        if not service.use_mock and api_key:
            print(f"\n5️⃣  Generating test feedback with {model_choice}...")
            feedback = service.generate_feedback(
                student_name="Test Student",
                marks=85,
                category="Distinction",
                course="Python Programming"
            )
            print(f"   ✅ Generated feedback:")
            print(f"   '{feedback}'")
            return True
        else:
            print(f"\n5️⃣  Using mock feedback (API key not set)")
            feedback = service.generate_feedback(
                student_name="Test Student",
                marks=85,
                category="Distinction",
                course="Python Programming"
            )
            print(f"   ✅ Generated mock feedback:")
            print(f"   '{feedback}'")
            print(f"\n   💡 Hint: Set HF_API_KEY in .env to use real AI feedback!")
            return True
            
    except Exception as e:
        print(f"   ❌ Error: {str(e)[:200]}")
        import traceback
        traceback.print_exc()
        return False
    
    print("\n" + "=" * 60)
    print("✅ All tests passed! Your setup is ready.")
    print("=" * 60)
    return True

if __name__ == "__main__":
    success = test_hf_integration()
    sys.exit(0 if success else 1)

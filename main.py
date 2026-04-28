import os
from app import create_app

def main():
    """Initialize and run Flask application."""
    app = create_app()
    
    # Create uploads directory if it doesn't exist
    os.makedirs(os.path.join(os.path.dirname(__file__), 'uploads'), exist_ok=True)
    
    # Run Flask app
    print("\n" + "=" * 70)
    print("🚀 EXAM RESULT SUMMARIZER + NOTIFIER")
    print("=" * 70)
    print("📍 Open http://localhost:5000 in your browser")
    print("\n🔐 Demo Login:")
    print("   Admin:  admin / admin123")
    print("   Faculty: faculty / faculty123")
    print("\n📋 Quick Start:")
    print("   1. Upload exam results (CSV/Excel)")
    print("   2. View dashboard with statistics")
    print("   3. Generate AI feedback (if HF_API_KEY set)")
    print("   4. Send email notifications")
    print("\n🤖 LLM Status:")
    api_key = os.getenv('HF_API_KEY', '')
    model = os.getenv('HF_MODEL', 'mistral')
    if api_key:
        print(f"   ✅ Hugging Face enabled (Model: {model})")
        print("   📚 See HF_SETUP_GUIDE.md for model details")
    else:
        print("   ℹ️  Using mock feedback (no HF_API_KEY)")
        print("   💡 Set HF_API_KEY in .env to enable AI feedback")
        print("   📚 See HF_SETUP_GUIDE.md for setup instructions")
    print("\n📚 Documentation:")
    print("   README.md - Full project documentation")
    print("   HF_SETUP_GUIDE.md - Hugging Face API setup")
    print("   test_llm.py - Test your LLM configuration")
    print("\n" + "=" * 70)
    
    app.run(debug=True, host='0.0.0.0', port=5000)


if __name__ == "__main__":
    main()


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Test script to verify Gemini API key and available models
"""
import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()

def test_gemini_api():
    api_key = os.getenv('GEMINI_API_KEY')
    model_name = os.getenv('GEMINI_MODEL', 'gemini-1.5-flash')

    if not api_key:
        print("❌ No GEMINI_API_KEY found in environment variables")
        return False

    print(f"✅ API Key loaded: {api_key[:20]}...")
    print(f"🎯 Target model: {model_name}")

    try:
        # Configure the API
        genai.configure(api_key=api_key)
        print("✅ API configured successfully")

        # Test the specified model
        print(f"🔄 Testing specified model: {model_name}...")
        try:
            test_model = genai.GenerativeModel(model_name)
            response = test_model.generate_content("Say 'Hello World' in exactly 2 words.")
            print(f"✅ Model '{model_name}' test successful: {response.text.strip()}")
        except Exception as model_test_e:
            print(f"⚠️  Specified model '{model_name}' failed: {model_test_e}")
            print("🔄 Trying fallback models...")
            
            # Try fallback models
            fallback_models = ['gemini-1.5-flash', 'gemini-pro', 'gemini-1.5-pro']
            working_model = None
            
            for fallback in fallback_models:
                try:
                    test_model = genai.GenerativeModel(fallback)
                    response = test_model.generate_content("Test")
                    working_model = fallback
                    print(f"✅ Fallback model '{fallback}' works")
                    break
                except:
                    continue
            
            if working_model:
                print(f"💡 Consider using: GEMINI_MODEL={working_model}")
            else:
                print("❌ No working models found")
                return False

        # List available models
        print("🔄 Listing available models...")
        models = list(genai.list_models())
        print(f"📋 Total models found: {len(models)}")

        # Filter models that support generateContent
        content_models = [m for m in models if 'generateContent' in m.supported_generation_methods]
        print(f"🤖 Models supporting generateContent: {len(content_models)}")

        print("\n📝 Available Gemini models:")
        for i, model in enumerate(content_models[:5]):  # Show first 5
            model_name = model.name.split('/')[-1]
            print(f"  {i+1}. {model_name}")

        print(f"\n🎉 SUCCESS: Gemini API is working with model: {model_name}")
        return True

    except Exception as e:
        print(f"❌ API Error: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Testing Gemini API Key and Models")
    print("=" * 40)

    success = test_gemini_api()

    if not success:
        print("\n🔧 Troubleshooting:")
        print("1. Check your API key at: https://makersuite.google.com/app/apikey")
        print("2. Make sure your .env file has: GEMINI_API_KEY=your_key_here")
        print("3. Verify your Google Cloud project has Gemini API enabled")
        print("4. Check if you have API quota remaining")
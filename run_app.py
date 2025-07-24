#!/usr/bin/env python3
"""Script to run the Streamlit chatbot app."""

import subprocess
import sys
import os

def main():
    """Run the Streamlit app."""
    # Check if .env file exists
    if not os.path.exists('.env'):
        print("⚠️  Warning: .env file not found!")
        print("Make sure you have GOOGLE_AI_API_KEY set in your .env file")
        print("Example .env content:")
        print("GOOGLE_AI_API_KEY=your_api_key_here")
        return
    
    print("🚀 Starting Vietnamese Tax Law Chatbot...")
    print("📱 The app will open in your browser automatically")
    print("🛑 Press Ctrl+C to stop the server")
    print("-" * 50)
    
    try:
        # Run streamlit using uv
        subprocess.run([
            "uv", "run", "streamlit", "run", "app.py",
            "--server.address", "localhost", 
            "--server.port", "8501",
            "--browser.gatherUsageStats", "false"
        ])
    except KeyboardInterrupt:
        print("\n👋 Chatbot stopped. Goodbye!")

if __name__ == "__main__":
    main()
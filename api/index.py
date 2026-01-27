"""
Vercel serverless function entry point for Weather Wiz
"""
import os
import sys

# Add the parent directory to the path so we can import our modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app

# Vercel expects the Flask app to be available as 'app'
# This is the entry point for Vercel serverless functions
if __name__ == "__main__":
    app.run()
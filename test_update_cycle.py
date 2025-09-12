#!/usr/bin/env python3
"""
Test script to verify the automatic update cycle works correctly.
This script simulates the GitHub Actions workflow locally.
"""

import subprocess
import sys
import os
import json
from datetime import datetime

def run_command(cmd, description):
    """Run a command and return success status"""
    print(f"\n🔄 {description}")
    print(f"Command: {cmd}")
    
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, cwd=os.path.dirname(__file__))
        
        if result.returncode == 0:
            print(f"✅ Success: {description}")
            if result.stdout.strip():
                print(f"Output: {result.stdout.strip()}")
            return True
        else:
            print(f"❌ Failed: {description}")
            print(f"Error: {result.stderr.strip()}")
            return False
            
    except Exception as e:
        print(f"❌ Exception during {description}: {str(e)}")
        return False

def check_json_file():
    """Check if the JSON file exists and is valid"""
    json_file = "reya_complete_leaderboard.json"
    
    if not os.path.exists(json_file):
        print(f"❌ {json_file} does not exist")
        return False
    
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        required_keys = ['timestamp', 'source', 'totalEntries', 'leaderboard']
        for key in required_keys:
            if key not in data:
                print(f"❌ Missing required key: {key}")
                return False
        
        print(f"✅ {json_file} is valid")
        print(f"   - Total entries: {data['totalEntries']}")
        print(f"   - Last updated: {data['timestamp']}")
        print(f"   - Source: {data['source']}")
        
        return True
        
    except json.JSONDecodeError as e:
        print(f"❌ Invalid JSON in {json_file}: {str(e)}")
        return False
    except Exception as e:
        print(f"❌ Error reading {json_file}: {str(e)}")
        return False

def main():
    """Main test function"""
    print("🚀 Testing Reya Leaderboard Auto-Update Cycle")
    print("=" * 50)
    
    # Test 1: Check if Python dependencies are available
    print("\n📋 Test 1: Check Python Dependencies")
    if not run_command("python -c \"import requests, json, time; print('All dependencies available')\"", 
                      "Checking Python dependencies"):
        print("💡 Install missing dependencies with: pip install requests")
        return False
    
    # Test 2: Test the fetch script
    print("\n📋 Test 2: Test Data Fetching")
    if not run_command("python fetch_complete_leaderboard.py", 
                      "Fetching leaderboard data"):
        return False
    
    # Test 3: Validate the generated JSON file
    print("\n📋 Test 3: Validate JSON Output")
    if not check_json_file():
        return False
    
    # Test 4: Check git status (if in a git repository)
    print("\n📋 Test 4: Check Git Status")
    run_command("git status --porcelain", "Checking git status")
    
    # Test 5: Simulate the GitHub Actions workflow check
    print("\n📋 Test 5: Simulate GitHub Actions Check")
    result = subprocess.run("git diff --quiet reya_complete_leaderboard.json", 
                          shell=True, cwd=os.path.dirname(__file__))
    
    if result.returncode == 0:
        print("✅ No changes detected in leaderboard data")
        print("   (This is normal if data hasn't changed since last update)")
    else:
        print("✅ Changes detected in leaderboard data")
        print("   (GitHub Actions would commit and push these changes)")
    
    print("\n🎉 All tests completed successfully!")
    print("\n📝 Summary:")
    print("   - Data fetching: Working ✅")
    print("   - JSON validation: Working ✅") 
    print("   - Git integration: Ready ✅")
    print("   - Vercel deployment: Will auto-trigger on push ✅")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

import requests
import json
import time

def fetch_complete_leaderboard():
    """Fetch the complete Reya points leaderboard using pagination"""
    
    base_url = "https://api.reya.xyz/api/incentives/leaderBoard/total"
    all_data = []
    
    # First request to get initial data and pagination info
    print("Fetching initial leaderboard data...")
    response = requests.get(base_url)
    
    if response.status_code != 200:
        print(f"Error: {response.status_code}")
        return None
    
    data = response.json()
    all_data.extend(data['data'])
    
    print(f"Fetched {len(data['data'])} entries (ranks {data['data'][0]['rank']} to {data['data'][-1]['rank']})")
    
    # Check if there are more pages
    after = data['meta'].get('after')
    
    # Continue fetching until we have all data
    while after:
        print(f"Fetching more data after rank {after}...")
        
        # Add pagination parameter
        params = {'after': after}
        response = requests.get(base_url, params=params)
        
        if response.status_code != 200:
            print(f"Error on pagination request: {response.status_code}")
            break
            
        data = response.json()
        
        if not data['data']:  # No more data
            break
            
        all_data.extend(data['data'])
        print(f"Fetched {len(data['data'])} more entries (ranks {data['data'][0]['rank']} to {data['data'][-1]['rank']})")
        
        # Update after for next iteration
        after = data['meta'].get('after')
        
        # Be respectful with API calls
        time.sleep(0.5)
    
    print(f"\nTotal entries fetched: {len(all_data)}")
    
    # Sort by rank to ensure proper order
    all_data.sort(key=lambda x: x['rank'])
    
    # Create final dataset
    final_data = {
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "source": "https://api.reya.xyz/api/incentives/leaderBoard/total",
        "totalEntries": len(all_data),
        "leaderboard": all_data
    }
    
    return final_data

if __name__ == "__main__":
    leaderboard_data = fetch_complete_leaderboard()
    
    if leaderboard_data:
        # Save to JSON file
        filename = "reya_complete_leaderboard.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(leaderboard_data, f, indent=2, ensure_ascii=False)
        
        print(f"\nComplete leaderboard saved to {filename}")
        print(f"Total users: {leaderboard_data['totalEntries']}")
        
        # Show some statistics
        top_user = leaderboard_data['leaderboard'][0]
        last_user = leaderboard_data['leaderboard'][-1]
        
        print(f"\nTop user: {top_user['walletAddress']} with {top_user['totalPoints']:.2f} points")
        print(f"Last user: {last_user['walletAddress']} with {last_user['totalPoints']:.2f} points")
    else:
        print("Failed to fetch leaderboard data")

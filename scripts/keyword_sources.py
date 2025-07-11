import requests

def get_google_suggestions(keyword):
    url = f"https://suggestqueries.google.com/complete/search?client=firefox&q={keyword}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            suggestions = response.json()[1]
            return suggestions
        else:
            print("Failed to fetch suggestions:", response.status_code)
            return []
    except Exception as e:
        print("Error:", str(e))
        return []
    

def get_bing_suggestions(keyword):
    url = f"https://api.bing.com/osjson.aspx?query={keyword}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()[1]
        else:
            print("Failed to fetch suggestiosn:",response.status_code)
            return []
    except Exception as e:
        print("Bing exception:",e)
        return []
    
def get_youtube_suggestions(keyword):
    url = f"http://suggestqueries.google.com/complete/search?client=firefox&ds=yt&q={keyword}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()[1]
        else:
            print("YouTube error:", response.status_code)
            return []
    except Exception as e:
        print("YouTube exception:", e)
        return []
    

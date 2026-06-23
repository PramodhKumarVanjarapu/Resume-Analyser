import requests

def get_leetcode_stats(username: str) -> int:
    url = "https://leetcode.com/graphql"

    query = """
    query getUserProfile($username: String!) {
        matchedUser(username: $username) {
            submitStats {
                acSubmissionNum {
                    difficulty
                    count
                }
            }
        }
    }
    """

    try:
        res = requests.post(
            url,
            json={"query": query, "variables": {"username": username}},
            timeout=10
        )
        data = res.json()

        stats = data["data"]["matchedUser"]["submitStats"]["acSubmissionNum"]
        total = next(x["count"] for x in stats if x["difficulty"] == "All")

        return total
    except:
        return 0
    
def get_codeforces_stats(username: str) -> int:
    url = f"https://codeforces.com/api/user.info?handles={username}"

    try:
        res = requests.get(url, timeout=10)
        data = res.json()

        user = data["result"][0]
        return user.get("rating", 0)
    except:
        return 0
    

def get_username_from_url(url: str) -> str:
    return url.rstrip("/").split("/")[-1]


def process_profiles(profiles: dict):
    result = {
        "leetcode_solved": 0,
        "codeforces_rating": 0
    }

    # LeetCode
    if profiles.get("leetcode"):
        username = get_username_from_url(profiles["leetcode"])
        result["leetcode_solved"] = get_leetcode_stats(username)

    # Codeforces
    if profiles.get("codeforces"):
        username = get_username_from_url(profiles["codeforces"])
        result["codeforces_rating"] = get_codeforces_stats(username)

    return result
# import requests

# def get_leetcode_stats(username: str) -> int:
#     url = "https://leetcode.com/graphql"

#     query = """
#     query getUserProfile($username: String!) {
#         matchedUser(username: $username) {
#             submitStats {
#                 acSubmissionNum {
#                     difficulty
#                     count
#                 }
#             }
#         }
#     }
#     """

#     try:
#         res = requests.post(
#             url,
#             json={"query": query, "variables": {"username": username}},
#             timeout=10
#         )
#         data = res.json()

#         stats = data["data"]["matchedUser"]["submitStats"]["acSubmissionNum"]
#         total = next(x["count"] for x in stats if x["difficulty"] == "All")

#         return total
#     except:
#         return 0
    
# def get_codeforces_stats(username: str) -> int:
#     url = f"https://codeforces.com/api/user.info?handles={username}"

#     try:
#         res = requests.get(url, timeout=10)
#         data = res.json()

#         user = data["result"][0]
#         return user.get("rating", 0)
#     except:
#         return 0
    

# def get_username_from_url(url: str) -> str:
#     return url.rstrip("/").split("/")[-1]


# def process_profiles(profiles: dict):
#     result = {
#         "leetcode_solved": 0,
#         "codeforces_rating": 0
#     }

#     # LeetCode
#     if profiles.get("leetcode"):
#         username = get_username_from_url(profiles["leetcode"])
#         result["leetcode_solved"] = get_leetcode_stats(username)

#     # Codeforces
#     if profiles.get("codeforces"):
#         username = get_username_from_url(profiles["codeforces"])
#         result["codeforces_rating"] = get_codeforces_stats(username)

#     return result



import requests
from bs4 import BeautifulSoup
import re


def get_username(url: str):
    return url.rstrip("/").split("/")[-1]


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
        res = requests.post(url, json={"query": query, "variables": {"username": username}})
        data = res.json()

        stats = data["data"]["matchedUser"]["submitStats"]["acSubmissionNum"]
        return next(x["count"] for x in stats if x["difficulty"] == "All")
    except:
        return 0


def get_codeforces_solved(username: str) -> int:
    solved = set()

    for page in range(1, 4):
        url = f"https://codeforces.com/submissions/{username}/page/{page}"

        try:
            res = requests.get(url)
            soup = BeautifulSoup(res.text, "lxml")

            rows = soup.select("table.status-frame-datatable tr")

            for row in rows:
                verdict = row.select_one(".verdict-accepted")
                if verdict:
                    problem = row.select_one(".problemname")
                    if problem:
                        solved.add(problem.text.strip())
        except:
            break

    return len(solved)


def get_codechef_solved(username: str) -> int:
    url = f"https://www.codechef.com/users/{username}"

    try:
        res = requests.get(url)
        soup = BeautifulSoup(res.text, "lxml")

        text = soup.get_text()
        match = re.search(r"Fully Solved \((\d+)\)", text)

        if match:
            return int(match.group(1))

        return 0
    except:
        return 0


def process_profiles(profiles: dict):
    result = {
        "leetcode_solved": 0,
        "codeforces_solved": 0,
        "codechef_solved": 0
    }

    if profiles.get("leetcode"):
        username = get_username(profiles["leetcode"])
        result["leetcode_solved"] = get_leetcode_stats(username)

    if profiles.get("codeforces"):
        username = get_username(profiles["codeforces"])
        result["codeforces_solved"] = get_codeforces_solved(username)

    if profiles.get("codechef"):
        username = get_username(profiles["codechef"])
        result["codechef_solved"] = get_codechef_solved(username)

    return result
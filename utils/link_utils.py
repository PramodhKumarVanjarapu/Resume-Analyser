import re

PLATFORMS = ["github", "leetcode", "codeforces", "codechef", "hackerrank"]

def clean_text(text: str):
    text = text.lower()
    text = text.replace("\n", " ")
    text = re.sub(r"\s+", " ", text)
    return text

def extract_urls(text: str):
    return re.findall(r"https?://[^\s]+", text)

def validate_github(url):
    return re.match(r"https?://(www\.)?github\.com/[a-zA-Z0-9_-]+/?$", url)

def validate_leetcode(url):
    return re.match(r"https?://(www\.)?leetcode\.com/(u/)?[a-zA-Z0-9_-]+/?$", url)

def validate_codeforces(url):
    return re.match(r"https?://(www\.)?codeforces\.com/profile/[a-zA-Z0-9_-]+/?$", url)

def validate_codechef(url):
    return re.match(r"https?://(www\.)?codechef\.com/users/[a-zA-Z0-9_-]+/?$", url)

def validate_hackerrank(url):
    return re.match(r"https?://(www\.)?hackerrank\.com/[a-zA-Z0-9_-]+/?$", url)

def extract_usernames(text: str):
    usernames = {}

    patterns = {
        "github": r"github\s*[:\-]\s*([a-zA-Z0-9_-]+)",
        "leetcode": r"leetcode\s*[:\-]\s*([a-zA-Z0-9_-]+)",
        "codeforces": r"codeforces\s*[:\-]\s*([a-zA-Z0-9_-]+)",
        "codechef": r"codechef\s*[:\-]\s*([a-zA-Z0-9_-]+)",
        "hackerrank": r"hackerrank\s*[:\-]\s*([a-zA-Z0-9_-]+)",
    }

    for platform, pattern in patterns.items():
        match = re.search(pattern, text)
        if match:
            usernames[platform] = match.group(1)

    return usernames

def categorize_links(text: str, urls: list):
    text = clean_text(text)
    usernames = extract_usernames(text)

    profiles = {
        "github": "",
        "leetcode": "",
        "codeforces": "",
        "codechef": "",
        "hackerrank": ""
    }

    for url in urls:
        url = url.split("|")[0].strip()

        if validate_github(url):
            profiles["github"] = url

        elif validate_leetcode(url):
            profiles["leetcode"] = url

        elif validate_codeforces(url):
            profiles["codeforces"] = url

        elif validate_codechef(url):
            profiles["codechef"] = url

        elif validate_hackerrank(url):
            profiles["hackerrank"] = url

    if not profiles["github"] and "github" in usernames:
        profiles["github"] = f"https://github.com/{usernames['github']}"

    if not profiles["leetcode"] and "leetcode" in usernames:
        profiles["leetcode"] = f"https://leetcode.com/{usernames['leetcode']}"

    if not profiles["codeforces"] and "codeforces" in usernames:
        profiles["codeforces"] = f"https://codeforces.com/profile/{usernames['codeforces']}"

    if not profiles["codechef"] and "codechef" in usernames:
        profiles["codechef"] = f"https://codechef.com/users/{usernames['codechef']}"

    if not profiles["hackerrank"] and "hackerrank" in usernames:
        profiles["hackerrank"] = f"https://hackerrank.com/{usernames['hackerrank']}"

    return profiles
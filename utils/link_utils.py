import re

DSA_PATTERN = r"(https?:\/\/)?(www\.)?(github\.com|leetcode\.com|codeforces\.com|codechef\.com|hackerrank\.com)\/[^\s]+"

def extract_dsa_links(text: str):
    matches = re.findall(DSA_PATTERN, text)

    links = []
    for match in matches:
        full = "".join(match)

        if not full.startswith("http"):
            full = "https://" + full

        links.append(full)

    return list(set(links))


def categorize_links(links):
    profiles = {
        "github": "",
        "leetcode": "",
        "codeforces": "",
        "codechef": "",
        "hackerrank": ""
    }

    for link in links:
        if "github" in link:
            profiles["github"] = link
        elif "leetcode" in link:
            profiles["leetcode"] = link
        elif "codeforces" in link:
            profiles["codeforces"] = link
        elif "codechef" in link:
            profiles["codechef"] = link
        elif "hackerrank" in link:
            profiles["hackerrank"] = link

    return profiles
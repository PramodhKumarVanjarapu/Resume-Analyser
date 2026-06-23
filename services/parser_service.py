from services.pdf_service import extract_text_and_links_from_pdf
from utils.link_utils import categorize_links, extract_urls
from services.profile_service import process_profiles


def process_resume(uid: str, url: str):
    text, clickable_links = extract_text_and_links_from_pdf(url)

    if not text:
        return {
            "UID": uid,
            "github": "",
            "leetcode": "",
            "codeforces": "",
            "codechef": "",
            "hackerrank": "",
            "leetcode_solved": 0,
            "codeforces_solved": 0,
            "codechef_solved": 0
        }

    text_links = extract_urls(text)
    all_links = list(set(text_links + clickable_links))

    profiles = categorize_links(text, all_links)
    stats = process_profiles(profiles)

    return {
        "UID": uid,
        **profiles,
        **stats
    }
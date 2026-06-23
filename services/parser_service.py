from services.pdf_service import extract_text_and_links_from_pdf
from utils.link_utils import categorize_links, extract_urls


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
        }

    text_links = extract_urls(text)

    all_links = list(set(text_links + clickable_links))

    profiles = categorize_links(text, all_links)

    return {"UID": uid, **profiles}
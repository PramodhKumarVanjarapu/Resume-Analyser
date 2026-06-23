from services.pdf_service import extract_text_from_pdf
from utils.link_utils import extract_dsa_links, categorize_links

def process_resume(uid: str, url: str):
    text = extract_text_from_pdf(url)

    if not text:
        return {
            "UID": uid,
            "github": "",
            "leetcode": "",
            "codeforces": "",
            "codechef": "",
            "hackerrank": "",
        }

    links = extract_dsa_links(text)
    profiles = categorize_links(links)

    return {"UID": uid, **profiles}
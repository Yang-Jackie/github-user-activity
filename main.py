import argparse
import requests

parser = argparse.ArgumentParser(prog="github-activity")
parser.add_argument("username", help="Github username")
args = parser.parse_args()

print("Username:", args.username)

url = f"https://api.github.com/users/{args.username}/events/public"
resp = requests.get(url, headers = {"Accept": "application/vnd.github+json",
                                    "User-Agent": "github-acitivity-cli (learning project)"})

if resp.status_code == 404:
    print("User not found.")
    raise SystemExit(1)

if resp.status_code == 403:
    print("Request forbidden or rate-limited. Try again later!")
    raise SystemExit(1)

if not resp.ok:
    print("GitHub API error:", resp.status_code)
    raise SystemExit(1)

try:
    data = resp.json()
except ValueError:
    raise SystemExit("Response is not valid JSON")


def format_event(ev):
    etype = ev["type"]
    repo = ev["repo"]["name"]
    payload = ev["payload"]

    if etype == "PushEvent":
        return f"Pushed to {repo}"
    elif etype == "WatchEvent":
        return f"Starred {repo}"
    elif etype == "CreateEvent":
        return f"Created {payload["ref_type"]} in {repo}"
    elif etype == "DeleteEvent":
        return f"Deleted {payload["ref_type"]} in {repo}"
    elif etype == "IssueEvent":
        return f"{payload.ref_type.capitalize()} an issue in {repo}"
    else: return f"{etype} in {repo}"

if not data: print("This user has no public events.")
else:   
    for ev in data[:20]:
        print("-", format_event(ev))





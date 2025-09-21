import json
import os
import sys
import requests
from requests.exceptions import HTTPError, ConnectionError, Timeout, RequestException


API_URL = "http://31.97.60.222:3000/api/project.all"
OUTPUT_FILE = "project_all.json"
ENV_VAR = "testDjahFOGCKZEzXTIcUrofTzOtzwHngjnRZRUZWaYgCGSXftaoBMJWFAlhMVLyjemR"

def fetch_projects(api_key: str, app_name: str) -> bytes:
    """Fetch projects from Dokploy API and return raw response bytes."""
    headers = {
        "accept": "application/json",
        "x-api-key": api_key,
    }
    req = requests.get(API_URL, headers=headers, timeout=30)
    req.raise_for_status()
    data = req.json()

    # Safely iterate and find the requested application by name
    for project in data or []:
        environments = project.get("environments", [])
        for env in environments:
            applications = env.get("applications", [])
            for app in applications:
                if app.get("appName") == app_name:
                    print(app.get("applicationId"))

    return req.content



def save_json(content_bytes: bytes, output_path: str) -> None:
    """Save bytes as pretty JSON if possible; fallback to raw text file if not JSON."""
    # Attempt to detect encoding from headers isn't available here, default to utf-8
    text = content_bytes.decode("utf-8", errors="replace")
    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        # Save raw response for troubleshooting
        raw_path = os.path.splitext(output_path)[0] + ".raw.txt"
        # with open(raw_path, "w", encoding="utf-8") as f:
        #     f.write(text)
        print(f"Response was not valid JSON. Saved raw response to {raw_path}")
        return
    
    #print(data[0]["environments"][0]["applications"])

    # with open(output_path, "w", encoding="utf-8") as f:
    #     json.dump(data, f, ensure_ascii=False, indent=2, sort_keys=True)
    # print(f"Saved JSON to {output_path}")


def main() -> int:
    api_key = ENV_VAR

    try:
        content = fetch_projects(api_key, "yoyo-cicdddddd-742gyy")
    except HTTPError as e:
        # requests HTTPError
        msg = str(e)
        if getattr(e, "response", None) is not None:
            msg = f"{e.response.status_code} {e.response.reason}"
            try:
                body = e.response.text
                if body:
                    msg += f"\n{body}"
            except Exception:
                pass
        print(f"HTTP error: {msg}", file=sys.stderr)
        return 2
    except (ConnectionError, Timeout) as e:
        print(f"Network error: {e}", file=sys.stderr)
        return 3
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        return 4

    #save_json(content, OUTPUT_FILE)
    return 0


if __name__ == "__main__":
    sys.exit(main())



#!/usr/bin/env python3
"""
Edit an existing image via OpenAI chatgpt-image-latest (images/edits endpoint).
Keeps the source composition, applies a natural-language change.

Usage:
  python3 tools/edit-image.py <in.png> <out.png> "<edit instruction>" [--size 1536x1024]

Key: set the OPENAI_API_KEY environment variable (falls back to the
`env` block in ~/.claude/settings.json if you use Claude Code).
"""
import os, sys, json, base64, argparse, mimetypes, urllib.request, uuid


def load_key():
    key = os.environ.get("OPENAI_API_KEY")
    if key:
        return key
    try:
        return json.load(open(os.path.expanduser("~/.claude/settings.json")))["env"]["OPENAI_API_KEY"]
    except (FileNotFoundError, KeyError):
        sys.exit("Set the OPENAI_API_KEY environment variable first.")


def multipart(fields, files):
    """Build a multipart/form-data body. fields: dict[str,str]; files: list[(name, path)]."""
    boundary = "----wmboundary" + uuid.uuid4().hex
    nl = b"\r\n"
    body = b""
    for k, v in fields.items():
        body += b"--" + boundary.encode() + nl
        body += f'Content-Disposition: form-data; name="{k}"'.encode() + nl + nl
        body += str(v).encode() + nl
    for name, path in files:
        fn = os.path.basename(path)
        ctype = mimetypes.guess_type(path)[0] or "image/png"
        body += b"--" + boundary.encode() + nl
        body += f'Content-Disposition: form-data; name="{name}"; filename="{fn}"'.encode() + nl
        body += f"Content-Type: {ctype}".encode() + nl + nl
        body += open(path, "rb").read() + nl
    body += b"--" + boundary.encode() + b"--" + nl
    return body, boundary


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("infile")
    ap.add_argument("out")
    ap.add_argument("instruction")
    ap.add_argument("--size", default="1536x1024")
    a = ap.parse_args()

    fields = {"model": "chatgpt-image-latest", "prompt": a.instruction, "size": a.size}
    body, boundary = multipart(fields, [("image", a.infile)])
    req = urllib.request.Request(
        "https://api.openai.com/v1/images/edits",
        data=body,
        headers={
            "Authorization": f"Bearer {load_key()}",
            "Content-Type": f"multipart/form-data; boundary={boundary}",
        },
        method="POST",
    )
    try:
        r = json.load(urllib.request.urlopen(req, timeout=300))
        open(a.out, "wb").write(base64.b64decode(r["data"][0]["b64_json"]))
        print("ok:", a.out)
    except urllib.error.HTTPError as e:
        print("HTTP", e.code, e.read().decode()[:600])
        sys.exit(1)


if __name__ == "__main__":
    main()

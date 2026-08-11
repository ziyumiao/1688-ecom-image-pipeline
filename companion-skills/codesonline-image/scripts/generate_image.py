#!/usr/bin/env python3
"""Generate or edit images through image.codesonline.dev."""

import argparse
import base64
import json
import mimetypes
import os
from pathlib import Path
import sys
import urllib.error
import urllib.request
import uuid

BASE_URL = "https://image.codesonline.dev/v1"


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--prompt", required=True)
    parser.add_argument("--image", action="append", default=[])
    parser.add_argument("--mask")
    parser.add_argument("--model", default="gpt-image-2")
    parser.add_argument("--n", type=int, default=1, choices=range(1, 5))
    parser.add_argument("--size", default="1:1")
    parser.add_argument("--quality", choices=["high", "medium", "low"], default="high")
    parser.add_argument("--style", choices=["natural", "vivid"], default="natural")
    parser.add_argument("--background", choices=["opaque", "transparent", "auto"], default="auto")
    parser.add_argument("--response-format", choices=["url", "b64_json"], default="url")
    parser.add_argument("--upscale", choices=["2k", "4k"])
    parser.add_argument("--output", required=True)
    return parser.parse_args()


def multipart(fields, files):
    boundary = "----codesonline-" + uuid.uuid4().hex
    chunks = []
    for name, value in fields.items():
        if value is None:
            continue
        chunks.extend([
            f"--{boundary}\r\n".encode(),
            f'Content-Disposition: form-data; name="{name}"\r\n\r\n'.encode(),
            str(value).encode("utf-8"),
            b"\r\n",
        ])
    for field, path in files:
        file_path = Path(path)
        mime = mimetypes.guess_type(file_path.name)[0] or "application/octet-stream"
        chunks.extend([
            f"--{boundary}\r\n".encode(),
            f'Content-Disposition: form-data; name="{field}"; filename="{file_path.name}"\r\n'.encode(),
            f"Content-Type: {mime}\r\n\r\n".encode(),
            file_path.read_bytes(),
            b"\r\n",
        ])
    chunks.append(f"--{boundary}--\r\n".encode())
    return b"".join(chunks), f"multipart/form-data; boundary={boundary}"


def request_json(url, key, body, content_type):
    request = urllib.request.Request(
        url,
        data=body,
        headers={"Authorization": f"Bearer {key}", "Content-Type": content_type},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=300) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"API request failed ({exc.code}): {detail[:1000]}") from None
    except urllib.error.URLError as exc:
        raise RuntimeError(f"API connection failed: {exc.reason}") from None


def output_paths(base, count):
    base = Path(base).resolve()
    if count == 1:
        return [base]
    suffix = base.suffix or ".png"
    stem = base.stem
    return [base.with_name(f"{stem}-{index + 1}{suffix}") for index in range(count)]


def main():
    args = parse_args()
    key = os.environ.get("CODESONLINE_IMAGE_API_KEY")
    if not key:
        raise RuntimeError("CODESONLINE_IMAGE_API_KEY is not set.")

    common = {
        "model": args.model,
        "prompt": args.prompt,
        "n": args.n,
        "size": args.size,
        "quality": args.quality,
        "style": args.style,
        "background": args.background,
        "response_format": args.response_format,
        "upscale": args.upscale,
    }

    if args.image:
        image_paths = [Path(path).resolve() for path in args.image]
        for path in image_paths:
            if not path.is_file():
                raise RuntimeError(f"Reference image not found: {path}")
        files = [("image", image_paths[0])]
        files.extend(("image[]", path) for path in image_paths[1:])
        if args.mask:
            mask_path = Path(args.mask).resolve()
            if not mask_path.is_file():
                raise RuntimeError(f"Mask not found: {mask_path}")
            files.append(("mask", mask_path))
        body, content_type = multipart(common, files)
        result = request_json(f"{BASE_URL}/images/edits", key, body, content_type)
    else:
        body = json.dumps({k: v for k, v in common.items() if v is not None}).encode("utf-8")
        result = request_json(f"{BASE_URL}/images/generations", key, body, "application/json")

    items = result.get("data") or []
    if not items:
        raise RuntimeError(f"API returned no images: {json.dumps(result, ensure_ascii=False)[:1000]}")

    paths = output_paths(args.output, len(items))
    for item, path in zip(items, paths):
        path.parent.mkdir(parents=True, exist_ok=True)
        if item.get("b64_json"):
            content = base64.b64decode(item["b64_json"])
        else:
            image_url = item.get("url") or item.get("fallback_url")
            if not image_url:
                raise RuntimeError("Image response contains neither url nor b64_json.")
            with urllib.request.urlopen(image_url, timeout=300) as response:
                content = response.read()
        if not content:
            raise RuntimeError("Downloaded image is empty.")
        path.write_bytes(content)
        print(path)


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)

#!/usr/bin/env python3
"""Universal audio & video crawler and WeChat-ready waveform card asset generator.

Scans a webpage (URL or local HTML file) for embedded or linked audio/video
assets (<audio>, <video>, <source>, direct media links, GitHub/HF asset links),
downloads them to a local directory, and generates minimalist Base64-ready
waveform preview PNGs for WAV files using scipy/wave + numpy + Pillow.
"""

import argparse
import base64
import json
import os
import re
import sys
from typing import Dict, List, Optional
from urllib.parse import urljoin, urlparse, unquote

import numpy as np
import requests
from bs4 import BeautifulSoup
from PIL import Image, ImageDraw
from scipy.io import wavfile

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

AUDIO_EXTS = {".wav", ".mp3", ".flac", ".ogg", ".m4a", ".aac", ".opus"}
VIDEO_EXTS = {".mp4", ".webm", ".mov", ".m4v", ".mkv"}
MEDIA_EXTS = AUDIO_EXTS | VIDEO_EXTS

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
    )
}


def normalize_media_url(url: str) -> str:
    """Convert GitHub/HuggingFace blob viewer URLs into direct raw download URLs."""
    # GitHub blob -> raw.githubusercontent.com
    gh_match = re.match(
        r"^https?://github\.com/([^/]+/[^/]+)/blob/(.+)$", url
    )
    if gh_match:
        return f"https://raw.githubusercontent.com/{gh_match.group(1)}/{gh_match.group(2)}"

    # Hugging Face blob -> resolve
    hf_match = re.match(
        r"^https?://huggingface\.co/(.+?)/blob/(.+)$", url
    )
    if hf_match:
        return f"https://huggingface.co/{hf_match.group(1)}/resolve/{hf_match.group(2)}"

    return url


def infer_media_kind(url: str, tag_name: str = "", content_type: str = "") -> Optional[str]:
    """Determine whether a resource is 'audio' or 'video'."""
    ct = (content_type or "").lower()
    if ct.startswith("audio/"):
        return "audio"
    if ct.startswith("video/"):
        return "video"

    ext = os.path.splitext(urlparse(url).path)[1].lower()
    if ext in AUDIO_EXTS:
        return "audio"
    if ext in VIDEO_EXTS:
        return "video"

    if tag_name in ("audio",):
        return "audio"
    if tag_name in ("video",):
        return "video"

    return None


def extract_context_label(tag) -> str:
    """Extract a clean human-readable label near an HTML media element."""
    for attr in ("aria-label", "title", "data-label", "alt"):
        val = tag.get(attr)
        if val and val.strip():
            return val.strip()[:80]

    # Check parent figure/figcaption or table cell context
    fig = tag.find_parent("figure")
    if fig:
        cap = fig.find("figcaption")
        if cap and cap.get_text(strip=True):
            return cap.get_text(" ", strip=True)[:80]

    td = tag.find_parent(["td", "th"])
    if td:
        tr = td.find_parent("tr")
        if tr:
            cells = tr.find_all(["td", "th"])
            idx = cells.index(td) if td in cells else -1
            table = tr.find_parent("table")
            header_label = ""
            if table and idx >= 0:
                headers = table.find_all("th")
                if idx < len(headers):
                    header_label = headers[idx].get_text(" ", strip=True)
            row_label = cells[0].get_text(" ", strip=True) if cells and idx > 0 else ""
            combined = " - ".join(p for p in [row_label, header_label] if p)
            if combined:
                return combined[:80]

    # Check preceding sibling text or heading
    for prev in tag.find_all_previous(["h1", "h2", "h3", "h4", "strong", "p", "label"], limit=3):
        txt = prev.get_text(" ", strip=True)
        if txt and len(txt) <= 80:
            return txt

    return ""


def discover_media(html: str, base_url: str) -> List[Dict[str, str]]:
    """Discover unique audio/video URLs and optional poster images from HTML."""
    soup = BeautifulSoup(html, "html.parser")
    found: List[Dict[str, str]] = []
    seen_urls = set()

    def add_item(raw_url: str, kind: Optional[str], label: str, poster: str = "") -> None:
        if not raw_url or raw_url.startswith("data:") or raw_url.startswith("blob:"):
            return
        abs_url = normalize_media_url(urljoin(base_url, raw_url.strip()))
        if abs_url in seen_urls:
            return
        seen_urls.add(abs_url)
        found.append(
            {
                "url": abs_url,
                "kind": kind or "unknown",
                "label": label,
                "poster": urljoin(base_url, poster.strip()) if poster else "",
            }
        )

    # 1. <audio> and <video> tags (including nested <source> and lazy data-src)
    for tag in soup.find_all(["audio", "video"]):
        tag_name = tag.name.lower()
        label = extract_context_label(tag)
        poster = tag.get("poster", "") if tag_name == "video" else ""

        direct_src = tag.get("src") or tag.get("data-src")
        if direct_src:
            add_item(direct_src, infer_media_kind(direct_src, tag_name), label, poster)

        for src_tag in tag.find_all("source"):
            s_src = src_tag.get("src") or src_tag.get("data-src")
            if s_src:
                stype = src_tag.get("type", "")
                kind = infer_media_kind(s_src, tag_name, stype)
                add_item(s_src, kind, label, poster)

    # 2. Direct <a href="..."> links to audio/video extensions
    for a_tag in soup.find_all("a", href=True):
        href = a_tag["href"]
        kind = infer_media_kind(href)
        if kind:
            label = a_tag.get_text(" ", strip=True)[:80] or extract_context_label(a_tag)
            add_item(href, kind, label)

    # 3. Fallback regex scan for raw media URLs inside JSON/scripts/markdown
    raw_pattern = re.compile(
        r"""https?://[^\s"'<>\\]+?\.(?:wav|mp3|flac|ogg|m4a|mp4|webm|mov)(?:\?[^\s"'<>\\]*)?""",
        re.IGNORECASE,
    )
    for match in raw_pattern.findall(html):
        kind = infer_media_kind(match)
        add_item(match, kind, "")

    return found


def sanitize_filename(name: str, default_ext: str = ".bin") -> str:
    """Create a safe cross-platform filename."""
    clean = re.sub(r"[^\w.\-]+", "_", unquote(name)).strip("._")
    if not clean:
        clean = "media_file"
    if not os.path.splitext(clean)[1]:
        clean += default_ext
    return clean[:120]


def guess_ext_from_ct(content_type: str, fallback: str = ".bin") -> str:
    """Map common audio/video MIME types to file extensions."""
    ct = (content_type or "").split(";")[0].strip().lower()
    mapping = {
        "audio/wav": ".wav",
        "audio/x-wav": ".wav",
        "audio/mpeg": ".mp3",
        "audio/mp3": ".mp3",
        "audio/flac": ".flac",
        "audio/ogg": ".ogg",
        "audio/mp4": ".m4a",
        "audio/aac": ".aac",
        "video/mp4": ".mp4",
        "video/webm": ".webm",
        "video/quicktime": ".mov",
    }
    return mapping.get(ct, fallback)


def render_wav_waveform_png(wav_path: str, png_path: str, label: str = "") -> Optional[Dict[str, float]]:
    """Render a clean minimalist waveform PNG for a WAV file using scipy + Pillow."""
    try:
        sr, data = wavfile.read(wav_path)
    except Exception:
        return None

    if data.size == 0 or sr <= 0:
        return None

    # Downmix to mono float in [-1, 1]
    arr = data.astype(np.float64)
    if arr.ndim > 1:
        arr = arr.mean(axis=1)
    peak = np.max(np.abs(arr))
    if peak > 0:
        arr = arr / peak

    duration = len(arr) / float(sr)
    width, height = 1080, 180
    pad_x, pad_y = 24, 24
    usable_w = width - 2 * pad_x
    usable_h = height - 2 * pad_y
    mid_y = height // 2

    # Compute amplitude envelope across bar buckets
    bar_step = 6
    bar_w = 3
    num_bars = usable_w // bar_step
    chunks = np.array_split(arr, max(1, num_bars))
    amps = [float(np.max(np.abs(c))) if len(c) else 0.0 for c in chunks]

    img = Image.new("RGB", (width, height), color=(245, 245, 247))
    draw = ImageDraw.Draw(img)

    # Subtle center baseline
    draw.line([(pad_x, mid_y), (width - pad_x, mid_y)], fill=(210, 210, 215), width=2)

    for idx, amp in enumerate(amps):
        x0 = pad_x + idx * bar_step
        half_h = max(3, int(amp * (usable_h * 0.44)))
        draw.rounded_rectangle(
            [(x0, mid_y - half_h), (x0 + bar_w, mid_y + half_h)],
            radius=1,
            fill=(29, 29, 31),
        )

    img.save(png_path, format="PNG")
    return {"sample_rate": int(sr), "duration_sec": round(duration, 2)}


def download_media_item(
    item: Dict[str, str], index: int, out_dir: str, max_bytes: int
) -> Optional[Dict[str, object]]:
    """Stream-download a single media asset and optionally render its waveform."""
    url = item["url"]
    try:
        resp = requests.get(url, headers=HEADERS, stream=True, timeout=20, allow_redirects=True)
        if resp.status_code != 200:
            return None

        ct = resp.headers.get("Content-Type", "")
        if "text/html" in ct.lower():
            return None

        cl = resp.headers.get("Content-Length")
        if cl and int(cl) > max_bytes:
            return None

        kind = infer_media_kind(url, item.get("kind", ""), ct)
        if not kind:
            return None

        ext = os.path.splitext(urlparse(resp.url).path)[1].lower()
        if not ext:
            ext = guess_ext_from_ct(ct, ".wav" if kind == "audio" else ".mp4")

        raw_name = os.path.basename(urlparse(resp.url).path) or f"sample_{index}"
        filename = f"{index:02d}_{sanitize_filename(raw_name, ext)}"
        local_path = os.path.join(out_dir, filename)

        downloaded = 0
        with open(local_path, "wb") as f:
            for chunk in resp.iter_content(chunk_size=65536):
                if not chunk:
                    continue
                downloaded += len(chunk)
                if downloaded > max_bytes:
                    f.close()
                    os.remove(local_path)
                    return None
                f.write(chunk)

        result: Dict[str, object] = {
            "index": index,
            "kind": kind,
            "label": item.get("label", ""),
            "source_url": url,
            "local_path": local_path,
            "filename": filename,
            "size_kb": round(downloaded / 1024.0, 1),
        }

        if kind == "audio" and ext == ".wav":
            png_name = f"{os.path.splitext(filename)[0]}_waveform.png"
            png_path = os.path.join(out_dir, png_name)
            meta = render_wav_waveform_png(local_path, png_path, item.get("label", ""))
            if meta:
                result["waveform_png"] = png_path
                result["sample_rate"] = meta["sample_rate"]
                result["duration_sec"] = meta["duration_sec"]

        if kind == "video" and item.get("poster"):
            try:
                p_resp = requests.get(item["poster"], headers=HEADERS, timeout=15)
                if p_resp.status_code == 200 and p_resp.headers.get("Content-Type", "").startswith("image/"):
                    p_ext = guess_ext_from_ct(p_resp.headers.get("Content-Type", ""), ".png")
                    if p_ext == ".bin":
                        p_ext = ".png"
                    p_name = f"{os.path.splitext(filename)[0]}_poster{p_ext}"
                    p_path = os.path.join(out_dir, p_name)
                    with open(p_path, "wb") as pf:
                        pf.write(p_resp.content)
                    result["poster_png"] = p_path
            except Exception:
                pass

        return result
    except Exception:
        return None


def inject_base64_images_into_html(html_path: str, base_dir: str = "") -> int:
    """Embed local PNG/JPG/WEBP preview images in HTML as Base64 Data URIs for WeChat paste."""
    resolved_base = base_dir or os.path.dirname(os.path.abspath(html_path))
    with open(html_path, "r", encoding="utf-8") as f:
        content = f.read()

    replaced_count = 0

    def replace_img_src(match: re.Match) -> str:
        nonlocal replaced_count
        src = match.group(1)
        if src.startswith("data:") or src.startswith("http"):
            return match.group(0)

        img_path = os.path.normpath(os.path.join(resolved_base, src))
        if not os.path.exists(img_path):
            return match.group(0)

        ext = os.path.splitext(img_path)[1].lower().replace(".", "")
        mime_map = {"png": "image/png", "jpg": "image/jpeg", "jpeg": "image/jpeg", "webp": "image/webp"}
        mime = mime_map.get(ext, "image/png")
        with open(img_path, "rb") as img_f:
            b64_data = base64.b64encode(img_f.read()).decode("ascii")

        replaced_count += 1
        return f'src="data:{mime};base64,{b64_data}"'

    new_content = re.sub(
        r'src=["\']([^"\']+\.(?:png|jpg|jpeg|webp))["\']',
        replace_img_src,
        content,
        flags=re.IGNORECASE,
    )
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(new_content)
    return replaced_count


def main() -> int:
    parser = argparse.ArgumentParser(description="Extract audio/video demos from a project webpage.")
    parser.add_argument("--url", help="Target webpage URL")
    parser.add_argument("--html", help="Local HTML file path (optional)")
    parser.add_argument("--base-url", default="", help="Base URL when reading --html")
    parser.add_argument("--out-dir", default="./media", help="Output directory for downloaded assets")
    parser.add_argument("--max-files", type=int, default=12, help="Maximum media files to download")
    parser.add_argument("--max-mb", type=float, default=50.0, help="Max file size in MB per file")
    parser.add_argument("--inject-html", help="Inject local preview images as Base64 into target HTML")
    parser.add_argument("--json", action="store_true", help="Output JSON manifest")
    args = parser.parse_args()

    if args.inject_html:
        count = inject_base64_images_into_html(args.inject_html)
        print(f"Injected {count} image(s) into {args.inject_html}")
        if not args.url and not args.html:
            return 0

    if not args.url and not args.html:
        print("Error: provide --url or --html", file=sys.stderr)
        return 1

    if args.html:
        with open(args.html, "r", encoding="utf-8", errors="ignore") as f:
            html = f.read()
        base_url = args.base_url or args.url or ""
    else:
        resp = requests.get(args.url, headers=HEADERS, timeout=20)
        resp.raise_for_status()
        html = resp.text
        base_url = resp.url

    candidates = discover_media(html, base_url)
    os.makedirs(args.out_dir, exist_ok=True)
    max_bytes = int(args.max_mb * 1024 * 1024)

    downloaded: List[Dict[str, object]] = []
    for idx, item in enumerate(candidates[: args.max_files * 2], start=1):
        if len(downloaded) >= args.max_files:
            break
        res = download_media_item(item, len(downloaded) + 1, args.out_dir, max_bytes)
        if res:
            downloaded.append(res)

    manifest = {
        "source": args.url or args.html,
        "candidates_found": len(candidates),
        "downloaded_count": len(downloaded),
        "assets": downloaded,
    }

    if args.json:
        print(json.dumps(manifest, ensure_ascii=False, indent=2))
    else:
        print(f"Found {len(candidates)} candidate(s), downloaded {len(downloaded)} asset(s) to {args.out_dir}")
        for a in downloaded:
            print(f" - [{a['kind']}] {a['local_path']} ({a['size_kb']} KB) label={a.get('label', '')}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

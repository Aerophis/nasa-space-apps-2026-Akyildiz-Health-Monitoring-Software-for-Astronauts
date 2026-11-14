"""Explicit, reproducible acquisition of the reviewed unrestricted NASA files.

Run: .venv/Scripts/python.exe -m astrocare.acquire_research
The Streamlit app itself never downloads data. Original files are not overwritten.
"""

import json
import hashlib
import sys
from datetime import datetime, timezone

import requests

from astrocare.research import ResearchError, load_research, parse_cmp, read_manifest, research_directory


def fetch_bytes(url, limit=2_000_000):
    try:
        with requests.get(url, timeout=(10, 30), stream=True) as response:
            response.raise_for_status()
            chunks, size = [], 0
            for chunk in response.iter_content(65536):
                size += len(chunk)
                if size > limit:
                    raise ResearchError("NASA response exceeds the reviewed download size limit.")
                chunks.append(chunk)
            return b"".join(chunks)
    except requests.RequestException as exc:
        raise ResearchError("NASA acquisition failed. Check network access and retry; no substitute dataset was created.") from exc


def acquire():
    manifest = read_manifest()
    root = research_directory()
    if (root / "receipt.json").exists():
        return load_research(root)
    try:
        listing = json.loads(fetch_bytes(manifest["files_api"]))
        entry = next(item for item in listing["studies"]["OSD-575"]["study_files"]
                     if item["file_name"] == manifest["file_name"])
        if entry["restricted"] is not False or "https://osdr.nasa.gov" + entry["remote_url"] != manifest["download_url"]:
            raise ResearchError("The NASA file is restricted or its official download URL changed; acquisition stopped.")
        sources = [(manifest["file_name"], manifest["download_url"], manifest["sha256"]),
                   ("study_metadata.json", manifest["metadata_api"], manifest["metadata_sha256"])]
        downloads = {}
        for name, url, expected in sources:
            path = root / name
            payload = path.read_bytes() if path.exists() else fetch_bytes(url)
            if hashlib.sha256(payload).hexdigest() != expected:
                raise ResearchError(f"Checksum mismatch for {name}; the file was not overwritten. Review any upstream changes separately.")
            downloads[name] = payload
        parse_cmp(downloads[manifest["file_name"]], json.loads(downloads["study_metadata.json"]), manifest)
        root.mkdir(parents=True, exist_ok=True)
        for name, payload in downloads.items():
            if not (root / name).exists():
                with (root / name).open("xb") as output:
                    output.write(payload)
        receipt = {"dataset_id": "OSD-575", "study_version": manifest["study_version"],
                   "retrieved_at_utc": datetime.now(timezone.utc).isoformat(),
                   "download_url": manifest["download_url"], "metadata_url": manifest["metadata_api"],
                   "file_name": manifest["file_name"], "sha256": manifest["sha256"],
                   "metadata_sha256": manifest["metadata_sha256"], "license": manifest["license"],
                   "license_evidence": manifest["license_evidence"], "restricted": False}
        with (root / "receipt.json").open("x", encoding="utf-8") as output:
            json.dump(receipt, output, indent=2)
        return load_research(root)
    except (OSError, ValueError, KeyError, StopIteration, TypeError) as exc:
        raise ResearchError("Acquisition could not complete. Check NASA metadata and local permissions; existing files were not overwritten.") from exc


if __name__ == "__main__":
    try:
        bundle = acquire()
        print(f"OSD-575 ready offline: {bundle.observations.sample_name.nunique()} samples; "
              f"{len(bundle.observations)} selected analyte observations. SHA-256: {bundle.manifest['sha256']}")
    except ResearchError as exc:
        print(str(exc), file=sys.stderr)
        raise SystemExit(1)

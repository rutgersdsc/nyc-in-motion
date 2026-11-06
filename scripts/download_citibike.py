#!/usr/bin/env python3
r"""Download NYC Citi Bike Aug + Sep 2025 trip histories into data/public/.

Run from the extracted NYC in Motion public bundle:
    py -3 scripts\download_citibike.py

No third-party Python packages required. The GENERATED TRIP DATA is for
local analysis; do not distribute the source ZIPs or merged CSV standalone.
Official sources: https://citibikenyc.com/system-data
Terms: https://citibikenyc.com/data-sharing-policy
"""
from __future__ import annotations

import argparse
import csv
import gzip
import io
import sys
import zipfile
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import unquote, urlparse
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parent.parent
PUBLIC = ROOT / "data" / "public"
CACHE = ROOT / "data" / "citibike_local"
OUTPUT = PUBLIC / "citibike_combined_trips.csv.gz"
MONTHS = ("202508", "202509")
BASE = "https://s3.amazonaws.com/tripdata/"
CHUNK_BYTES = 2 * 1024 * 1024


def official_candidates(month: str) -> list[str]:
    urls = {
        "202508": "https://s3.amazonaws.com/tripdata/202508-citibike-tripdata.zip",
        "202509": "https://s3.amazonaws.com/tripdata/202509-citibike-tripdata.zip",
    }
    return [urls[month]]


def validate_official_url(url: str, month: str) -> None:
    parsed = urlparse(url)
    if not (parsed.scheme == "https" and
            ((parsed.hostname == "s3.amazonaws.com" and parsed.path.startswith("/tripdata/"))
             or parsed.hostname == "tripdata.s3.amazonaws.com") and
            parsed.path.endswith(".zip")):
        raise ValueError("Only official Citi Bike S3 tripdata HTTPS .zip URLs are accepted")
    name = Path(unquote(parsed.path)).name
    if not name.startswith(f"{month}-citibike-tripdata"):
        raise ValueError(f"Wrong month/NYC archive for {month}: {name}. Avoid JC- files.")


def stream_download(url: str, dest: Path) -> None:
    temp = dest.with_name(dest.name + ".part")
    request = Request(url, headers={"User-Agent": "NYC-in-Motion-Datathon/1.0"})
    try:
        with urlopen(request, timeout=120) as response, temp.open("wb") as stream:
            while True:
                chunk = response.read(CHUNK_BYTES)
                if not chunk:
                    break
                stream.write(chunk)
        if not zipfile.is_zipfile(temp):
            raise ValueError("The server response was not a valid ZIP archive")
        temp.replace(dest)
    finally:
        temp.unlink(missing_ok=True)


def get_archive(month: str, override_url: str | None = None, local_zip: Path | None = None) -> Path:
    CACHE.mkdir(parents=True, exist_ok=True)
    if local_zip is not None:
        if not local_zip.exists() or not zipfile.is_zipfile(local_zip):
            raise ValueError(f"Local ZIP is missing or invalid: {local_zip}")
        print(f"[local] {month}: {local_zip}", flush=True)
        return local_zip

    candidates = [override_url] if override_url else official_candidates(month)
    errors = []
    for url in candidates:
        assert url is not None
        validate_official_url(url, month)
        filename = Path(unquote(urlparse(url).path)).name
        destination = CACHE / filename
        if destination.is_file():
            if zipfile.is_zipfile(destination):
                print(f"[cached] {month}: {destination}", flush=True)
                return destination
            print(f"[retry] Invalid cached ZIP; removing {filename}", flush=True)
            destination.unlink()
        print(f"[download] {month}: {url}", flush=True)
        try:
            stream_download(url, destination)
            print(f"[saved] {destination} ({destination.stat().st_size / 1024**2:.1f} MiB)", flush=True)
            return destination
        except HTTPError as exc:
            errors.append(f"HTTP {exc.code}: {url}")
            if exc.code not in {403, 404, 410}:
                break
        except (URLError, OSError, ValueError) as exc:
            errors.append(f"{type(exc).__name__}: {exc} ({url})")
            if override_url:
                break
    raise RuntimeError(
        f"No usable official NYC Citi Bike ZIP found for {month}.\n"
        + "\n".join(errors) + "\n"
        + "Find the month on https://s3.amazonaws.com/tripdata/index.html "
        + "and rerun with --aug-url / --sep-url as appropriate."
    )


def merge_archives(archives: list[Path], output: Path = OUTPUT) -> tuple[int, int]:
    """Merge CSV members incrementally; reorder columns consistently; bound memory."""
    if len(archives) != 2 or len(set(archives)) != 2:
        raise ValueError("Provide distinct August and September archives")
    output.parent.mkdir(parents=True, exist_ok=True)
    temp = output.with_name(output.name + ".part")
    header: list[str] | None = None
    all_count = 0
    count_csvs = 0
    try:
        with gzip.open(temp, "wt", encoding="utf-8", newline="", compresslevel=5) as combined:
            writer = csv.writer(combined)
            for month, archive in zip(MONTHS, archives):
                month_count = 0
                with zipfile.ZipFile(archive) as zf:
                    parts = sorted((part for part in zf.infolist()
                                    if not part.is_dir()
                                    and part.filename.lower().endswith(".csv")
                                    and not part.filename.startswith("__MACOSX/")),
                                   key=lambda part: part.filename)
                    if not parts:
                        raise ValueError(f"No trip CSVs in {archive.name}")
                    for part in parts:
                        with zf.open(part) as data, io.TextIOWrapper(data, encoding="utf-8-sig", newline="") as source:
                            reader = csv.reader(source)
                            columns = next(reader, None)
                            if not columns or len(columns) != len(set(columns)):
                                raise ValueError(f"Invalid CSV columns: {part.filename}")
                            if header is None:
                                header = columns
                                if not {"started_at", "ended_at"}.issubset(header):
                                    raise ValueError(f"Unexpected Citi Bike fields: {header}")
                                writer.writerow(header)
                            if set(columns) != set(header):
                                raise ValueError(f"CSV schema differs in {part.filename}; merge halted")
                            indexes = [columns.index(key) for key in header]
                            started_index = columns.index("started_at")
                            for row in reader:
                                if not row:
                                    continue
                                if len(row) != len(columns):
                                    raise ValueError(f"Malformed row in {part.filename}")
                                # Keep only trips started during that month, even if
                                # publisher files contain boundary-crossing records.
                                if row[started_index][:7].replace("-", "") != month:
                                    continue
                                writer.writerow([row[i] for i in indexes])
                                month_count += 1
                            count_csvs += 1
                print(f"[merged] {month}: {month_count:,} trips from {len(parts)} CSV(s)", flush=True)
                all_count += month_count
                if month_count == 0:
                    raise ValueError(f"No trips in {month}; check source archive")
        temp.replace(output)
    finally:
        temp.unlink(missing_ok=True)
    print(f"[done] {all_count:,} trips across {count_csvs} CSVs -> {output}", flush=True)
    return all_count, count_csvs


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--aug-url", help="Official NYC August 2025 trip-history ZIP URL (optional)")
    parser.add_argument("--sep-url", help="Official NYC September 2025 trip-history ZIP URL (optional)")
    parser.add_argument("--aug-zip", type=Path, help="Use an August 2025 ZIP already on disk")
    parser.add_argument("--sep-zip", type=Path, help="Use a September 2025 ZIP already on disk")
    parser.add_argument("--force", action="store_true", help="Rebuild the merged output if it already exists")
    args = parser.parse_args()
    if args.aug_url and args.aug_zip or args.sep_url and args.sep_zip:
        parser.error("Specify either a URL or a local ZIP for each month, not both")
    if OUTPUT.exists() and not args.force:
        if OUTPUT.stat().st_size == 0:
            print(f"[retry] Removing empty output: {OUTPUT}")
            OUTPUT.unlink()
        else:
            print(f"[exists] {OUTPUT}\nRe-run with --force to rebuild it.")
            return
    print("Official source: https://citibikenyc.com/system-data")
    august = get_archive("202508", override_url=args.aug_url, local_zip=args.aug_zip)
    september = get_archive("202509", override_url=args.sep_url, local_zip=args.sep_zip)
    merge_archives([august, september])

    # Delete downloaded monthly archives after a successful merge
    deleted = 0

    for archive, local_file in (
        (august, args.aug_zip),
        (september, args.sep_zip),
    ):
        if local_file is None and archive.resolve().parent == CACHE.resolve():
            archive.unlink(missing_ok=True)
            deleted += 1

    # Remove the cache folder if it's empty
    if CACHE.exists() and not any(CACHE.iterdir()):
        CACHE.rmdir()


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, RuntimeError, zipfile.BadZipFile, EOFError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        sys.exit(1)

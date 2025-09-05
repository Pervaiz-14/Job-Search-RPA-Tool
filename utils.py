import logging
from typing import List, Dict


def deduplicate_jobs(jobs: List[Dict]) -> List[Dict]:
    """Simple dedupe by URL or (title, company, location)."""
    seen = set()
    out = []
    for job in jobs:
        key = job.get("url") or f"{job.get('title')}|{job.get('company')}|{job.get('location')}"
        if key in seen:
            continue
        seen.add(key)
        out.append(job)
    logging.info("Deduplicated jobs: %s -> %s", len(jobs), len(out))
    return out

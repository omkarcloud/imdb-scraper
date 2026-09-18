"""Configuration for the IMDb Scraper. Everything can be set with an
environment variable; the defaults work out of the box.

    PORT        port the API listens on (default 8000)
    IMDB_PROXY  proxy URL for every request, e.g. http://user:pass@host:port
                (default: none — direct). IMDb's GraphQL API did not rate-limit
                at 100 sequential requests from one IP, so you very likely
                don't need this. Set it only if you start seeing failures at
                high volume.

Everything else below is a plain constant with a working default — edit it
here if you need to.
"""
import os

PORT = int(os.environ.get("PORT", "8000"))

# Retry policy for transport errors and blocks (every request).
MAX_RETRIES = 3
RETRY_BACKOFF = 2          # seconds, multiplied by the attempt number

IMDB_PROXY = os.environ.get("IMDB_PROXY") or None

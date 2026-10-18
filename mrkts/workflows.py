"""Standalone async workflows built on the MRKT API."""

import asyncio
from collections.abc import AsyncIterator
from math import isfinite
from typing import Any

from .client import MrktClient


def fetch_feed(
    client: MrktClient,
    *,
    interval: float = 1.0,
    **filters: Any,
) -> AsyncIterator[dict]:
    """Poll the preloaded market gifts feed and yield each response."""
    if not isfinite(interval) or interval <= 0:
        raise ValueError("interval must be a finite number greater than zero")
    if not hasattr(client, "market"):
        raise RuntimeError("Preload 'market' before running fetch_feed()")
    if client.http is None or client.http.closed:
        raise RuntimeError("Start the MrktClient before running fetch_feed()")

    async def poll() -> AsyncIterator[dict]:
        while True:
            yield await client.market.gifts.feed(**filters)
            await asyncio.sleep(interval)

    return poll()

import asyncio
from collections.abc import Awaitable, Callable
from typing import Any

from .client import MrktClient
from .utils import get_tokens


class _PoolClient(MrktClient):
    async def __aexit__(self, *args: Any) -> None:
        # The pool owns worker lifetimes and closes them after all map calls.
        return None


class MrktPool:
    def __init__(
        self,
        *,
        tokens: list[str] | None = None,
        sessions: list[str] | None = None,
        workdir: str = ".",
        tasks: list[tuple[str, dict]] | None = None,
        proxy: str | None = None,
        unlimited: bool = False,
        preload: tuple[str, ...] | None = None,
        concurrency: int = 5,
    ):
        if tokens is not None and sessions is not None:
            raise ValueError("Client can not run with tokens and sessions both")
        if tokens is None and sessions is None:
            raise ValueError("Client can not run without tokens or sessions")
        if not tokens and not sessions:
            raise ValueError("Client pool must contain at least one account")
        if concurrency < 1:
            raise ValueError("concurrency must be greater than zero")

        self._tokens = tokens
        self._sessions = sessions
        self._session_concurrency = concurrency
        self._preload = preload
        self._tasks = tasks
        self.proxy = proxy
        self.workdir = workdir
        self._unlimited = unlimited
        self.clients: list[MrktClient] = []
        self._started = False
        self._entered = False
        self._map_lock = asyncio.Lock()

    @classmethod
    async def from_sessions(
        cls,
        sessions: list[str],
        *,
        workdir: str = ".",
        proxy: str | None = None,
        concurrency: int = 5,
        **kwargs: Any,
    ) -> "MrktPool":
        return cls(
            sessions=sessions,
            workdir=workdir,
            proxy=proxy,
            concurrency=concurrency,
            **kwargs,
        )

    async def start(self) -> "MrktPool":
        if self._started:
            return self

        if self._tokens is None:
            self._tokens = await get_tokens(
                self._sessions or [],
                workdir=self.workdir,
                proxy=self.proxy,
                concurrency=self._session_concurrency,
            )
        self._started = True
        return self

    def _ensure_workers(self, count: int) -> None:
        while len(self.clients) < count:
            self.clients.append(
                _PoolClient(
                    preload=self._preload,
                    workdir=self.workdir,
                    proxy=self.proxy,
                )
            )

    async def map(
        self,
        coro_func: Callable[[MrktClient], Awaitable[Any]],
        *,
        concurrency: int | None = None,
    ) -> list[Any | Exception]:
        if concurrency is None:
            concurrency = self._session_concurrency
        if concurrency < 1:
            raise ValueError("concurrency must be greater than zero")

        async with self._map_lock:
            await self.start()
            tokens = self._tokens or []
            worker_count = (
                len(tokens)
                if self._unlimited
                else min(concurrency, len(tokens))
            )
            self._ensure_workers(worker_count)
            results: list[Any | Exception] = [None] * len(tokens)
            next_index = 0

            async def worker(client: MrktClient) -> None:
                nonlocal next_index
                while next_index < len(tokens):
                    index = next_index
                    next_index += 1
                    try:
                        client.set_token(tokens[index])
                        results[index] = await coro_func(client)
                    except Exception as exc:
                        results[index] = exc

            try:
                await asyncio.gather(
                    *(worker(client) for client in self.clients[:worker_count])
                )
                return results
            finally:
                if not self._entered:
                    await self.close()

    async def close(self) -> None:
        if self.clients:
            await asyncio.gather(
                *(MrktClient.close(client) for client in self.clients),
                return_exceptions=True,
            )
            self.clients.clear()
        self._started = False

    async def __aenter__(self) -> "MrktPool":
        await self.start()
        self._entered = True
        return self

    async def __aexit__(self, *args: Any) -> None:
        try:
            await self.close()
        finally:
            self._entered = False

import asyncio
import urllib.parse
import pyrogram
from .auth import refresh_token


def _pyrogram_proxy(proxy: str | dict | None) -> dict | None:
    if proxy is None or isinstance(proxy, dict):
        return proxy

    parsed = urllib.parse.urlsplit(proxy if "://" in proxy else f"http://{proxy}")
    if not parsed.hostname or parsed.port is None:
        raise ValueError("proxy must contain a hostname and port")

    scheme = parsed.scheme.lower()
    if scheme not in {"http", "socks4", "socks5"}:
        raise ValueError(f"Unsupported Pyrogram proxy scheme: {scheme}")

    result = {
        "scheme": scheme,
        "hostname": parsed.hostname,
        "port": parsed.port,
    }
    if parsed.username:
        result["username"] = urllib.parse.unquote(parsed.username)
    if parsed.password:
        result["password"] = urllib.parse.unquote(parsed.password)
    return result


async def get_init_data(
    session: str,
    workdir: str = ".",
    proxy: str | dict | None = None,
    username: str = "mrkt",
) -> str:
    async with pyrogram.Client(
        session,
        workdir=workdir,
        proxy=_pyrogram_proxy(proxy),
    ) as cli:
        bot = await cli.resolve_peer(username)
        url = await cli.get_main_web_app(bot.user_id, bot.user_id)
        init_data = urllib.parse.parse_qs(
            urllib.parse.urlsplit(url).query
        ).get("tgWebAppData")
        if not init_data or not init_data[0]:
            raise ValueError("Telegram WebApp URL does not contain tgWebAppData")
        return init_data[0]


async def get_tokens(
    sessions: list[str],
    *,
    workdir: str = ".",
    proxy: str | dict | None = None,
    concurrency: int = 5
) -> list[str]:
    if concurrency < 1:
        raise ValueError("concurrency must be greater than zero")

    results: list[str | None] = [None] * len(sessions)
    next_index = 0

    async def worker() -> None:
        nonlocal next_index
        while next_index < len(sessions):
            index = next_index
            next_index += 1
            try:
                results[index] = await refresh_token(
                    sessions[index],
                    workdir=workdir,
                    proxy=proxy,
                )
            except Exception as exc:
                raise RuntimeError(
                    f"Failed to refresh Telegram session at index {index}"
                ) from exc

    worker_results = await asyncio.gather(
        *(worker() for _ in range(min(concurrency, len(sessions)))),
        return_exceptions=True,
    )
    for result in worker_results:
        if isinstance(result, BaseException):
            raise result

    return [result for result in results if result is not None]

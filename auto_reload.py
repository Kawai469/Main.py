import asyncio
from pathlib import Path
from typing import Dict, List


def get_cog_files(cogs_dir: Path) -> List[str]:
    if not cogs_dir.exists():
        return []

    return [
        path.name
        for path in sorted(cogs_dir.iterdir())
        if path.is_file() and path.suffix == ".py" and path.name != "__init__.py"
    ]


class AutoReloader:
    def __init__(self, bot, cogs_dir: str, interval: float = 2.0):
        self.bot = bot
        self.cogs_dir = Path(cogs_dir)
        self.interval = interval
        self._last_mtimes: Dict[str, float] = {}

    def _get_mtimes(self) -> Dict[str, float]:
        result = {}
        for name in get_cog_files(self.cogs_dir):
            path = self.cogs_dir / name
            result[name] = path.stat().st_mtime
        return result

    async def reload_changed_cogs(self) -> int:
        current = self._get_mtimes()
        changed = []

        for name, mtime in current.items():
            prev = self._last_mtimes.get(name)
            if prev is None or mtime != prev:
                changed.append(name)

        self._last_mtimes = current

        for name in changed:
            cog_name = f"cogs.{Path(name).stem}"
            try:
                await self.bot.reload_extension(cog_name)
                print(f"Reloaded {cog_name}")
            except Exception as exc:
                print(f"Failed to reload {cog_name}: {exc}")

        return len(changed)

    async def run(self):
        while True:
            await self.reload_changed_cogs()
            await asyncio.sleep(self.interval)

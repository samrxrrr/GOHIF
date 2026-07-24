from __future__ import annotations

import asyncio
import sys
from pathlib import Path

from gae.executor.parallel import ParallelExecutor
from gae.registry.plugin_registry import PluginRegistry
from gae.plugins.http.plugin import HTTPPlugin


async def main():

    if len(sys.argv) != 2:
        raise SystemExit(
            "Usage: python -m gae.cli.batch batchfile.txt"
        )

    batch_file = Path(sys.argv[1])

    manifests = []

    with batch_file.open() as f:

        for line in f:

            line = line.strip()

            if not line:
                continue

            if line.startswith("#"):
                continue

            manifests.append(Path(line))

    registry = PluginRegistry()

    registry.register(
        "http",
        HTTPPlugin,
    )

    executor = ParallelExecutor(
        registry,
        workers=4,
    )

    results = await executor.execute(
        manifests
    )

    successful = 0

    failed = 0

    for result in results:

        print(result)

        if result["success"]:
            successful += 1
        else:
            failed += 1

    print()

    print("====================================")
    print("Batch Summary")
    print("====================================")
    print(f"Total      : {len(results)}")
    print(f"Successful : {successful}")
    print(f"Failed     : {failed}")


if __name__ == "__main__":
    asyncio.run(main())

#!/usr/bin/env bash
set -e

export PYTHONPATH=src

BATCH=$1

while read manifest
do
    [ -z "$manifest" ] && continue

    echo
    echo "=========================================="
    echo "Running: $manifest"
    echo "=========================================="

    python -m gae.cli.main "$manifest"

done < "$BATCH"

echo
echo "Batch Complete."

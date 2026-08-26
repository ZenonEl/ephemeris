#!/usr/bin/env python3
"""Сверить номер версии во всех местах, где он записан.

Манифестов три — Claude Code, его маркетплейс и Codex, — плюс бейджи в двух
README. Оба хоста при обновлении сравнивают ТОЛЬКО номер версии: отставший
манифест означает, что правка не доедет до установленных копий, а команда
обновления отрапортует, что всё уже свежее. Расхождение тихое, поэтому проверка
машинная.
"""
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent


def read(path, get):
    p = ROOT / path
    if not p.exists():
        return path, None, "файла нет"
    try:
        return path, get(json.loads(p.read_text(encoding="utf-8"))), None
    except Exception as exc:                      # noqa: BLE001
        return path, None, str(exc)


def badge(path):
    p = ROOT / path
    if not p.exists():
        return path, None, "файла нет"
    m = re.search(r"badge/version-([0-9]+\.[0-9]+\.[0-9]+)-", p.read_text(encoding="utf-8"))
    return path, (m.group(1) if m else None), (None if m else "бейдж версии не найден")


found = [
    read(".claude-plugin/plugin.json", lambda d: d["version"]),
    read(".claude-plugin/marketplace.json", lambda d: d["plugins"][0]["version"]),
    read(".codex-plugin/plugin.json", lambda d: d["version"]),
    badge("README.md"),
    badge("README.ru.md"),
]

width = max(len(p) for p, _, _ in found)
versions = set()
broken = False

for path, version, err in found:
    if err:
        print(f"  {path:<{width}}  ОШИБКА: {err}")
        broken = True
        continue
    print(f"  {path:<{width}}  {version}")
    versions.add(version)

if broken:
    sys.exit(1)

if len(versions) == 1:
    print(f"\nверсии совпадают: {versions.pop()}")
    sys.exit(0)

print(f"\nРАСХОЖДЕНИЕ: {', '.join(sorted(versions))}")
sys.exit(1)

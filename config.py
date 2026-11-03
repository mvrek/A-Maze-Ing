#!/usr/bin/env python3

class ConfigError(Exception):
    """The configuration file is unreadable or invalid."""


def read_config(path: str) -> dict[str, str]:
    try:
        with open(path, encoding="utf-8") as stream:
            lines = stream.read().splitlines()
    except (OSError, UnicodeDecodeError) as error:
        raise ConfigError(f"cannot read '{path}': {error}") from error

    values: dict[str, str] = {}
    for number, raw in enumerate(lines, start=1):
        line = raw.strip()

        if not line or line.startswith("#"):
            continue

        if "=" not in line:
            raise ConfigError(f"ERROR: line {number}: expected"
                              f" KEY=VALUE, got '{line}'")

        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip()

        if not key or key in values:
            raise ConfigError(f"ERROR: line {number}: empty or "
                              f"duplicated key '{key}'")

        values[key] = value

    return values


def _parse_int(key: str, text: str) -> int:
    try:
        int(text)
    except ValueError:
        raise ConfigError(f"{key}: '{text}' is not an integer")
    return text


def _parse_point(key: str, text: str) -> tuple[int, int]:
    parts: tuple[str, str] = text.split(",")
    if len(parts) != 2:
        raise ConfigError(f"ERROR: ")

if __name__=="__main__":
    print(read_config("/home/lfoti/Desktop/A-Maze-Ing/config.txt"))

    #TODO CONTINUARE PARSING#
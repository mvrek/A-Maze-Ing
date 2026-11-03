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
            raise ConfigError(f"line {number}: expected"
                              f" KEY=VALUE, got '{line}'")

        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip()

        if not key or key in values:
            raise ConfigError(f"line {number}: empty or "
                              f"duplicated key '{key}'")

        values[key] = value

    return values

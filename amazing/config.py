"""Reading and validation of the configuration file."""

from dataclasses import dataclass


class ConfigError(Exception):
    """The configuration file is unreadable or invalid."""


def read_config(path: str) -> dict[str, str]:
    """Reads config.txt and returns values."""
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


def _parse_int(key: str, text: str) -> int:
    """Convert text to an integer.

    Raises:
        ConfigError: if text is not an integer.
    """
    try:
        return int(text)
    except ValueError:
        raise ConfigError(f"{key}: '{text}' is not an integer")


def _parse_point(key: str, text: str) -> tuple[int, int]:
    """Convert 'x,y' to a (x, y) tuple of integers.

    Raises:
        ConfigError: if text is not two comma-separated integers.
    """
    parts: list[str] = text.split(",")
    if len(parts) != 2:
        raise ConfigError(f"unexpected format: {key}: "
                          f"'{text}' Use 'x,y' format instead")
    x = _parse_int(key, parts[0].strip())
    y = _parse_int(key, parts[1].strip())
    return (x, y)


def _parse_bool(key: str, text: str) -> bool:
    """Convert 'True' or 'False' to a bool.

    Raises:
        ConfigError: for any other text.
    """
    if text == "True":
        return True
    if text == "False":
        return False
    raise ConfigError(f"{key}: '{text}' is not True or False")


REQUIRED_KEYS = ("WIDTH", "HEIGHT", "ENTRY", "EXIT",
                 "OUTPUT_FILE", "PERFECT")


@dataclass(frozen=True)
class Config:
    """Validated maze generation settings."""

    width: int
    height: int
    entry: tuple[int, int]
    exit_pos: tuple[int, int]
    output_file: str
    perfect: bool
    seed: int | None = None


def _validate(config: Config) -> None:
    """Check the constraints between settings.

    Raises:
        ConfigError: if a setting is out of range or inconsistent.
    """
    if config.width < 1:
        raise ConfigError(
            f"WIDTH must be at least 1, got {config.width}."
        )
    if config.height < 1:
        raise ConfigError(
            f"HEIGHT must be at least 1, got {config.height}."
        )
    for name, (x, y) in (
        ("ENTRY", config.entry),
        ("EXIT", config.exit_pos)
    ):
        if not (0 <= x < config.width and 0 <= y < config.height):
            raise ConfigError(
                f"{name} ({x}, {y}) is outside the "
                f"{config.width}x{config.height} maze"
            )
    if config.entry == config.exit_pos:
        raise ConfigError(
            f"ENTRY and EXIT must be different, "
            f"both are {config.entry}"
        )
    if config.output_file == "":
        raise ConfigError("OUTPUT FILE is empty")


def load_config(path: str) -> Config:
    """Read a configuration file and build a Config.

    Raises:
        ConfigError: if the file is unreadable or a value is missing
            or invalid.
    """
    values = read_config(path)
    missing: list[str] = []
    for key in REQUIRED_KEYS:
        if key not in values:
            missing.append(key)
    if missing:
        raise ConfigError(f"missing keys: {', '.join(missing)}")
    seed = (_parse_int("SEED", values["SEED"])
            if "SEED" in values else None)
    config = Config(
        width=_parse_int("WIDTH", values["WIDTH"]),
        height=_parse_int("HEIGHT", values["HEIGHT"]),
        entry=_parse_point("ENTRY", values["ENTRY"]),
        exit_pos=_parse_point("EXIT", values["EXIT"]),
        output_file=values["OUTPUT_FILE"],
        perfect=_parse_bool("PERFECT", values["PERFECT"]),
        seed=seed
    )
    _validate(config)
    return config

from pathlib import Path

PART_FILES = (
    "bootstrap.py",
    "events.py",
    "commands_discovery_raid_dumping.py",
    "commands_account.py",
    "commands_utility.py",
    "commands_text.py",
    "commands_fun_media.py",
    "commands_logging_system.py",
    "commands_moderation.py",
    "commands_memes.py",
    "commands_ai.py",
    "commands_music.py",
    "gui.py",
)

_entry_file = __file__
_parts_dir = Path(_entry_file).resolve().parent / "src" / "parts"

for _filename in PART_FILES:
    _path = _parts_dir / _filename
    _source = _path.read_text(encoding="utf-8")
    __file__ = str(_path)
    exec(compile(_source, str(_path), "exec"), globals(), globals())

__file__ = _entry_file
del _entry_file, _parts_dir, _filename, _path, _source

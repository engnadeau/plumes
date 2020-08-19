from pathlib import Path

from dynaconf import Dynaconf

user_settings_path = Path.home() / ".plumes.toml"
settings_files = [user_settings_path, "settings.toml", ".secrets.toml"]
settings = Dynaconf(envvar_prefix="PLUMES", settings_files=settings_files)

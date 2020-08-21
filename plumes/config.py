from pathlib import Path

from dynaconf import Dynaconf

user_config_path = Path.home() / ".plumes.toml"
package_config_path = Path(__file__).parent / "settings.toml"
settings = Dynaconf(
    envvar_prefix="PLUMES", settings_files=[user_config_path, package_config_path]
)

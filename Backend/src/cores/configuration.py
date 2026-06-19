import os
from pathlib import Path
import logging

from pydantic import Field, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict

# # Logging Setup

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
log = logging.getLogger(__name__)

"""Application configuration module for environment-based settings."""

# Path Logic
ROOT_DIR = Path(__file__).resolve().parents[3]
APP_ENV = os.getenv("APP_ENV", "dev")

# Define the two files we want to load
ENV_FILES = (ROOT_DIR / f".env.docker.{APP_ENV}", ROOT_DIR / f".env.app.{APP_ENV}")


class BaseConfig(BaseSettings):
    """Base configuration that loads environment files."""

    # All classes inheriting from BaseConfig will now automatically load BOTH env files
    model_config = SettingsConfigDict(env_file=ENV_FILES, extra="ignore")


class NATSConfig(BaseConfig):
    """NATS messaging configuration."""

    host: str = Field(default="localhost", validation_alias="NATS_HOST")
    port: int = Field(default=4222, validation_alias="NATS_PORT")
    user: str = Field(default="nats_user", validation_alias="NATS_USER")
    password: str = Field(default="nats_password", validation_alias="NATS_PASSWORD")


class ValkeyConfig(BaseConfig):
    """Valkey (Redis-compatible) configuration."""

    host: str = Field(default="localhost", validation_alias="VALKEY_HOST")
    port: int = Field(default=6379, validation_alias="VALKEY_PORT")
    password: str = Field(default="password", validation_alias="VALKEY_PASSWORD")


class PostgresConfig(BaseConfig):
    """PostgreSQL database configuration."""

    host: str = Field(default="localhost", validation_alias="POSTGRES_HOST")
    port: int = Field(default=5432, validation_alias="POSTGRES_PORT")
    user: str = Field(default="postgres", validation_alias="POSTGRES_USER")
    password: str = Field(default="password", validation_alias="POSTGRES_PASSWORD")
    db: str = Field(default="postgres", validation_alias="POSTGRES_DB")

    @computed_field
    @property
    def connection_string(self) -> str:
        """Build PostgreSQL connection string."""
        # return f"host={self.host} port={self.port} user={self.user} password={self.password} dbname={self.db}"
        return (
            f"host={self.host} port={self.port} "
            f"user={self.user} password={self.password} "
            f"dbname={self.db}"
        )


class AppConfig(BaseConfig):
    """Application-level configuration."""

    port: int = Field(5000, validation_alias="APP_PORT")
    host: str = Field("localhost", validation_alias="APP_HOST")
    tz: str = Field("UTC", validation_alias="TZ")
    namespace: str = Field("DEFAULT", validation_alias="DEFAULT_NAMESPACE")
    base_dir: Path = ROOT_DIR / "Data_Lake"


class Settings(BaseSettings):
    """Main settings container combining all configs."""

    model_config = SettingsConfigDict(env_file=ENV_FILES, extra="ignore")

    app: AppConfig = AppConfig()
    nats: NATSConfig = NATSConfig()
    valkey: ValkeyConfig = ValkeyConfig()
    postgres: PostgresConfig = PostgresConfig()


# Singleton instance
settings = Settings()


# ==========================================
# Path Logic 2.0
# ==========================================
class PathManager:
    def __init__(self, base_dir: Path):
        # 1. Root groups
        self.public = base_dir / "Public"
        self.bin = base_dir / "Bin"

        # 2. System folders
        self.system_paths = {
            "logs": self.bin / "Logs",
            "state_manager": self.bin / "State_Manager",
            "backups": self.bin / "Backups",
            "downloads": self.bin / "Downloads",
        }

        # # 3. Data folders
        # self.data_paths = {
        #     "init": self.public / "Data_Init",
        #     "archive": self.public / "Archives",
        # }

        # # 4. Dataset Specifics (depends on data_paths["archive"])
        # archive = self.data_paths["archive"]
        # self.datasets = {
        #     "compressed": archive / "Compressed_Archive",
        #     "audit": archive / "Audit",
        #     "corporate_actions": archive / "DataSet=Manual_Corporate_Actions",
        #     "pr_zip": archive / "DataSet=PR_zip",
        #     "pd_files": archive / "DataSet=PD_files",
        #     "bc_files": archive / "DataSet=BC_files",
        #     "mcap_files": archive / "DataSet=Mcap_files",
        #     "var_files": archive / "DataSet=VAR_files",
        #     "debug": archive / "Process=debug",
        # }

        # --- THE FIX: Call injection for all dictionaries ---
        self._inject_paths(self.system_paths)
        # self._inject_paths(self.data_paths)
        # self._inject_paths(self.datasets)

    def _inject_paths(self, path_dict: dict):
        """Converts dictionary keys into class attributes for dot-notation access."""
        for key, path in path_dict.items():
            setattr(self, key, path)

    def create_all(self):
        """
        Automatically finds all Path objects or Dictionaries of Paths
        and creates them on the disk.
        """
        paths_to_create = []

        # Iterate through all attributes of this class
        for value in vars(self).values():
            # If it's a direct Path object (like self.public or injected attributes)
            if isinstance(value, Path):
                paths_to_create.append(value)

            # If it's a dictionary (like self.datasets), add its values
            elif isinstance(value, dict):
                for item in value.values():
                    if isinstance(item, Path):
                        paths_to_create.append(item)

        # Create the folders
        for path in paths_to_create:
            try:
                path.mkdir(parents=True, exist_ok=True)
                #     print(f"Ensured directory exists: {path}")
                # except Exception as e:
                #     print(f"Failed to create directory {path}: {e}")
                log.info("Ensured directory exists: %s", path)
            except OSError as e:
                log.error("Failed to create directory %s: %s", path, e)


# ==========================================
# EXECUTION
# ==========================================

# Initialize Paths
paths = PathManager(settings.app.base_dir)
paths.create_all()

# # Now these all work perfectly without keys!
# print(paths.logs)              # From system_paths
# print(paths.state_manager)     # From system_paths
# print(paths.init)              # From data_paths
# print(paths.archive)           # From data_paths
# print(paths.corporate_actions) # From datasets
# print(paths.debug)             # From datasets

from dataclasses import dataclass
import yaml


@dataclass
class Config:
    persist_message_to_thread: bool

    @classmethod
    def from_yaml(cls, file_path: str):
        with open(file_path, "r") as file:
            config_dict = yaml.safe_load(file)
        return cls(**config_dict)

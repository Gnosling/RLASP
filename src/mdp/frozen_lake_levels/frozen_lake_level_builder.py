from .frozen_lake_level_4x4 import FrozenLakeLevel4x4


class FrozenLakeLevelBuilder:

    # TODO: extend!
    @staticmethod
    def build_level(level: str):
        if level == "4x4":
            return FrozenLakeLevel4x4()

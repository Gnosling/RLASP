from .frozen_lake_level_4x4 import FrozenLakeLevel4x4
from .frozen_lake_level_8x8 import FrozenLakeLevel8x8


class FrozenLakeLevelBuilder:

    # TODO: extend!
    @staticmethod
    def build_level(level: str):
        if level == "4x4":
            return FrozenLakeLevel4x4()
        elif level == '8x8':
            return FrozenLakeLevel8x8()

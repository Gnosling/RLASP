from .frozen_lake_level_4x4_A import FrozenLakeLevel4x4_A
from .frozen_lake_level_4x4_B import FrozenLakeLevel4x4_B
from .frozen_lake_level_5x5_A import FrozenLakeLevel5x5_A
from .frozen_lake_level_8x8 import FrozenLakeLevel8x8


class FrozenLakeLevelBuilder:

    # TODO: extend!
    @staticmethod
    def build_level(level: str):
        if level == "4x4_A":
            return FrozenLakeLevel4x4_A()
        elif level == '4x4_B':
            return FrozenLakeLevel4x4_A()
        elif level == '5x5_A':
            return FrozenLakeLevel5x5_A()
        elif level == '8x8':
            return FrozenLakeLevel8x8()

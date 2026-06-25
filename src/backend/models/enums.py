try:
    from enum import StrEnum
except ImportError:  # Python 3.10 on the development board does not include StrEnum.
    from enum import Enum

    class StrEnum(str, Enum):
        pass


class MaterialCategory(StrEnum):
    electronic_component = "electronic_component"
    power_fitting = "power_fitting"
    tool = "tool"
    consumable = "consumable"
    unknown = "unknown"


class TaskState(StrEnum):
    queued = "queued"
    detecting = "detecting"
    planning = "planning"
    moving = "moving"
    verifying = "verifying"
    succeeded = "succeeded"
    failed = "failed"
    cancelled = "cancelled"
    paused = "paused"


class TaskType(StrEnum):
    pick_sort = "pick_sort"
    stack = "stack"


class ArmState(StrEnum):
    offline = "offline"
    initializing = "initializing"
    idle = "idle"
    detecting = "detecting"
    planning = "planning"
    moving = "moving"
    paused = "paused"
    stopped = "stopped"
    fault = "fault"

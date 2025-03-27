from enum import Enum


class InteractionStatus(Enum):
    SUCCESS = "SUCCESS"  # Banner was successfully handled
    NOT_FOUND = "NOT_FOUND"  # Banner couldn't be found
    FAILED = "FAILED"  # Interaction failed but banner exists

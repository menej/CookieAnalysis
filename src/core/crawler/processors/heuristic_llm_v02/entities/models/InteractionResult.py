from dataclasses import dataclass

from src.core.crawler.processors.heuristic_llm_v02.entities.enums.InteractionStatus import InteractionStatus


@dataclass
class InteractionResult:
    result: InteractionStatus
    redirected: bool = False
    any_force_clicks: bool = False
    num_clicks: int = 0

from enum import Enum


class CrawlMode(Enum):
    # Algorithm based on heuristics with the usage of LLM
    HEURISTIC_LLM = "HEURISTIC_LLM"

    # Plugin combination of Consent-o-Matic and SuperAgent
    PLGN_DUAL_COM_SA = "PLGN_COM_SA"
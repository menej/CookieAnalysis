from importlib.metadata import metadata
from typing import Optional, Any
from pydantic import BaseModel


class SystemSettings(BaseModel):
    num_attempt: int
    num_crawls: int
    allow_invisible: bool
    llm_model_used: str
    min_consensus: float
    num_llm_attempts: int
    strict_consensus: bool


class AcceptMainLevel(BaseModel):
    level_reached: bool = False
    level_success: bool = False
    found_best_candidate: bool = False
    is_visible: bool = False
    banner_text: str = ""
    banner_z_index: Optional[int] = None
    banner_position: Optional[str] = None
    banner_disappeared: bool = False
    redirected: bool = False
    num_clicks: int = 0
    any_force_clicks: bool = False
    llm_response_raw: Optional[str] = None
    llm_response_parsed: Optional[dict] = None
    llm_consensus_reached: bool = False
    llm_consensus_value: float = 0
    element_text: Optional[str] = None
    element_ambiguous: bool = False
    element_evidence: str = ""

class DeclineMainLevel(BaseModel):
    level_reached: bool = False
    level_success: bool = False
    found_best_candidate: bool = False
    is_visible: bool = False
    banner_text: str = ""
    banner_z_index: Optional[int] = None
    banner_position: Optional[str] = None
    banner_disappeared: bool = False
    redirected: bool = False
    direct_decline_attempt: bool = False
    num_clicks: int = 0
    any_force_clicks: bool = False
    llm_response_raw: Optional[str] = None
    llm_response_parsed: Optional[dict] = None
    llm_consensus_reached: bool = False
    llm_consensus_value: float = 0
    element_text: Optional[str] = None
    element_ambiguous: bool = False
    element_evidence: str = ""


class DeclineSettingsLevel(BaseModel):
    level_reached: bool = False
    level_success: bool = False
    found_best_candidate: bool = False
    is_visible: bool = False
    banner_text: str = ""
    banner_z_index: Optional[int] = None
    banner_position: Optional[str] = None
    banner_disappeared: bool = False
    redirected: bool = False

    settings_decline_attempt: bool = False
    settings_decline_num_clicks: int = 0
    settings_decline_any_force_clicks: bool = False
    settings_decline_llm_response_raw: Optional[str] = None
    settings_decline_llm_response_parsed: Optional[dict] = None
    settings_decline_llm_consensus_reached: bool = False
    settings_decline_llm_consensus_value: float = 0
    settings_decline_element_text: Optional[str] = None
    settings_decline_element_ambiguous: bool = False
    settings_decline_element_evidence: str = ""

    save_settings_attempt: bool = False
    save_settings_num_clicks: int = 0
    save_settings_any_force_clicks: bool = False
    save_settings_llm_response_raw: Optional[str] = None
    save_settings_llm_response_parsed: Optional[dict] = None
    save_settings_llm_consensus_reached: bool = False
    save_settings_llm_consensus_value: float = 0
    save_settings_element_text: Optional[str] = None


class DeclineStageMetadata(BaseModel):
    system_settings: SystemSettings
    stage_outcome: Optional[str] = None
    main_level: DeclineMainLevel
    settings_level: DeclineSettingsLevel


class AcceptStageMetadata(BaseModel):
    system_settings: SystemSettings
    stage_outcome: Optional[str] = None
    main_level: AcceptMainLevel


def initialize_metadata_accept_stage(
        num_attempt: int,
        num_crawls: int,
        allow_invisible: bool,
        llm_model_used: str,
        min_consensus: float,
        num_llm_attempts: int,
        strict_consensus: bool
) -> AcceptStageMetadata:
    system_settings = SystemSettings(
        num_attempt=num_attempt,
        num_crawls=num_crawls,
        allow_invisible=allow_invisible,
        llm_model_used=llm_model_used,
        min_consensus=min_consensus,
        num_llm_attempts=num_llm_attempts,
        strict_consensus=strict_consensus,
    )
    main_level = AcceptMainLevel()

    return AcceptStageMetadata(
        system_settings=system_settings,
        stage_outcome=None,
        main_level=main_level,
    )


def initialize_metadata_decline_stage(
        num_attempt: int,
        num_crawls: int,
        allow_invisible: bool,
        llm_model_used: str,
        min_consensus: float,
        num_llm_attempts: int,
        strict_consensus: bool
) -> DeclineStageMetadata:
    system_settings = SystemSettings(
        num_attempt=num_attempt,
        num_crawls=num_crawls,
        allow_invisible=allow_invisible,
        llm_model_used=llm_model_used,
        min_consensus=min_consensus,
        num_llm_attempts=num_llm_attempts,
        strict_consensus=strict_consensus,
    )
    main_level = DeclineMainLevel()
    settings_level = DeclineSettingsLevel()

    return DeclineStageMetadata(
        system_settings=system_settings,
        stage_outcome=None,
        main_level=main_level,
        settings_level=settings_level
    )

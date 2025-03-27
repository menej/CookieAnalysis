from src.core.crawler.processors.heuristic_llm.entities.enums.BannerInteraction import BannerInteraction


def get_interaction_screenshot_filename(
        interaction_type: BannerInteraction,
        attempt: int,
        suffix: str = "",
        click_num: int = None) -> str:
    if interaction_type == BannerInteraction.ACCEPT:
        base = "accept_interaction"
    elif interaction_type == BannerInteraction.DECLINE:
        base = "decline_interaction"
    elif interaction_type == BannerInteraction.SETTINGS:
        base = "decline_interaction_settings"
    elif interaction_type == BannerInteraction.SAVE:
        base = "decline_interaction_save"
    else:
        base = "interaction"

    if click_num is not None:
        return f"{base}_{attempt}_click_{click_num}{f'_{suffix}' if suffix else ''}.png"

    return f"{base}_{attempt}{f'_{suffix}' if suffix else ''}.png"

def get_health_status(nutrition_summary):
    if (
        nutrition_summary["protein"] == "low"
        or nutrition_summary["fiber"] == "low"
        or nutrition_summary["fat"] == "high"
    ):
        return "red"
    return "green"

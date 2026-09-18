from typing import Dict, Any


def get_seasonal_baseline(biome: str, month: int) -> float:
    """Returns the expected seasonal phenological baseline NDVI for a biome and calendar month."""
    # Peak wet season / monsoon yields higher greenness (months 7, 8, 9)
    if "Deciduous" in biome or "Sal" in biome:
        if month in [7, 8, 9, 10]:
            return 0.78
        elif month in [3, 4, 5]:
            return 0.62  # Dry season leaf fall
        else:
            return 0.71
    elif "Rainforest" in biome:
        return 0.82  # Evergreen constant
    elif "Savanna" in biome:
        if month in [11, 12, 1, 2, 3]:
            return 0.68
        else:
            return 0.52
    return 0.70

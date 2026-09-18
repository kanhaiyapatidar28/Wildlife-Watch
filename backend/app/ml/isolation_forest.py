def compute_anomaly_score(delta_ndvi: float, historical_variance: float = 0.05) -> float:
    """
    Computes spectral anomaly score (Z-score / Isolation score proxy) for change detection triage.
    Returns value between -1.0 (severe anomaly) and 1.0 (normal).
    """
    if historical_variance == 0.0:
        historical_variance = 0.05
    z_score = delta_ndvi / historical_variance
    # Normalize
    if z_score < -3.0:
        return -0.95
    elif z_score < -2.0:
        return -0.75
    elif z_score < -1.0:
        return -0.40
    return 0.10

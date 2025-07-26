def calculate_spread(ltv_a, ltv_b):
    return round(ltv_a - ltv_b, 4)

def is_within_band(ltv, target, band):
    return abs(ltv - target) <= band

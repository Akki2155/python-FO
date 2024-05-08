def calculate_standard_pivot_point(high, low, close):
    pivot_point = (high + low + close) / 3
    return pivot_point

def calculate_fibonacci_pivot_points(high, low, close):
    pivot_point = (high + low + close) / 3
    s1 = pivot_point - 0.382 * (high - low)
    r1 = pivot_point + 0.382 * (high - low)
    return s1, r1

def calculate_s1_r1(high, low, close):
    pivot_point = (high + low + close) / 3
    s1 = 2 * pivot_point - high
    r1 = 2 * pivot_point - low
    return s1, r1

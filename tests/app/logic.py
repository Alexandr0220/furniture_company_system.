def calculate_production_time(times_in_workshops: list[int]) -> int:
    total = 0
    for t in times_in_workshops:
        if t is None or t < 0:
            return -1
        total += int(t)
    return total

def calculate_raw_material(product_type_coef: float, material_loss_percent: float, quantity: int, param1: float, param2: float) -> int:
    if quantity <= 0 or param1 <= 0 or param2 <= 0:
        return -1
    if product_type_coef <= 0 or material_loss_percent < 0:
        return -1

    base = param1 * param2 * product_type_coef
    total = base * quantity
    total_with_loss = total * (1 + material_loss_percent / 100.0)
    return int(total_with_loss)

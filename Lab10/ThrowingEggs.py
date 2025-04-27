def find_critical_floor(critical_floor: int, max_floor: int = 100):
    step = 14  # x + (x-1) + (x-2) + ... + 1 ≥ 100 решая x(x+1)/2 ≥ 100, находим x = 14
    current_floor = step
    drops = 0
    eggs = 2
    prev_floor = -1

    while eggs > 1 and current_floor <= max_floor:
        drops += 1
        if current_floor >= critical_floor:
            eggs -= 1
            break
        step -= 1
        prev_floor = current_floor
        current_floor += step

    if eggs == 1:
        current_floor = prev_floor + 1
        while current_floor <= max_floor:
            drops += 1
            if current_floor >= critical_floor:
                return current_floor, drops
            current_floor += 1

    return current_floor-2, drops


for n in range(0, 101):
    found, attempts = find_critical_floor(n)
    assert found == n, f"Failed for {n} != {found}"
    print(f"Этаж {n}: найдено за {attempts} бросков")

MENU = {
    'Hamburger': 80,
    'Pizza': 120,
    'Kola': 20,
    'Salata': 30,
    'Tatlı': 45,
}

MENU_IMAGES = {
    'Hamburger': 'hamburger.jpg',
    'Pizza': 'pizza.jpg',
    'Kola': 'kola.jpg',
    'Salata': 'salata.jpg',
    'Tatlı': 'tatli.jpg',
}


def price_order(names, quantities):
    if not names:
        raise ValueError('empty')

    total = 0
    parts = []
    lines = []
    for name, raw_quantity in zip(names, quantities):
        if name not in MENU:
            raise ValueError('unknown item')
        quantity = int(raw_quantity)
        if quantity < 1:
            raise ValueError('quantity')
        unit_price = MENU[name]
        line_total = unit_price * quantity
        total += line_total
        parts.append(f'{name} (x{quantity})')
        lines.append({
            'name': name,
            'quantity': quantity,
            'unit_price': unit_price,
            'line_total': line_total,
        })
    return total, ', '.join(parts), lines

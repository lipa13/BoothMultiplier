# Funkcja pomocnicza do konwersji liczby na listę bitów
def int_to_bits(n, width):
    bits = [int(b) for b in f'{n:0{width}b}']
    return bits[::-1]  # Odwrócenie bitów, aby indeksacja była od najmłodszego do najstarszego

# Algorytm mnożenia Bootha radix-8 (Full-width) z poprawioną indeksacją
def booth_radix8_full(x, y):
    # Uzyskanie bitów mnożnika z poprawną indeksacją
    y_bits = int_to_bits(y, 9)  # Przyjmujemy 8-bitowy mnożnik
    w = (len(y_bits) + 2) // 3  # Liczba częściowych produktów

    # Lista do przechowywania częściowych produktów
    partial_products = []

    # Generowanie częściowych produktów z kontrolą indeksowania
    for i in range(w):
        # Bezpieczne indeksowanie, aby uniknąć "index out of range"
        if 3 * i + 2 < len(y_bits):
            # Ustawienie bitu overlap, jeśli jest poza zakresem, używając wartości domyślnej
            overlap_bit = y_bits[3 * i - 1] if (3 * i - 1) >= 0 else 0

            # Obliczenie wartości di
            di = -4 * y_bits[3 * i + 2] + 2 * y_bits[3 * i + 1] + y_bits[3 * i] + overlap_bit

            # Wybór odpowiedniej operacji w zależności od wartości di
            if di == 0:
                partial_products.append(0)
            elif di == 1:
                partial_products.append(x << (3 * i))
            elif di == 2:
                partial_products.append((x << 1) << (3 * i))
            elif di == 3:
                partial_products.append((x + (x << 1)) << (3 * i))
            elif di == 4:
                partial_products.append((x << 2) << (3 * i))
            elif di == -1:
                partial_products.append((~x + 1) << (3 * i))
            elif di == -2:
                partial_products.append(~((x << 1)) + 1 << (3 * i))
            elif di == -3:
                partial_products.append(~((x + (x << 1))) + (1 << (3 * i)))
            elif di == -4:
                partial_products.append(~((x << 2) + 1 << (3 * i)))

    # Sumowanie wszystkich częściowych produktów
    result = sum(partial_products)

    return result


# Test algorytmu z przykładowymi wartościami
x = 5000  # Mnożna
y = 128  # Mnożnik

# Wynik dla wersji full-width
result_full = booth_radix8_full(x, y)
print("Wynik radix-8 (full-width):", result_full)
import time

# Funkcja pomocnicza do konwersji liczby na listę bitów
def int_to_bits(n, width):
    # Jeśli liczba bitów nie jest podzielna przez 2, powielić bity znaku
    if width % 2 != 0:
        # Obliczanie liczby dodatkowych bitów znaku
        additional_sign_bits = 2 - (width % 2)

        # Rozszerzenie liczby bitów o dodatkowe bity znaku
        width += additional_sign_bits

    # Dla liczby ujemnej dodaj odpowiednią wartość do konwersji na dopełnienie do dwóch
    if n < 0:
        n = (1 << width) + n

    bits = [int(b) for b in f'{n:0{width}b}']

    return bits[::-1]  # Odwrócenie bitów, aby indeksacja była od najmłodszego do najstarszego


# Algorytm mnożenia Bootha radix-4 (Full-width)
def booth_radix4_full(x, y):
    # Uzyskanie bitowej reprezentacji mnożnika
    y_bits = int_to_bits(y, 10)
    w = (len(y_bits) + 1) // 2  # Liczba częściowych produktów

    # Lista do przechowywania częściowych produktów
    partial_products = []

    # Generowanie częściowych produktów z kontrolą indeksowania
    for i in range(w):
        # Ustawienie bitu overlap, jeśli jest poza zakresem, używając wartości domyślnej
        overlap_bit = y_bits[2 * i - 1] if (2 * i - 1) >= 0 else 0

        # Obliczenie wartości di
        di = -2 * y_bits[2 * i + 1] + y_bits[2 * i] + overlap_bit


        if di == 0:
            partial_product = 0
        elif di == 1:
            partial_product = x
        elif di == 2:
            partial_product = (x << 1)
        elif di == -1:
            partial_product = (~x + 1)
        elif di == -2:
            partial_product = ~(x << 1) + 1

        partial_product_shifted = partial_product << (2 * i)  # Przesunięcie i dodanie do listy częściowych produktów
        partial_products.append(partial_product_shifted)

    # Sumowanie wszystkich częściowych produktów
    result = sum(partial_products)

    return result


def booth_radix4_fixed(x, y, n):
    mask = ((1 << (2 * n)) - 1) ^ ((1 << n) - 1)

    result = booth_radix4_full(x, y) & mask

    return result


# Test algorytmu z przykładowymi wartościami
x = 7  # Mnożna
y = 12  # Mnożnik


# Wynik mnożenia radix-4 full-width

start_time = time.perf_counter()
result_full = booth_radix4_full(x, y)
end_time = time.perf_counter()
time_in_micro = (end_time - start_time) * (10 ** 6)
print("Wynik mnożenia radix-4 full-width:", result_full)
print("Czas dzialania algorytmu: ", round(time_in_micro, 2))


# Wynik mnożenie radix-4 post-truncated

n = 4  # liczba bitow mnoznika i mnoznej (wynik mnozenia: 2n + 1)
start_time = time.perf_counter()
result_post_truncated = booth_radix4_fixed(x, y, n)
end_time = time.perf_counter()
time_in_micro = (end_time - start_time) * (10 ** 6)
print("Wynik mnożenia radix-4 fixed-width post-truncated:", result_post_truncated)
print("Czas dzialania algorytmu: ", round(time_in_micro, 2))
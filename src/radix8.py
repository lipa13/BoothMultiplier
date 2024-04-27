# Funkcja pomocnicza do konwersji liczby na listę bitów
def int_to_bits(n, width):

    # Jeśli liczba bitów nie jest podzielna przez 3, powielić bity znaku
    if width % 3 != 0:
        # Obliczanie liczby dodatkowych bitów znaku
        additional_sign_bits = 3 - (width % 3)

        # Rozszerzenie liczby bitów o dodatkowe bity znaku
        width += additional_sign_bits

    # Dla liczby ujemnej dodaj odpowiednią wartość do konwersji na dopełnienie do dwóch
    if n < 0:
        n = (1 << width) + n

    bits = [int(b) for b in f'{n:0{width}b}']

    return bits[::-1]  # Odwrócenie bitów, aby indeksacja była od najmłodszego do najstarszego


# Algorytm mnożenia Bootha radix-8 (Full-width)
def booth_radix8_full(x, y):
    # Uzyskanie bitowej reprezentacji mnożnika
    y_bits = int_to_bits(y, 10)
    w = (len(y_bits) + 2) // 3  # Liczba częściowych produktów

    # Lista do przechowywania częściowych produktów
    partial_products = []

    # Generowanie częściowych produktów z kontrolą indeksowania
    for i in range(w):
            # Ustawienie bitu overlap, jeśli jest poza zakresem, używając wartości domyślnej
            overlap_bit = y_bits[3 * i - 1] if (3 * i - 1) >= 0 else 0

            # Obliczenie wartości di
            di = -4 * y_bits[3 * i + 2] + 2 * y_bits[3 * i + 1] + y_bits[3 * i] + overlap_bit

            # Wybór odpowiedniej operacji w zależności od wartości di
            """if di == 0:
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
                partial_products.append(~((x << 2) + 1 << (3 * i)))"""

            # Generate the partial product with controlled shifting
            partial_product = x*di

            # Shift and apply mask to ensure fixed-width without affecting the sign bit
            partial_product_shifted = partial_product << (3 * i)

            partial_products.append(partial_product_shifted)

    # Sumowanie wszystkich częściowych produktów
    result = sum(partial_products)

    return result


def booth_radix8_post_truncated(x, y, n):
    # Musimy wyliczyc ile bitow bedzie mial wynik (2n+1) i ograniczyc  czesciowe do n bitow (starszych, mlodsze ucinamy)
    #mask = ((1 << (n+1)) - 1) << n
    mask = ((1 << (2 * n)) - 1) ^ ((1 << n) - 1)

    result = booth_radix8_full(x, y) & mask

    return result


# Test algorytmu z przykładowymi wartościami
x = 7 # Mnożna
y = 7 # Mnożnik

# Wynik mnozenia radix-8 full-width
result_full = booth_radix8_full(x, y)
print("Wynik mnożenia radix-8 full-width:", result_full)

n = 4 # liczba bitow mnoznika i mnoznej (wynik mnozenia: 2n + 1)

result_post_truncated = booth_radix8_post_truncated(x, y, n)
print("Post-truncated radix-8 result:", result_post_truncated)

import random
import time

def half_adder(bit1, bit2):
    sum_bit = bit1 ^ bit2
    carry_out = bit1 & bit2
    return sum_bit, carry_out

def full_adder(bit1, bit2, carry_in):
    half_sum, half_carry = half_adder(bit1, bit2)
    final_sum, final_carry = half_adder(half_sum, carry_in)
    carry_out = half_carry | final_carry
    return final_sum, carry_out

def int_to_bits(n, width):
    if width % 3 != 0:
        additional_sign_bits = 3 - (width % 3)
        width += additional_sign_bits

    if n < 0:
        n = (1 << width) + n

    bits = [int(b) for b in f'{n:0{width}b}']
    return bits[::-1]


def bits_to_int(bits):
    n = len(bits)
    result = 0
    for i in range(n):
        result += bits[i] << i

    # Sprawdź, czy liczba jest ujemna (najstarszy bit ustawiony na 1)
    if bits[-1] == 1:
        result -= (1 << n)

    return result


def booth_radix8_full(x, y):
    # zamiana mnożnika na U2
    bit_length = max(x.bit_length(), y.bit_length()) + 1
    bit_length = (bit_length + 2) // 3 * 3
    y_bits = int_to_bits(y, bit_length)
    w = (len(y_bits) + 2) // 3

    # tablica produktów częsciowych (PPA)
    partial_products = []

    # Podzial mnoznika na w grup i wyznaczenie wartości di
    for i in range(w):
        overlap_bit = y_bits[3 * i - 1] if (3 * i - 1) >= 0 else 0
        di = -4 * y_bits[3 * i + 2] + 2 * y_bits[3 * i + 1] + y_bits[3 * i] + overlap_bit

        if di == 0:
            partial_product = 0
        elif di == 1:
            partial_product = x
        elif di == 2:
            partial_product = x << 1
        elif di == 3:
            partial_product = x + (x << 1)
        elif di == 4:
            partial_product = x << 2
        elif di == -1:
            partial_product = -x
        elif di == -2:
            partial_product = -(x << 1)
        elif di == -3:
            partial_product = -(x + (x << 1))
        elif di == -4:
            partial_product = -(x << 2)

        # Dodanie wyznaczonego iloczynu częściowego do PPA
        partial_product_shifted = partial_product << (3 * i)
        partial_product_bits = int_to_bits(partial_product_shifted, 2 * bit_length)
        partial_products.append(partial_product_bits)


    result_bits = [0] * (2 * bit_length)
    carry = 0

    # Jednostka sumująca
    for bit_position in range(2 * bit_length):
        column_sum = carry
        for pp in partial_products:
            if bit_position < len(pp):
                column_sum += pp[bit_position]

        result_bits[bit_position] = column_sum % 2
        carry = column_sum // 2


    result = bits_to_int(result_bits)

    return result


def booth_radix8_fixed(x, y):
    # zamiana mnożnika na U2
    bit_length = max(x.bit_length(), y.bit_length()) + 1
    bit_length = (bit_length + 2) // 3 * 3
    y_bits = int_to_bits(y, bit_length)
    w = (len(y_bits) + 2) // 3

    # tablica produktów częsciowych (PPA)
    partial_products = []

    # Podzial mnoznika na w grup i wyznaczenie wartości di
    for i in range(w):
        overlap_bit = y_bits[3 * i - 1] if (3 * i - 1) >= 0 else 0
        di = -4 * y_bits[3 * i + 2] + 2 * y_bits[3 * i + 1] + y_bits[3 * i] + overlap_bit

        if di == 0:
            partial_product = 0
        elif di == 1:
            partial_product = x
        elif di == 2:
            partial_product = x << 1
        elif di == 3:
            partial_product = x + (x << 1)
        elif di == 4:
            partial_product = x << 2
        elif di == -1:
            partial_product = -x
        elif di == -2:
            partial_product = -(x << 1)
        elif di == -3:
            partial_product = -(x + (x << 1))
        elif di == -4:
            partial_product = -(x << 2)

        # Dodanie wyznaczonego iloczynu częściowego do PPA
        partial_product_shifted = partial_product << (3 * i)
        partial_product_bits = int_to_bits(partial_product_shifted, 2 * bit_length)
        partial_products.append(partial_product_bits)


    result_bits = [0] * 2 * bit_length
    carry = 0

    # Generator przeniesienia - propagacja przeniesienia z młodszych n bitów
    for bit_position in range(bit_length):
        column_sum = carry
        for pp in partial_products:
            column_sum += pp[bit_position]

        carry = column_sum // 2

    # Jednostka sumująca - sumowanie starszych n bitow (z propagowanym przeniesieniem)
    for bit_position in range(bit_length, 2 * bit_length):
        column_sum = carry  # dla n+1 bitu
        for pp in partial_products:
            if bit_position < len(pp):
                column_sum += pp[bit_position]

        result_bits[bit_position] = column_sum % 2
        carry = column_sum // 2

    result = bits_to_int(result_bits)

    return result


"""
# Test algorytmu z przykładowymi wartościami
x = 7  # Mnożna
y = 12  # Mnożnik

time_in_micro = 0

# Petla do pomiarow dla radix-8 full-width
for i in range(100):
    start_time = time.perf_counter()
    result_full = booth_radix8_full(x, y)
    end_time = time.perf_counter()
    time_in_micro += (end_time - start_time) * (10 ** 6)

print("Sredni czas mnozenia radix-8 full-width dla 100 pomiarow: ", time_in_micro / 100.0)
print("Wynik:", result_full)

# Petla do pomiarow dla radix-8 full-width
for i in range(100):
    start_time = time.perf_counter()
    result_fixed = booth_radix8_fixed(x, y)
    end_time = time.perf_counter()
    time_in_micro += (end_time - start_time) * (10 ** 6)
    #print("Wynik mnożenia radix-8 full-width:", result_full)

print("Sredni czas mnozenia radix-8 fixed-width (post-truncated) dla 100 pomiarow: ", time_in_micro / 100.0)
print("Wynik:", result_fixed)
"""

def pomiary_radix_8(n):

    # Losowe operandy n-bitowe (w biarnym n-1-bitowe, wtedy przy konwersji na U2 - n-bitowe)
    x_bits = [0] * n
    y_bits = [0] * n
    time_in_micro = 0

    # 100 pomiarow
    for i in range(100):

        # Najpierw generujemy dwa operandy o dlugosci n bitow w U2
        for bit in range(n):
            x_bits[bit] = random.randrange(2)
            y_bits[bit] = random.randrange(2)

        # Zamiana na int
        x = bits_to_int(x_bits)
        y = bits_to_int(y_bits)

        start_time = time.perf_counter()
        booth_radix8_fixed(x, y)
        end_time = time.perf_counter()

        time_in_micro += (end_time - start_time) * (10 ** 6)

    print(f"Sredni czas mnozenia radix-8 fixed-width (post-truncated) dla 100 pomiarow, dla {n}-bitowych operandow: {round(time_in_micro / 100.0, 2)}")

pomiary_radix_8(80)
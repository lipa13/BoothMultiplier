import time


def int_to_bits(n, width):
    if width % 2 != 0:
        width += 1

    if n < 0:
        n = (1 << width) + n

    bits = [int(b) for b in f'{n:0{width}b}']
    return bits[::-1]

def bits_to_int(bits):
    result = 0
    for i, bit in enumerate(bits):
        result += bit << i
    return result

def booth_radix4_full(x, y):
    bit_length = max(x.bit_length(), y.bit_length()) + 1
    bit_length = (bit_length + 1) // 2 * 2
    x_bits = int_to_bits(x, bit_length)
    y_bits = int_to_bits(y, bit_length)
    w = (len(y_bits) + 1) // 2

    partial_products = []

    for i in range(w):
        overlap_bit = y_bits[2 * i - 1] if (2 * i - 1) >= 0 else 0
        di = -2 * y_bits[2 * i + 1] + y_bits[2 * i] + overlap_bit

        if di == 0:
            partial_product = 0
        elif di == 1:
            partial_product = x
        elif di == 2:
            partial_product = x << 1
        elif di == -1:
            partial_product = -x
        elif di == -2:
            partial_product = -(x << 1)

        partial_product_shifted = partial_product << (2 * i)
        partial_product_bits = int_to_bits(partial_product_shifted, 2 * bit_length)
        partial_products.append(partial_product_bits)

    result_bits = [0] * (2 * bit_length)
    carry = 0

    for bit_position in range(2 * bit_length):
        column_sum = carry
        for pp in partial_products:
            if bit_position < len(pp):
                column_sum += pp[bit_position]

        result_bits[bit_position] = column_sum % 2
        carry = column_sum // 2

    result = bits_to_int(result_bits)

    # Correct the sign if the result is negative
    if result_bits[-1] == 1:
        result -= (1 << (2 * bit_length))

    return result


def booth_radix4_fixed(x, y):
    bit_length = max(x.bit_length(), y.bit_length()) + 1
    bit_length = (bit_length + 1) // 2 * 2
    x_bits = int_to_bits(x, bit_length)
    y_bits = int_to_bits(y, bit_length)
    w = (len(y_bits) + 1) // 2

    partial_products = []

    for i in range(w):
        overlap_bit = y_bits[2 * i - 1] if (2 * i - 1) >= 0 else 0
        di = -2 * y_bits[2 * i + 1] + y_bits[2 * i] + overlap_bit

        if di == 0:
            partial_product = 0
        elif di == 1:
            partial_product = x
        elif di == 2:
            partial_product = x << 1
        elif di == -1:
            partial_product = -x
        elif di == -2:
            partial_product = -(x << 1)

        partial_product_shifted = partial_product << (2 * i)
        partial_product_bits = int_to_bits(partial_product_shifted, 2 * bit_length)
        partial_products.append(partial_product_bits)

    # Wynik o dlugosci 2n (mlodsze n - same 0)
    result_bits = [0] * (2 * bit_length)
    carry = 0

    # Wyliczamy przeniesienie z mlodszych n bitow
    for bit_position in range(bit_length):
        column_sum = carry
        # dla kazdego iloczynu czesciowego:
        for pp in partial_products:
            column_sum += pp[bit_position]

        carry = column_sum // 2

    # Sumowanie starszych n bitow (z propagowanym przeniesieniem)
    for bit_position in range(bit_length, 2 * bit_length):
        column_sum = carry    # dla n+1 bitu
        for pp in partial_products:
            if bit_position < len(pp):
                column_sum += pp[bit_position]

        result_bits[bit_position] = column_sum % 2
        carry = column_sum // 2

    result = bits_to_int(result_bits)

    # Correct the sign if the result is negative
    if result_bits[-1] == 1:
        result -= (1 << (2 * bit_length))

    return result


# Testowanie
x = -7
y = 12

time_in_micro = 0

# Petla do pomiarow dla radix-8 full-width
for i in range(100):
    start_time = time.perf_counter()
    result_full = booth_radix4_full(x, y)
    end_time = time.perf_counter()
    time_in_micro += (end_time - start_time) * (10 ** 6)

print("Sredni czas mnozenia radix-8 full-width dla 100 pomiarow: ", time_in_micro / 100.0)
print("Wynik:", result_full)

# Petla do pomiarow dla radix-8 full-width
for i in range(100):
    start_time = time.perf_counter()
    result_fixed = booth_radix4_fixed(x, y)
    end_time = time.perf_counter()
    time_in_micro += (end_time - start_time) * (10 ** 6)

print("Sredni czas mnozenia radix-8 fixed-width dla 100 pomiarow: ", time_in_micro / 100.0)
print("Wynik:", result_fixed)

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
    result = 0
    for i, bit in enumerate(bits):
        result += bit << i
    return result

def booth_radix8_full(x, y):
    bit_length = max(x.bit_length(), y.bit_length()) + 1
    bit_length = (bit_length + 2) // 3 * 3
    x_bits = int_to_bits(x, bit_length)
    y_bits = int_to_bits(y, bit_length)
    w = (len(y_bits) + 2) // 3

    partial_products = []

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

        partial_product_shifted = partial_product << (3 * i)
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


def booth_radix8_fixed(x, y):
    bit_length = max(x.bit_length(), y.bit_length()) + 1
    bit_length = (bit_length + 2) // 3 * 3
    x_bits = int_to_bits(x, bit_length)
    y_bits = int_to_bits(y, bit_length)
    w = (len(y_bits) + 2) // 3

    partial_products = []

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

        partial_product_shifted = partial_product << (3 * i)
        partial_product_bits = int_to_bits(partial_product_shifted, 2 * bit_length)
        partial_products.append(partial_product_bits)

    # Wynik o dlugosci 2n (mlodsze n - same 0)
    result_bits = [0] * 2 * bit_length
    carry = [0] * (bit_length + 1)



    # Wyliczamy przeniesienie z mldoszych n bitow
    for bit_position in range(bit_length):
        column_sum = carry[bit_position]
        # dla kazdego iloczynu czesciowego:
        for pp in partial_products:
            column_sum += pp[bit_position]

        # nastepne przenisienie to column_sum mod 2
        carry[bit_position + 1] = column_sum // 2


    # Sumowanie starszych n bitow (z propagowanym przeniesieniem)
    carry_in = carry[6]
    for bit_position in range(bit_length, 2 * bit_length):
        column_sum = carry_in    # dla n+1 bitu
        for pp in partial_products:
            if bit_position < len(pp):
                column_sum += pp[bit_position]

        result_bits[bit_position] = column_sum % 2
        carry_in = column_sum // 2

    result = bits_to_int(result_bits)

    # Correct the sign if the result is negative
    if result_bits[-1] == 1:
        result -= (1 << bit_length)

    return result


# Test algorytmu z przykładowymi wartościami
x = 7  # Mnożna
y = 12 # Mnożnik


#result = booth_radix8_full(x, y)
#print("Wynik mnozenie Bootha radix-8 full-width: ", x, " * ", y, " = ", result, "\n")

#result = booth_radix8_fixed(x, y)
#print("Wynik mnozenie Bootha radix-8 fixed-width (post-truncated): ", x, " * ", y, " = ", result, "\n")


time_in_micro = 0

# Petla do pomiarow dla radix-8 full-width
for i in range(100):
    start_time = time.perf_counter()
    result_full = booth_radix8_full(x, y)
    end_time = time.perf_counter()
    time_in_micro += (end_time - start_time) * (10 ** 6)
    #print("Wynik mnożenia radix-8 full-width:", result_full)

print("Sredni czas mnozenia radix-8 full-width dla 100 pomiarow: ", time_in_micro / 100.0)
print("Wynik:", result_full)


n = 4  # liczba bitow mnoznika i mnoznej (wynik mnozenia: 2n + 1)

# Petla do pomiarow dla radix-8 full-width
for i in range(100):
    start_time = time.perf_counter()
    result_fixed = booth_radix8_fixed(x, y)
    end_time = time.perf_counter()
    time_in_micro += (end_time - start_time) * (10 ** 6)
    #print("Wynik mnożenia radix-8 full-width:", result_full)

print("Sredni czas mnozenia radix-8 fixed-width (post-truncated) dla 100 pomiarow: ", time_in_micro / 100.0)
print("Wynik:", result_fixed)

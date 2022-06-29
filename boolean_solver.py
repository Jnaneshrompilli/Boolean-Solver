'''
Author: Jnaneswara Rao Rompilli
Description: 
'''
import os

ref_dict = {
    0: ["a", "a'"],
    1: ["b", "b'"],
    2: ["c", "c'"],
    3: ["d", "d'"],
    4: ["e", "e'"],
    5: ["f", "f'"],
    6: ["g", "g'"],
    7: ["h", "h'"],
}

# Declaring variables
final_expression = []
values_variable = []
values_binary = []
values_decimal = []
dont_care_terms = []
no_of_variables = 0


def minterm_finder(terms):
    terms = terms[:]
    terms_updated = []
    matched = False
    for i in range(len(terms)):
        size = len(terms[i])
        cur_str = terms[i]
        count = 0
        over = True
        for j in range(size):
            if cur_str[j].isalpha():
                count = count + 1
            if cur_str[j] == "-":
                over = False
                matched = True
                temp = list(terms[i][:])
                temp[j] = ref_dict[count][0]
                terms_updated.append("".join(temp))
                temp = list(terms[i][:])
                temp[j] = ref_dict[count][1]
                terms_updated.append("".join(temp))
                break
        if over and not terms[i] in final_expression:
            final_expression.append(terms[i])

    if matched:
        return minterm_finder(terms_updated)
    else:
        return final_expression


def var_gap_filler(values_variable):
    values_variable = values_variable[:]
    var_divided = []
    for term in values_variable:
        sub_var_divided = []
        for j in range(len(term)):
            if j == len(term) - 1:
                if term[j].isalpha():
                    sub_var_divided.append(term[j])
                break
            if term[j].isalpha() and term[j + 1].isalpha():
                sub_var_divided.append(term[j])

            elif term[j].isalpha() and term[j + 1] == "'":
                var = term[j] + term[j + 1]
                sub_var_divided.append(var)
        var_divided.append(sub_var_divided)

    for i in range(len(var_divided)):
        sub_var_divided = var_divided[i]
        for k in range(len(sub_var_divided) - 1):
            for j in range(len(sub_var_divided) - 1):
                first = sub_var_divided[j][0]
                second = sub_var_divided[j + 1][0]
                if ord(first) > ord(second):
                    sub_var_divided[j], sub_var_divided[j + 1] = (
                        sub_var_divided[j + 1],
                        sub_var_divided[j],
                    )
        var_divided[i] = sub_var_divided

    for i in range(len(var_divided)):
        sub_var_divided = var_divided[i]
        for j in range(no_of_variables):
            try:
                if not (
                    sub_var_divided[j] == ref_dict[j][0]
                    or sub_var_divided[j] == ref_dict[j][1]
                ):
                    sub_var_divided.insert(j, "-")
            except IndexError:
                sub_var_divided.append("-")
        var_divided[i] = "".join(sub_var_divided)

    return var_divided


def var_term_to_bin_term(min_term):
    min_term = min_term[:]
    min_term_bin = []
    for term in min_term:
        bin_term = ""
        for j in range(len(term)):
            if j == len(term) - 1:
                if term[j].isalpha():
                    bin_term = bin_term + "1"
                break
            if term[j].isalpha() and term[j + 1].isalpha():
                bin_term = bin_term + "1"
            elif term[j].isalpha() and term[j + 1] == "'":
                bin_term = bin_term + "0"
        min_term_bin.append(bin_term)
    return min_term_bin


def binaryto_decimal(min_term_bin):
    min_term_dec = []
    min_term_bin = min_term_bin[:]
    for i in range(len(min_term_bin)):
        value = int(min_term_bin[i], 2)
        min_term_dec.append(value)
    return min_term_dec


def decimaltobinary(values_decimal):
    data_set_bin = []
    for i in range(len(values_decimal)):
        data_set = bin(int(values_decimal[i])).replace("0b", "")
        data_set_bin.append(data_set)
    return data_set_bin


def binarytodecimal(point):
    m = len(point)
    value = 0
    for j in range(m):
        value = value + int(point[j]) * pow(2, m - j - 1)
    return value


def bits_equalizer(values_binary, n):
    max_char = len(max(values_binary, key=len))

    for i in range(n):
        add_string = ""
        if len(values_binary[i]) < max_char:
            for j in range(max_char - len(values_binary[i])):
                add_string = add_string + "0"
            values_binary[i] = add_string + values_binary[i]


def sort_terms(values_binary, values_decimal, n):
    for i in range(n):
        min_value = values_decimal[i]
        for j in range(i, n):
            if values_decimal[j] <= min_value:
                min_value = values_decimal[j]
                index = j
        values_binary[i], values_binary[index] = values_binary[index], values_binary[i]
        values_decimal[i], values_decimal[index] = (
            values_decimal[index],
            values_decimal[i],
        )

    for i in range(0, n):
        for j in range(1, n):
            if values_binary[j].count("1") < values_binary[j - 1].count("1"):
                values_binary[j], values_binary[j - 1] = (
                    values_binary[j - 1],
                    values_binary[j],
                )
                values_decimal[j], values_decimal[j - 1] = (
                    values_decimal[j - 1],
                    values_decimal[j],
                )
                swapped = "true"
        try:
            if swapped != "true":
                break
        except:
            pass


def booleansimplifier(
    data_set, values_decimal, max_char, implicants_binary, implicants_decimal
):
    n = len(data_set)
    simplified = 0
    terms_binary = []
    terms_decimal = []
    for i in range(n):
        matched = 0
        current_val = data_set[i]
        for j in range(0, n):
            compare_val = data_set[j]
            count = 0
            for a in range(max_char):
                if current_val[a] != compare_val[a]:
                    index = a
                    count = count + 1
            if count == 1:
                simplified = 1
                matched = 1
                temp_list = list(current_val)
                temp_list[index] = "-"
                common_val = "".join(temp_list)
                if not common_val in terms_binary:
                    terms_binary.append(common_val)
                    if isinstance(values_decimal[i], int):
                        terms_decimal.append(
                            (values_decimal[i], values_decimal[j]))
                    else:
                        terms_decimal.append(
                            (values_decimal[i] + values_decimal[j]))

        if matched == 0:
            implicants_decimal.append(data_set[i])
            implicants_binary.append(values_decimal[i])

    if simplified != 0:
        return booleansimplifier(
            terms_binary,
            terms_decimal,
            max_char,
            implicants_binary,
            implicants_decimal,
        )
    else:
        return implicants_decimal, implicants_binary


def prime_table_solver(prime_implicants_decimal, prime_implicant_binary):
    m = len(prime_implicants_decimal)
    for x in range(m):
        if isinstance(prime_implicants_decimal[x], int):
            prime_implicants_decimal[x] = (prime_implicants_decimal[x],)
    min_expressions_dec = []
    min_expressions_bin = []
    for reverse in range(2):
        for k in range(m):
            prime_implicants_dec = prime_implicants_decimal[:]
            prime_implicants_bin = prime_implicant_binary[:]
            if reverse == 1:
                prime_implicants_dec.reverse()
                prime_implicants_bin.reverse()
            m = len(prime_implicants_dec)
            i = k
            while i < m:
                matched = True
                current_term = prime_implicants_dec[i]

                for j in range(len(current_term)):
                    current_value = current_term[j]
                    compare = sum(
                        prime_implicants_dec[0:i] +
                        prime_implicants_dec[i + 1: m], ()
                    )
                    if not current_value in compare and (
                        not current_value in dont_care_terms
                    ):
                        matched = False
                if matched:
                    prime_implicants_dec[i] = ()
                    prime_implicants_bin[i] = ""
                if k == 0 and i == m - 1:
                    break
                if i == k - 1:
                    break
                if i == m - 1:
                    i = 0
                else:
                    i = i + 1

            prime_implicants_dec = list(filter(None, prime_implicants_dec))
            prime_implicants_bin = list(filter(None, prime_implicants_bin))
            if reverse == 1:
                prime_implicants_dec.reverse()
                prime_implicants_bin.reverse()
            if not prime_implicants_dec in min_expressions_dec:
                min_expressions_dec.append(prime_implicants_dec)
                min_expressions_bin.append(prime_implicants_bin)
    least = len(min(min_expressions_dec, key=len))
    for i in range(len(min_expressions_dec)):
        if len(min_expressions_dec[i]) > least:
            min_expressions_dec[i] = []
            min_expressions_bin[i] = []
    min_expressions_dec = list(filter(None, min_expressions_dec))
    min_expressions_bin = list(filter(None, min_expressions_bin))
    return min_expressions_bin, min_expressions_dec


def binary_to_variable(min_sum_bin, max_char):
    dict_n = {
        "0": ["a", "a'"],
        "1": ["b", "b'"],
        "2": ["c", "c'"],
        "3": ["d", "d'"],
        "4": ["e", "e'"],
        "5": ["f", "f'"],
        "6": ["g", "g'"],
        "7": ["h", "h'"],
    }
    min_sum_var = []
    min_sum_bin = min_sum_bin[:]
    a = len(min_sum_bin)
    for k in range(a):
        min_sum_var_temp = ""
        b = len(min_sum_bin[k])
        for i in range(b):
            cur_val = list(min_sum_bin[k][i])
            for j in range(max_char):
                if cur_val[j] == "1":
                    cur_val[j] = dict_n[f"{j}"][0]
                if cur_val[j] == "0":
                    cur_val[j] = dict_n[f"{j}"][1]
                if cur_val[j] == "-":
                    cur_val[j] = ""
            cur_val = "".join(cur_val)
            if i != b - 1:
                min_sum_var_temp = min_sum_var_temp + cur_val + " + "
            else:
                min_sum_var_temp = min_sum_var_temp + cur_val
        min_sum_var.append(min_sum_var_temp)
    return min_sum_var


def print_output(min_sum_var, min_sum_bin, min_sum_dec, essential_prime_implicants):
    size = len(min_sum_bin)
    print(
        f"Essential prime implicants using Method 2: [ {str(essential_prime_implicants[0]).replace('+',',')} ]"
    )
    print("\n\n\n---All Possible terms after simplification---")

    for i in range(size):
        print(f"\n---{i+1}---")
        print(f"Expression: {min_sum_var[i]}", end="")
        print(f"\nDecimal combinations: {min_sum_dec[i]}")
    print("\n ")


def essential_prime_implicants_finder_alt(
    prime_implicants_decimal, prime_implicants_binary, n
):
    prime_implicants_decimal = prime_implicants_decimal[:]
    prime_implicants_binary = prime_implicants_binary[:]
    essential_prime_implicants_alt_bin = []
    essential_prime_implicants_alt_dec = []
    for i in range(n):
        count = 0
        for j in range(len(prime_implicants_decimal)):
            if isinstance(prime_implicants_decimal[j], int):
                prime_implicants_decimal[j] = (prime_implicants_decimal[j],)
            size = len(prime_implicants_decimal[j])
            for k in range(size):
                if values_decimal[i] == int(prime_implicants_decimal[j][k]):
                    count = count + 1
                    index = j
        if count == 1 and (not values_decimal[i] in dont_care_terms):
            if (
                not str(prime_implicants_binary[index])
                in essential_prime_implicants_alt_bin
            ):
                essential_prime_implicants_alt_bin.append(
                    prime_implicants_binary[index]
                )
                essential_prime_implicants_alt_dec.append(
                    prime_implicants_decimal[index]
                )
    return essential_prime_implicants_alt_bin


def essential_prime_implicants_finder(
    prime_implicants_binary, prime_implicants_decimal, min_sum_bin
):
    essential_prime_implicants = []
    essential_prime_implicants_dec = []
    for i in range(len(prime_implicants_binary)):
        current_value = prime_implicants_binary[i]
        present = True
        for j in range(len(min_sum_bin)):
            compare_expression = min_sum_bin[j]
            if not current_value in compare_expression:
                present = False
        if present:
            essential_prime_implicants.append(current_value)
            essential_prime_implicants_dec.append(prime_implicants_decimal[i])

    return essential_prime_implicants


def main():
    global values_variable
    global values_binary
    global values_decimal
    global dont_care_terms
    global no_of_variables
    print("------------Input Methods-----------")
    print("1: Decimal Values  Eg- [0, 7, 5]  ")
    print("2: Binary Values   Eg- ['000', '111', '101'] ")
    print("3: Algebric Expression   Eg- abc' + ab'c' + abc")
    option = input("\nChoose a Valid Option: ")

    if option == "1":
        if values_decimal:
            values_decimal = values_decimal + dont_care_terms
            values_binary = decimaltobinary(values_decimal)
            n = len(values_binary)
        else:
            values_decimal = [
                int(x)
                for x in input("Enter Minterms (Each seperated by spaces): ").split()
            ]
            dont_care_terms = [
                int(x)
                for x in input(
                    "Enter Dont care terms (Each seperated by space):"
                ).split()
            ]
            values_decimal = values_decimal + dont_care_terms
            n = len(values_decimal)
            values_binary = decimaltobinary(values_decimal)

    elif option == "2":
        if not values_binary:
            values_binary = [
                x for x in input("Enter Minterms (Each seperated by spaces): ").split()
            ]
            dont_care_terms = [
                int(x)
                for x in input(
                    "Enter Dont care terms (Each seperated by space):"
                ).split()
            ]
            values_binary = values_binary + dont_care_terms
            n = len(values_decimal)
            values_decimal = binaryto_decimal(values_binary)
        else:
            values_binary = values_binary + dont_care_terms
            n = len(values_binary)
            values_decimal = binaryto_decimal(values_binary)

    elif option == "3":
        if values_variable:
            values_variable = minterm_finder(values_variable)
            values_binary = var_term_to_bin_term(values_variable)
            values_decimal = binaryto_decimal(values_binary)
            n = len(values_decimal)
        else:
            no_of_variables = int(input("Enter no of variables: "))
            expression = input("Enter expression(Eg: ab'd' + a'd + c'd): ").replace(
                " ", ""
            )
            values_variable = expression.split("+")
            values_variable = var_gap_filler(values_variable)
            values_variable = minterm_finder(values_variable)
            values_binary = var_term_to_bin_term(values_variable)
            values_decimal = binaryto_decimal(values_binary)
            n = len(values_decimal)
        print(values_variable)
    else:
        print("\nInvalid Option")
        exit()

    bits_equalizer(values_binary, n)
    sort_terms(values_binary, values_decimal, n)
    max_char = len(max(values_binary, key=len))

    implicants_binary = []
    implicants_decimal = []
    prime_implicants_binary, prime_implicants_decimal = booleansimplifier(
        values_binary, values_decimal, max_char, implicants_binary, implicants_decimal,
    )

    os.system("cls")
    print("\n---------Your Input----------")
    print(f"In Decimal: {values_decimal}")
    print(f"In Binary: {values_binary}")
    print(f"Don't care terms: {dont_care_terms}")

    prime_implicants_var = binary_to_variable(
        [prime_implicants_binary], max_char)
    print(
        f"\n\nPrime Implicants: [ { str(prime_implicants_var[0]).replace('+',',') } ]"
    )

    min_sum_bin, min_sum_dec = prime_table_solver(
        prime_implicants_decimal, prime_implicants_binary
    )

    essential_prime_implicants_alt = essential_prime_implicants_finder_alt(
        prime_implicants_decimal, prime_implicants_binary, n
    )
    essential_prime_implicants_alt = binary_to_variable(
        [essential_prime_implicants_alt], max_char
    )
    print(
        f"Essential Prime implicants using Method 1: {essential_prime_implicants_alt[0]}"
    )

    essential_prime_implicants = essential_prime_implicants_finder(
        prime_implicants_binary, prime_implicants_decimal, min_sum_bin
    )
    essential_prime_implicants = binary_to_variable(
        [essential_prime_implicants], max_char
    )

    min_sum_var = binary_to_variable(min_sum_bin, max_char)
    print_output(min_sum_var, min_sum_bin, min_sum_dec,
                 essential_prime_implicants)


if __name__ == "__main__":
    main()

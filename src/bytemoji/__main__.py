import json

BASE = 1812
LAST = BASE - 1  # 1811

BITS = 11  # log_2(1812) == 10.82336724

DATA = {}  # dict

with open("data-ordered-emoji.json") as json_file:
    DATA = json.load(json_file)


def is_inside_base(number: int, base: int = BASE):
    """Checks if number is inside our bytemojibase base."""

    if (number >= 0) and (number <= base - 1):
        return True

    return False


def int_to_bits(number: int) -> str:
    """Transforms `int` to bit map (`str`)"""

    return format(number, "b")


def get_base_hashmoji(bitmap_str: str) -> list[str]:  # maybe we should accept
    # bytes()
    list_of_numbers = list()

    while bitmap_str:
        chunk_size = 11  # let's try it first
        number = int(bitmap_str[0:chunk_size], base=2)
        eleven_greater_than_base = not is_inside_base(number)
        chunk_size = 10 if eleven_greater_than_base else 11
        chunk = bitmap_str[0:chunk_size]
        list_of_numbers.append(chunk)

        bitmap_str = bitmap_str[chunk_size:]

    return list_of_numbers


def get_bytemoji_list(indexes, data=DATA):
    bytemoji_list = list()

    for bytemoji_index in indexes:
        index = int(bytemoji_index, base=2)
        bytemoji_char = data[index]
        bytemoji_list.append(bytemoji_char)

    return bytemoji_list


# encoding

some_number = 786543392320949749
bitmap = int_to_bits(some_number)
list_of_indexes = get_base_hashmoji(bitmap)
bytemoji_list = get_bytemoji_list(list_of_indexes)
bytemoji_hash = "".join(bytemoji_list)

print(bytemoji_hash)

# decoding


def decode_bytemoji(bytemoji_list, data=DATA):

    list_of_numbers = list()  # list of numerical values for each char
    list_of_bitmaps = list()  # list of bit values for each char, zero-filled
    # to 11 bits, so to we later add up and divide in
    # chunks of 8 bits (byte)

    # get the numerical integer for each bytemoji
    # for item in bytemoji_list:
    #     #print(item)
    #     if item in data:
    #         number = data.index(item)
    #         #print(number)
    #         list_of_numbers.append(number)
    list_of_numbers = [data.index(item) for item in bytemoji_list if item in data]

    # last item will be specially treated because of the leading zeroes
    last_item = bytemoji_list.pop()  # last item

    # fill all items (except the last one) with zeroes, till 11 bits for char
    for item in list_of_numbers:
        item_to_bit_string = int_to_bits(item)
        full_base = item_to_bit_string.zfill(11)  # some bitmsps are like 00110
        # before convertion, which
        # make them lose the leading
        # zeroes at conversion to int
        list_of_bitmaps.append(full_base)

    bitmap = "".join(list_of_bitmaps)
    padding_size = (len(bitmap) + len(last_item)) % BITS
    padded_last_item = last_item.zfill(padding_size)
    list_of_bitmaps.append(padded_last_item)

    return list_of_bitmaps


list_of_bitmaps = decode_bytemoji(bytemoji_list)

a = "".join(list_of_bitmaps)

print(int(a, base=2))

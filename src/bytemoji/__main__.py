import json

BASE = 1812
LAST = BASE - 1  # 1811

BITS = 11  # log_2(1812) == 10.82336724

DATA = {}  # dict

with open("data-ordered-emoji.json") as json_file:
    DATA = json.load(json_file)


class Bytemoji:
    def __init__(self, number: int = None, bytemoji: str = None):
        # later let's change this to bytes()

        if number:
            self.number = number
            self.encode()

        elif bytemoji:
            self.bytemoji = bytemoji
            decode()

        #else:
        #   set Bytemoji.number and run Bytemoji.encode() or
        #   set Bytemoji.bytemoji_hash and run Bytemoji.decode()

    def encode(self):
        self.bitmap = self._int_to_bits(self.number)
        self.list_of_bits = self.get_base_hashmoji(self.bitmap)
        self.bytemoji_list = self.get_bytemoji_list(self.list_of_bits)
        self.bytemoji_hash = "".join(self.bytemoji_list)

    def decode(self):
        pass

    def get_base_hashmoji(self, bitmap_str: str) -> list[str]:
        # maybe we should accept
        # bytes()
        list_of_bits = list()

        while bitmap_str:
            chunk_size = 11  # let's try it first
            number = int(bitmap_str[0:chunk_size], base=2)
            eleven_greater_than_base = not self._is_inside_base(number)
            chunk_size = 10 if eleven_greater_than_base else 11
            chunk = bitmap_str[0:chunk_size]
            list_of_bits.append(chunk)

            bitmap_str = bitmap_str[chunk_size:]

        return list_of_bits

    def decode_bytemoji(self, bytemoji_list, data=DATA):

        list_of_indexes = list()  # list of numerical values for each char
        list_of_bitmaps = list()  # list of bit values for each char,
        # zero-filled
        # to 11 bits, so to we later add up and divide in
        # chunks of 8 bits (byte)

        # get the numerical integer for each bytemoji
        list_of_indexes = [data.index(item) for item in bytemoji_list if item in data]

        # last item will be specially treated because of the leading zeroes
        last_item = list_of_indexes.pop()  # last item
        last_item_bitmap = int_to_bits(last_item)

        # fill all items (except the last one) with zeroes, till 11 bits for char
        # some bitmsps are like 001100 before convertion, which make them lose
        # the leading zeroes at conversion to int
        list_of_bitmaps = [int_to_bits(item).zfill(11) for item in list_of_indexes]

        bitmap = "".join(list_of_bitmaps)
        padding_size = (len(bitmap) + len(last_item_bitmap)) % BITS
        padded_last_item = last_item_bitmap.zfill(padding_size)

        list_of_bitmaps.append(padded_last_item)

        return list_of_bitmaps

    def get_bytemoji_list(self, indexes, data=DATA):
        bytemoji_list = list()

        for bytemoji_index in indexes:
            index = int(bytemoji_index, base=2)
            bytemoji_char = data[index]
            bytemoji_list.append(bytemoji_char)

        return bytemoji_list

    def _is_inside_base(self, number: int, base: int = BASE):
        """Checks if number is inside our bytemojibase base."""

        if (number >= 0) and (number <= base - 1):
            return True

        return False

    def _int_to_bits(self, number: int) -> str:
        """Transforms `int` to bit map (`str`)"""

        return format(number, "b")


# encoding

some_number = 786543392320949749
bitmap = int_to_bits(some_number)
list_of_indexes = get_base_hashmoji(bitmap)
bytemoji_list = get_bytemoji_list(list_of_indexes)
bytemoji_hash = "".join(bytemoji_list)

print(bytemoji_hash)

# decoding


list_of_bitmaps = decode_bytemoji(bytemoji_list)

print(list_of_bitmaps)

a = "".join(list_of_bitmaps)
print(a)
print(int(a, base=2))

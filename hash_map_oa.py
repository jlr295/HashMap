# Description: An implementation of a HashMap class that uses open addressing with
# quadratic probing for collision resolution within a DA


from a6_include import (DynamicArray, HashEntry,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Initialize new HashMap that uses
        quadratic probing for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(None)

        self._hash_function = function
        self._size = 0

    def __str__(self) -> str:
        """
        Override string method to provide more readable output
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self._buckets.length()):
            out += str(i) + ': ' + str(self._buckets[i]) + '\n'
        return out

    def _next_prime(self, capacity: int) -> int:
        """
        Increment from given number to find the closest prime number
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity % 2 == 0:
            capacity += 1

        while not self._is_prime(capacity):
            capacity += 2

        return capacity

    @staticmethod
    def _is_prime(capacity: int) -> bool:
        """
        Determine if given integer is a prime number and return boolean
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity == 2 or capacity == 3:
            return True

        if capacity == 1 or capacity % 2 == 0:
            return False

        factor = 3
        while factor ** 2 <= capacity:
            if capacity % factor == 0:
                return False
            factor += 2

        return True

    def get_size(self) -> int:
        """
        Return size of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._size

    def get_capacity(self) -> int:
        """
        Return capacity of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._capacity

    # ------------------------------------------------------------------ #

    def put(self, key: str, value: object) -> None:
        """
        Updates the key/value pair in the hashmap.  If it's given key is already in the Hashmap,
        the the key's value must be updated with the one provided.
        """
        # Check load factor, if >= 0.5 resize
        load_fac = self.table_load()
        if load_fac >= 0.5:
            self.resize_table(self._capacity * 2)

        is_key_pres = self.contains_key(str(key))
        # Find its location(index) using hash function
        if self._hash_function == hash_function_1:
            location = hash_function_1(key) % self._capacity
        else:
            location = hash_function_2(key) % self._capacity

        # If key is present, find location of the key and update the value
        if is_key_pres is True:
            if self._buckets[location].key == key:
                if self._buckets[location].is_tombstone is True:
                    self._size += 1
                    self._buckets[location].is_tombstone = False
                self._buckets[location].value = value
            else: # key is not in current location
                j = 1
                new_location = (location +(j**2)) % self._capacity
                while self._buckets[new_location].key != key:
                    new_location = (location + j**2) % self._capacity
                    j += 1
                location = new_location
            if self._buckets[location].is_tombstone is True:
                self._size += 1
                self._buckets[location].is_tombstone = False
            self._buckets[location].value = value

        else: # key is not present in the Array _
            if self._buckets[location] is not None:  # If current location is occupied
                if self._buckets[location].key != key:  # If the current location is not occupied with the given key
                    j = 1
                    new_location = (location + (j ** 2)) % self._capacity
                    while self._buckets[new_location] is not None:  # Probe to find then next open spot.
                        new_location = (location + (j ** 2)) % self._capacity
                        j += 1
                    location = new_location

            self._buckets.set_at_index(location, HashEntry(key, value))
            self._size += 1

    def table_load(self) -> float:
        """
        Returns the current HashTable load factor
        """
        return self._size / self._capacity

    def empty_buckets(self) -> int:
        """
        Returns the number of empty buckets.
        """
        return self._capacity - self._size

    def resize_table(self, new_capacity: int) -> None:
        """
        Changes the new capacity of the internal hashtable.
        """
        # new_capacity cannot be less than the table size.
        if new_capacity < self._size:
            return
        # Determine whether new_capacity is prime
        if not self._is_prime(new_capacity):
            new_capacity = self._next_prime(new_capacity)
        # Save old buckets
        old_buckets = self._buckets
        old_size = self._size
        # Empty buckets
        self._buckets = DynamicArray()
        self._size = 0
        for index in range(new_capacity):
            self._buckets.append(None)
        # Set capacity
        self._capacity = new_capacity
        # Iterate through old buckets and re-hash any values
        if old_buckets.length() != 0:
            # Iterate through each item in the old bucket
            for index in range(old_buckets.length()):
                if old_buckets[index] is None:
                    continue
                    # If a value is present rehash it into the array
                else:
                    self.put(old_buckets[index].key, old_buckets[index].value)

    def get(self, key: str) -> object:
        """
        Returns a value associated with the given key. If key is not in the HashMap,
        None is returned.
        """
        # Check to see if key is in the hashmap
        if not self.contains_key(key):
            return None
        # Find its location(index) using hash function
        if self._hash_function == hash_function_1:
            location = hash_function_1(key) % self._capacity
        else:
            location = hash_function_2(key) % self._capacity

        if self._buckets[location] is not None:
            if self._buckets[location].key == key:
                return self._buckets[location].value
            else:  # key is not in current location
                j = 1
                new_location = (location + (j ** 2)) % self._capacity
                while self._buckets[new_location].key != key:
                    new_location = (location + j ** 2) % self._capacity
                    j += 1
                location = new_location
            return self._buckets[location].value

    def contains_key(self, key: str) -> bool:
        """
        Returns True if the given key is in the HashMap, otherwise will return False
        """
        # If size of hashmap is zero then the key is not present
        if self._size == 0:
            return False
        # Size is greater than zero
        # Find location
        if self._hash_function == hash_function_1:
            location = hash_function_1(key) % self._capacity
        else:
            location = hash_function_2(key) % self._capacity
        # Check to see if key is at the location indicated.
        if self._buckets[location] is not None:
            if self._buckets[location].key == key:
                return True
        # If key is not location probe until next position is reached.
        j = 1
        new_location = (location + j ** 2) % self._capacity
        # Continue to probe until empty spot is reached
        while self._buckets[new_location] is not None:
            if self._buckets[new_location].key == key:
                return True
            else:
                j += 1  # Increment J
                new_location = (location + j ** 2) % self._capacity  # Set new_location to next element
                # If the new_location is out of bounds
                if new_location > self._capacity - 1:
                    return False
        return False

    def remove(self, key: str) -> None:
        """
        Removes the given key and the associated value from the hashmap.
        If the key is not in the hashmap it returns nothing.
        """
        if not self.contains_key(key):
            return
        # Find value
        # Find its location(index) using hash function
        if self._hash_function == hash_function_1:
            location = hash_function_1(key) % self._capacity
        else:
            location = hash_function_2(key) % self._capacity

        if self._buckets[location] is not None:
            if self._buckets[location].key == key:
                if self._buckets[location].is_tombstone:
                    return
                self._buckets[location].is_tombstone = True
            else:  # key is not in current location
                j = 1
                new_location = (location + (j ** 2)) % self._capacity
                while self._buckets[new_location].key != key:
                    new_location = (location + j ** 2) % self._capacity
                    j += 1
                if self._buckets[new_location].is_tombstone:
                    return
                self._buckets[new_location].is_tombstone = True
        self._size = self._size - 1

    def clear(self) -> None:
        """
        Clears the hashmap without altering its capacity.
        """
        # Set each value in bucket to None
        for index in range(self._capacity):
            self._buckets.set_at_index(index, None)
        # Set size to zero
        self._size = 0

    def get_keys_and_values(self) -> DynamicArray:
        """
        Returns a dynamic array where each index contains a tuple with a key/value pair.
        """
        # Initialize new array
        new_arr = DynamicArray()

        # Determine if size is zero; if it is return Array
        if self._size == 0:
            return new_arr

        # Iterate through each bucket
        for index in range(self._capacity):
            # If index is not empty
            if self._buckets[index] is not None and self._buckets[index].is_tombstone is not True:
                new_arr.append((self._buckets[index].key, self._buckets[index].value))
            else:
                continue
        return new_arr

# hash_map.py
# ===================================================
# Implement a hash map with chaining
# Author: Sara Baber
# Date: 05/04/2020
# Course: CS261 Data Structures, Portfolio Project
# ===================================================


class SLNode:
    """Initializes a node in a singly linked list"""
    def __init__(self, key, value):
        self.next = None
        self.key = key
        self.value = value

    def __str__(self):
        return '(' + str(self.key) + ', ' + str(self.value) + ')'


class LinkedList:
    """Initializes linked list"""
    def __init__(self):
        self.head = None
        self.size = 0

    def add_front(self, key, value):
        """Create a new node and inserts it at the front of the linked list
        Args:
            key: the key for the new node
            value: the value for the new node"""
        new_node = SLNode(key, value)
        new_node.next = self.head
        self.head = new_node
        self.size = self.size + 1

    def is_empty(self):
        """
        Checks if the list is empty

        Returns:
            True if the list has no data nodes, False otherwise
        """
        current = self.head

        if current.next == self.tail:
            return True
        else:
            return False

    def remove(self, key):
        """Removes node from linked list
        Args:
            key: key of the node to remove """
        if self.head is None:
            return False
        if self.head.key == key:
            self.head = self.head.next
            self.size = self.size - 1
            return True
        cur = self.head.next
        prev = self.head
        while cur is not None:
            if cur.key == key:
                prev.next = cur.next
                self.size = self.size - 1
                return True
            prev = cur
            cur = cur.next
        return False

    def contains(self, key):
        """Searches linked list for a node with a given key
        Args:
        	key: key of node
        Return:
        	node with matching key, otherwise None"""
        if self.head is not None:
            cur = self.head
            while cur is not None:
                if cur.key == key:
                    return cur
                cur = cur.next
        return None

    def __str__(self):
        """prints out linked list"""
        out = '['
        if self.head != None:
            cur = self.head
            out = out + str(self.head)
            cur = cur.next
            while cur != None:
                out = out + ' -> ' + str(cur)
                cur = cur.next
        out = out + ']'
        return out


def hash_function_1(key):
    """Takes a key and returns a hash number"""
    hash = 0
    for i in key:
        hash = hash + ord(i)
    return hash


def hash_function_2(key):
    """Takes a key and returns a hash number"""
    hash = 0
    index = 0
    for i in key:
        hash = hash + (index + 1) * ord(i)
        index = index + 1
    return hash


class HashMap:
    """
    Creates a new hash map with the specified number of buckets.
    Args:
        capacity: the total number of buckets to be created in the hash table
        function: the hash function to use for hashing values
    """

    def __init__(self, capacity, function):
        """Initializes HashMap"""
        self._buckets = []
        for i in range(capacity):
            self._buckets.append(LinkedList())
        self.capacity = capacity
        self._hash_function = function
        self.size = 0

    def clear(self):
        """
        Empties out the hash table deleting all links in the hash table.
        """
        self.size = 0  # set size to 0 and reinitialize buckets as empty
        self._buckets = []

    def get(self, key):
        """
        Returns the value with the given key.
        Args:
            key: the value of the key to look for
        Return:
            The value associated to the key. None if the link isn't found.
        """
        hash_key = self._hash_function(key) % self.capacity  # returns hashed keys corresponding bucket index
        bucket = self._buckets[hash_key]  # get bucket for that index

        current = bucket.head  # set bucket.head to variable as not to override linked list

        while current is not None:  # iterate through linked list until value is found, or returns None
            if current.key == key:
                return current.value
            current = current.next

    def resize_table(self, capacity):
        """
        Resizes the hash table to have a number of buckets equal to the given
        capacity. All links need to be rehashed in this function after resizing
        Args:
            capacity: the new number of buckets.
        """
        old_buckets = self._buckets  # save current buckets with variable

        self._buckets = []  # initialize new empty buckets
        self.capacity = capacity
        for i in range(capacity):
            self._buckets.append(LinkedList())
        self.size = 0

        for bucket in old_buckets:  # loops through old hashmap and adds key/value pairs to new hashmap
            if bucket.size == 0:
                pass
            else:
                while bucket.head is not None:
                    self.put(bucket.head.key, bucket.head.value)
                    bucket.remove(bucket.head.key)

    def put(self, key, value):
        """
        Updates the given key-value pair in the hash table. If a link with the given
        key already exists, this will just update the value and skip traversing. Otherwise,
        it will create a new link with the given key and value and add it to the table
        bucket's linked list.

        Args:
            key: they key to use to hash the entry
            value: the value associated with the entry
        """
        hash_key = self._hash_function(key) % self.capacity  # finds index for new key/value pair

        if self._buckets[hash_key].size == 0:  # if bucket is empty, add new key/value pair
            self.size += 1
            self._buckets[hash_key].add_front(key, value)
        else:
            if self._buckets[hash_key].contains(key):
                self._buckets[hash_key].remove(key)  # if key already exists, delete old key/value pair
                self.size -= 1
            self._buckets[hash_key].add_front(key, value)  # add new key/value pair
            self.size += 1

    def remove(self, key):
        """
        Removes and frees the link with the given key from the table. If no such link
        exists, this does nothing. Remember to search the entire linked list at the
        bucket.
        Args:
            key: they key to search for and remove along with its value
        """
        if self.contains_key(key):  # if key exists in hashmap, remove key/value pair
            hash_key = self._hash_function(key) % self.capacity
            bucket = self._buckets[hash_key]
            bucket.remove(key)

    def contains_key(self, key):
        """
        Searches to see if a key exists within the hash table

        Returns:
            True if the key is found False otherwise
        """
        hash_key = self._hash_function(key) % self.capacity
        bucket = self._buckets[hash_key]

        if bucket.contains(key):
            return True
        else:
            return False

    def empty_buckets(self):
        """
        Returns:
            The number of empty buckets in the table
        """
        count = 0

        for bucket in self._buckets:
            if bucket.size == 0:  # adds 1 to count every time a buckets size is 0
                count += 1

        return count

    def table_load(self):
        """
        Returns:
            the ratio of (number of links) / (number of buckets) in the table as a float.
        """
        buckets = self.capacity
        elements = self.size

        return float(elements/buckets)

    def __str__(self):
        """
        Prints all the links in each of the buckets in the table.
        """
        out = ""
        index = 0
        for bucket in self._buckets:
            out = out + str(index) + ': ' + str(bucket) + '\n'
            index = index + 1
        return out


x1 = 'pool'
x2 = 'loop'
y1 = hash_function_1(x1)
y2 = hash_function_1(x2)
z1 = hash_function_2(x1)
z2 = hash_function_2(x2)

hash_key_test = z1 % 5
hash_key_test2 = z2 % 5

print("{} hashes to {} with hash_function_1".format(x1, y1))
print("{} hashes to {} with hash_function_1 \n".format(x2, y2))
print("{} hashes to {} with hash_function_2".format(x1, z1))
print("{} hashes to {} with hash_function_2".format(x2, z2))

print(hash_key_test)
print(hash_key_test2)
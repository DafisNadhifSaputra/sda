from node import Node 
from memo import Memo 

class SinglyLinkedList:
    """Implementasi Singly Linked List kustom untuk menyimpan objek Memo."""
    def __init__(self):
        self.head = None

    def is_empty(self):
        return self.head is None

    def appends(self, data):
        new_node = Node(data)
        if self.is_empty():
            self.head = new_node
            return
        last_node = self.head
        while last_node.next:
            last_node = last_node.next
        last_node.next = new_node

    def display(self): # Untuk debugging atau versi konsol
        if self.is_empty():
            print("Tidak ada data memo.")
            return
        current = self.head
        count = 1
        while current:
            print(f"--- Memo {count} ---")
            print(current.data)
            current = current.next
            count += 1

    def cari_node_by_judul(self, judul):
        current = self.head
        while current:
            if current.data.judul.lower() == judul.lower():
                return current
            current = current.next
        return None

    def delete_node_by_judul(self, judul):
        if self.is_empty():
            # print("List kosong, tidak ada yang bisa dihapus.") # Akan ditangani GUI
            return False
        if self.head.data.judul.lower() == judul.lower():
            self.head = self.head.next
            # print(f"Memo '{judul}' berhasil dihapus.")
            return True
        current = self.head
        prev = None
        while current and current.data.judul.lower() != judul.lower():
            prev = current
            current = current.next
        if current is None:
            # print(f"Memo '{judul}' tidak ditemukan.")
            return False
        prev.next = current.next
        # print(f"Memo '{judul}' berhasil dihapus.")
        return True

    def get_length(self):
        count = 0
        current = self.head
        while current:
            count += 1
            current = current.next
        return count

    def insertion_sort_by_judul(self):
        if self.is_empty() or self.head.next is None:
            return
        sorted_list_head = None
        current = self.head
        while current:
            next_node_to_process = current.next
            if sorted_list_head is None or \
               current.data.judul.lower() <= sorted_list_head.data.judul.lower():
                current.next = sorted_list_head
                sorted_list_head = current
            else:
                search_ptr = sorted_list_head
                while search_ptr.next is not None and \
                      search_ptr.next.data.judul.lower() < current.data.judul.lower():
                    search_ptr = search_ptr.next
                current.next = search_ptr.next
                search_ptr.next = current
            current = next_node_to_process
        self.head = sorted_list_head
        # print("Memo telah diurutkan berdasarkan judul.")

    def insertion_sort_by_tanggal(self):
        if self.is_empty() or self.head.next is None:
            return
        sorted_list_head = None
        current = self.head
        while current:
            next_node_to_process = current.next
            if sorted_list_head is None or \
               current.data.created_tanggal <= sorted_list_head.data.created_tanggal:
                current.next = sorted_list_head
                sorted_list_head = current
            else:
                search_ptr = sorted_list_head
                while search_ptr.next is not None and \
                      search_ptr.next.data.created_tanggal < current.data.created_tanggal:
                    search_ptr = search_ptr.next
                current.next = search_ptr.next
                search_ptr.next = current
            current = next_node_to_process
        self.head = sorted_list_head
        # print("Memo telah diurutkan berdasarkan tanggal.")

    def to_list_of_dicts(self):
        if self.is_empty():
            return []
        count = self.get_length()
        result = [None] * count
        current = self.head
        index = 0
        while current and index < count:
            result[index] = current.data.to_dict()
            current = current.next
            index += 1
        return result

    def load_from_list_of_dicts(self, list_of_dicts):
        self.head = None
        for data_dict in list_of_dicts:
            data_obj = Memo.from_dict(data_dict) # Menggunakan Memo dari memo.py
            self.appends(data_obj)
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, simpledialog
import json
from memo import Memo
from linkedlist import SinglyLinkedList # Tidak lagi Node karena sudah dihandle linkedlist
# Node tidak perlu diimpor langsung di GUI lagi

class MemoAppGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Aplikasi Memo Sederhana - GUI Version")
        self.root.geometry("800x600") # Ukuran disesuaikan
        self.root.configure(bg='#f0f0f0')

        # Data
        self.memos_list = SinglyLinkedList() # Satu list utama untuk semua memo
        self.data_file = "memos_data.json" # Nama file data baru

        # Muat data
        self.load_data_dari_json()
        if self.memos_list.is_empty(): # Cek apakah list memo kosong
            self._inisialisasi_default_memos()

        # Buat GUI
        self.buat_widget()
        self.perbarui_daftar_memo() # Langsung perbarui daftar memo global

    def _inisialisasi_default_memos(self):
        """Inisialisasi memo default jika belum ada."""
        default_memos_data = [
            ("Catatan Belanja", "Beli susu, telur, dan roti."),
            ("Tugas SDA", "Selesaikan implementasi LinkedList dan Sorting."),
            ("Ide Proyek", "Buat aplikasi memo sederhana dengan Python Tkinter.")
        ]
        for judul, konten in default_memos_data:
            if not self.memos_list.cari_node_by_judul(judul): # Cek duplikasi
                self.memos_list.appends(Memo(judul, konten))
        self.simpan_data_ke_json()

    def buat_widget(self):
        """Membuat semua widget GUI."""
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        title_label = ttk.Label(main_frame, text="Aplikasi Memo",
                               font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20)) # columnspan 2

        # Panel Kiri (Sebelumnya Middle) - Daftar Memo Global
        list_memo_frame = ttk.LabelFrame(main_frame, text="Daftar Semua Memo", padding="10")
        list_memo_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0,5))

        self.memos_tree = ttk.Treeview(list_memo_frame, columns=('judul', 'tanggal'),
                                      show='headings', height=20) # Tinggi disesuaikan
        self.memos_tree.heading('judul', text='Judul')
        self.memos_tree.heading('tanggal', text='Tanggal')
        self.memos_tree.column('judul', width=200)
        self.memos_tree.column('tanggal', width=150)
        self.memos_tree.grid(row=0, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.memos_tree.bind('<<TreeviewSelect>>', self.saat_memo_dipilih)

        memo_button_frame = ttk.Frame(list_memo_frame)
        memo_button_frame.grid(row=1, column=0, columnspan=3, pady=(10, 0), sticky=tk.W+tk.E)

        ttk.Button(memo_button_frame, text="Tambah Memo",
                  command=self.tambah_memo).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(memo_button_frame, text="Edit Memo",
                  command=self.edit_memo).pack(side=tk.LEFT, padx=5)
        ttk.Button(memo_button_frame, text="Hapus Memo",
                  command=self.hapus_memo).pack(side=tk.LEFT, padx=5)

        sort_frame = ttk.Frame(list_memo_frame)
        sort_frame.grid(row=2, column=0, columnspan=3, pady=(5, 0), sticky=tk.W+tk.E)

        ttk.Button(sort_frame, text="Urutkan: Judul",
                  command=self.urutkan_berdasarkan_judul).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(sort_frame, text="Urutkan: Tanggal",
                  command=self.urutkan_berdasarkan_tanggal).pack(side=tk.LEFT, padx=5)
        ttk.Button(sort_frame, text="Cari Memo",
                  command=self.cari_memo).pack(side=tk.LEFT, padx=5)
        ttk.Button(sort_frame, text="Ekspor ke TXT",
                  command=self.ekspor_semua_memo_ke_txt).pack(side=tk.LEFT, padx=5) # Nama fungsi ekspor diubah

        # Panel Kanan - Konten Memo
        right_frame = ttk.LabelFrame(main_frame, text="Isi Memo", padding="10")
        right_frame.grid(row=1, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(5, 0))

        self.memo_judul_var = tk.StringVar()
        ttk.Label(right_frame, text="Judul:").grid(row=0, column=0, sticky=tk.W)
        judul_entry = ttk.Entry(right_frame, textvariable=self.memo_judul_var,
                               state='readonly', width=40)
        judul_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=(0, 5))

        self.memo_tanggal_var = tk.StringVar()
        ttk.Label(right_frame, text="Tanggal:").grid(row=1, column=0, sticky=tk.W)
        tanggal_entry = ttk.Entry(right_frame, textvariable=self.memo_tanggal_var,
                              state='readonly', width=40)
        tanggal_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=(0, 10))

        ttk.Label(right_frame, text="Konten:").grid(row=2, column=0, sticky=tk.W+tk.N)
        self.note_content = scrolledtext.ScrolledText(right_frame, width=50, height=25,
                                                     state='disabled', wrap=tk.WORD)
        self.note_content.grid(row=2, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))

        # Konfigurasi bobot grid
        main_frame.grid_rowconfigure(1, weight=1)
        main_frame.grid_columnconfigure(0, weight=1) # Panel daftar memo
        main_frame.grid_columnconfigure(1, weight=1) # Panel isi memo

        list_memo_frame.grid_rowconfigure(0, weight=1)
        list_memo_frame.grid_columnconfigure(0, weight=1)

        right_frame.grid_rowconfigure(2, weight=1)
        right_frame.grid_columnconfigure(1, weight=1)

    def perbarui_daftar_memo(self):
        """Memperbarui daftar semua memo di treeview."""
        for item in self.memos_tree.get_children():
            self.memos_tree.delete(item)

        if self.memos_list.is_empty():
            return

        current = self.memos_list.head
        while current:
            memo = current.data
            self.memos_tree.insert('', tk.END, values=(memo.judul, memo.created_tanggal))
            current = current.next

    def saat_memo_dipilih(self, event):
        """Handler ketika memo dipilih."""
        selection = self.memos_tree.selection()
        if selection:
            item = self.memos_tree.item(selection[0])
            memo_judul = item['values'][0]
            
            # Cari memo di self.memos_list (tidak lagi self.current_memobook)
            node = self.memos_list.cari_node_by_judul(memo_judul)
            if node:
                self.tampilkan_memo(node.data)

    def tampilkan_memo(self, memo):
        """Menampilkan isi memo di panel kanan."""
        self.memo_judul_var.set(memo.judul)
        self.memo_tanggal_var.set(memo.created_tanggal)

        self.note_content.config(state='normal')
        self.note_content.delete(1.0, tk.END)
        self.note_content.insert(1.0, memo.content)
        self.note_content.config(state='disabled')

    def bersihkan_tampilan_memo(self):
        """Membersihkan tampilan memo."""
        self.memo_judul_var.set("")
        self.memo_tanggal_var.set("")
        self.note_content.config(state='normal')
        self.note_content.delete(1.0, tk.END)
        self.note_content.config(state='disabled')

    def tambah_memo(self):
        """Menambah memo baru ke daftar global."""
        dialog = MemoDialog(self.root, "Tambah Memo Baru")
        if dialog.result:
            judul, content = dialog.result

            if self.memos_list.cari_node_by_judul(judul):
                messagebox.showerror("Error", "Memo dengan judul tersebut sudah ada.")
                return

            new_memo = Memo(judul, content)
            self.memos_list.appends(new_memo)

            self.perbarui_daftar_memo()
            self.simpan_data_ke_json()
            messagebox.showinfo("Sukses", f"Memo '{judul}' berhasil ditambahkan.")

    def edit_memo(self):
        """Mengedit memo yang dipilih."""
        selection = self.memos_tree.selection()
        if not selection:
            messagebox.showwarning("Peringatan", "Pilih memo yang akan diedit.")
            return

        item = self.memos_tree.item(selection[0])
        memo_judul_lama = item['values'][0]

        memo_node = self.memos_list.cari_node_by_judul(memo_judul_lama)

        if memo_node:
            memo_to_edit = memo_node.data
            dialog = MemoDialog(self.root, f"Edit Memo: {memo_judul_lama}",
                                memo_judul=memo_to_edit.judul, memo_content=memo_to_edit.content)
            if dialog.result:
                new_judul, new_content = dialog.result

                if new_judul.lower() != memo_to_edit.judul.lower(): # Hanya cek jika judul berubah
                    existing = self.memos_list.cari_node_by_judul(new_judul)
                    if existing:
                        messagebox.showerror("Error", "Judul baru sudah digunakan oleh memo lain.")
                        return

                memo_to_edit.update_judul(new_judul)
                memo_to_edit.update_content(new_content)

                self.perbarui_daftar_memo()
                # Jika memo yang diedit sedang ditampilkan, perbarui juga
                if self.memo_judul_var.get() == memo_judul_lama:
                    self.tampilkan_memo(memo_to_edit)
                self.simpan_data_ke_json()
                messagebox.showinfo("Sukses", "Memo berhasil diupdate.")
        else:
            messagebox.showerror("Error", f"Memo '{memo_judul_lama}' tidak ditemukan untuk diedit.")


    def hapus_memo(self):
        """Menghapus memo yang dipilih."""
        selection = self.memos_tree.selection()
        if not selection:
            messagebox.showwarning("Peringatan", "Pilih memo yang akan dihapus.")
            return

        item = self.memos_tree.item(selection[0])
        memo_judul = item['values'][0]

        result = messagebox.askyesno("Konfirmasi",
                                   f"Apakah Anda yakin ingin menghapus memo '{memo_judul}'?")
        if result:
            if self.memos_list.delete_node_by_judul(memo_judul):
                self.perbarui_daftar_memo()
                self.bersihkan_tampilan_memo()
                self.simpan_data_ke_json()
                messagebox.showinfo("Sukses", f"Memo '{memo_judul}' berhasil dihapus.")
            else:
                messagebox.showerror("Error", f"Memo '{memo_judul}' tidak ditemukan untuk dihapus.")


    def urutkan_berdasarkan_judul(self):
        """Mengurutkan semua memo berdasarkan judul."""
        self.memos_list.insertion_sort_by_judul()
        self.perbarui_daftar_memo()
        self.simpan_data_ke_json()
        messagebox.showinfo("Sukses", "Memo berhasil diurutkan berdasarkan judul.")

    def urutkan_berdasarkan_tanggal(self):
        """Mengurutkan semua memo berdasarkan tanggal."""
        self.memos_list.insertion_sort_by_tanggal()
        self.perbarui_daftar_memo()
        self.simpan_data_ke_json()
        messagebox.showinfo("Sukses", "Memo berhasil diurutkan berdasarkan tanggal.")

    def cari_memo(self):
        """Mencari memo berdasarkan judul di daftar global."""
        judul_to_search = simpledialog.askstring("Cari Memo", "Masukkan judul memo yang dicari:")
        if judul_to_search:
            node = self.memos_list.cari_node_by_judul(judul_to_search)
            if node:
                for item_id in self.memos_tree.get_children():
                    if self.memos_tree.item(item_id)['values'][0] == node.data.judul:
                        self.memos_tree.selection_set(item_id)
                        self.memos_tree.focus(item_id)
                        self.tampilkan_memo(node.data)
                        break
                messagebox.showinfo("Ditemukan", f"Memo '{judul_to_search}' ditemukan dan dipilih.")
            else:
                messagebox.showinfo("Tidak Ditemukan", f"Memo '{judul_to_search}' tidak ditemukan.")

    def ekspor_semua_memo_ke_txt(self):
        """Mengekspor semua memo ke file TXT."""
        if self.memos_list.is_empty():
            messagebox.showwarning("Peringatan", "Tidak ada memo untuk diekspor.")
            return

        filename = "semua_memo_export.txt"
        try:
            with open(filename, "w", encoding="utf-8") as f:
                f.write(f"--- Semua Memo ---\n\n")
                current = self.memos_list.head
                memo_count = 1
                while current:
                    f.write(f"--- Memo {memo_count} ---\n")
                    f.write(f"Judul: {current.data.judul}\n")
                    f.write(f"Tanggal: {current.data.created_tanggal}\n")
                    f.write("Konten:\n")
                    f.write(current.data.content.replace("\\n", "\n")) # Ganti \\n jadi newline asli
                    f.write("\n\n--------------------------\n\n")
                    current = current.next
                    memo_count += 1
            messagebox.showinfo("Sukses", f"Semua memo berhasil diekspor ke '{filename}'.")
        except IOError:
            messagebox.showerror("Error", f"Gagal mengekspor memo. Terjadi kesalahan saat menulis ke file '{filename}'.")


    def simpan_data_ke_json(self):
        """Menyimpan daftar memo ke file JSON."""
        # Data yang disimpan adalah list dari dictionary memo
        data_to_save = self.memos_list.to_list_of_dicts()
        try:
            with open(self.data_file, "w", encoding="utf-8") as f:
                json.dump(data_to_save, f, indent=4)
        except Exception as e:
            messagebox.showerror("Error", f"Gagal menyimpan data: {str(e)}")

    def load_data_dari_json(self):
        """Memuat daftar memo dari file JSON."""
        try:
            with open(self.data_file, "r", encoding="utf-8") as f:
                # Data yang dimuat adalah list dari dictionary memo
                list_of_memo_dicts = json.load(f)
                self.memos_list.load_from_list_of_dicts(list_of_memo_dicts)
        except FileNotFoundError:
            self.memos_list = SinglyLinkedList() # Atau biarkan kosong jika file tidak ada
        except json.JSONDecodeError:
            self.memos_list = SinglyLinkedList()
            messagebox.showerror("Error", "File data memiliki format JSON yang tidak valid.")
        except Exception as e:
            self.memos_list = SinglyLinkedList()
            messagebox.showerror("Error", f"Terjadi kesalahan saat memuat data: {str(e)}")

class MemoDialog: # Kelas ini bisa tetap sama
    def __init__(self, parent, title, memo_judul="", memo_content=""):
        self.result = None
        self.dialog = tk.Toplevel(parent)
        self.dialog.title(title)
        self.dialog.geometry("600x400")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        self.dialog.geometry(f"+{parent.winfo_rootx()+50}+{parent.winfo_rooty()+50}")

        main_frame = ttk.Frame(self.dialog, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(main_frame, text="Judul:").pack(anchor=tk.W)
        self.judul_entry = ttk.Entry(main_frame, width=60)
        self.judul_entry.pack(fill=tk.X, pady=(0, 10))
        self.judul_entry.insert(0, memo_judul)

        ttk.Label(main_frame, text="Konten:").pack(anchor=tk.W)
        self.content_text = scrolledtext.ScrolledText(main_frame, width=60, height=15, wrap=tk.WORD)
        self.content_text.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        # Ganti "\\n" dengan newline asli saat memuat ke ScrolledText
        self.content_text.insert(1.0, memo_content.replace("\\n", "\n"))


        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X)

        ttk.Button(button_frame, text="Simpan", command=self.simpan).pack(side=tk.RIGHT, padx=(10, 0))
        ttk.Button(button_frame, text="Batal", command=self.batal).pack(side=tk.RIGHT)

        self.judul_entry.focus()
        self.dialog.bind('<Return>', self.saat_enter_ditekan)
        self.dialog.bind('<Escape>', self.saat_escape_ditekan)
        self.dialog.wait_window()

    def simpan(self):
        judul = self.judul_entry.get().strip()
        content_raw = self.content_text.get(1.0, tk.END).strip()
        # Simpan newline sebagai "\\n" untuk konsistensi internal dan JSON
        content = content_raw.replace("\n", "\\n")


        if not judul:
            messagebox.showerror("Error", "Judul tidak boleh kosong.", parent=self.dialog)
            return
        if not content_raw: # Validasi berdasarkan content_raw sebelum replace
            messagebox.showerror("Error", "Konten tidak boleh kosong.", parent=self.dialog)
            return

        self.result = (judul, content)
        self.dialog.destroy()

    def batal(self):
        self.dialog.destroy()

    def saat_enter_ditekan(self, event):
        self.simpan()

    def saat_escape_ditekan(self, event):
        self.batal()

def main():
    root = tk.Tk()
    app = MemoAppGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
"""
kelolabuku.py
Halaman kelola buku: tambah, ubah, hapus, dan cari judul/penulis.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import db

WARNA_AKSEN = "#3b6fe0"


class JendelaKelolaBuku(tk.Toplevel):
    def __init__(self, induk, user):
        super().__init__(induk)
        self.user = user
        self.title("Kelola Buku")
        self.geometry("700x460")
        db.layar_penuh(self)
        self._buat_tampilan()
        self._muat_data()

    def _buat_tampilan(self):
        atas = tk.Frame(self)
        atas.pack(fill="x", padx=15, pady=10)
        tk.Label(atas, text="Kelola buku", font=("Segoe UI", 13, "bold")).pack(side="left")

        cari_frame = tk.Frame(atas)
        cari_frame.pack(side="right")
        self.var_cari = tk.StringVar()
        entri_cari = ttk.Entry(cari_frame, textvariable=self.var_cari, width=20)
        entri_cari.pack(side="left", padx=5)
        entri_cari.bind("<Return>", lambda e: self._muat_data())
        tk.Button(cari_frame, text="Cari", command=self._muat_data).pack(side="left")
        tk.Button(cari_frame, text="+ Tambah", bg=WARNA_AKSEN, fg="white", relief="flat",
                  command=self.form_tambah).pack(side="left", padx=5)

        kolom = ("judul", "penulis", "kategori", "stok", "rating", "status")
        self.tabel = ttk.Treeview(self, columns=kolom, show="headings", height=14)
        label_kolom = {"judul": "Judul", "penulis": "Penulis", "kategori": "Kategori",
                       "stok": "Stok", "rating": "Rating", "status": "Status"}
        for k in kolom:
            self.tabel.heading(k, text=label_kolom[k])
            self.tabel.column(k, width=100)
        self.tabel.pack(fill="both", expand=True, padx=15, pady=10)

        bawah = tk.Frame(self)
        bawah.pack(fill="x", padx=15, pady=5)
        tk.Button(bawah, text="Ubah", command=self.form_ubah).pack(side="left")
        tk.Button(bawah, text="Hapus", command=self.hapus).pack(side="left", padx=5)

    def _muat_data(self):
        for i in self.tabel.get_children():
            self.tabel.delete(i)
        kata = self.var_cari.get().lower()
        for b in db.semua_buku():
            if kata and kata not in b["judul"].lower() and kata not in (b["penulis"] or "").lower():
                continue
            self.tabel.insert("", "end", iid=b["id"],
                values=(b["judul"], b["penulis"], b["kategori"], b["stok"], b["rating"], b["status"]))

    def _dipilih(self):
        pilihan = self.tabel.selection()
        if not pilihan:
            messagebox.showwarning("Perhatian", "Pilih data terlebih dahulu.")
            return None
        return int(pilihan[0])

    def form_tambah(self):
        FormBuku(self, on_simpan=self._muat_data)

    def form_ubah(self):
        id_buku = self._dipilih()
        if id_buku:
            data = db.get_buku(id_buku)
            FormBuku(self, data=data, on_simpan=self._muat_data)

    def hapus(self):
        id_buku = self._dipilih()
        if id_buku and messagebox.askyesno("Konfirmasi", "Hapus buku ini?"):
            db.hapus_buku(id_buku)
            self._muat_data()


class FormBuku(tk.Toplevel):
    def __init__(self, induk, data=None, on_simpan=None):
        super().__init__(induk)
        self.data = data
        self.on_simpan = on_simpan
        self.title("Ubah buku" if data else "Tambah buku")
        self.geometry("320x340")

        self.entri = {}
        kolom = [("judul", "Judul"), ("penulis", "Penulis"), ("kategori", "Kategori"),
                 ("stok", "Stok"), ("rating", "Rating (0-5)")]
        for kunci, label in kolom:
            tk.Label(self, text=label).pack(anchor="w", padx=15, pady=(8, 0))
            e = ttk.Entry(self)
            e.pack(fill="x", padx=15)
            if data:
                e.insert(0, data[kunci])
            self.entri[kunci] = e

        tk.Button(self, text="Simpan", bg=WARNA_AKSEN, fg="white", relief="flat",
                  command=self.simpan).pack(fill="x", padx=15, pady=15)

    def simpan(self):
        judul = self.entri["judul"].get().strip()
        penulis = self.entri["penulis"].get().strip()
        kategori = self.entri["kategori"].get().strip()
        stok = self.entri["stok"].get().strip()
        rating = self.entri["rating"].get().strip() or "0"

        if not judul or not stok:
            messagebox.showwarning("Perhatian", "Judul dan stok wajib diisi.")
            return
        try:
            stok = int(stok)
            rating = float(rating)
        except ValueError:
            messagebox.showerror("Gagal", "Stok harus angka bulat, rating harus angka desimal.")
            return

        if self.data:
            db.update_buku(self.data["id"], judul, penulis, kategori, stok, rating)
        else:
            db.tambah_buku(judul, penulis, kategori, stok, rating)

        if self.on_simpan:
            self.on_simpan()
        self.destroy()


if __name__ == "__main__":
    db.init_db()
    root = tk.Tk()
    root.withdraw()
    JendelaKelolaBuku(root, {"peran": "Petugas", "nama": "Uji Coba"})
    root.mainloop()

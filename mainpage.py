"""
mainpage.py
Halaman utama (dasbor) setelah login berhasil. Berisi sidebar navigasi
menuju halaman kelola buku, kelola user, dan kelola peminjaman.
"""

import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import db

WARNA_AKSEN = "#3b6fe0"
WARNA_BG_AKSEN = "#e8effd"
WARNA_ABU = "#6b7280"


class HalamanUtama(tk.Tk):
    def __init__(self, user):
        super().__init__()
        self.user = user  # dict: id, nama, email, peran, ...
        self.title("Perpus Digital - Dasbor")
        self.geometry("980x600")
        db.layar_penuh(self)
        db.perbarui_status_terlambat()
        self._buat_sidebar()
        self._buat_konten()

    def _buat_sidebar(self):
        sisi = tk.Frame(self, bg="#fafbfc", width=110)
        sisi.pack(side="left", fill="y")
        sisi.pack_propagate(False)

        tk.Label(sisi, text="📚 Perpus Digital", font=("Segoe UI", 11, "bold"),
                 bg="#fafbfc").pack(pady=20)

        # Tombol navigasi biasa, sederhana tanpa binding rumit
        tk.Button(sisi, text="🏠 Utama", font=("Segoe UI", 9, "bold"), fg=WARNA_AKSEN,
                  bg="#fafbfc", relief="flat", anchor="w",
                  command=lambda: None).pack(fill="x", padx=10, pady=4)
        tk.Button(sisi, text="📗 Buku", font=("Segoe UI", 9), fg=WARNA_ABU,
                  bg="#fafbfc", relief="flat", anchor="w",
                  command=self.buka_kelola_buku).pack(fill="x", padx=10, pady=4)
        tk.Button(sisi, text="👤 User", font=("Segoe UI", 9), fg=WARNA_ABU,
                  bg="#fafbfc", relief="flat", anchor="w",
                  command=self.buka_kelola_user).pack(fill="x", padx=10, pady=4)
        tk.Button(sisi, text="📋 Pinjam", font=("Segoe UI", 9), fg=WARNA_ABU,
                  bg="#fafbfc", relief="flat", anchor="w",
                  command=self.buka_kelola_peminjaman).pack(fill="x", padx=10, pady=4)

        tk.Button(sisi, text="Keluar", font=("Segoe UI", 9), relief="flat",
                  command=self.keluar).pack(side="bottom", fill="x", padx=10, pady=15)

    def _buat_konten(self):
        konten = tk.Frame(self, bg="white")
        konten.pack(side="left", fill="both", expand=True)

        atas = tk.Frame(konten, bg="white")
        atas.pack(fill="x", padx=20, pady=15)
        tk.Label(atas, text="Dasbor", font=("Segoe UI", 15, "bold"), bg="white").pack(anchor="w")
        tanggal = datetime.now().strftime("%d-%m-%Y")
        tk.Label(atas, text=f"Selamat datang, {self.user['nama']} ({self.user['peran']}) · {tanggal}",
                 font=("Segoe UI", 9), fg=WARNA_ABU, bg="white").pack(anchor="w")

        self.frame_statistik = tk.Frame(konten, bg="white")
        self.frame_statistik.pack(fill="x", padx=20)
        self._muat_statistik()

        tk.Button(konten, text="🔄 Segarkan data", relief="flat", bg="#f4f5f7",
                  command=self._muat_statistik).pack(anchor="w", padx=20, pady=15)

    def _muat_statistik(self):
        for w in self.frame_statistik.winfo_children():
            w.destroy()

        total_buku = len(db.semua_buku())
        total_dipinjam = len([p for p in db.semua_peminjaman() if p["status"] != "Selesai"])
        total_anggota = len([u for u in db.semua_user() if u["peran"] == "Anggota"])
        total_terlambat = len([p for p in db.semua_peminjaman() if p["status"] == "Terlambat"])

        kartu = [
            ("Total buku", total_buku, "#f4f5f7", "#1c1e21"),
            ("Dipinjam", total_dipinjam, "#f4f5f7", "#1c1e21"),
            ("Anggota", total_anggota, "#f4f5f7", "#1c1e21"),
            ("Terlambat", total_terlambat, "#fdeaea", "#d94040"),
        ]
        for i, (label, nilai, bg, fg) in enumerate(kartu):
            kotak = tk.Frame(self.frame_statistik, bg=bg, padx=15, pady=10)
            kotak.grid(row=0, column=i, padx=6, sticky="ew")
            self.frame_statistik.columnconfigure(i, weight=1)
            tk.Label(kotak, text=label, font=("Segoe UI", 8), bg=bg, fg=fg).pack(anchor="w")
            tk.Label(kotak, text=str(nilai), font=("Segoe UI", 16, "bold"), bg=bg, fg=fg).pack(anchor="w")

    def buka_kelola_buku(self):
        import kelolabuku
        kelolabuku.JendelaKelolaBuku(self, self.user)

    def buka_kelola_user(self):
        if self.user["peran"] != "Petugas":
            messagebox.showwarning("Ditolak", "Hanya petugas yang dapat mengakses halaman ini.")
            return
        import kelolauser
        kelolauser.JendelaKelolaUser(self, self.user)

    def buka_kelola_peminjaman(self):
        import kelolapeminjamam
        kelolapeminjamam.JendelaKelolaPeminjaman(self, self.user)

    def keluar(self):
        self.destroy()
        import login
        app = login.HalamanLogin()
        app.mainloop()


if __name__ == "__main__":
    db.init_db()
    user_uji = dict(db.cek_login("admin@perpus.com", "admin123"))
    app = HalamanUtama(user_uji)
    app.mainloop()

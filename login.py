"""
login.py
Halaman login sekaligus titik masuk (entry point) aplikasi.
Jalankan file ini untuk memulai program: python login.py
"""

import tkinter as tk
from tkinter import ttk, messagebox
import db

WARNA_AKSEN = "#3b6fe0"
WARNA_BG_AKSEN = "#e8effd"


class HalamanLogin(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Perpus Digital - Login")
        self.geometry("640x420")
        self.configure(bg="white")
        db.layar_penuh(self)
        self.peran_dipilih = tk.StringVar(value="Petugas")
        self._buat_tampilan()

    def _buat_tampilan(self):
        # panel kiri (informasi)
        kiri = tk.Frame(self, bg=WARNA_BG_AKSEN, width=250)
        kiri.pack(side="left", fill="both")
        kiri.pack_propagate(False)
        tk.Label(kiri, text="📚", font=("Segoe UI Emoji", 30), bg=WARNA_BG_AKSEN).pack(pady=(90, 10))
        tk.Label(kiri, text="Perpus Digital", font=("Segoe UI", 16, "bold"),
                 fg=WARNA_AKSEN, bg=WARNA_BG_AKSEN).pack()
        tk.Label(kiri, text="Kelola koleksi, anggota, dan\npeminjaman dalam satu sistem",
                 font=("Segoe UI", 9), fg=WARNA_AKSEN, bg=WARNA_BG_AKSEN, justify="center").pack(pady=8)

        # panel kanan (form login)
        kanan = tk.Frame(self, bg="white")
        kanan.pack(side="left", fill="both", expand=True, padx=30, pady=30)

        tk.Label(kanan, text="Masuk sebagai", font=("Segoe UI", 9), fg="#6b7280", bg="white").pack(anchor="w")
        peran_frame = tk.Frame(kanan, bg="white")
        peran_frame.pack(anchor="w", pady=(2, 15))
        ttk.Radiobutton(peran_frame, text="Petugas", value="Petugas",
                        variable=self.peran_dipilih).pack(side="left")
        ttk.Radiobutton(peran_frame, text="Anggota", value="Anggota",
                        variable=self.peran_dipilih).pack(side="left", padx=10)

        tk.Label(kanan, text="Email", font=("Segoe UI", 9), fg="#6b7280", bg="white").pack(anchor="w")
        self.input_email = ttk.Entry(kanan, width=32)
        self.input_email.pack(pady=(2, 10), fill="x")

        tk.Label(kanan, text="Kata sandi", font=("Segoe UI", 9), fg="#6b7280", bg="white").pack(anchor="w")
        self.input_password = ttk.Entry(kanan, width=32, show="•")
        self.input_password.pack(pady=(2, 15), fill="x")
        self.input_password.bind("<Return>", lambda e: self.proses_login())

        tk.Button(kanan, text="Masuk", bg=WARNA_AKSEN, fg="white", relief="flat",
                  font=("Segoe UI", 10, "bold"), command=self.proses_login).pack(fill="x", ipady=6)

        bawah = tk.Frame(kanan, bg="white")
        bawah.pack(pady=12)
        tk.Label(bawah, text="Belum punya akun?", bg="white", fg="#6b7280", font=("Segoe UI", 9)).pack(side="left")
        link_daftar = tk.Label(bawah, text=" Daftar", bg="white", fg=WARNA_AKSEN,
                                font=("Segoe UI", 9, "bold"), cursor="hand2")
        link_daftar.pack(side="left")
        link_daftar.bind("<Button-1>", self.buka_daftar)

        tk.Label(kanan, text="Contoh akun petugas: admin@perpus.com / admin123",
                 font=("Segoe UI", 8), fg="#9aa0a8", bg="white").pack(pady=(10, 0))

    def proses_login(self):
        email = self.input_email.get().strip()
        password = self.input_password.get().strip()
        peran = self.peran_dipilih.get()

        if not email or not password:
            messagebox.showwarning("Perhatian", "Email dan kata sandi wajib diisi.")
            return

        user = db.cek_login(email, password)
        if user is None:
            messagebox.showerror("Gagal", "Email atau kata sandi salah.")
            return
        if user["peran"] != peran:
            messagebox.showerror("Gagal", f"Akun ini terdaftar sebagai {user['peran']}, bukan {peran}.")
            return
        if user["status"] != "Aktif":
            messagebox.showerror("Gagal", "Akun Anda nonaktif. Hubungi petugas.")
            return

        self.destroy()
        import mainpage
        app = mainpage.HalamanUtama(dict(user))
        app.mainloop()

    def buka_daftar(self, event=None):
        self.destroy()
        import daftar
        app = daftar.HalamanDaftar()
        app.mainloop()


if __name__ == "__main__":
    db.init_db()
    app = HalamanLogin()
    app.mainloop()

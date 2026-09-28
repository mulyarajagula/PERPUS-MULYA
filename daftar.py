"""
daftar.py
Halaman pendaftaran akun baru (khusus peran Anggota).
"""

import tkinter as tk
from tkinter import ttk, messagebox
import db

WARNA_AKSEN = "#3b6fe0"
WARNA_BG_AKSEN = "#e8effd"


class HalamanDaftar(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Perpus Digital - Daftar")
        self.geometry("640x480")
        self.configure(bg="white")
        db.layar_penuh(self)
        self._buat_tampilan()

    def _buat_tampilan(self):
        kiri = tk.Frame(self, bg=WARNA_BG_AKSEN, width=220)
        kiri.pack(side="left", fill="both")
        kiri.pack_propagate(False)
        tk.Label(kiri, text="📝", font=("Segoe UI Emoji", 28), bg=WARNA_BG_AKSEN).pack(pady=(110, 10))
        tk.Label(kiri, text="Bergabung sekarang", font=("Segoe UI", 13, "bold"),
                 fg=WARNA_AKSEN, bg=WARNA_BG_AKSEN, wraplength=170, justify="center").pack()
        tk.Label(kiri, text="Akses katalog dan pinjam\nbuku lebih mudah",
                 font=("Segoe UI", 9), fg=WARNA_AKSEN, bg=WARNA_BG_AKSEN, justify="center").pack(pady=8)

        kanan = tk.Frame(self, bg="white")
        kanan.pack(side="left", fill="both", expand=True, padx=25, pady=20)

        self.entri = {}
        kolom = [
            ("nama", "Nama lengkap"), ("no_induk", "No. induk"),
            ("email", "Email"), ("no_hp", "No. HP"),
            ("password", "Kata sandi"), ("konfirmasi", "Konfirmasi sandi"),
        ]
        grid = tk.Frame(kanan, bg="white")
        grid.pack(fill="x", pady=(10, 0))
        for i, (kunci, label) in enumerate(kolom):
            baris, kolom_pos = divmod(i, 2)
            sub = tk.Frame(grid, bg="white")
            sub.grid(row=baris, column=kolom_pos, padx=5, pady=6, sticky="ew")
            tk.Label(sub, text=label, font=("Segoe UI", 8), fg="#6b7280", bg="white").pack(anchor="w")
            tampil = "•" if "sandi" in kunci else None
            entri = ttk.Entry(sub, width=22, show=tampil)
            entri.pack()
            self.entri[kunci] = entri
        grid.columnconfigure(0, weight=1)
        grid.columnconfigure(1, weight=1)

        self.var_setuju = tk.BooleanVar()
        ttk.Checkbutton(kanan, text="Saya setuju dengan ketentuan perpustakaan",
                        variable=self.var_setuju).pack(anchor="w", pady=(10, 5))

        tk.Button(kanan, text="Daftar", bg=WARNA_AKSEN, fg="white", relief="flat",
                  font=("Segoe UI", 10, "bold"), command=self.proses_daftar).pack(fill="x", ipady=6)

        bawah = tk.Frame(kanan, bg="white")
        bawah.pack(pady=10)
        tk.Label(bawah, text="Sudah punya akun?", bg="white", fg="#6b7280", font=("Segoe UI", 9)).pack(side="left")
        link = tk.Label(bawah, text=" Masuk", bg="white", fg=WARNA_AKSEN,
                        font=("Segoe UI", 9, "bold"), cursor="hand2")
        link.pack(side="left")
        link.bind("<Button-1>", self.kembali_login)

    def proses_daftar(self):
        data = {k: v.get().strip() for k, v in self.entri.items()}
        if not all(data.values()):
            messagebox.showwarning("Perhatian", "Semua kolom wajib diisi.")
            return
        if data["password"] != data["konfirmasi"]:
            messagebox.showerror("Gagal", "Konfirmasi kata sandi tidak cocok.")
            return
        if not self.var_setuju.get():
            messagebox.showwarning("Perhatian", "Anda harus menyetujui ketentuan perpustakaan.")
            return
        if db.email_terpakai(data["email"]):
            messagebox.showerror("Gagal", "Email sudah terdaftar.")
            return

        db.tambah_user(data["nama"], data["email"], data["password"], "Anggota",
                        data["no_induk"], data["no_hp"])
        messagebox.showinfo("Berhasil", "Pendaftaran berhasil. Silakan masuk.")
        self.kembali_login()

    def kembali_login(self, event=None):
        self.destroy()
        import login
        app = login.HalamanLogin()
        app.mainloop()


if __name__ == "__main__":
    db.init_db()
    app = HalamanDaftar()
    app.mainloop()

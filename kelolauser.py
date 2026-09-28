"""
kelolauser.py
Halaman kelola user: tambah, ubah, hapus, cari, dan filter berdasarkan peran.
Hanya dapat diakses oleh Petugas (dicek dari mainpage.py).
"""

import tkinter as tk
from tkinter import ttk, messagebox
import db

WARNA_AKSEN = "#3b6fe0"


class JendelaKelolaUser(tk.Toplevel):
    def __init__(self, induk, user):
        super().__init__(induk)
        self.user = user
        self.title("Kelola User")
        self.geometry("750x460")
        db.layar_penuh(self)
        self.filter_peran = tk.StringVar(value="Semua")
        self._buat_tampilan()
        self._muat_data()

    def _buat_tampilan(self):
        atas = tk.Frame(self)
        atas.pack(fill="x", padx=15, pady=10)
        tk.Label(atas, text="Kelola user", font=("Segoe UI", 13, "bold")).pack(side="left")

        kanan = tk.Frame(atas)
        kanan.pack(side="right")
        self.var_cari = tk.StringVar()
        entri_cari = ttk.Entry(kanan, textvariable=self.var_cari, width=18)
        entri_cari.pack(side="left", padx=5)
        entri_cari.bind("<Return>", lambda e: self._muat_data())
        tk.Button(kanan, text="Cari", command=self._muat_data).pack(side="left")
        tk.Button(kanan, text="+ Tambah", bg=WARNA_AKSEN, fg="white", relief="flat",
                  command=self.form_tambah).pack(side="left", padx=5)

        tab_frame = tk.Frame(self)
        tab_frame.pack(fill="x", padx=15)
        for nilai in ("Semua", "Petugas", "Anggota"):
            tk.Radiobutton(tab_frame, text=nilai, value=nilai, variable=self.filter_peran,
                           indicatoron=False, command=self._muat_data, padx=10).pack(side="left", padx=3)

        kolom = ("nama", "peran", "email", "no_hp", "bergabung", "status")
        self.tabel = ttk.Treeview(self, columns=kolom, show="headings", height=14)
        label_kolom = {"nama": "Nama", "peran": "Peran", "email": "Email", "no_hp": "No. HP",
                       "bergabung": "Bergabung", "status": "Status"}
        for k in kolom:
            self.tabel.heading(k, text=label_kolom[k])
            self.tabel.column(k, width=110)
        self.tabel.pack(fill="both", expand=True, padx=15, pady=10)

        bawah = tk.Frame(self)
        bawah.pack(fill="x", padx=15, pady=5)
        tk.Button(bawah, text="Ubah", command=self.form_ubah).pack(side="left")
        tk.Button(bawah, text="Hapus", command=self.hapus).pack(side="left", padx=5)

    def _muat_data(self):
        for i in self.tabel.get_children():
            self.tabel.delete(i)
        kata = self.var_cari.get().lower()
        peran = self.filter_peran.get()
        for u in db.semua_user():
            if peran != "Semua" and u["peran"] != peran:
                continue
            if kata and kata not in u["nama"].lower() and kata not in u["email"].lower():
                continue
            self.tabel.insert("", "end", iid=u["id"],
                values=(u["nama"], u["peran"], u["email"], u["no_hp"], u["tanggal_gabung"], u["status"]))

    def _dipilih(self):
        pilihan = self.tabel.selection()
        if not pilihan:
            messagebox.showwarning("Perhatian", "Pilih data terlebih dahulu.")
            return None
        return int(pilihan[0])

    def form_tambah(self):
        FormUser(self, on_simpan=self._muat_data)

    def form_ubah(self):
        id_user = self._dipilih()
        if id_user:
            data = [u for u in db.semua_user() if u["id"] == id_user][0]
            FormUser(self, data=data, on_simpan=self._muat_data)

    def hapus(self):
        id_user = self._dipilih()
        if id_user and messagebox.askyesno("Konfirmasi", "Hapus user ini?"):
            db.hapus_user(id_user)
            self._muat_data()


class FormUser(tk.Toplevel):
    def __init__(self, induk, data=None, on_simpan=None):
        super().__init__(induk)
        self.data = data
        self.on_simpan = on_simpan
        self.title("Ubah user" if data else "Tambah user")
        self.geometry("320x430")

        self.entri = {}
        for kunci, label in [("nama", "Nama"), ("email", "Email"), ("no_hp", "No. HP")]:
            tk.Label(self, text=label).pack(anchor="w", padx=15, pady=(8, 0))
            e = ttk.Entry(self)
            e.pack(fill="x", padx=15)
            if data:
                e.insert(0, data[kunci] or "")
            self.entri[kunci] = e

        if not data:
            tk.Label(self, text="Kata sandi").pack(anchor="w", padx=15, pady=(8, 0))
            e = ttk.Entry(self, show="•")
            e.pack(fill="x", padx=15)
            self.entri["password"] = e

        tk.Label(self, text="Peran").pack(anchor="w", padx=15, pady=(8, 0))
        self.var_peran = tk.StringVar(value=data["peran"] if data else "Anggota")
        ttk.Combobox(self, textvariable=self.var_peran, values=["Petugas", "Anggota"],
                     state="readonly").pack(fill="x", padx=15)

        tk.Label(self, text="Status").pack(anchor="w", padx=15, pady=(8, 0))
        self.var_status = tk.StringVar(value=data["status"] if data else "Aktif")
        ttk.Combobox(self, textvariable=self.var_status, values=["Aktif", "Nonaktif"],
                     state="readonly").pack(fill="x", padx=15)

        tk.Button(self, text="Simpan", bg=WARNA_AKSEN, fg="white", relief="flat",
                  command=self.simpan).pack(fill="x", padx=15, pady=15)

    def simpan(self):
        nama = self.entri["nama"].get().strip()
        email = self.entri["email"].get().strip()
        no_hp = self.entri["no_hp"].get().strip()
        peran = self.var_peran.get()
        status = self.var_status.get()

        if not nama or not email:
            messagebox.showwarning("Perhatian", "Nama dan email wajib diisi.")
            return

        if self.data:
            db.update_user(self.data["id"], nama, email, peran, no_hp, status)
        else:
            password = self.entri["password"].get().strip()
            if not password:
                messagebox.showwarning("Perhatian", "Kata sandi wajib diisi.")
                return
            if db.email_terpakai(email):
                messagebox.showerror("Gagal", "Email sudah digunakan.")
                return
            db.tambah_user(nama, email, password, peran, "-", no_hp)

        if self.on_simpan:
            self.on_simpan()
        self.destroy()


if __name__ == "__main__":
    db.init_db()
    root = tk.Tk()
    root.withdraw()
    JendelaKelolaUser(root, {"peran": "Petugas", "nama": "Uji Coba"})
    root.mainloop()


import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta
import db

WARNA_AKSEN = "#3b6fe0"
DENDA_PER_HARI = 1000  # rupiah


class JendelaKelolaPeminjaman(tk.Toplevel):
    def __init__(self, induk, user):
        super().__init__(induk)
        self.user = user
        self.title("Kelola Peminjaman")
        self.geometry("780x460")
        db.layar_penuh(self)
        db.perbarui_status_terlambat()
        self.filter_status = tk.StringVar(value="Semua")
        self._buat_tampilan()
        self._muat_data()

    def _buat_tampilan(self):
        atas = tk.Frame(self)
        atas.pack(fill="x", padx=15, pady=10)
        tk.Label(atas, text="Peminjaman", font=("Segoe UI", 13, "bold")).pack(side="left")
        tk.Button(atas, text="+ Catat peminjaman", bg=WARNA_AKSEN, fg="white", relief="flat",
                  command=self.form_tambah).pack(side="right")

        tab_frame = tk.Frame(self)
        tab_frame.pack(fill="x", padx=15)
        for nilai in ("Semua", "Dipinjam", "Terlambat", "Selesai"):
            tk.Radiobutton(tab_frame, text=nilai, value=nilai, variable=self.filter_status,
                           indicatoron=False, command=self._muat_data, padx=10).pack(side="left", padx=3)

        kolom = ("peminjam", "buku", "tgl_pinjam", "jatuh_tempo", "denda", "status")
        self.tabel = ttk.Treeview(self, columns=kolom, show="headings", height=14)
        label_kolom = {"peminjam": "Peminjam", "buku": "Buku", "tgl_pinjam": "Tgl pinjam",
                       "jatuh_tempo": "Jatuh tempo", "denda": "Denda", "status": "Status"}
        for k in kolom:
            self.tabel.heading(k, text=label_kolom[k])
            self.tabel.column(k, width=115)
        self.tabel.pack(fill="both", expand=True, padx=15, pady=10)

        bawah = tk.Frame(self)
        bawah.pack(fill="x", padx=15, pady=5)
        tk.Button(bawah, text="Tandai kembali", command=self.kembalikan).pack(side="left")
        tk.Button(bawah, text="Hapus", command=self.hapus).pack(side="left", padx=5)

    def _muat_data(self):
        for i in self.tabel.get_children():
            self.tabel.delete(i)
        status = self.filter_status.get()
        for p in db.semua_peminjaman():
            if status != "Semua" and p["status"] != status:
                continue
            denda = f'Rp{p["denda"]}' if p["denda"] else "-"
            self.tabel.insert("", "end", iid=p["id"], values=(
                p["nama_user"], p["judul_buku"], p["tgl_pinjam"], p["jatuh_tempo"],
                denda, p["status"]))

    def _dipilih(self):
        pilihan = self.tabel.selection()
        if not pilihan:
            messagebox.showwarning("Perhatian", "Pilih data terlebih dahulu.")
            return None
        return int(pilihan[0])

    def form_tambah(self):
        FormPeminjaman(self, on_simpan=self._muat_data)

    def kembalikan(self):
        id_p = self._dipilih()
        if not id_p:
            return
        data = [p for p in db.semua_peminjaman() if p["id"] == id_p][0]
        if data["status"] == "Selesai":
            messagebox.showinfo("Info", "Peminjaman ini sudah selesai.")
            return
        denda = 0
        if data["status"] == "Terlambat":
            hari = (datetime.now() - datetime.strptime(data["jatuh_tempo"], "%Y-%m-%d")).days
            denda = max(hari, 0) * DENDA_PER_HARI
        db.kembalikan_buku(id_p, denda)
        self._muat_data()

    def hapus(self):
        id_p = self._dipilih()
        if id_p and messagebox.askyesno("Konfirmasi", "Hapus data peminjaman ini?"):
            db.hapus_peminjaman(id_p)
            self._muat_data()


class FormPeminjaman(tk.Toplevel):
    def __init__(self, induk, on_simpan=None):
        super().__init__(induk)
        self.on_simpan = on_simpan
        self.title("Catat peminjaman")
        self.geometry("320x270")

        anggota = [u for u in db.semua_user() if u["peran"] == "Anggota"]
        buku_tersedia = [b for b in db.semua_buku() if b["stok"] > 0]
        self.map_anggota = {f'{a["nama"]} ({a["email"]})': a["id"] for a in anggota}
        self.map_buku = {f'{b["judul"]} (stok {b["stok"]})': b["id"] for b in buku_tersedia}

        tk.Label(self, text="Peminjam").pack(anchor="w", padx=15, pady=(10, 0))
        self.var_anggota = tk.StringVar()
        ttk.Combobox(self, textvariable=self.var_anggota, values=list(self.map_anggota.keys()),
                     state="readonly").pack(fill="x", padx=15)

        tk.Label(self, text="Buku").pack(anchor="w", padx=15, pady=(10, 0))
        self.var_buku = tk.StringVar()
        ttk.Combobox(self, textvariable=self.var_buku, values=list(self.map_buku.keys()),
                     state="readonly").pack(fill="x", padx=15)

        tk.Label(self, text="Lama pinjam (hari)").pack(anchor="w", padx=15, pady=(10, 0))
        self.var_lama = tk.StringVar(value="7")
        ttk.Entry(self, textvariable=self.var_lama).pack(fill="x", padx=15)

        tk.Button(self, text="Simpan", bg=WARNA_AKSEN, fg="white", relief="flat",
                  command=self.simpan).pack(fill="x", padx=15, pady=15)

    def simpan(self):
        if not self.var_anggota.get() or not self.var_buku.get():
            messagebox.showwarning("Perhatian", "Pilih peminjam dan buku.")
            return
        try:
            lama = int(self.var_lama.get())
        except ValueError:
            messagebox.showerror("Gagal", "Lama pinjam harus berupa angka.")
            return

        user_id = self.map_anggota[self.var_anggota.get()]
        buku_id = self.map_buku[self.var_buku.get()]
        tgl_pinjam = datetime.now().strftime("%Y-%m-%d")
        jatuh_tempo = (datetime.now() + timedelta(days=lama)).strftime("%Y-%m-%d")

        db.tambah_peminjaman(user_id, buku_id, tgl_pinjam, jatuh_tempo)
        if self.on_simpan:
            self.on_simpan()
        self.destroy()


if __name__ == "__main__":
    db.init_db()
    root = tk.Tk()
    root.withdraw()
    JendelaKelolaPeminjaman(root, {"peran": "Petugas", "nama": "Uji Coba"})
    root.mainloop()

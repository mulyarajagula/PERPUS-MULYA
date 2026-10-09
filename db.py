import sqlite3
import os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "perpustakaan.db")


def layar_penuh(jendela):
    """Membuka jendela dalam keadaan maksimal (layar penuh).
    Tombol F11 = fullscreen tanpa bingkai, Esc = kembali normal."""
    try:
        jendela.state("zoomed")  
    except Exception:
        jendela.attributes("-fullscreen", True)  
    jendela.bind("<F11>", lambda e: jendela.attributes(
        "-fullscreen", not jendela.attributes("-fullscreen")))
    jendela.bind("<Escape>", lambda e: jendela.attributes("-fullscreen", False))


def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nama TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        peran TEXT NOT NULL,
        no_induk TEXT,
        no_hp TEXT,
        status TEXT DEFAULT 'Aktif',
        tanggal_gabung TEXT
    )""")
    cur.execute("""CREATE TABLE IF NOT EXISTS buku (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        judul TEXT NOT NULL,
        penulis TEXT,
        kategori TEXT,
        stok INTEGER DEFAULT 0,
        rating REAL DEFAULT 0,
        status TEXT DEFAULT 'Tersedia'
    )""")
    cur.execute("""CREATE TABLE IF NOT EXISTS peminjaman (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        buku_id INTEGER,
        tgl_pinjam TEXT,
        jatuh_tempo TEXT,
        tgl_kembali TEXT,
        denda INTEGER DEFAULT 0,
        status TEXT DEFAULT 'Dipinjam'
    )""")

  
    cur.execute("SELECT COUNT(*) FROM users")
    if cur.fetchone()[0] == 0:
        cur.execute(
            """INSERT INTO users (nama, email, password, peran, no_induk, no_hp, status, tanggal_gabung)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            ("Admin Petugas", "admin@perpus.com", "admin123", "Petugas", "-", "-",
             "Aktif", datetime.now().strftime("%Y-%m-%d")),
        )
        cur.execute(
            """INSERT INTO buku (judul, penulis, kategori, stok, rating, status)
               VALUES (?, ?, ?, ?, ?, ?)""",
            ("Laskar Pelangi", "Andrea Hirata", "Fiksi", 4, 4.8, "Tersedia"),
        )
        cur.execute(
            """INSERT INTO buku (judul, penulis, kategori, stok, rating, status)
               VALUES (?, ?, ?, ?, ?, ?)""",
            ("Filosofi Teras", "Henry Manampiring", "Nonfiksi", 7, 4.7, "Tersedia"),
        )
    conn.commit()
    conn.close()



def cek_login(email, password):
    conn = get_conn()
    row = conn.execute(
        "SELECT * FROM users WHERE email=? AND password=?", (email, password)
    ).fetchone()
    conn.close()
    return row


def email_terpakai(email):
    conn = get_conn()
    row = conn.execute("SELECT id FROM users WHERE email=?", (email,)).fetchone()
    conn.close()
    return row is not None


def tambah_user(nama, email, password, peran, no_induk="-", no_hp="-"):
    conn = get_conn()
    conn.execute(
        """INSERT INTO users (nama, email, password, peran, no_induk, no_hp, status, tanggal_gabung)
           VALUES (?, ?, ?, ?, ?, ?, 'Aktif', ?)""",
        (nama, email, password, peran, no_induk, no_hp, datetime.now().strftime("%Y-%m-%d")),
    )
    conn.commit()
    conn.close()


def semua_user():
    conn = get_conn()
    rows = conn.execute("SELECT * FROM users ORDER BY id DESC").fetchall()
    conn.close()
    return rows


def update_user(id_user, nama, email, peran, no_hp, status):
    conn = get_conn()
    conn.execute(
        "UPDATE users SET nama=?, email=?, peran=?, no_hp=?, status=? WHERE id=?",
        (nama, email, peran, no_hp, status, id_user),
    )
    conn.commit()
    conn.close()


def hapus_user(id_user):
    conn = get_conn()
    conn.execute("DELETE FROM users WHERE id=?", (id_user,))
    conn.commit()
    conn.close()


def tambah_buku(judul, penulis, kategori, stok, rating=0):
    status = "Tersedia" if int(stok) > 0 else "Habis"
    conn = get_conn()
    conn.execute(
        "INSERT INTO buku (judul, penulis, kategori, stok, rating, status) VALUES (?,?,?,?,?,?)",
        (judul, penulis, kategori, stok, rating, status),
    )
    conn.commit()
    conn.close()


def semua_buku():
    conn = get_conn()
    rows = conn.execute("SELECT * FROM buku ORDER BY id DESC").fetchall()
    conn.close()
    return rows


def get_buku(id_buku):
    conn = get_conn()
    row = conn.execute("SELECT * FROM buku WHERE id=?", (id_buku,)).fetchone()
    conn.close()
    return row


def update_buku(id_buku, judul, penulis, kategori, stok, rating):
    status = "Tersedia" if int(stok) > 0 else "Habis"
    conn = get_conn()
    conn.execute(
        "UPDATE buku SET judul=?, penulis=?, kategori=?, stok=?, rating=?, status=? WHERE id=?",
        (judul, penulis, kategori, stok, rating, status, id_buku),
    )
    conn.commit()
    conn.close()


def hapus_buku(id_buku):
    conn = get_conn()
    conn.execute("DELETE FROM buku WHERE id=?", (id_buku,))
    conn.commit()
    conn.close()


def ubah_stok_buku(id_buku, delta):
    conn = get_conn()
    row = conn.execute("SELECT stok FROM buku WHERE id=?", (id_buku,)).fetchone()
    if row:
        stok_baru = row["stok"] + delta
        status = "Tersedia" if stok_baru > 0 else "Habis"
        conn.execute("UPDATE buku SET stok=?, status=? WHERE id=?", (stok_baru, status, id_buku))
        conn.commit()
    conn.close()


def tambah_peminjaman(user_id, buku_id, tgl_pinjam, jatuh_tempo):
    conn = get_conn()
    conn.execute(
        """INSERT INTO peminjaman (user_id, buku_id, tgl_pinjam, jatuh_tempo, status)
           VALUES (?, ?, ?, ?, 'Dipinjam')""",
        (user_id, buku_id, tgl_pinjam, jatuh_tempo),
    )
    conn.commit()
    conn.close()
    ubah_stok_buku(buku_id, -1)


def semua_peminjaman():
    conn = get_conn()
    rows = conn.execute("""
        SELECT p.*, u.nama AS nama_user, b.judul AS judul_buku
        FROM peminjaman p
        LEFT JOIN users u ON p.user_id = u.id
        LEFT JOIN buku b ON p.buku_id = b.id
        ORDER BY p.id DESC
    """).fetchall()
    conn.close()
    return rows


def kembalikan_buku(id_peminjaman, denda=0):
    conn = get_conn()
    row = conn.execute("SELECT buku_id FROM peminjaman WHERE id=?", (id_peminjaman,)).fetchone()
    conn.execute(
        "UPDATE peminjaman SET status='Selesai', tgl_kembali=?, denda=? WHERE id=?",
        (datetime.now().strftime("%Y-%m-%d"), denda, id_peminjaman),
    )
    conn.commit()
    conn.close()
    if row:
        ubah_stok_buku(row["buku_id"], 1)


def hapus_peminjaman(id_peminjaman):
    conn = get_conn()
    conn.execute("DELETE FROM peminjaman WHERE id=?", (id_peminjaman,))
    conn.commit()
    conn.close()


def perbarui_status_terlambat():
    conn = get_conn()
    hari_ini = datetime.now().strftime("%Y-%m-%d")
    conn.execute(
        "UPDATE peminjaman SET status='Terlambat' WHERE status='Dipinjam' AND jatuh_tempo < ?",
        (hari_ini,),
    )
    conn.commit()
    conn.close()

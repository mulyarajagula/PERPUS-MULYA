APLIKASI PENGELOLA PERPUSTAKAAN (Tkinter)
==========================================

Cara menjalankan:
1. Pastikan Python 3 sudah terinstal (tkinter sudah bawaan Python).
2. Buka terminal/command prompt di folder ini.
3. Jalankan: python login.py

Akun contoh (petugas):
  Email    : admin@perpus.com
  Password : admin123

Daftar file:
- db.py                 -> modul database (SQLite), dipakai semua file lain
- login.py              -> halaman login (jalankan file ini untuk mulai)
- daftar.py             -> halaman pendaftaran akun anggota baru
- mainpage.py           -> dasbor utama + sidebar navigasi
- kelolauser.py         -> CRUD data user (khusus petugas)
- kelolabuku.py         -> CRUD data buku
- kelolapeminjamam.py   -> catat & kelola peminjaman buku

Catatan:
- Database otomatis dibuat sebagai file "perpustakaan.db" saat pertama kali
  dijalankan, lengkap dengan 1 akun petugas contoh dan 2 buku contoh.
- Semua file harus berada dalam satu folder yang sama karena saling
  meng-import satu sama lain.

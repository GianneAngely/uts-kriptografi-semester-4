#!/usr/bin/env python3
"""
Sistem Pengiriman Pesan Terenkripsi - TUI (Terminal User Interface)
Menggunakan algoritma Vigenère Cipher untuk enkripsi dan dekripsi pesan.

Cara menjalankan:
    python main.py
"""

import os
import sys

from crypto import vigenere_decrypt, vigenere_encrypt
from network import DEFAULT_PORT, receive_message, send_message

# ── ANSI color codes ─────────────────────────────────────────────────────────
RESET = "\033[0m"
BOLD = "\033[1m"
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
MAGENTA = "\033[95m"
WHITE = "\033[97m"
BG_BLUE = "\033[44m"
BG_DARK = "\033[40m"


def clear_screen() -> None:
    """Membersihkan layar terminal."""
    os.system("cls" if os.name == "nt" else "clear")


def print_header() -> None:
    """Menampilkan judul aplikasi."""
    print(f"{CYAN}{BOLD}")
    print("╔══════════════════════════════════════════════════════╗")
    print("║       SISTEM PESAN TERENKRIPSI                       ║")
    print("║         Algoritma: Vigenère Cipher                   ║")
    print("╚══════════════════════════════════════════════════════╝")
    print(f"{RESET}")


def print_separator() -> None:
    """Mencetak garis pemisah."""
    print(f"{CYAN}{'─' * 56}{RESET}")


def print_error(message: str) -> None:
    """Menampilkan pesan error."""
    print(f"\n{RED}❌  Error: {message}{RESET}\n")


def print_success(message: str) -> None:
    """Menampilkan pesan sukses."""
    print(f"\n{GREEN}✅  {message}{RESET}")


def get_input(prompt: str) -> str:
    """
    Meminta input dari pengguna dengan validasi tidak kosong.

    Args:
        prompt: Teks yang ditampilkan sebagai label input.

    Returns:
        String yang dimasukkan pengguna (stripped).
    """
    while True:
        try:
            value = input(f"{YELLOW}{prompt}{RESET} ").strip()
        except (KeyboardInterrupt, EOFError):
            print(f"\n\n{YELLOW}Program dihentikan.{RESET}")
            sys.exit(0)
        if value:
            return value
        print(f"{RED}  ⚠  Input tidak boleh kosong. Silakan coba lagi.{RESET}")


def get_key_input(prompt: str) -> str:
    """
    Meminta kunci dari pengguna dengan validasi mengandung huruf.

    Args:
        prompt: Teks yang ditampilkan sebagai label input.

    Returns:
        Kunci yang valid (mengandung setidaknya satu huruf alfabet).
    """
    while True:
        key = get_input(prompt)
        if any(c.isalpha() for c in key):
            return key
        print(f"{RED}  ⚠  Kunci harus mengandung minimal satu huruf.{RESET}")


def show_encrypt_menu() -> None:
    """Menu enkripsi: menerima pesan dan kunci, lalu menampilkan hasil enkripsi."""
    clear_screen()
    print_header()
    print(f"{BOLD}{MAGENTA}  [ ENKRIPSI PESAN ]{RESET}\n")
    print_separator()

    plaintext = get_input("  📝 Masukkan pesan  :")
    key = get_key_input("  🔑 Masukkan kunci  :")

    try:
        ciphertext = vigenere_encrypt(plaintext, key)
    except ValueError as exc:
        print_error(str(exc))
        _pause()
        return

    print_separator()
    print_success("Enkripsi berhasil!")
    print()
    print(f"  {WHITE}Pesan asli      :{RESET} {plaintext}")
    print(f"  {WHITE}Kunci           :{RESET} {key.upper()}")
    print(f"  {GREEN}{BOLD}Pesan terenkripsi:{RESET} {GREEN}{ciphertext}{RESET}")
    print_separator()
    _pause()


def show_decrypt_menu() -> None:
    """Menu dekripsi: menerima ciphertext dan kunci, lalu menampilkan hasil dekripsi."""
    clear_screen()
    print_header()
    print(f"{BOLD}{MAGENTA}  [ DEKRIPSI PESAN ]{RESET}\n")
    print_separator()

    ciphertext = get_input("  🔐 Masukkan pesan terenkripsi :")
    key = get_key_input("  🔑 Masukkan kunci              :")

    try:
        plaintext = vigenere_decrypt(ciphertext, key)
    except ValueError as exc:
        print_error(str(exc))
        _pause()
        return

    print_separator()
    print_success("Dekripsi berhasil!")
    print()
    print(f"  {WHITE}Pesan terenkripsi:{RESET} {ciphertext.upper()}")
    print(f"  {WHITE}Kunci             :{RESET} {key.upper()}")
    print(f"  {GREEN}{BOLD}Pesan asli        :{RESET} {GREEN}{plaintext}{RESET}")
    print_separator()
    _pause()


def _pause() -> None:
    """Menunggu pengguna menekan Enter sebelum kembali ke menu utama."""
    try:
        input(f"\n{CYAN}  Tekan Enter untuk kembali ke menu utama...{RESET}")
    except (KeyboardInterrupt, EOFError):
        pass


def _parse_port(port_input: str) -> int:
    """Menguraikan input port dan mengembalikan nomor port yang valid (1-65535)."""
    if port_input.isdigit():
        port = int(port_input)
        if 1 <= port <= 65535:
            return port
    return DEFAULT_PORT


def show_send_menu() -> None:
    """Menu kirim pesan: enkripsi pesan lalu kirim ke IP tujuan via TCP."""
    clear_screen()
    print_header()
    print(f"{BOLD}{MAGENTA}  [ KIRIM PESAN TERENKRIPSI ]{RESET}\n")
    print_separator()

    plaintext = get_input("  📝 Masukkan pesan  :")
    key = get_key_input("  🔑 Masukkan kunci  :")

    try:
        ciphertext = vigenere_encrypt(plaintext, key)
    except ValueError as exc:
        print_error(str(exc))
        _pause()
        return

    print(f"\n  {GREEN}{BOLD}Pesan terenkripsi:{RESET} {GREEN}{ciphertext}{RESET}\n")
    print_separator()

    ip_address = get_input("  🌐 Masukkan IP tujuan :")
    port_input = input(
        f"{YELLOW}  🔌 Masukkan port (kosongkan untuk default {DEFAULT_PORT}): {RESET}"
    ).strip()
    port = _parse_port(port_input)

    print(f"\n{CYAN}  Mengirim pesan ke {ip_address}:{port} ...{RESET}")
    try:
        send_message(ip_address, ciphertext, port)
    except ConnectionRefusedError:
        print_error(
            f"Koneksi ditolak. Pastikan alamat {ip_address} sedang mendengarkan pada port {port}."
        )
        _pause()
        return
    except OSError as exc:
        print_error(str(exc))
        _pause()
        return

    print_separator()
    print_success(f"Pesan terenkripsi berhasil dikirim ke {ip_address}:{port}!")
    print_separator()
    _pause()


def show_receive_menu() -> None:
    """Menu terima pesan: dengarkan koneksi masuk dan tampilkan pesan terenkripsi."""
    clear_screen()
    print_header()
    print(f"{BOLD}{MAGENTA}  [ TERIMA PESAN TERENKRIPSI ]{RESET}\n")
    print_separator()

    port_input = input(
        f"{YELLOW}  🔌 Masukkan port (kosongkan untuk default {DEFAULT_PORT}): {RESET}"
    ).strip()
    port = _parse_port(port_input)

    print(
        f"\n{CYAN}  Mendengarkan pada port {port} ... (tekan Ctrl+C untuk batal){RESET}"
    )
    try:
        ciphertext, sender_ip = receive_message(port)
    except KeyboardInterrupt:
        print(f"\n{YELLOW}  Penerimaan dibatalkan.{RESET}")
        _pause()
        return
    except TimeoutError:
        print_error("Waktu tunggu habis. Tidak ada koneksi masuk.")
        _pause()
        return
    except UnicodeDecodeError:
        print_error("Pesan yang diterima mengandung karakter tidak valid.")
        _pause()
        return
    except OSError as exc:
        print_error(str(exc))
        _pause()
        return

    print_separator()
    print_success(f"Pesan diterima dari {sender_ip}!")
    print()
    print(f"  {WHITE}Pesan terenkripsi:{RESET} {GREEN}{ciphertext}{RESET}")
    print_separator()

    decrypt_choice = (
        input(f"{YELLOW}  Dekripsi pesan sekarang? [y/N]: {RESET}").strip().lower()
    )
    if decrypt_choice == "y":
        key = get_key_input("  🔑 Masukkan kunci  :")
        try:
            plaintext = vigenere_decrypt(ciphertext, key)
        except ValueError as exc:
            print_error(str(exc))
            _pause()
            return
        print_success("Dekripsi berhasil!")
        print()
        print(f"  {GREEN}{BOLD}Pesan asli:{RESET} {GREEN}{plaintext}{RESET}")
        print_separator()

    _pause()


def show_main_menu() -> None:
    """Menampilkan menu utama aplikasi."""
    clear_screen()
    print_header()
    print(f"{BOLD}  Selamat datang di Sistem Pesan Terenkripsi!{RESET}")
    print(f"  Aplikasi ini menggunakan {YELLOW}Vigenère Cipher{RESET} untuk")
    print("  menjaga kerahasiaan pesan Anda.\n")
    print_separator()
    print(f"  {CYAN}[1]{RESET}   Enkripsi Pesan")
    print(f"  {CYAN}[2]{RESET}   Dekripsi Pesan")
    print(f"  {CYAN}[3]{RESET}   Kirim Pesan ke IP")
    print(f"  {CYAN}[4]{RESET}   Terima Pesan dari Jaringan")
    print(f"  {CYAN}[5]{RESET}   Keluar")
    print_separator()


def main() -> None:
    """Titik masuk utama aplikasi TUI."""
    while True:
        show_main_menu()
        try:
            choice = input(f"{YELLOW}  Pilih menu [1/2/3/4/5]: {RESET}").strip()
        except (KeyboardInterrupt, EOFError):
            print(f"\n\n{YELLOW}Program dihentikan.{RESET}")
            sys.exit(0)

        if choice == "1":
            show_encrypt_menu()
        elif choice == "2":
            show_decrypt_menu()
        elif choice == "3":
            show_send_menu()
        elif choice == "4":
            show_receive_menu()
        elif choice == "5":
            clear_screen()
            print(
                f"\n{CYAN}  Terima kasih telah menggunakan Sistem Pesan Terenkripsi!{RESET}"
            )
            print(f"  {YELLOW}Sampai jumpa! {RESET}\n")
            sys.exit(0)
        else:
            print(f"{RED}  ⚠  Pilihan tidak valid. Masukkan 1, 2, 3, 4, atau 5.{RESET}")
            _pause()


if __name__ == "__main__":
    main()

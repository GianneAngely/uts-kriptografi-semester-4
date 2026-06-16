"""
Modul Jaringan - Pengiriman Pesan via TCP
Menyediakan fungsi untuk mengirim dan menerima pesan terenkripsi melalui jaringan lokal.
"""

import socket

DEFAULT_PORT = 5000
BUFFER_SIZE = 4096
TIMEOUT = 10
ACCEPT_TIMEOUT = 300  # maksimum waktu tunggu koneksi masuk (detik)


def send_message(host: str, message: str, port: int = DEFAULT_PORT) -> None:
    """
    Mengirim pesan ke host tujuan melalui koneksi TCP.

    Args:
        host: Alamat IP tujuan.
        message: Pesan (sudah terenkripsi) yang akan dikirim.
        port: Port tujuan (default: 5000).

    Raises:
        ConnectionRefusedError: Jika koneksi ditolak oleh host tujuan.
        OSError: Jika terjadi kesalahan jaringan lainnya.
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(TIMEOUT)
        sock.connect((host, port))
        sock.sendall(message.encode("utf-8"))


def receive_message(port: int = DEFAULT_PORT) -> tuple[str, str]:
    """
    Mendengarkan koneksi masuk dan menerima satu pesan.

    Args:
        port: Port yang akan didengarkan (default: 5000).

    Returns:
        Tuple (pesan, alamat_pengirim) di mana pesan adalah teks yang diterima
        dan alamat_pengirim adalah IP pengirim.

    Raises:
        OSError: Jika terjadi kesalahan jaringan.
        UnicodeDecodeError: Jika data yang diterima bukan UTF-8 yang valid.
        TimeoutError: Jika tidak ada koneksi masuk dalam waktu ACCEPT_TIMEOUT detik.
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_sock:
        server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_sock.bind(("0.0.0.0", port))
        server_sock.settimeout(ACCEPT_TIMEOUT)
        server_sock.listen(1)
        conn, addr = server_sock.accept()
        with conn:
            chunks = []
            while True:
                chunk = conn.recv(BUFFER_SIZE)
                if not chunk:
                    break
                chunks.append(chunk)
            message = b"".join(chunks).decode("utf-8")
    return message, addr[0]

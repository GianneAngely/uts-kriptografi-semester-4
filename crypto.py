"""
Modul Kriptografi - Vigenère Cipher
Menyediakan fungsi enkripsi dan dekripsi menggunakan algoritma Vigenère Cipher.
"""

ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


def _prepare_key(text: str, key: str) -> str:
    """Menyesuaikan panjang kunci agar sama dengan panjang teks (hanya huruf)."""
    key = key.upper()
    filtered = [c for c in text.upper() if c in ALPHABET]
    repeated = (key * ((len(filtered) - 1) // len(key) + 1))[: len(filtered)]
    return repeated


def vigenere_encrypt(plaintext: str, key: str) -> str:
    """
    Mengenkripsi plaintext menggunakan Vigenère Cipher.

    Args:
        plaintext: Pesan yang akan dienkripsi.
        key: Kunci enkripsi (hanya huruf alfabet).

    Returns:
        Pesan terenkripsi (ciphertext).

    Raises:
        ValueError: Jika kunci atau plaintext kosong, atau kunci tidak valid.
    """
    if not plaintext:
        raise ValueError("Pesan tidak boleh kosong.")
    if not key:
        raise ValueError("Kunci tidak boleh kosong.")
    key_clean = "".join(c for c in key.upper() if c in ALPHABET)
    if not key_clean:
        raise ValueError("Kunci harus mengandung minimal satu huruf alfabet.")

    extended_key = _prepare_key(plaintext, key_clean)
    result = []
    key_index = 0

    for char in plaintext.upper():
        if char in ALPHABET:
            p = ALPHABET.index(char)
            k = ALPHABET.index(extended_key[key_index])
            c = (p + k) % 26
            result.append(ALPHABET[c])
            key_index += 1
        else:
            result.append(char)

    return "".join(result)


def vigenere_decrypt(ciphertext: str, key: str) -> str:
    """
    Mendekripsi ciphertext menggunakan Vigenère Cipher.

    Args:
        ciphertext: Pesan terenkripsi yang akan didekripsi.
        key: Kunci dekripsi (harus sama dengan kunci enkripsi).

    Returns:
        Pesan asli (plaintext).

    Raises:
        ValueError: Jika kunci atau ciphertext kosong, atau kunci tidak valid.
    """
    if not ciphertext:
        raise ValueError("Pesan terenkripsi tidak boleh kosong.")
    if not key:
        raise ValueError("Kunci tidak boleh kosong.")
    key_clean = "".join(c for c in key.upper() if c in ALPHABET)
    if not key_clean:
        raise ValueError("Kunci harus mengandung minimal satu huruf alfabet.")

    extended_key = _prepare_key(ciphertext, key_clean)
    result = []
    key_index = 0

    for char in ciphertext.upper():
        if char in ALPHABET:
            c = ALPHABET.index(char)
            k = ALPHABET.index(extended_key[key_index])
            p = (c - k) % 26
            result.append(ALPHABET[p])
            key_index += 1
        else:
            result.append(char)

    return "".join(result)

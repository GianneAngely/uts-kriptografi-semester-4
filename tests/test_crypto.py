"""
Unit tests for crypto.py (Vigenère Cipher).
"""

import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from crypto import vigenere_decrypt, vigenere_encrypt


class TestVigenereEncrypt:
    def test_basic_encrypt(self):
        assert vigenere_encrypt("HELLO", "KEY") == "RIJVS"

    def test_basic_decrypt_roundtrip(self):
        plaintext = "HELLOWORLD"
        key = "SECRET"
        assert vigenere_decrypt(vigenere_encrypt(plaintext, key), key) == plaintext

    def test_encrypt_is_uppercase(self):
        result = vigenere_encrypt("hello", "key")
        assert result == result.upper()

    def test_non_alpha_chars_preserved(self):
        result = vigenere_encrypt("HELLO, WORLD!", "KEY")
        assert result[5] == ","
        assert result[6] == " "
        assert result[12] == "!"

    def test_lowercase_plaintext(self):
        result = vigenere_encrypt("hello", "key")
        assert result == vigenere_encrypt("HELLO", "KEY")

    def test_lowercase_key(self):
        assert vigenere_encrypt("HELLO", "key") == vigenere_encrypt("HELLO", "KEY")

    def test_key_repeated_for_long_message(self):
        plaintext = "ATTACKATDAWN"
        key = "LEMON"
        ciphertext = vigenere_encrypt(plaintext, key)
        assert vigenere_decrypt(ciphertext, key) == plaintext

    def test_encrypt_empty_plaintext_raises(self):
        with pytest.raises(ValueError, match="Pesan tidak boleh kosong"):
            vigenere_encrypt("", "KEY")

    def test_encrypt_empty_key_raises(self):
        with pytest.raises(ValueError, match="Kunci tidak boleh kosong"):
            vigenere_encrypt("HELLO", "")

    def test_encrypt_non_alpha_key_raises(self):
        with pytest.raises(ValueError, match="minimal satu huruf alfabet"):
            vigenere_encrypt("HELLO", "123")

    def test_encrypt_key_with_numbers_uses_letters(self):
        # Key "K3Y" should behave like key "KY"
        result = vigenere_encrypt("HELLO", "K3Y")
        assert result == vigenere_encrypt("HELLO", "KY")


class TestVigenereDecrypt:
    def test_basic_decrypt(self):
        assert vigenere_decrypt("RIJVS", "KEY") == "HELLO"

    def test_decrypt_empty_ciphertext_raises(self):
        with pytest.raises(ValueError, match="Pesan terenkripsi tidak boleh kosong"):
            vigenere_decrypt("", "KEY")

    def test_decrypt_empty_key_raises(self):
        with pytest.raises(ValueError, match="Kunci tidak boleh kosong"):
            vigenere_decrypt("RIJVS", "")

    def test_decrypt_non_alpha_key_raises(self):
        with pytest.raises(ValueError, match="minimal satu huruf alfabet"):
            vigenere_decrypt("RIJVS", "!@#")

    def test_non_alpha_chars_preserved_in_decrypt(self):
        ciphertext = vigenere_encrypt("HELLO, WORLD!", "KEY")
        plaintext = vigenere_decrypt(ciphertext, "KEY")
        assert plaintext[5] == ","
        assert plaintext[6] == " "
        assert plaintext[12] == "!"

    def test_roundtrip_with_spaces(self):
        original = "HELLO WORLD"
        key = "MYKEY"
        assert vigenere_decrypt(vigenere_encrypt(original, key), key) == original

    def test_well_known_vigenere_example(self):
        # Classic Vigenère example
        assert vigenere_encrypt("ATTACKATDAWN", "LEMON") == "LXFOPVEFRNHR"
        assert vigenere_decrypt("LXFOPVEFRNHR", "LEMON") == "ATTACKATDAWN"

import http.client
import os
import unittest
from urllib.request import urlopen
from urllib.error import URLError


import pytest

BASE_URL = "http://localhost:5000"
BASE_URL_MOCK = "http://localhost:8081"
DEFAULT_TIMEOUT = 2  # in secs

@pytest.mark.api
class TestApi(unittest.TestCase):
    def setUp(self):
        self.assertIsNotNone(BASE_URL, "URL no configurada")
        self.assertTrue(len(BASE_URL) > 8, "URL no configurada")

    def test_api_add(self):
        url = f"{BASE_URL}/calc/add/1/2"
        response = urlopen(url, timeout=DEFAULT_TIMEOUT)
        self.assertEqual(
            response.status, http.client.OK, f"Error en la petición API a {url}"
        )
        self.assertEqual(
            response.read().decode(), "3", "ERROR ADD"
        )

    def test_api_sqrt(self):
        url = f"{BASE_URL_MOCK}/calc/sqrt/64"
        response = urlopen(url, timeout=DEFAULT_TIMEOUT)
        self.assertEqual(
            response.status, http.client.OK, f"Error en la petición API a {url}"
        )
        self.assertEqual(
            response.read().decode(), "8", "ERROR SQRT"
        )

    def test_api_multiply(self):
        url = f"{BASE_URL}/calc/multiply/3/4"
        response = urlopen(url, timeout=DEFAULT_TIMEOUT)
        self.assertEqual(
            response.status, http.client.OK, f"Error en la petición API a {url}"
        )
        self.assertEqual(
            response.read().decode(), "12", "ERROR MULTIPLY"
        )

        with self.assertRaises(URLError):
            url = f"{BASE_URL}/calc/multiply/a/4"
            urlopen(url, timeout=DEFAULT_TIMEOUT)

    def test_api_divide(self):
        url = f"{BASE_URL}/calc/divide/10/2"
        response = urlopen(url, timeout=DEFAULT_TIMEOUT)
        self.assertEqual(
            response.status, http.client.OK, f"Error en la petición API a {url}"
        )
        self.assertEqual(
            response.read().decode(), "5.0", "ERROR DIVIDE"
        )

        url = f"{BASE_URL}/calc/divide/10/0"
        try:
            response = urlopen(url, timeout=DEFAULT_TIMEOUT)
        except urllib.error.HTTPError as e:
            self.assertEqual(e.code, 406, "No devolvió el código de error esperado (406)")
            self.assertEqual(e.reason, "NOT ACCEPTABLE", "El mensaje de error no coincide")
        else:
            self.fail("No se lanzó un error HTTP cuando el divisor es 0")


if __name__ == "__main__":  # pragma: no cover
    unittest.main()

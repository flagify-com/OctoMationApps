import unittest
from om_python_xtools import encrypt_aes_encrypt, encrypt_aes_decrypt,encrypt_rsa_encrypt,encrypt_rsa_decrypt

# @unittest.skip("skip")
class TestEncryptRSAEncryptAndDecrypt(unittest.TestCase):
    def setUp(self):
        self.params = {
            "str": "你好，Brother!",
            "str_rsa_encrypted": "",
            "str_rsa_decrypted": "",
            "public_key": "",
            "private_key": "",
            "encoding": "utf-8",
            "padding_method": "PKCS1v15"
        }

    def test_rsa_keys_from_openssl_with_string_password(self):
        #https://tool.lvtao.net/rsa
        public_key_str = """-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAw2HjVsjayK+JaRNwC+d9
UOZIzKRG3oyKe6SA1qx7OgaGYzvhYznWTLEz/c7zWDDHGABZdreXOQxvNc2lq6Ip
14W35XGIn0FFhmrEqCj6KBsztuK+GVYyiXosD4G6fYvSYrW61XPNyrRTsKyF/lI6
1M6aVcOMdbggI/P4+aeqxXeLlHXHLc8VXlC6GlOAdgkN7oP3e6mHqk6+ERM/5uuG
fsbwWFnix/Q0PYncsZrAhJMbWFKqKs3X01GuN2aTv7+7Vps7xv4htW4l6rs2nVcP
IUrwxOVJidhYS2TJ0YfFKkxCwXU1NitfHDd9qw2HIbvv3S1hIRFqqiYq2M1U6qOp
dwIDAQAB
-----END PUBLIC KEY-----"""
        private_key_str = """-----BEGIN ENCRYPTED PRIVATE KEY-----
MIIFJDBWBgkqhkiG9w0BBQ0wSTAxBgkqhkiG9w0BBQwwJAQQM/DDrXOvDIcgQFkY
n9w4agICCAAwDAYIKoZIhvcNAgkFADAUBggqhkiG9w0DBwQIhpwf3EwIKhEEggTI
afULM6KcCuVYb2BqaGhkXrGhWkGS9VKDAMolku6PzoHyWpFsuP5JEno6BjC0LG8J
VZ0pHbSZogppfnd4lRKFc35I1jUT8Vi0hFQGhhyEkDp9RYMdw3xhtbAMj4FKKcJ+
8WR+Da+z5G4EQYrH3jQOvNnnbCa3IScu4SEaG/UyBHl+3QR8WGAnvoWFVYr02bH+
6Q6la7HWqm3kjMm0VwQYFtzd+mvKbLTIjh7L0jCWaRHrXAT5cSDDTI1MQc6aBmF/
iSUYJO64tvpI7GXv4Ap5T1Fc6Ldm0bYS9lkRiM/ZdlyEldPn9IQh1tZVUcgulMzw
nndcAbEHzPu5p44cWInvp20e94TpV54yTIvCb4iTWJPDtyGG55VevAJB64JBbcSY
0f0t+WsqHzxe7U+Dn/vgyUuLFOma/wrr5qo/KcUew4NmuIOqrZp4Lt+DpIi3rUJF
nvnaS7yaaNo+qI1N2nMIwzjVllK2tg55TkZOq15Ko2fUxB2wpLqZV9h8/6lo7qZ3
Wtc+hrjYW3VC2Ec0WM9hDhAZZvc18BexfWs0WT7CvtGUyDioggyIK5NCK1HBBe6S
dLe3VoZxhfj9AVvaAbaenFcPR+rjUcXPqZxYtBf4bN6A9YJ/FzX3tn/M10uhdlbx
UPYWK4yyJgIp2qictYcplD6rCsw71eysVomWlMeKDYDziFpulhw1ImGXsFS71img
k3Gbz0NqsYjm/hHv09vKo9aRYg48xRK2NR1+2Obz28Of0R/7DG2rGupoAVp1ezo9
PGtPbd1PWZPu6lY09A4blEmv1zkkritQoCIE5fXwPn9/kHTt+ENx6h8XaArc8AQD
yvrBFEuR5rWSEFmMSQJdrQEV8YboKEDGwd9U4SDCvd4yoDpgSsSguuB0VAQK75Cc
9HWBaZwBs6RPBQrwhheUCcYf8VQ+5tkWYhlm2fdodw7vWPhtfkre5WaocwU13xI8
OVAqKm0DCWHqgrSqB7/Ugrp7Ct7EXGIvWknzNFuXVxX0s6hwDB1El8oMD5PrU5ql
/Z7wkwFYbMJ1WuSM1+Y1huIfMG31awgw5Frn8S5KBpEWm+aNOJhodXvuiZmpwxmM
Gqnk6WbJv043ix1w6jriOQy1LR1qi+O7U4aXL0vjwBKs3AiFmzMHSX1Y2jgEABgF
5wiYW1+wQLEhrs6x64eNCspmVB5BDB8vGbrSWPLJI6EtSIkCP59PgIct8nbvSzXa
+rL9oLbCICpnUsP4kKDFoj/fwFcBh6LA+HStUmII6BdNv8c/ywmJAAG3JINTkLxp
Lb5yBqmfa3xyhfcfNzYiRU/diAs8nq283R+0JkUTh23dD5/ci4J4DTI72ETgLVgI
e5UmAcBZLENLLT3JQgCaPLGkrMTbLtbMYOLOfa2D5OFF58kVzePJ7LLp2JIGCGxN
SyTdgnVM05qKaHtpTu5ni0b/YMDwRoJ7+ToYZiyTfzI+E1OZ9/dSUOGr0xZz5X0u
DjemQSB8nuqrmS5MbSCCwSS5Sx7EbHQwI6wx46BgSH+YR8xgY8Xeb8GBFpygk4dJ
ulc7udVqwjOYYk6CxE1pwP5cG/mQVZbyh6gLjC4JGmUaQEzt1yXW6ZSqsiU509VV
5CHevWer6Ml6HlaeursKiP8JEDKOQ3m3
-----END ENCRYPTED PRIVATE KEY-----"""
        self.params["public_key"] = public_key_str
        self.params["private_key"] = private_key_str
        self.params["padding_method"] = "OAEP_SHA256"
        self.params["private_key_has_password"] = True
        self.params["private_key_password"] = "123456"
        self.params["str"] = 'OpenSSL命令：openssl genrsa -out ./x1.pem -passout pass:"123456" -des3 2048;openssl rsa -pubout -in ./x1.pem -passin pass:"123456" -out ./x1_pub.pem'
        result = encrypt_rsa_encrypt(self.params, None, None)
        print(result)
        self.assertEqual(result["code"], 200)
        self.assertNotEqual(result["data"]["str_rsa_encrypted"], "")
        self.params["str_rsa_encrypted"] = result["data"]["str_rsa_encrypted"]
        result = encrypt_rsa_decrypt(self.params, None, None)
        print(result)
        self.assertEqual(result["code"], 200)
        self.assertEqual(result["data"]["str_rsa_decrypted"], self.params["str"])

    def test_rsa_keys_from_openssl_with_empty_password(self):
        #https://tool.lvtao.net/rsa
        public_key_str = """-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAp5p+00HlcBpbsQjs1yCH
bAGjc7KVvL/bzIqKO3NKcGf8lJstt/c52k0p1e3LCIZE3IybufbMzbyH1cqgr4lw
qgzmCRrGOCsFpyCaAgIFFdJV72xl5KgYgl5RgrCVha1DctwGCPcBwua1ZqXVZpJM
8kiz4dhdR9WrEqFzh9kAedLN+ZOe84eMX7qiBT6zuYvgQUVksqi2CoLUX2t3A0vR
vJY0A0uU4h3mT1ljL0mkenS+ZH0oDfvYK6qiumxtR7ZZOaK/I32DcQcRZ//HzJQz
hjT4AvylCA0Xc5JPjLV0jW8OFqwhj4C97eCVxSKzmgq9OHbnlscggrUHJFxQ9L5t
KwIDAQAB
-----END PUBLIC KEY-----"""
        private_key_str = """-----BEGIN ENCRYPTED PRIVATE KEY-----
MIIFJDBWBgkqhkiG9w0BBQ0wSTAxBgkqhkiG9w0BBQwwJAQQWu0A8Ld/TtOo9xAN
xZEPxAICCAAwDAYIKoZIhvcNAgkFADAUBggqhkiG9w0DBwQINNZlsIWFNHUEggTI
tgML8RKJrFJCu5APnamyG47L4X1ZQN5WOhQO46Wm3vvVKWBOd72I62aK1W4ktSki
IhvwojFgYqaf6HJ2ITDiDg0XNfP220aQ0Sil+z0w8t5w6ZQPSJHyTUkdbENvs1Eh
rpnOFaaDpSA39AvF6rcPChqDu+9oHHoqwca6V6fYnh5aTiovryRtuxqigKrh7BeU
9qG5maCYyO7Y9y3P48FcNgtgc2y90cV4Isf0apc6XQHSLJezuTiCKoncqcVRZEeU
GbeMdDQZOv2n+WWCxxuLM5P/0nOl9igr/7Ztfn/dBOpUAThXfqsPsWj4Myo9/Nzc
7Yxey7hzLXUwl30N4CqlnACizKV9H4H/v7nXPWJTmfYm4KPMFm/yU5XR2zRPg0LH
Cilf3E7e6qXsFMPH2xMO5mQlPDeYQBf1D7/rdeZufsIxnAPH7TA5wek8dLzmddFh
7SOJYyhkoqfW3keVLYJ5gIzPAucJH/5/DaPB8LWYOZvgJcJk8n/WTGlYUpFIbzBy
N1QINIlCENLbPQsaOLqYKoblJtumumUH+9JVoSEbiTgy2ADFxQ6E63A3Fp6PT1Uy
/QA99pxryv6xdK5j8YVyzUEIZcm6fTQhcJNcv1SckJOXTmn8KAxkh/b/tfpH+pOG
00c+yBOaiSxDcVANQRgzK9kYB969VlUTKYRnMecH5A9T42zbGwK8VpzVaO9LzyU3
Erg2OgDRh84T5QucUBI260U1V4Z+a9B75/oPIFm2ovPN9/Wq9gc9gVinUFVuZR5d
nJofsQaRK+Hc5NwOHKSL3UDIjOEKvW7ExFR+BTwoETtjXVaXOj12+jyzGQJF4MYK
WW5hEOuFzezw6ujGbzTLnIGowJ2znwEvNXKq/SB5/deoB9v+Mucww3+OlCZGSZvH
bsimayPPqHouvUM72+6/A4UGA7ZUVqKBZFD5n4+iMo7j8tHlpZR8eEz+SG7Gkfkw
KsvogDYVx8H10O6jzJU658BNaoaXDFeO2CH8YhfWVpFvJJBNS5aBNBjjQjv/AfkF
h62LWdxiBNV49CnBlzE35kBLjoiDSiTb4pG4QX+ba9im3EivXQ7FzruLQWMrXLBv
nT7dYqmJ3nsOjbS2IzFPq2JdQjEXBDJb7pmgCyldtXFyrQlb71urF6lLo9GHw+j8
6R9MaVCdSPid98mJ8fHScq8NHKKSB6MZTelzs+B7f42gfZW+Syb8TQ+mcZIvZKuM
OcfeHVdem91sdtYQOqxIjCUBPQ0MX6LxWoqH6evA8mafkMuXp9uSFOAZ3/35kcg1
NG1kslcUHqSBxAUGCj+Hh1pm1mxtJ+EwXv6sxizyGEMjfDkUDovaG6xQ6y5bHiMF
w+r6fJF8ozayKlQGUQqSJfDdBqpqIpzzLgrvrjFOQrUarETAhS+HwULsH5R7/ILK
X1pdHIU0D5rMblaSvyKTRX7qoY1cs8orUpS/cjL43n6ahrsK//3FhnAyYXccgNUz
HMqqX+AihE4tf0MPgaOyEcYRlXn/8OZpwjxVyU1tjYNysnawo+MnuByeB0lWBQQR
WlN+wqOMddC6RbEp3H+VP9FLv4kWmXLCKnwaYxc4mlqg9DKK0g1LchcvvCE+3NS9
kIC8EP6s/mopGE7ZAOaPRPNTOLG2sUpv
-----END ENCRYPTED PRIVATE KEY-----"""
        self.params["public_key"] = public_key_str
        self.params["private_key"] = private_key_str
        # self.params["padding_method"] = "PKCS1v15"
        self.params["private_key_has_password"] = True
        self.params["private_key_password"] = ""
        self.params["str"] = 'OpenSSL命令：openssl genrsa -out ./myPrivateKey.pem -passout pass:"" -des3 2048;openssl rsa -pubout -in ./myPrivateKey.pem -passin pass:"" -out ./myPublicKey.pem'
        self.params["padding_method"] = "OAEP_SHA256"
        result = encrypt_rsa_encrypt(self.params, None, None)
        print(result)
        self.assertEqual(result["code"], 200)
        self.assertNotEqual(result["data"]["str_rsa_encrypted"], "")
        self.params["str_rsa_encrypted"] = result["data"]["str_rsa_encrypted"]
        result = encrypt_rsa_decrypt(self.params, None, None)
        print(result)
        self.assertEqual(result["code"], 200)
        self.assertEqual(result["data"]["str_rsa_decrypted"], self.params["str"])

    # @unittest.skip("skip")
    def test_rsa_keys_from_javascript(self):
        #https://tool.lvtao.net/rsa
        public_key_str = """-----BEGIN PUBLIC KEY-----
MIIBITANBgkqhkiG9w0BAQEFAAOCAQ4AMIIBCQKCAQB/xDswXqnRKPAyHXb2GWUA
TLtpBsBbSMrZ3feoJujbUBOIzTz0C4l9wS46UT30Oco0dZvD3T6WP6kCPZaE+HCP
dl1opBWvjnw1+DEIyeCf1StyIXBK4iZlfKwVrVdah5UyF/xUMtQk4lVzdQ2HlepF
OSLtzNhSNiCTz0qn1GgoS0Dt0XCp+C7de2FvejrpsAAASPaw7qwvAryqGTR4eMCk
WUoBoFucUDdIYXX5+NbCdIRWlzteBUmJJ6XxuZrWDHXOCXpAnmBWRjjCKN9piDgq
HQiJsEIY3CQT3dsX5KwrUdJ3TaziHbOhnbbxCgmWpAWMRUXhQPb99VfrhNQVI4i9
AgMBAAE=
-----END PUBLIC KEY-----"""
        private_key_str = """-----BEGIN RSA PRIVATE KEY-----
MIIEowIBAAKCAQB/xDswXqnRKPAyHXb2GWUATLtpBsBbSMrZ3feoJujbUBOIzTz0
C4l9wS46UT30Oco0dZvD3T6WP6kCPZaE+HCPdl1opBWvjnw1+DEIyeCf1StyIXBK
4iZlfKwVrVdah5UyF/xUMtQk4lVzdQ2HlepFOSLtzNhSNiCTz0qn1GgoS0Dt0XCp
+C7de2FvejrpsAAASPaw7qwvAryqGTR4eMCkWUoBoFucUDdIYXX5+NbCdIRWlzte
BUmJJ6XxuZrWDHXOCXpAnmBWRjjCKN9piDgqHQiJsEIY3CQT3dsX5KwrUdJ3Tazi
HbOhnbbxCgmWpAWMRUXhQPb99VfrhNQVI4i9AgMBAAECggEAQF0jkCdwFv0vm596
SVnbpr4A/1S2XIYcIosOcvg/ABSj8pup5CtXtTE3T4uT0U+3jJvev1naaKhjRMyv
4gah9bOkNM3MWudFrY59bTb94KbrvxAXWLH6s8+NhVIQmnuI7nZk2CnO81HNyF8k
VLRyEzNIZFF4fFnmKXAY5Nk9K2ab/EGs2FE2Z5nE3ylbAKnTzDDZR7fGnVsTTkaI
i6W9nha5Swl6t0vfbcM3bOMKgrct7oMvCkngnkCsoIK12D0h2Ipuco18MPubKn6F
Mx8JFO3PWlY6fyZKUCFJC1lWbMVUQEVUOqOXrSbl5FZHgkqIWQC+ABSaUEpThxgR
zig8oQKBgQDbwP5DjgIUuydCrQsqtnJieME0FSzZmT+7yU4QjUGkBT/PIoGyPnbQ
uAhyo84UL8+850DctmTHChGhPvgafuxdFHBylBp8R4P4lq8MQGoNlrGYw04Ca4u4
LPhZJUsty969toIhVNJkCP2m0tLw4adqhj2DWTwyCBudG99qC2ZkxQKBgQCU1x0/
95YtysS8gC50i5GCtzxpEWit8DcTkgV3uSMskKyiJc62I6aHR/Fw0q+Li1GIxt09
Sw9M5EQv2R7Lmf8aOVvvlwWAdgNoJCSaObOxoOGtC9sG8gg+QiJAYdoMQXF5zpfC
e1xGOzUuR4sBGWbA6df4vcPZcofbKl8l1OcDmQKBgQCm4bv1v10TM0FQYCsPx7e7
0ioejEogAUImMGyJI0yK67WWboUBwG/odylrLbwtFlXzBcb7FcQYZywWQMSXEnYb
BY+TY6dtY73zxTKv4ibnpN2/vel66wMS3YvH3wtlfuHrPjM6brjLYQyHaKjqZuMF
gWYrXlPZRtD5kZYraPbcZQKBgB3EY+ouJw/jdLNKY4AVhbWB1gghXjEjULCOTJ+k
HD/Gc3A+ZXgR6zU1EzmAOXGMHHNhak/e2iGDqYt0Pe90Tgu9mwBw0L3fXFEQoW1i
yuhkh53nOBfMgg+JhHYh280FrZ8xzTItH8hAASPPVSKUJPPCENqDgU7U1AzmDX9w
c/9JAoGBANTO5nuw1ckZnhtho0QSS8safHzfy/zEXguSAr7bCFY/1lYEJR8mfX2w
yks2AyhKDNjyjmcLWiXfaRsMFkW9gUML9+mvQ+lGEAgryY4DVHZcfMq7dE4RaB4q
cLVtcuwhEOOF8ObOpOGB9gkmbqh/qIOgy4c2Jm7mpNgAPicTXfk3
-----END RSA PRIVATE KEY-----"""
        self.params["public_key"] = public_key_str
        self.params["private_key"] = private_key_str
        self.params["padding_method"] = "PKCS1v15"
        # self.params["private_key_has_password"] = False
        # self.params["private_key_password"] = ""
        
        result = encrypt_rsa_encrypt(self.params, None, None)
        print(result)
        self.assertEqual(result["code"], 200)
        self.assertNotEqual(result["data"]["str_rsa_encrypted"], "")
        self.params["str_rsa_encrypted"] = result["data"]["str_rsa_encrypted"]
        result = encrypt_rsa_decrypt(self.params, None, None)
        print(result)
        self.assertEqual(result["code"], 200)
        self.assertEqual(result["data"]["str_rsa_decrypted"], self.params["str"])
        self.params["str_rsa_encrypted"] = "evYeKA2TpRvAW7ldA3vhVUA3IpCT3OyO6sBYGm/LnjbVlEU4QjB5jUCJHwYaFZ11+UL+oxo1ZAgQgCH+ayKfbM4U50LFq8ordDEXF/72AcZwCiK/5jMc6r/p8FZplEZi+zR60L/AqAeRmRJH2G0NQkcCoXlmK3qHDbNBmtUOIbI0tb9ogADWiTjE3sENu6OOpF2BxHGMuT0+YU37MJo1N4Ff/8FgIfbpfICiaaLKSJgEk7CtyO0bSra3KyKeQ+Hotc7UDmFNHYLdRqbUUebn4K/1uRLCGtGrnbVVV4ozCRa5/PNM3Uo5tB9+gbeu5Ty3kv0xkSR95HzwLmU4Bps/uw=="
        self.params["padding_method"] = "PKCS1v15"
        result = encrypt_rsa_decrypt(self.params, None, None)
        print(result)
        self.assertEqual(result["code"], 200)
        self.assertEqual(result["data"]["str_rsa_decrypted"], "你好，https://tool.lvtao.net/rsa")

    # @unittest.skip("Skip for now")
    def test_empty_string(self):
        self.params["str"] = ""
        result = encrypt_rsa_encrypt(self.params, None, None)
        self.assertEqual(result["summary"]["statusCode"], 400)
        self.assertEqual(result["summary"]["msg"], "Empty string")

    # @unittest.skip("Skip for now")
    def test_empty_public_key(self):
        self.params["public_key"] = ""
        result = encrypt_rsa_encrypt(self.params, None, None)
        self.assertEqual(result["summary"]["statusCode"], 400)
        self.assertEqual(result["summary"]["msg"], "Empty public key")

# @unittest.skip("Skip for now")
class TestEncryptAES(unittest.TestCase):

    def test_encrypt_aes_encrypt_happy_path_CBC(self):
        params = {
            "str": "Hello, World!",
            "key": "1234567890123456",
            "mode": "CBC",
            "encode": "utf-8",
            "cbc_iv": "1234567890123456"
        }
        result = encrypt_aes_encrypt(params, None, None)
        self.assertEqual(result["code"], 200)
        self.assertEqual(result["data"]["str_aes_encrypted"], "KQ8kBYRmIyMCoh9rwsq6YA==")

    def test_encrypt_aes_encrypt_happy_path_ECB(self):
        params = {
            "str": "Hello, World!",
            "key": "1234567890123456",
            "mode": "ECB",
            "encode": "utf-8",
            "cbc_iv": "1234567890123456"
        }
        result = encrypt_aes_encrypt(params, None, None)
        self.assertEqual(result["code"], 200)
        self.assertEqual(result["data"]["str_aes_encrypted"], "s1aiR0qHAayxg11CyTDX1Q==")

    def test_encrypt_aes_encrypt_empty_string(self):
        params = {
            "str": "",
            "key": "1234567890123456",
            "mode": "CBC",
            "encode": "utf-8",
            "cbc_iv": "1234567890123456"
        }
        result = encrypt_aes_encrypt(params, None, None)
        self.assertEqual(result["summary"]["statusCode"], 400)
        self.assertEqual(result["summary"]["msg"], "Empty string")

    def test_encrypt_aes_encrypt_empty_key(self):
        params = {
            "str": "Hello, World!",
            "key": "",
            "mode": "CBC",
            "encode": "utf-8",
            "cbc_iv": "1234567890123456"
        }
        result = encrypt_aes_encrypt(params, None, None)
        self.assertEqual(result["summary"]["statusCode"], 400)
        self.assertEqual(result["summary"]["msg"], "Empty key")

    def test_encrypt_aes_encrypt_invalid_key_length(self):
        params = {
            "str": "Hello, World!",
            "key": "12345",
            "mode": "CBC",
            "encode": "utf-8",
            "cbc_iv": "1234567890123456"
        }
        result = encrypt_aes_encrypt(params, None, None)
        self.assertEqual(result["summary"]["statusCode"], 400)
        self.assertEqual(result["summary"]["msg"], "Invalid key length")

    def test_encrypt_aes_encrypt_invalid_mode(self):
        params = {
            "str": "Hello, World!",
            "key": "1234567890123456",
            "mode": "INVALID",
            "encode": "utf-8",
            "cbc_iv": "1234567890123456"
        }
        result = encrypt_aes_encrypt(params, None, None)
        self.assertEqual(result["summary"]["statusCode"], 400)
        self.assertEqual(result["summary"]["msg"], "Invalid mode")

# @unittest.skip("Skip for now")
class TestEncryptAESDecrypt(unittest.TestCase):

    def test_happy_path_cbc(self):
        params = {
            "str_aes_encrypted": "KQ8kBYRmIyMCoh9rwsq6YA==",
            "key": "1234567890123456",
            "mode": "CBC",
            "encode": "utf-8",
            "cbc_iv": "1234567890123456"
        }
        result = encrypt_aes_decrypt(params, None, None)
        self.assertEqual(result["code"], 200)
        self.assertEqual(result["data"]["str_aes_decrypted"], "Hello, World!")

    def test_happy_path_ecb(self):
        params = {
            "str_aes_encrypted": "s1aiR0qHAayxg11CyTDX1Q==",
            "key": "1234567890123456",
            "mode": "ECB",
            "encode": "utf-8"
        }
        result = encrypt_aes_decrypt(params, None, None)
        self.assertEqual(result["code"], 200)
        self.assertEqual(result["data"]["str_aes_decrypted"], "Hello, World!")

    def test_empty_crypted_string(self):
        params = {
            "str_aes_encrypted": "",
            "key": "1234567890123456",
            "mode": "CBC",
            "encode": "utf-8",
            "cbc_iv": "1234567890123456"
        }
        result = encrypt_aes_decrypt(params, None, None)
        self.assertEqual(result["summary"]["statusCode"], 400)
        self.assertEqual(result["summary"]["msg"], "Empty aes encrypted string")

    def test_empty_key(self):
        params = {
            "str_aes_encrypted": "KQ8kBYRmIyMCoh9rwsq6YA==",
            "key": "",
            "mode": "CBC",
            "encode": "utf-8",
            "cbc_iv": "1234567890123456"
        }
        result = encrypt_aes_decrypt(params, None, None)
        self.assertEqual(result["summary"]["statusCode"], 400)
        self.assertEqual(result["summary"]["msg"], "Empty key")

    def test_invalid_key_length(self):
        params = {
            "str_aes_encrypted": "KQ8kBYRmIyMCoh9rwsq6YA==",
            "key": "12345",
            "mode": "CBC",
            "encode": "utf-8",
            "cbc_iv": "1234567890123456"
        }
        result = encrypt_aes_decrypt(params, None, None)
        self.assertEqual(result["summary"]["statusCode"], 400)
        self.assertEqual(result["summary"]["msg"], "Invalid key length")

    def test_invalid_mode(self):
        params = {
            "str_aes_encrypted": "KQ8kBYRmIyMCoh9rwsq6YA==",
            "key": "1234567890123456",
            "mode": "INVALID",
            "encode": "utf-8",
            "cbc_iv": "1234567890123456"
        }
        result = encrypt_aes_decrypt(params, None, None)
        self.assertEqual(result["summary"]["statusCode"], 400)
        self.assertEqual(result["summary"]["msg"], "Invalid mode")

if __name__ == '__main__':
    unittest.main()
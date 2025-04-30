REGISTER API:
POST: http://localhost:8080/api/v1/auth/register

EXAMPLE BODY:
{
    "firstname": "alibaba",
    "lastname" : "calibaba",
    "email":"minecraft.minse@gmail.com",
    "hashedPassword":"1234"
}

RESPONDS WITH 200 OK AND JWT TOKEN BASED ON THE DATA GIVEN
----------------------------------------------------------------

AUTHENTICATE API:
POST: http://localhost:8080/api/v1/auth/authenticate

EXAMPLE BODY:

{
    "email":"minecraft.minse@gmail.com",
    "hashedPassword":"1234"
}
200 OK
BODY:RESPONDS WITH THE JWT TOKEN BASED ON THE EMAIL AND PASSWORD

----------------------------------------------------------------
TEST DEMO AUTHENTICATE:
GET:http://localhost:8080/api/v1/demo-controller
AUTH TYPE: BEARER TOKEN
TOKEN: <INSERT JWT TOKEN FROM REGISTER/AUTHENTICATE>

SHOULD RESPOND 200 OK



ENCRYPT API:

FOR NOW WORKS WITH EXISTING FILES IN THE UPLOADS FOLDER:
http://localhost:8080/api/secure-content/{FILENAME.EXTENSION}
EXAMPLE:
http://localhost:8080/api/secure-content/test2.epub
AUTH TYPE: BEARER TOKEN
TOKEN: <INSERT JWT TOKEN FROM REGISTER/AUTHENTICATE>

NEEDS TO BE DONE IN CURL IF TESTED:POSTMAN CANNOT LOG A RESPONSE THIS LONG

SHOULD RESPOND WITH: 200 OK
BYTE ARRAY[] <-- ENCRYPTED FILE


DECRYPT API:

FOR NOW WORKS WITH EXISTING FILES IN THE UPLOADS FOLDER:
http://localhost:8080/api/secure-content/decrypt/{FILENAME.EXTENSION}
EXAMPLE:
http://localhost:8080/api/secure-content/decrypt/test_pdf.bin
AUTH TYPE: BEARER TOKEN
TOKEN: <INSERT JWT TOKEN FROM REGISTER/AUTHENTICATE>

NEEDS TO BE DONE IN CURL IF TESTED:POSTMAN CANNOT LOG A RESPONSE THIS LONG

SHOULD RESPOND WITH: 200 OK
BYTE ARRAY[] <-- DECRYPTED FILE



EXAMPLE ENCRYPTION AND DECRYPTION SCRIPTS:

PDF:
$token = "eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJtaW5lY3JhZnQubWluc2VAZ21haWwuY29tIiwiaXNzIjoibGVjdHVyaXVtIiwiaWF0IjoxNzQ2MDIxMDA0LCJleHAiOjE3NDYwMjI0NDR9.H0hSum15GAP61yZGycJ2FlsddxWRxliPnqDNg6rEEZ8"

$headers = @{
    "Authorization" = "Bearer $token"
}

Invoke-WebRequest -Uri "http://localhost:8080/api/secure-content/test.pdf" -Headers $headers -OutFile "test_pdf.bin"


EPUB:
$token = "eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJtaW5lY3JhZnQubWluc2VAZ21haWwuY29tIiwiaXNzIjoibGVjdHVyaXVtIiwiaWF0IjoxNzQ2MDIxMDA0LCJleHAiOjE3NDYwMjI0NDR9.H0hSum15GAP61yZGycJ2FlsddxWRxliPnqDNg6rEEZ8"

$headers = @{
    "Authorization" = "Bearer $token"
}

Invoke-WebRequest -Uri "http://localhost:8080/api/secure-content/test2.epub" -Headers $headers -OutFile "test_epub.bin"


DECRYPTION:
------------------------------------------------------
PDF:
$token = "eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJtaW5lY3JhZnQubWluc2VAZ21haWwuY29tIiwiaXNzIjoibGVjdHVyaXVtIiwiaWF0IjoxNzQ2MDIxMDA0LCJleHAiOjE3NDYwMjI0NDR9.H0hSum15GAP61yZGycJ2FlsddxWRxliPnqDNg6rEEZ8"

$headers = @{
    "Authorization" = "Bearer $token"
}

Invoke-WebRequest -Uri "http://localhost:8080/api/secure-content/decrypt/test_pdf.bin" -Headers $headers -OutFile "happyPathPdf.pdf"
EPUB:


$token = "eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJtaW5lY3JhZnQubWluc2VAZ21haWwuY29tIiwiaXNzIjoibGVjdHVyaXVtIiwiaWF0IjoxNzQ2MDIxMDA0LCJleHAiOjE3NDYwMjI0NDR9.H0hSum15GAP61yZGycJ2FlsddxWRxliPnqDNg6rEEZ8"

$headers = @{
    "Authorization" = "Bearer $token"
}

Invoke-WebRequest -Uri "http://localhost:8080/api/secure-content/decrypt/test_epub.bin" -Headers $headers -OutFile "happyPathEpub.epub"
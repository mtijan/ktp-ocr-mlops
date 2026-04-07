import cv2
import easyocr
import re

# init OCR (load sekali)
reader = easyocr.Reader(['id','en'])


def extract_ktp_data(image_path):
    # ======================
    # LOAD + PREPROCESS
    # ======================
    img = cv2.imread(image_path)

    if img is None:
        raise ValueError("Image not found")

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (3,3), 0)

    # ======================
    # OCR
    # ======================
    results = reader.readtext(blur)
    raw_text = " ".join([r[1] for r in results])

    # ======================
    # CLEAN TEXT
    # ======================
    clean = raw_text.upper()

    clean = clean.replace("TEMPATTGL", "TEMPAT TGL")
    clean = clean.replace("RTIRW", "RT RW")
    clean = clean.replace("KELLDESA", "KEL/DESA")

    # ======================
    # EXTRACT NIK
    # ======================
    nik = re.findall(r'\d{16}', raw_text)
    nik = nik[0] if nik else None

    # ======================
    # EXTRACT NAMA
    # ======================
    nama = None
    match = re.search(r'NAMA\s+([A-Z\s]+?)\s+TEMPAT', clean)
    if match:
        nama = match.group(1).strip()

    # ======================
    # EXTRACT TTL
    # ======================
    tempat = None
    tanggal = None

    match = re.search(r'([A-Z]+),\s*(\d{2}-\d{2}-\d{4})', clean)
    if match:
        tempat = match.group(1)
        tanggal = match.group(2)

    # ======================
    # EXTRACT GENDER
    # ======================
    jk = None
    if "LAKI" in clean:
        jk = "Laki-laki"
    elif "PEREMPUAN" in clean:
        jk = "Perempuan"

    # ======================
    # EXTRACT ALAMAT
    # ======================
    alamat = None
    match = re.search(r'ALAMAT\s+(.+?)(RT|KEL|KECAMATAN|AGAMA)', clean)
    if match:
        alamat = match.group(1).strip()
        alamat = alamat.replace("  ", " ")

    # ======================
    # OUTPUT
    # ======================
    return {
        "nik": nik,
        "nama": nama,
        "tempat_lahir": tempat,
        "tanggal_lahir": tanggal,
        "jenis_kelamin": jk,
        "alamat": alamat,
        "raw_text": raw_text  # penting buat debug
    }


# ======================
# TEST LOCAL
# ======================
if __name__ == "__main__":
    result = extract_ktp_data("data/sample_ktp_2.jpg")
    print(result)
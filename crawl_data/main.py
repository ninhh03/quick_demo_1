import re
import json
import time
import random
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# URL gốc
BASE_URL = "https://www.chotot.com"
CATEGORY_PATH = "/mua-ban-thoi-trang-do-dung-ca-nhan"

# Random user-agent
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36"
]

def get_headers():
    return {"User-Agent": random.choice(USER_AGENTS)}

def get_soup(url: str):
    """Trả về soup nếu request thành công"""
    try:
        resp = requests.get(url, headers=get_headers(), timeout=10)
        if resp.status_code == 200:
            return BeautifulSoup(resp.text, "html.parser")
    except requests.exceptions.RequestException as e:
        print("Lỗi request:", e)
    return None

def get_detail_info(link_chi_tiet: str):
    """Lấy thông tin chi tiết từ trang sản phẩm"""
    soup = get_soup(link_chi_tiet)
    if not soup:
        return None

    # --- Tên sản phẩm ---
    name_tag = soup.select_one("h1.AdDecription_adTitle__S--XB")
    ten_san_pham = name_tag.get_text(strip=True) if name_tag else None

    # --- Mô tả chi tiết ---
    desc_block = soup.find("div", {"class": "cr3by7y"})
    if desc_block:
        mo_ta = " ".join(p.get_text(strip=True) for p in desc_block.find_all("p"))
    else:
        desc_tag = soup.find("p", {"itemprop": "description"})
        mo_ta = desc_tag.get_text(strip=True) if desc_tag else None

    # --- Ảnh chi tiết ---
    anh_chi_tiet = []
    for img in soup.find_all("img"):
        src = img.get("src", "")
        alt = img.get("alt", "")
        if not src.startswith("http"):
            continue
        if any(x in src for x in ["uac2/", "chotot-icons", "icon", "svg", "logo", "favicon"]):
            continue
        if ten_san_pham and ten_san_pham in alt:
            anh_chi_tiet.append(src)
        elif "cdn.chotot.com" in src:
            anh_chi_tiet.append(src)
    anh_chi_tiet = list(set(anh_chi_tiet))  # bỏ trùng

    # --- Số lượng đánh giá ---
    so_luong_danh_gia = None
    for span in soup.find_all("span"):
        text = span.get_text(strip=True)
        if "đánh giá" in text:
            m = re.search(r"(\d+)", text)
            if m:
                so_luong_danh_gia = int(m.group(1))
            break


    return {
        "ten_san_pham": ten_san_pham,
        "mo_ta": mo_ta,
        "anh_chi_tiet": anh_chi_tiet,
        "so_luong_danh_gia": so_luong_danh_gia
    }


def crawl_page(page: int):
    """Crawl dữ liệu 1 trang"""
    url = f"{BASE_URL}{CATEGORY_PATH}" if page == 1 else f"{BASE_URL}{CATEGORY_PATH}?page={page}"
    soup = get_soup(url)
    if not soup:
        return {}

    print(f"Kết nối thành công page {page}!")

    results = {}
    ul_tag = soup.find("ul")
    lis = ul_tag.find_all("li") if ul_tag else []

    for li in lis:
        # --- Tên sản phẩm ---
        name_tag = li.find("h3")
        if not name_tag:
            continue
        ten_san_pham = name_tag.get_text(strip=True)

        # --- Giá ---
        gia_tag = li.find("span", string=lambda x: x and "đ" in x)
        gia = gia_tag.get_text(strip=True) if gia_tag else None

        # --- Ảnh ---
        link_anh = next((img["src"] for img in li.find_all("img") if img.get("src", "").startswith("http")), None)

        # --- Link chi tiết ---
        a_tag = li.find("a", href=True)
        link_chi_tiet = urljoin(BASE_URL, a_tag["href"]) if a_tag else None

        # --- ID sản phẩm ---
        product_id = None
        if link_chi_tiet:
            m = re.search(r"/(\d+)\.htm", link_chi_tiet)
            if m:
                product_id = m.group(1)
        if not product_id:
            continue

        # --- Địa chỉ ---
        dia_chi = None
        location_svg = li.find("svg", {"id": "LocationFilled"})
        if location_svg:
            parent_div = location_svg.find_parent("div")
            dia_chi_tag = parent_div.find("span") if parent_div else None
            dia_chi = dia_chi_tag.get_text(strip=True) if dia_chi_tag else None

        # --- Thông tin chi tiết ---
        mo_ta, anh_chi_tiet, so_luong_danh_gia = None, [], None
        if link_chi_tiet:
            detail_info = get_detail_info(link_chi_tiet)
            if detail_info:
                mo_ta = detail_info.get("mo_ta")
                anh_chi_tiet = detail_info.get("anh_chi_tiet", [])
                so_luong_danh_gia = detail_info.get("so_luong_danh_gia")
            time.sleep(random.uniform(1, 2))  # tránh spam


        results[product_id] = {
            "ten_san_pham": ten_san_pham,
            "gia": gia,
            "link_anh": link_anh,
            "link_chi_tiet": link_chi_tiet,
            "so_luong_danh_gia": so_luong_danh_gia,
            "dia_chi": dia_chi,
            "mo_ta": mo_ta,
            "anh_chi_tiet": anh_chi_tiet
        }

    return results

if __name__ == "__main__":
    all_results = {}
    for page in range(1, 15):  # crawl 2 trang đầu
        data = crawl_page(page)
        for pid, info in data.items():
            if pid not in all_results:  # tránh trùng
                all_results[pid] = info
        time.sleep(random.uniform(2, 4))

    # Convert dict -> array document (chỉ giữ các trường cần)
    mongo_docs = []
    for pid, info in all_results.items():
        doc = {
            "_id": pid,
            "ten_san_pham": info.get("ten_san_pham"),
            "link_anh": info.get("anh_chi_tiet", []),  # thay bằng danh sách ảnh chi tiết
            "gia": info.get("gia"),
            "so_luong_danh_gia": info.get("so_luong_danh_gia"),
            "dia_chi": info.get("dia_chi"),
            "mo_ta": info.get("mo_ta"),
        }
        mongo_docs.append(doc)

    # Save JSON dạng array
    with open("result.json", "w", encoding="utf-8") as f:
        json.dump(mongo_docs, f, ensure_ascii=False, indent=2)

    print(f"Đã lưu {len(mongo_docs)} sản phẩm vào result.json (MongoDB ready)")
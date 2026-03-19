import os
import requests
from bs4 import BeautifulSoup
from pypdf import PdfWriter
from urllib.parse import urljoin

# 1. 기본 설정
TARGET_URL = "https://pages.cs.wisc.edu/~remzi/OSTEP/"
DOWNLOAD_DIR = "./os_english_pdfs"
OUTPUT_PDF = "OSTEP_English_Full.pdf"

if not os.path.exists(DOWNLOAD_DIR):
    os.makedirs(DOWNLOAD_DIR)

def main():
    print("1. OSTEP 웹페이지에서 PDF 링크를 추출합니다...")
    response = requests.get(TARGET_URL)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')

    # PDF 링크가 가장 많은 메인 표(Table) 찾기
    best_table = None
    max_pdfs = 0
    for table in soup.find_all('table'):
        pdfs = [a for a in table.find_all('a') if a.get('href', '').endswith('.pdf')]
        if len(pdfs) > max_pdfs:
            best_table = table
            max_pdfs = len(pdfs)

    if not best_table:
        print("에러: PDF 링크가 포함된 표를 찾을 수 없습니다.")
        return

    pdf_links = []
    
    # ⭐ 핵심: 표를 '가로'가 아닌 '세로(Column) 방향'으로 읽어서 오름차순 순서 맞추기
    rows = best_table.find_all('tr')
    # 표에서 가장 긴 가로 칸 수(열의 최대 개수) 구하기
    max_cols = max(len(row.find_all(['td', 'th'])) for row in rows)
    
    for col_idx in range(max_cols):
        for row in rows:
            cells = row.find_all(['td', 'th'])
            # 현재 행(row)에 해당 열(col_idx)이 존재하는지 확인
            if col_idx < len(cells):
                link = cells[col_idx].find('a')
                if link and link.get('href', '').endswith('.pdf'):
                    full_url = urljoin(TARGET_URL, link['href'])
                    # 중복 방지
                    if full_url not in pdf_links:
                        pdf_links.append(full_url)

    print(f"총 {len(pdf_links)}개의 PDF 링크를 정확한 챕터 순서대로 찾았습니다.\n")

    downloaded_files = []

    print("2. PDF 다운로드를 시작합니다 (챕터 순서 유지)...")
    for index, url in enumerate(pdf_links, start=1):
        # 파일명 앞에 01_, 02_ 처럼 번호를 붙여 로컬에서도 순서가 꼬이지 않게 보호
        original_name = url.split('/')[-1]
        filename = f"{index:02d}_{original_name}"
        filepath = os.path.join(DOWNLOAD_DIR, filename)
        
        if not os.path.exists(filepath):
            print(f"다운로드 중 ({index}/{len(pdf_links)}): {filename}")
            try:
                res = requests.get(url)
                res.raise_for_status()
                with open(filepath, 'wb') as f:
                    f.write(res.content)
            except Exception as e:
                print(f"다운로드 실패 ({filename}): {e}")
                continue
        else:
            print(f"이미 존재함, 건너뜀: {filename}")
            
        downloaded_files.append(filepath)

    print("\n3. 다운로드한 PDF 파일들을 하나로 병합합니다...")
    merger = PdfWriter()
    
    for pdf in downloaded_files:
        try:
            merger.append(pdf)
            print(f"병합 추가: {os.path.basename(pdf)}")
        except Exception as e:
            print(f"병합 오류 ({pdf}): {e}")

    merger.write(OUTPUT_PDF)
    merger.close()
    
    print(f"\n 완료 챕터 순으로 병합된 최종 영문 파일이 생성되었습니다: {OUTPUT_PDF}")

if __name__ == "__main__":
    main()
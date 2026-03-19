import os
import re
import requests
from pypdf import PdfWriter  # <-- PdfMerger 대신 PdfWriter를 불러옵니다!

# 1. 깃허브 README 마크다운 텍스트 (원하는 텍스트를 그대로 넣습니다)
markdown_text = """

# OSTEP (Korean Version)

<p align="center">
  <img src=cover.jpg/>
</p>

Welcome to the Korean translation of OSTEP, v0.91. 
Translation by Youjip Won, Minkyu Park, Sungjin Lee.

Interested in buying?
- [Hardcover](http://www.hongpub.co.kr/sub.php?goPage=view_product&flashpage=&Code=20170523160625)
- [Softcover](http://www.hongpub.co.kr/sub.php?goPage=view_product&flashpage=&Code=20170327120039)

Book chapters, available freely here:

| intro                                     | virtualization                                    |                                                      | concurrency                                             | persistence                                                 | 
| ----------------------------------------- | ------------------------------------------------- | ---------------------------------------------------- | ------------------------------------------------------- | ----------------------------------------------------------- | 
| [Preface](https://pages.cs.wisc.edu/~remzi/OSTEP/Korean/00-preface.pdf)                 | 3 [Dialogue](https://pages.cs.wisc.edu/~remzi/OSTEP/Korean/03-dialogue-virtualization.pdf)      | 12 [Dialogue](https://pages.cs.wisc.edu/~remzi/OSTEP/Korean/12-dialogue-vm.pdf)                    | 25 [Dialogue](https://pages.cs.wisc.edu/~remzi/OSTEP/Korean/25_dialogue-concurrency.pdf)              | 35 [Dialogue](https://pages.cs.wisc.edu/~remzi/OSTEP/Korean/35_dialogue-persistence.pdf)                  | 
| [Preface-Translate](https://pages.cs.wisc.edu/~remzi/OSTEP/Korean/00-preface-tx.pdf)    | 4 [Processes](https://pages.cs.wisc.edu/~remzi/OSTEP/Korean/04-cpu-intro.pdf)                   | 13 [Address Spaces](https://pages.cs.wisc.edu/~remzi/OSTEP/Korean/13-vm-intro.pdf)                 | 26 [Concurrency and Threads](https://pages.cs.wisc.edu/~remzi/OSTEP/Korean/26_threads-intro.pdf)      | 36 [I/O Devices](https://pages.cs.wisc.edu/~remzi/OSTEP/Korean/36_file-devices.pdf)                       | 
| [TOC](https://pages.cs.wisc.edu/~remzi/OSTEP/Korean/00-toc.pdf)                         | 5 [Process API](https://pages.cs.wisc.edu/~remzi/OSTEP/Korean/05-cpu-api.pdf)                   | 14 [Memory API](https://pages.cs.wisc.edu/~remzi/OSTEP/Korean/14-vm-api.pdf)                       | 27 [Thread API](https://pages.cs.wisc.edu/~remzi/OSTEP/Korean/27_threads-api.pdf)                     | 37 [Hard Disk Drives](https://pages.cs.wisc.edu/~remzi/OSTEP/Korean/37_file_disks.pdf)                    | 
| 1 [Dialogue](https://pages.cs.wisc.edu/~remzi/OSTEP/Korean/01-dialogue-threeeasy.pdf)   | 6 [Direct Execution](https://pages.cs.wisc.edu/~remzi/OSTEP/Korean/06-cpu-mechanisms.pdf)       | 15 [Address Translation](https://pages.cs.wisc.edu/~remzi/OSTEP/Korean/15-vm-mechanism.pdf)        | 28 [Locks](https://pages.cs.wisc.edu/~remzi/OSTEP/Korean/28_threads-locks.pdf)                        | 38 [Redundant Disk Arrays (RAID)](https://pages.cs.wisc.edu/~remzi/OSTEP/Korean/38_RAID.pdf)              | 
| 2 [Introduction](https://pages.cs.wisc.edu/~remzi/OSTEP/Korean/02-intro.pdf)            | 7 [CPU Scheduling](https://pages.cs.wisc.edu/~remzi/OSTEP/Korean/07-cpu-sched.pdf)              | 16 [Segmentation](https://pages.cs.wisc.edu/~remzi/OSTEP/Korean/16-vm-segmentation.pdf)            | 29 [Locked Data Structures](https://pages.cs.wisc.edu/~remzi/OSTEP/Korean/29_threads-locks-usage.pdf) | 39 [Files and Directories](https://pages.cs.wisc.edu/~remzi/OSTEP/Korean/39_interlude-file-directory.pdf) | 
|                                                                   | 8 [Multi-level Feedback](https://pages.cs.wisc.edu/~remzi/OSTEP/Korean/08-cpu-sched-mlfq.pdf)   | 17 [Free Space Management](https://pages.cs.wisc.edu/~remzi/OSTEP/Korean/17-vm-freespace.pdf)      | 30 [Condition Variables](https://pages.cs.wisc.edu/~remzi/OSTEP/Korean/30_threads-cv.pdf)             | 40 [File System Implementation](https://pages.cs.wisc.edu/~remzi/OSTEP/Korean/40_FS-implementation.pdf)   | 
|                                                                   | 9 [Lottery Scheduling](https://pages.cs.wisc.edu/~remzi/OSTEP/Korean/09-cpu-sched-lottery.pdf)  | 18 [Introduction to Paging](https://pages.cs.wisc.edu/~remzi/OSTEP/Korean/18-vm-paging.pdf)        | 31 [Semaphores](https://pages.cs.wisc.edu/~remzi/OSTEP/Korean/31_threads-sema.pdf)                    | 41 [Fast File System (FFS)](https://pages.cs.wisc.edu/~remzi/OSTEP/Korean/41_FFS.pdf)                     | 
|                                                                   | 10 [Multi-CPU Scheduling](https://pages.cs.wisc.edu/~remzi/OSTEP/Korean/10-cpu-sched-multi.pdf) | 19 [Translation Lookaside Buffers](https://pages.cs.wisc.edu/~remzi/OSTEP/Korean/19_vm-tlbs.pdf)   | 32 [Concurrency Bugs](https://pages.cs.wisc.edu/~remzi/OSTEP/Korean/32_threads-bugs.pdf)              | 42 [FSCK and Journaling](https://pages.cs.wisc.edu/~remzi/OSTEP/Korean/42_crash-consistency.pdf)          | 
|                                                                   | 11 [Summary](https://pages.cs.wisc.edu/~remzi/OSTEP/Korean/11-cpu-dialogue.pdf)                 | 20 [Advanced Page Tables](https://pages.cs.wisc.edu/~remzi/OSTEP/Korean/20_vm-smalltables.pdf)     | 33 [Event-based Concurrency](https://pages.cs.wisc.edu/~remzi/OSTEP/Korean/33_threads-events.pdf)     | 43 [Log-Structured File System (LFS)](https://pages.cs.wisc.edu/~remzi/OSTEP/Korean/43_LFS.pdf)           |
|                                                                   |                                                                           | 21 [Swapping: Mechanisms](https://pages.cs.wisc.edu/~remzi/OSTEP/Korean/21_vm-beyondphys.pdf)      | 34 [Summary](https://pages.cs.wisc.edu/~remzi/OSTEP/Korean/34_threads_dialogue.pdf)                   | 44 [Data Integrity and Protection](https://pages.cs.wisc.edu/~remzi/OSTEP/Korean/44_data-integrity.pdf)   |
|                                                                   |                                                                           | 22 [Swapping: Policies](https://pages.cs.wisc.edu/~remzi/OSTEP/Korean/22_vm-beyondphys-policy.pdf) |                                                                                 | 45 [Summary](https://pages.cs.wisc.edu/~remzi/OSTEP/Korean/45_file-dialogue.pdf)                          |
|                                                                   |                                                                           | 23 [Case Study: VAX](https://pages.cs.wisc.edu/~remzi/OSTEP/Korean/23_vm-vax.pdf)                  |                                                                                 | 46 [Dialogue](https://pages.cs.wisc.edu/~remzi/OSTEP/Korean/46_dialogue-distribution.pdf)                 |
|                                                                   |                                                                           | 24 [Summary](https://pages.cs.wisc.edu/~remzi/OSTEP/Korean/24_vm-dialogue.pdf)                     |                                                                                 | 47 [Distributed Systems](https://pages.cs.wisc.edu/~remzi/OSTEP/Korean/47_dist-intro.pdf)                 |
|                                                                   |                                                                           |                                                      |                                                                                                         | 48 [Network File System (NFS)](https://pages.cs.wisc.edu/~remzi/OSTEP/Korean/48_NFS.pdf)                  |
|                                                                   |                                                                           |                                                      |                                                                                                         | 49 [Andrew File System (AFS)](https://pages.cs.wisc.edu/~remzi/OSTEP/Korean/49_AFS.pdf)                   |
|                                                                   |                                                                           |                                                      |                                                                                                         | 50 [Summary](https://pages.cs.wisc.edu/~remzi/OSTEP/Korean/50_dist-dialogue.pdf)                          |

"""

DOWNLOAD_DIR = "./ostep_korean_pdfs"
OUTPUT_PDF = "OSTEP_Korean_Full.pdf"

if not os.path.exists(DOWNLOAD_DIR):
    os.makedirs(DOWNLOAD_DIR)

def main():
    print("1. 마크다운 텍스트에서 PDF 링크를 추출합니다...")
    pdf_urls = re.findall(r'https?://[^\s\)"]+\.pdf', markdown_text)
    pdf_urls = list(set(pdf_urls))
    pdf_urls = sorted(pdf_urls, key=lambda url: url.split('/')[-1])
    
    print(f"총 {len(pdf_urls)}개의 PDF 링크를 찾고 챕터 순으로 정렬했습니다.\n")

    downloaded_files = []

    print("2. PDF 다운로드를 시작합니다 (챕터 오름차순)...")
    for url in pdf_urls:
        filename = url.split('/')[-1]
        filepath = os.path.join(DOWNLOAD_DIR, filename)
        
        if not os.path.exists(filepath):
            print(f"다운로드 중: {filename}")
            response = requests.get(url)
            response.raise_for_status()
            with open(filepath, 'wb') as f:
                f.write(response.content)
        else:
            print(f"이미 존재함, 건너뜀: {filename}")
            
        downloaded_files.append(filepath)

    print("\n3. 다운로드한 PDF 파일들을 하나로 병합합니다...")
    merger = PdfWriter()  # <-- PdfMerger() 대신 PdfWriter()를 사용합니다!
    
    for pdf in downloaded_files:
        try:
            merger.append(pdf)
            print(f"병합 추가: {os.path.basename(pdf)}")
        except Exception as e:
            print(f"병합 오류 ({pdf}): {e}")

    merger.write(OUTPUT_PDF)
    merger.close()
    
    print(f"\n완료! 챕터 순으로 병합된 최종 파일이 생성되었습니다: {OUTPUT_PDF}")

if __name__ == "__main__":
    main()
import os
import glob
import re

def create_html_subplots(folder_path="../checkpoints_all_waveforms"):
    # 1. 파일 찾기 및 정렬
    files = glob.glob(os.path.join(folder_path, "tsne_SNR_*.png"))
    if not files:
        print("❌ 이미지를 찾을 수 없습니다.")
        return

    # SNR 숫자 기준 정렬
    def get_snr(fname):
        match = re.search(r"SNR_([-\d]+)", fname)
        return int(match.group(1)) if match else 0

    files.sort(key=get_snr)
    snr_values = [get_snr(f) for f in files]

    print(f"📸 Found {len(files)} images. Generating grid HTML...")

    # 2. 각 이미지 HTML 태그 생성
    img_tags = ""
    for fpath, snr in zip(files, snr_values):
        rel_path = os.path.basename(fpath)  # 이미지가 같은 폴더에 있다고 가정
        img_tags += f"""
        <div class="img-box">
            <div class="snr-label">SNR {snr} dB</div>
            <img src="{rel_path}" alt="SNR {snr}" />
        </div>
        """

    # 3. HTML 구조
    html_content = f"""
    <!DOCTYPE html>
    <html lang="ko">
    <head>
        <meta charset="UTF-8">
        <title>t-SNE Grid Viewer (Subplots)</title>
        <style>
            body {{
                font-family: sans-serif;
                text-align: center;
                background: #fafafa;
                margin: 20px;
            }}
            h2 {{
                color: #333;
                margin-bottom: 30px;
            }}
            .grid {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
                gap: 20px;
                justify-items: center;
            }}
            .img-box {{
                background: white;
                padding: 10px;
                border-radius: 10px;
                box-shadow: 0 4px 10px rgba(0,0,0,0.1);
                transition: transform 0.2s ease;
            }}
            .img-box:hover {{
                transform: scale(1.03);
            }}
            .snr-label {{
                font-weight: bold;
                margin-bottom: 8px;
                color: #555;
            }}
            img {{
                width: 100%;
                height: auto;
                border-radius: 6px;
                border: 1px solid #ddd;
            }}
        </style>
    </head>
    <body>
        <h2>t-SNE Distributions per SNR</h2>
        <div class="grid">
            {img_tags}
        </div>
        <p style="color: #666; margin-top: 30px;">
            총 {len(files)}개 이미지 표시됨.
        </p>
    </body>
    </html>
    """

    # 4. HTML 저장
    output_file = "tsne_viewer_snr_grid.html"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"✅ Successfully created '{output_file}'")
    print("👉 이미지들과 같은 폴더에 HTML을 두고 브라우저로 열면 됩니다.")

# 실행
create_html_subplots(folder_path="../checkpoints_all_waveforms")

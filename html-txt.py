import os
import re
from bs4 import BeautifulSoup

# 出力先の最大サイズ (10MB = 10 * 1024 * 1024 bytes)
MAX_FILE_SIZE = 10 * 1024 * 1024

def html_to_text(html_content):
    """
    HTML文字列からテキストのみを抽出する関数。
    <script>, <style> タグなどの不要な部分を取り除いた上で、可読性向上のために少し整形。
    """
    soup = BeautifulSoup(html_content, "html.parser")

    # script, style, head, footerなど不要なタグを削除
    for tag in soup(["script", "style", "noscript", "header", "footer"]):
        tag.decompose()

    # ページ内のテキストを取得
    text = soup.get_text(separator="\n")

    # 余計な空白や改行の連続を整形
    text = re.sub(r'\n\s*\n+', '\n\n', text)  # 改行の連続を減らす
    text = text.strip()  # 先頭と末尾の空白を除去

    return text

def combine_html_files(input_dir, output_prefix="knowledge"):
    """
    指定ディレクトリ内のHTMLファイルをまとめてテキスト化し、
    10MBを超えないように分割して保存する関数。

    Parameters
    ----------
    input_dir : str
        HTMLファイルが格納されているディレクトリへのパス
    output_prefix : str
        出力ファイル名のプレフィックス（拡張子は .txt）
    """
    # 出力用バッファ
    combined_text = ""

    # ファイル出力のカウンタ
    file_index = 1

    # input_dir下のファイルを走査
    for filename in os.listdir(input_dir):
        file_path = os.path.join(input_dir, filename)
        if not os.path.isfile(file_path):
            continue
        # 拡張子が .html や .htm のものだけ処理
        if filename.lower().endswith((".html", ".htm")):
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                html_content = f.read()

            # HTMLからテキスト抽出
            text_content = html_to_text(html_content)

            # 結合テキストに追加
            # 途中で 10MB を超えそうなら、一旦ファイル保存する
            if (len(combined_text.encode('utf-8')) + len(text_content.encode('utf-8'))) > MAX_FILE_SIZE:
                # まずは現在のcombined_textをファイルとして保存
                output_name = f"{output_prefix}_{file_index}.txt"
                with open(output_name, "w", encoding="utf-8") as out_f:
                    out_f.write(combined_text)

                print(f"Saved: {output_name} (size: {len(combined_text.encode('utf-8'))} bytes)")
                file_index += 1

                # 新しいファイル用のバッファをリセット
                combined_text = text_content
            else:
                # 超えない場合は単純に追記
                combined_text += "\n\n" + text_content

    # ループ終了後、バッファに残っている分を保存
    if combined_text.strip():
        output_name = f"{output_prefix}_{file_index}.txt"
        with open(output_name, "w", encoding="utf-8") as out_f:
            out_f.write(combined_text)
        print(f"Saved: {output_name} (size: {len(combined_text.encode('utf-8'))} bytes)")

def main():
    # 例: "downloaded_pages" ディレクトリ内のHTMLを全部結合し、
    # "knowledge" という名前で分割テキストを出力する
    input_dir = "downloaded_pages"
    output_prefix = "knowledge"  # "knowledge_1.txt", "knowledge_2.txt" ... のように分割出力される

    combine_html_files(input_dir, output_prefix=output_prefix)

if __name__ == "__main__":
    main()

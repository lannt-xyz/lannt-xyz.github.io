#!/usr/bin/env python3
"""Chuyển nhiều file Excel/CSV sang Markdown để nạp vào AnythingLLM.

Dùng:
    python xlsx2md.py <thư_mục_gốc> [thư_mục_đầu_ra] [--style rows|table] [--max-rows 300] [--lang vi|ja]

Hai kiểu xuất:
  rows  (mặc định, khuyên dùng): mỗi dòng Excel = 1 dòng văn bản dạng
        "Tên cột: giá trị | Tên cột: giá trị ...". Mỗi đoạn AnythingLLM cắt ra
        vẫn tự mang đủ tên cột nên tìm kiếm chính xác hơn.
  table: bảng Markdown, header lặp lại sau mỗi 20 dòng.
"""
import argparse
import datetime as dt
import re
import gc
import sys
import time
import unicodedata
import zipfile
from pathlib import Path

import pandas as pd
from openpyxl import load_workbook

EXCEL_EXT = {".xlsx", ".xlsm"}
OTHER_EXT = {".xls", ".csv", ".tsv"}

LABELS = {
    "vi": dict(col="Cột {n}", sheet="Sheet", rows="Dòng dữ liệu {a}–{b} / {n}. Các cột: ", row="dòng {k}",
               date="%d/%m/%Y", dtime="%d/%m/%Y %H:%M", norm="NFC"),
    "ja": dict(col="列{n}", sheet="シート", rows="データ行 {a}〜{b} / 全{n}行。列: ", row="{k}行目",
               date="%Y/%m/%d", dtime="%Y/%m/%d %H:%M", norm="NFKC"),
}
L = LABELS["vi"]


def clean(v):
    """Chuẩn hóa một ô thành chuỗi; rỗng -> ''."""
    if v is None:
        return ""
    if isinstance(v, float):
        if v != v:  # NaN
            return ""
        return str(int(v)) if v.is_integer() else f"{v:.10g}"
    if isinstance(v, dt.datetime):
        return v.strftime(L["date"]) if (v.hour, v.minute, v.second) == (0, 0, 0) else v.strftime(L["dtime"])
    if isinstance(v, dt.date):
        return v.strftime(L["date"])
    s = unicodedata.normalize(L["norm"], str(v)).replace("\r", " ").replace("\n", " ").replace("|", "/").strip()
    return re.sub(r"\s{2,}", " ", s)


MAX_EMPTY_RUN = 1000  # gặp chừng này hàng trống liên tiếp thì coi như hết dữ liệu (bỏ vùng định dạng ảo)


def col_to_num(letters):
    n = 0
    for ch in letters:
        n = n * 26 + ord(ch) - 64
    return n


def merged_ranges(path, sheet_name):
    """Đọc danh sách ô gộp thẳng từ XML (không phải nạp cả sheet vào RAM). Trả [(r1,c1,r2,c2)]."""
    import re
    try:
        with zipfile.ZipFile(path) as z:
            wbx = z.read("xl/workbook.xml").decode("utf-8", "replace")
            rels = z.read("xl/_rels/workbook.xml.rels").decode("utf-8", "replace")
            m = re.search(r'<sheet\b[^>]*\bname="%s"[^>]*>' % re.escape(sheet_name.replace("&", "&amp;")), wbx)
            if not m:
                return []
            rid = re.search(r'r:id="([^"]+)"', m.group(0)).group(1)
            tgt = re.search(r'<Relationship\b[^>]*\bId="%s"[^>]*>' % re.escape(rid), rels).group(0)
            target = re.search(r'Target="([^"]+)"', tgt).group(1).lstrip("/")
            member = target if target.startswith("xl/") else "xl/" + target
            out, carry = [], b""
            pat = re.compile(rb'<mergeCell\b[^>]*ref="([A-Z]+)(\d+):([A-Z]+)(\d+)"')
            with z.open(member) as f:
                while True:
                    chunk = f.read(1 << 20)
                    if not chunk:
                        break
                    buf = carry + chunk
                    for a, b, c, d in pat.findall(buf):
                        out.append((int(b), col_to_num(a.decode()), int(d), col_to_num(c.decode())))
                    carry = buf[-300:]  # tránh cắt giữa thẻ; trùng lặp được khử bên dưới
            return list(dict.fromkeys(out))
    except Exception:
        return []


def sheet_rows_openpyxl(ws, path=None):
    """Đọc sheet .xlsx kiểu streaming: bỏ hàng/cột trống ở cuối, điền xuống ô gộp dọc."""
    grid, empty_run, max_w = [], 0, 0
    for row in ws.iter_rows(values_only=True):
        if any(v is not None and v != "" for v in row):
            grid.extend([[]] * empty_run)  # giữ hàng trống xen kẽ để số dòng không lệch
            empty_run = 0
            row = list(row)
            while row and (row[-1] is None or row[-1] == ""):
                row.pop()
            max_w = max(max_w, len(row))
            grid.append(row)
        else:
            empty_run += 1
            if empty_run >= MAX_EMPTY_RUN:
                break
    if path is not None and grid:
        for r1, c1, r2, c2 in merged_ranges(path, ws.title):
            if r1 - 1 >= len(grid):
                continue
            top = grid[r1 - 1][c1 - 1] if c1 - 1 < len(grid[r1 - 1]) else None
            if top is None:
                continue
            for r in range(r1, min(r2, len(grid)) + 1):  # chỉ điền xuống theo chiều dọc
                row = grid[r - 1]
                if len(row) < c1:
                    row.extend([None] * (c1 - len(row)))
                row[c1 - 1] = top
    return grid


def sheets_of(path: Path):
    """Trả về [(tên_sheet, grid)] với grid là list các hàng (list giá trị)."""
    ext = path.suffix.lower()
    out = []
    if ext in EXCEL_EXT:
        wb = load_workbook(path, data_only=True, read_only=True)
        try:
            for ws in wb.worksheets:
                if ws.sheet_state != "visible":
                    continue
                try:
                    ws.reset_dimensions()  # bỏ qua vùng "dimension" bị phình trong file
                except Exception:
                    pass
                out.append((ws.title, sheet_rows_openpyxl(ws, path)))
        finally:
            wb.close()
    elif ext == ".xls":
        for name, df in pd.read_excel(path, sheet_name=None, header=None).items():
            out.append((name, df.astype(object).where(df.notna(), None).values.tolist()))
    else:
        sep = "\t" if ext == ".tsv" else None
        df = pd.read_csv(path, header=None, sep=sep, engine="python", encoding_errors="replace")
        out.append((path.stem, df.astype(object).where(df.notna(), None).values.tolist()))
    return out


def split_header(grid):
    """Tìm dòng tiêu đề: dòng đầu (trong 15 dòng đầu) có >=60% ô không rỗng so với dòng rộng nhất."""
    grid = [[clean(c) for c in row] for row in grid]
    grid = [r for r in grid if any(r)]
    if not grid:
        return [], []
    width = max(sum(1 for c in r if c) for r in grid[:15])
    header_idx = 0
    for i, r in enumerate(grid[:15]):
        if sum(1 for c in r if c) >= max(1, 0.6 * width):
            header_idx = i
            break
    title_lines = [" ".join(c for c in r if c) for r in grid[:header_idx]]
    header = grid[header_idx]
    # tên cột trống -> "Cột N"; trùng -> thêm số
    seen, names = {}, []
    for j, h in enumerate(header):
        h = h or L["col"].format(n=j + 1)
        seen[h] = seen.get(h, 0) + 1
        names.append(h if seen[h] == 1 else f"{h} ({seen[h]})")
    body = grid[header_idx + 1:]
    return (title_lines, names), body


def render(file_label, sheet, title_lines, names, body, style, max_rows):
    """Sinh danh sách (hậu_tố, nội_dung_md); chia nhỏ theo max_rows dòng."""
    parts = []
    for start in range(0, len(body), max_rows):
        chunk = body[start:start + max_rows]
        first_row = start + 1
        last_row = start + len(chunk)
        lines = [f"# {file_label} — {L['sheet']}: {sheet}"]
        if title_lines:
            lines.append("")
            lines += [f"_{t}_" for t in title_lines if t]
        lines.append("\n" + L["rows"].format(a=first_row, b=last_row, n=len(body)) + ", ".join(names) + "\n")
        if style == "table":
            for k, row in enumerate(chunk):
                if k % 20 == 0:
                    lines.append("| " + " | ".join(names) + " |")
                    lines.append("|" + "---|" * len(names))
                row = row + [""] * (len(names) - len(row))
                lines.append("| " + " | ".join(row[:len(names)]) + " |")
                if k % 20 == 19:
                    lines.append("")
        else:
            for k, row in enumerate(chunk, start=first_row):
                row = row + [""] * (len(names) - len(row))
                cells = [f"{n}: {v}" for n, v in zip(names, row) if v]
                if cells:
                    lines.append(f"- [{file_label} / {sheet} / {L['row'].format(k=k)}] " + " | ".join(cells))
        parts.append((first_row, "\n".join(lines) + "\n"))
    return parts


def safe(s):
    return re.sub(r"[^\w\-. ]+", "_", s, flags=re.UNICODE).strip().replace(" ", "_")[:80]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("src")
    ap.add_argument("dst", nargs="?", default=None, help="thư mục đầu ra; bỏ trống = <src>_md cạnh thư mục gốc")
    ap.add_argument("--style", choices=["rows", "table"], default="rows")
    ap.add_argument("--max-rows", type=int, default=300, help="số dòng tối đa mỗi file .md")
    ap.add_argument("--lang", choices=list(LABELS), default="vi", help="ngôn ngữ nhãn/định dạng ngày: vi hoặc ja")
    a = ap.parse_args()
    global L
    L = LABELS[a.lang]

    # Windows: "D:\\TaiLieu\\" có dấu \\ cuối sẽ nuốt dấu nháy, làm dính cả tham số sau vào đường dẫn
    raw = a.src.strip().strip('"')
    src = Path(raw).expanduser().resolve()
    if not src.exists():
        sys.exit(f"Không tìm thấy thư mục: {src}\n"
                 "Gợi ý: đặt đường dẫn trong dấu nháy, KHÔNG để dấu \\ ở cuối (vd \"D:\\TaiLieu\"), "
                 "và kiểm tra chính tả/ổ đĩa.")
    if src.is_file():
        sys.exit(f"{src} là một file, hãy chỉ định THƯ MỤC chứa file Excel.")
    dst = Path(a.dst).resolve() if a.dst else src.parent / f"{src.name}_md"
    dst.mkdir(parents=True, exist_ok=True)
    files = sorted(p for p in src.rglob("*") if p.suffix.lower() in EXCEL_EXT | OTHER_EXT and not p.name.startswith("~$"))
    print(f"Đang quét: {src}")
    # liệt kê TẤT CẢ file trong thư mục gốc và mọi thư mục con, kèm trạng thái
    all_files = sorted(p for p in src.rglob("*") if p.is_file())
    todo = set(files)
    print(f"Tổng {len(all_files)} file trong cây thư mục:")
    for p in all_files:
        rel = p.relative_to(src).as_posix()
        if p in todo:
            tag = "[XỬ LÝ]  "
        elif p.name.startswith("~$"):
            tag = "[BỎ QUA] (file tạm của Excel)  "
        else:
            tag = "[BỎ QUA] (đuôi không hỗ trợ)  "
        print(f"  {tag}{rel}")
    print()
    if not files:
        from collections import Counter
        exts = Counter(p.suffix.lower() or "(không đuôi)" for p in src.rglob("*") if p.is_file())
        msg = f"Không thấy file Excel/CSV nào trong {src}\n"
        msg += ("Các loại file thực tế có trong thư mục: " + ", ".join(f"{e} ×{n}" for e, n in exts.most_common(10))
                if exts else "Thư mục trống (hoặc không có quyền đọc).")
        msg += f"\nĐang hỗ trợ: {', '.join(sorted(EXCEL_EXT | OTHER_EXT))}. (.xlsb, .ods chưa hỗ trợ: hãy Save As .xlsx)"
        sys.exit(msg)
    print(f"Tìm thấy {len(files)} file.")

    n_out = 0
    for idx, f in enumerate(files, 1):
        label = f.relative_to(src).as_posix()
        t0 = time.time()
        print(f"({idx}/{len(files)}) đang đọc {label} ({f.stat().st_size / 1e6:.1f} MB)...", flush=True)
        try:
            sheets = sheets_of(f)
        except Exception as e:  # file hỏng/có mật khẩu
            print(f"[BỎ QUA] {label}: {e}")
            continue
        for sheet, grid in sheets:
            res, body = split_header(grid)
            if not body:
                continue
            title_lines, names = res
            parts = render(label, sheet, title_lines, names, body, a.style, a.max_rows)
            for first_row, md in parts:
                suffix = f"_r{first_row}" if len(parts) > 1 else ""
                out_dir = dst / f.relative_to(src).parent  # giữ nguyên cấu trúc thư mục con
                out_dir.mkdir(parents=True, exist_ok=True)
                out = out_dir / f"{safe(f.stem)}__{safe(sheet)}{suffix}.md"
                out.write_text(md, encoding="utf-8")
                n_out += 1
        print(f"     [OK] {len(sheets)} sheet, {time.time() - t0:.1f}s", flush=True)
        del sheets
        gc.collect()
    print(f"\nXong: {n_out} file .md trong {dst}")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
48개 논문 .md 파일 파싱 → papers.json 생성
"""
import os, re, json

PAPERS_DIR = r"C:\Users\hsj04\Documents\SJ's vault\2. Study\a. 학위논문\윤제방 논문"
OUT_FILE   = r"C:\Users\hsj04\HR\papers.json"

# 파일명 패턴: (연도학위 저자명)제목.md
FNAME_RE = re.compile(r"\((\d{2})(석사|박사)\s+(.+?)\)")

def parse_frontmatter(text, fname):
    """첫 헤더/볼드 라인에서 저자/연도/학위/지도교수 추출"""
    meta = {}
    # 저자
    m = re.search(r"\*\*저자\*\*[:\s：]+([^\s|*\n]+)", text)
    if m: meta["author"] = m.group(1).strip()
    # 지도교수
    m = re.search(r"\*\*지도교수\*\*[:\s：|]+([^\s|*\n]+)", text)
    if m: meta["professor"] = m.group(1).strip()
    # 연도
    m = re.search(r"\*\*연도\*\*[:\s：|]+(\d{4})", text)
    if m: meta["year"] = int(m.group(1))
    # 학위(과정)
    m = re.search(r"\*\*(학위|과정)\*\*[:\s：|]+(석사|박사)", text)
    if m: meta["degree"] = m.group(2)

    # 파일명으로 보완
    fm = FNAME_RE.search(fname)
    if fm:
        yr2, deg, auth = fm.group(1), fm.group(2), fm.group(3)
        if "year" not in meta: meta["year"] = 2000 + int(yr2)
        if "degree" not in meta: meta["degree"] = deg
        if "author" not in meta: meta["author"] = auth
    return meta

def extract_section(text, *headers):
    """섹션 헤더 이후 다음 ## 까지의 텍스트 반환"""
    for h in headers:
        pattern = rf"##\s+.*{re.escape(h)}.*\n([\s\S]*?)(?=\n##\s|\Z)"
        m = re.search(pattern, text)
        if m:
            raw = m.group(1).strip()
            # 마크다운 제거 (볼드, 코드블록, 표, 링크)
            raw = re.sub(r"```[\s\S]*?```", "", raw)
            raw = re.sub(r"\|.*", "", raw)
            raw = re.sub(r"\*{1,2}([^*]+)\*{1,2}", r"\1", raw)
            raw = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", raw)
            raw = re.sub(r"\n{2,}", " ", raw).strip()
            return raw[:300]
    return ""

def extract_variables(text):
    """독립/매개/종속변수 추출 (연구모형 섹션 우선, 없으면 제목 파싱)"""
    iv, mv, dv = [], [], []

    # 연구모형/가설 섹션에서 명시적 변수 탐색
    model_m = re.search(r"##.*?(연구\s*모형|연구모형|Model).*?\n([\s\S]*?)(?=\n##\s|\Z)", text)
    model_txt = model_m.group(2) if model_m else text

    for line in model_txt.splitlines():
        line_c = line.strip()
        if re.search(r"\*\*독립변수\*\*|독립\s*변수\s*[：:]", line_c):
            parts = re.split(r"[：:]\s*", line_c, 1)
            if len(parts) > 1:
                iv += [v.strip().strip("*") for v in re.split(r"[,，/]", parts[1]) if v.strip()]
        elif re.search(r"\*\*매개변수\*\*|매개\s*변수\s*[：:]", line_c):
            parts = re.split(r"[：:]\s*", line_c, 1)
            if len(parts) > 1:
                mv += [v.strip().strip("*") for v in re.split(r"[,，/]", parts[1]) if v.strip()]
        elif re.search(r"\*\*종속변수\*\*|종속\s*변수\s*[：:]", line_c):
            parts = re.split(r"[：:]\s*", line_c, 1)
            if len(parts) > 1:
                dv += [v.strip().strip("*") for v in re.split(r"[,，/]", parts[1]) if v.strip()]

    return iv, mv, dv

def extract_title(text, fname):
    """H1 제목 추출"""
    m = re.search(r"^#\s+(.+)", text, re.MULTILINE)
    if m:
        t = m.group(1).strip()
        # 대괄호 접두어 제거
        t = re.sub(r"^\[.*?\]\s*", "", t)
        return t
    # 파일명에서
    clean = re.sub(r"^\(.*?\)\s*", "", os.path.splitext(fname)[0])
    return clean.strip()

def extract_hypotheses_summary(text):
    """가설 채택/기각 요약 (채택N개, 기각M개)"""
    adopted = len(re.findall(r"\*\*채택\*\*|채택(?!\w)", text))
    rejected = len(re.findall(r"\*\*기각\*\*|기각(?!\w)", text))
    if adopted or rejected:
        return f"가설 채택 {adopted}개" + (f", 기각 {rejected}개" if rejected else "")
    return ""

def build_keywords(title, iv, mv, dv, purpose):
    """검색용 키워드 집합 생성"""
    kws = set()
    # 제목 단어 (2글자 이상 한글)
    for w in re.findall(r"[가-힣]{2,}", title):
        kws.add(w)
    for lst in [iv, mv, dv]:
        for v in lst:
            for w in re.findall(r"[가-힣]{2,}", v):
                kws.add(w)
    for w in re.findall(r"[가-힣]{2,}", purpose[:200]):
        kws.add(w)
    # 불용어 제거
    stop = {"연구","관한","미치는","영향","관계","대한","위한","통해","에서","으로","이후","및","과","와","이","가","은","는","을","를","의","에","로","도","만","이란","이다","하다","있다"}
    return list(kws - stop)

def process_file(fpath):
    fname = os.path.basename(fpath)
    with open(fpath, encoding="utf-8") as f:
        text = f.read()

    meta   = parse_frontmatter(text, fname)
    title  = extract_title(text, fname)
    purpose= extract_section(text, "연구 목적", "목적", "Purpose")
    background = extract_section(text, "배경", "Background")
    iv, mv, dv = extract_variables(text)
    hypo_summary = extract_hypotheses_summary(text)
    keywords = build_keywords(title, iv, mv, dv, purpose)

    return {
        "id": re.sub(r"\s+", "_", os.path.splitext(fname)[0]),
        "title": title,
        "author": meta.get("author", ""),
        "degree": meta.get("degree", ""),
        "year": meta.get("year", 0),
        "professor": meta.get("professor", ""),
        "iv": iv,
        "mv": mv,
        "dv": dv,
        "purpose": purpose,
        "background": background,
        "hypo_summary": hypo_summary,
        "keywords": keywords,
    }

def main():
    files = sorted([
        os.path.join(PAPERS_DIR, f)
        for f in os.listdir(PAPERS_DIR)
        if f.endswith(".md")
    ])
    print(f"총 {len(files)}개 파일 처리 중...")
    papers = []
    for fp in files:
        try:
            papers.append(process_file(fp))
            print(f"  OK: {os.path.basename(fp)[:50]}")
        except Exception as e:
            print(f"  ERR: {os.path.basename(fp)} → {e}")

    with open(OUT_FILE, "w", encoding="utf-8") as f:
        json.dump(papers, f, ensure_ascii=False, indent=2)

    print(f"\n✓ {len(papers)}개 논문 → {OUT_FILE}")

if __name__ == "__main__":
    main()

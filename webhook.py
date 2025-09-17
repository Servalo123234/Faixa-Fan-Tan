
            f"ðŸ“£ <b>ENTRADA CONFIRMADA</b> â€” Jogada <b>{tag}</b>\n"
            f"Base: <code>{base}</code> â€¢ After: <code>{after}</code>\n"
            f"ðŸŽ¯ Nosso nÃºmero: <b>{suggested}</b>\n"
            f"ðŸ“ˆ Conf. curta={cs:.2f} â€¢ longa={cl:.2f} â€¢ tail={tail_len}\n"
            f"ðŸ”Ž PadrÃ£o: <code>{entry['pattern_key']}</code>"
        )
        await tg_send_text(TARGET_CHANNEL, txt)
        return {"ok": True, "opened": tag}

    return {"ok": True, "skipped": "nao_casou"}

# ===== Parsers auxiliares =====
PAREN_GROUP_RX = re.compile(r"\(([^)]*)\)")
ANY_14_RX      = re.compile(r"[1-4]")
def parse_close_numbers(text: str) -> List[int]:
    t = re.sub(r"\s+", " ", text)
    groups = PAREN_GROUP_RX.findall(t)
    if groups:
        nums = re.findall(r"[1-4]", groups[-1])
        return [int(x) for x in nums][:3]
    nums = ANY_14_RX.findall(t)
    return [int(x) for x in nums][:3]

def parse_candidates_and_pattern(t: str) -> Tuple[List[int], str]:
    KWOK_RX  = re.compile(r"\bKWOK\s*([1-4])\s*-\s*([1-4])", re.I)
    SSH_RX   = re.compile(r"\bSS?H\s*([1-4])(?:-([1-4]))?(?:-([1-4]))?(?:-([1-4]))?", re.I)
    ODD_RX   = re.compile(r"\bODD\b", re.I)
    EVEN_RX  = re.compile(r"\bEVEN\b", re.I)
    SEQ_RX   = re.compile(r"Sequ[eÃª]ncia:\s*([^\n\r]+)", re.I)
    m = KWOK_RX.search(t)
    if m:
        a,b = int(m.group(1)), int(m.group(2))
        base = sorted(list({a,b})); return base, f"KWOK-{a}-{b}"
    if ODD_RX.search(t): return [1,3], "ODD"
    if EVEN_RX.search(t): return [2,4], "EVEN"
    m = SSH_RX.search(t)
    if m:
        nums = [int(g) for g in m.groups() if g]
        base = sorted(list(dict.fromkeys(nums)))[:4]
        return base, "SSH-" + "-".join(str(x) for x in base) if base else "SSH"
    m = SEQ_RX.search(t)
    if m:
        parts = [int(x) for x in re.findall(r"[1-4]", m.group(1))]
        seen, base = set(), []
        for n in parts:
            if n not in seen:
                seen.add(n); base.append(n)
            if len(base) == 3: break
        if base: return base, "SEQ"
    return [1,2,3,4], "GEN"

def parse_entry_text(text: str) -> Optional[Dict]:
    ENTRY_RX = re.compile(r"ENTRADA\s+CONFIRMADA", re.I)
    t = re.sub(r"\s+", " ", text).strip()
    if not ENTRY_RX.search(t): return None
    base, pattern_key = parse_candidates_and_pattern(t)
    AFTER_RX = re.compile(r"ap[oÃ³]s\s+o\s+([1-4])", re.I)
    SEQ_RX   = re.compile(r"Sequ[eÃª]ncia:\s*([^\n\r]+)", re.I)
    mseq = SEQ_RX.search(t)
    seq = [int(x) for x in re.findall(r"[1-4]", mseq.group(1))] if mseq else []
    mafter = AFTER_RX.search(t)
    after_num = int(mafter.group(1)) if mafter else None
    return {"seq": seq, "after": after_num, "raw": t, "base": base, "pattern_key": pattern_key}
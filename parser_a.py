# parser_a.py
import re

def parse_week_text(text):
    """
    Simple parser that groups lines by detected day names (best-effort).
    Returns dict: { "Monday": [ {"meal_time":"Lunch","item":"Idli","quantity":3}, ...], ... }
    This is an example — replace with Student A's final logic if available.
    """
    lines = text.splitlines()
    DAYS = ["monday","tuesday","wednesday","thursday","friday","saturday","sunday",
            "mon","tue","wed","thu","fri","sat","sun",
            "തിങ്കൾ","ചൊവ്വ","ബുധൻ","വ്യാഴം","വെള്ളി","ശനി","ഞായർ"]
    MEALS = ["breakfast","lunch","dinner","prathal","ഉച്ചഭക്ഷണം","പ്രാതൽ","bf","b"]

    result = {}
    for raw in lines:
        line = raw.strip()
        if not line: 
            continue
        # find day
        day = None
        lw = line.lower()
        for d in DAYS:
            if d in lw:
                day = d.capitalize()
                break
        # find meal time
        meal_time = None
        for m in MEALS:
            if m in lw:
                meal_time = m.capitalize()
                break
        # quantity (last number)
        qty = None
        mnums = re.findall(r"[\(\{\[]?(\d+)[\)\}\]]?", line)
        if mnums:
            qty = int(mnums[-1])
        # item: remove leading number and day/meal labels roughly
        item = re.sub(r"^\d+\.\s*", "", line)   # remove numbering like "1."
        if day:
            item = re.sub(re.escape(day), "", item, flags=re.I).strip(" :-,")
        if meal_time:
            item = re.sub(re.escape(meal_time), "", item, flags=re.I).strip(" :-,")
        item = re.sub(r"[\(\{\[]\d+[\)\}\]]", "", item).strip()
        if not day:
            # put under 'Unsorted'
            day = "Unsorted"
        result.setdefault(day, []).append({
            "meal_time": meal_time or "",
            "item": item,
            "quantity": qty
        })
    return result

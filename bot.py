import os
import sys
import time
import json
import random
import requests
import argparse
from json import dumps as dp
from datetime import datetime
from colorama import *
from urllib.parse import parse_qs
from base64 import b64decode

init(autoreset=True)

merah = Fore.LIGHTRED_EX
putih = Fore.LIGHTWHITE_EX
hijau = Fore.LIGHTGREEN_EX
kuning = Fore.LIGHTYELLOW_EX
biru = Fore.LIGHTBLUE_EX
reset = Style.RESET_ALL
hitam = Fore.LIGHTBLACK_EX
magenta = Fore.LIGHTMAGENTA_EX


class BlumTod:
    def __init__(self):
        self.base_headers = {
            "accept": "application/json, text/plain, */*",
            "user-agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0',
            "content-type": "application/json",
            "origin": "https://telegram.blum.codes",
            "x-requested-with": "org.telegram.messenger",
            "sec-fetch-site": "same-site",
            "sec-fetch-mode": "cors",
            "sec-fetch-dest": "empty",
            # "Sec-Ch-Ua-Mobile": "?1",
            # "Sec-Ch-Ua-Platform": '"Android"',
            "referer": "https://telegram.blum.codes/",
            "accept-encoding": "gzip, deflate",
            "accept-language": "en,en-US;q=0.9",
        }
        self.garis = putih + "~" * 50

    def renew_access_token(self, tg_data):
        headers = self.base_headers.copy()
        data = dp(
            {
                "query": tg_data,
            },
        )
        headers["Content-Length"] = str(len(data))
        url = "https://user-domain.blum.codes/api/v1/auth/provider/PROVIDER_TELEGRAM_MINI_APP"
        time.sleep(3)
        try:
            res = self.http(url, headers, data)
            token = res.json().get("token")
            if token is None:
                self.log(f"{merah}'token' not found, please insert it into data.txt !!!")
                return 0

            access_token = token.get("access")

            return access_token
        except (requests.exceptions.JSONDecodeError, json.decoder.JSONDecodeError):
            self.log(f"{merah}Error reading the response, retrying")

    def solve(self, task: dict, access_token):
        headers = self.base_headers.copy()
        headers["authorization"] = f"Bearer {access_token}"
        ignore_tasks = [
            "39391eb2-f031-4954-bd8a-e7aecbb1f192",  # wallet connect
            "d3716390-ce5b-4c26-b82e-e45ea7eba258",  # invite task
            "f382ec3f-089d-46de-b921-b92adfd3327a",  # invite task
            "220ee7b1-cca4-4af8-838a-2001cb42b813",  # invite task
            "5ecf9c15-d477-420b-badf-058537489524",  # invite task
            "c4e04f2e-bbf5-4e31-917b-8bfa7c4aa3aa",  # invite task
        ]
        task_id = task.get("id")
        task_title = task.get("title")
        task_status = task.get("status")
        task_prog = task.get('type')
        start_task_url = f"https://earn-domain.blum.codes/api/v1/tasks/{task_id}/start"
        claim_task_url = f"https://earn-domain.blum.codes/api/v1/tasks/{task_id}/claim"
        validate_task_url = f"https://earn-domain.blum.codes/api/v1/tasks/{task_id}/validate"
        if task_id in ignore_tasks:
            return
        if task_status == "READY_FOR_CLAIM":
            try:
                time.sleep(3)
                _res = self.http(claim_task_url, headers, "")

                _status = _res.json().get("status")

                if _status == "FINISHED":
                    self.log(
                        f"{hijau}Completed task {putih}{task_title} "
                    )
                    return
            except (requests.exceptions.JSONDecodeError, json.decoder.JSONDecodeError):
                self.log(f"{merah}Error reading the response, retrying")
                return

        if task_status == "NOT_STARTED" and task_prog != "PROGRESS_TARGET":
            try:
                time.sleep(3)
                _res = self.http(start_task_url, headers, "")

                _status = _res.json().get("status")
                if _status == "STARTED":
                    time.sleep(3)
                    _res = self.http(claim_task_url, headers, "")
                    _status = _res.json().get("status")
                    if _status == "FINISHED":
                        self.log(
                            f"{hijau}Completed task {putih}{task_title} "
                        )
                        return
            except (requests.exceptions.JSONDecodeError, json.decoder.JSONDecodeError):
                self.log(f"{merah}Error reading the response, retrying")
                return

        if task_status == "READY_FOR_VERIFY" and task['validationType'] == 'KEYWORD':
            try:
                keywords = {
                    		"How to Analyze Crypto?": "VALUE",
                            "Forks Explained": "GO GET",
                            "Secure your Crypto!": "BEST PROJECT EVER",
                            "Navigating Crypto": "HEYBLUM",
                            "What are Telegram Mini Apps?": "CRYPTOBLUM",
                            "Say No to Rug Pull!": "SUPERBLUM",
                            "Liquidity Pools Guide": "BLUMERSSS",
                            "What Are AMMs?": "CRYPTOSMART",
                            "$2.5M+ DOGS Airdrop": "HAPPYDOGS",
                            "Doxxing? What's that?": "NODOXXING",
                            "Pre-Market Trading?": "WOWBLUM",
                            "Play track \u0026 type track name": "Blum - Big City Life",
                            "How to Memecoin?": "MEMEBLUM",
                            "Token Burning: How & Why?": "ONFIRE",
                            "Bitcoin Rainbow Chart?": "SOBLUM",
                            "Crypto Terms. Part 1": "BLUMEXPLORER"
                }

                payload = {'keyword': keywords.get(task_title)}
                time.sleep(3)
                _res = self.ses.post(validate_task_url, json=payload, headers=headers, timeout=30)
                _status = _res.json().get("status")

                if _status == "READY_FOR_CLAIM":
                    time.sleep(3)
                    _res1 = self.http(claim_task_url, headers, "")
                    _status1 = _res1.json().get("status")
                    if _status1 == "FINISHED":
                        self.log(
                            f"{hijau}Completed task {putih}{task_title} ")
                        return
            except (requests.exceptions.JSONDecodeError, json.decoder.JSONDecodeError):
                self.log(f"{merah}Error reading the response, retrying")
                return








    def solve_task(self, access_token):
        url_task = "https://earn-domain.blum.codes/api/v1/tasks"
        headers = self.base_headers.copy()
        headers["Authorization"] = f"Bearer {access_token}"

        try:
            time.sleep(3)
            res = self.http(url_task, headers)
            self.log(
                f"{hijau}Checking tasks "
            )
            restask = res.json()

        except (requests.exceptions.JSONDecodeError, json.decoder.JSONDecodeError):
            self.log(f"{merah}Error reading the response, retrying")
            return

        for tasks in restask:
            if isinstance(tasks, str):
                self.log(f"{kuning}Error retrieving task list")
                return
            for k in list(tasks.keys()):
                if k != "tasks" and k != "subSections":
                    continue
                for t in tasks.get(k):
                    if isinstance(t, dict):
                        subtasks = t.get("subTasks")
                        if subtasks is not None:
                            for task in subtasks:
                                self.solve(task, access_token)
                            self.solve(t, access_token)
                            continue
                        tasks_list = t.get("tasks")
                        if not tasks_list:
                            continue
                        for task in tasks_list:
                            self.solve(task, access_token)




    def set_proxy(self, proxy=None):
        self.ses = requests.Session()
        if proxy is not None:
            self.ses.proxies.update({"http": proxy, "https": proxy})

    def claim_farming(self, access_token):
        url = "https://game-domain.blum.codes/api/v1/farming/claim"
        headers = self.base_headers.copy()
        headers["Authorization"] = f"Bearer {access_token}"
        try:
            time.sleep(3)
            res = self.http(url, headers, "")
            balance = res.json().get("availableBalance", 0)
            self.log(f"{hijau}Balance after claiming: {putih}{balance}")
            return

        except (requests.exceptions.JSONDecodeError, json.decoder.JSONDecodeError):
            self.log(f"{merah}Error reading the response, retrying")

            return
    def get_balance(self, access_token, only_show_balance=False):
        url = "https://game-domain.blum.codes/api/v1/user/balance"
        headers = self.base_headers.copy()
        headers["Authorization"] = f"Bearer {access_token}"
        try:
            while True:
                time.sleep(3)
                res = self.http(url, headers)
                balance = res.json().get("availableBalance", 0)
                self.log(f"{hijau}Balance : {putih}{balance}")
                if only_show_balance:
                    return
                timestamp = res.json().get("timestamp")
                if timestamp is None:
                    self.countdown(3)
                    continue
                timestamp = round(timestamp / 1000)
                if "farming" not in res.json().keys():
                    return False, "not_started"
                end_farming = res.json().get("farming", {}).get("endTime")
                if end_farming is None:
                    self.countdown(3)
                    continue
                break
            end_farming = round(end_farming / 1000)
            if timestamp > end_farming:
                self.log(f"{hijau}It's time to claim")
                return True, end_farming

            self.log(f"{kuning}It's not time to claim yet")
            end_date = datetime.fromtimestamp(end_farming)
            self.log(f"{hijau}End of farming: {putih}{end_date}")
            return False, end_farming

        except (requests.exceptions.JSONDecodeError, json.decoder.JSONDecodeError):
            self.log(f"{merah}Error reading the response, retrying")

            return
    def start_farming(self, access_token):
        url = "https://game-domain.blum.codes/api/v1/farming/start"
        headers = self.base_headers.copy()
        headers["Authorization"] = f"Bearer {access_token}"
        try:
            while True:
                time.sleep(3)
                res = self.http(url, headers, "")
                end = res.json().get("endTime")
                if end is None:
                    self.countdown(3)
                    continue
                break

            end_date = datetime.fromtimestamp(end / 1000)
            self.log(f"{hijau}Farming started")
            self.log(f"{hijau}End of farming: {putih}{end_date}")
            return round(end / 1000)
        except (requests.exceptions.JSONDecodeError, json.decoder.JSONDecodeError):
            self.log(f"{merah}Error reading the response, retrying")

            return
    def get_friend(self, access_token):
        url = "https://user-domain.blum.codes/api/v1/friends/balance"
        headers = self.base_headers.copy()
        headers["Authorization"] = f"Bearer {access_token}"
        try:
            time.sleep(3)
            res = self.http(url, headers)
            can_claim = res.json().get("canClaim", False)

            if can_claim:
                url_claim = "https://user-domain.blum.codes/api/v1/friends/claim"
                time.sleep(3)
                res = self.http(url_claim, headers, "")
                if res.json().get("claimBalance") is not None:
                    self.log(f"{hijau}Referral claimed successfully")
                    return
                self.log(f"{merah}Error claiming referral")
                return

        except (requests.exceptions.JSONDecodeError, json.decoder.JSONDecodeError):
            self.log(f"{merah}Error reading the response, retrying")
            return

    def checkin(self, access_token):
        url = "https://game-domain.blum.codes/api/v1/daily-reward?offset=-420"
        headers = self.base_headers.copy()
        headers["Authorization"] = f"Bearer {access_token}"
        try:
            time.sleep(3)
            res = self.http(url, headers)
            if res.status_code == 404:
                self.log(f"{kuning}Already checked in today")
                return
            res = self.http(url, headers, "")
            if "ok" in res.text.lower():
                self.log(f"{hijau}Checked in successfully")
                return

            self.log(f"{merah}Check-in error")
            return

        except (requests.exceptions.JSONDecodeError, json.decoder.JSONDecodeError):
            self.log(f"{merah}Error reading the response, retrying")
            return

    def playgame(self, access_token):
        url_play = "https://game-domain.blum.codes/api/v1/game/play"
        url_claim = "https://game-domain.blum.codes/api/v1/game/claim"
        url_balance = "https://game-domain.blum.codes/api/v1/user/balance"
        headers = self.base_headers.copy()
        headers["Authorization"] = f"Bearer {access_token}"
        try:
            while True:
                time.sleep(3)
                res = self.http(url_balance, headers)
                play = res.json().get("playPasses")
                if play is None:
                    self.log(f"{kuning}Error retrieving the number of tickets")
                    break
                self.log(f"{hijau}Tickets: {putih}{play}{hijau} pcs")
                if play <= 0:
                    return
                for i in range(play):
                    if self.is_expired(access_token):
                        return True
                    time.sleep(3)
                    res = self.http(url_play, headers, "")
                    game_id = res.json().get("gameId")
                    if game_id is None:
                        message = res.json().get("message", "")
                        if message == "cannot start game":
                            self.log(
                                f"{kuning}{message}, I'll try again later"
                            )
                            return False
                        self.log(f"{kuning}{message}")
                        continue
                    while True:
                        self.countdown(30)
                        point = random.randint(self.MIN_WIN, self.MAX_WIN)
                        data = json.dumps({"gameId": game_id, "points": point})
                        time.sleep(3)
                        res = self.http(url_claim, headers, data)
                        if "OK" in res.text:
                            self.log(
                                f"{hijau}Received {putih}{point}{hijau} From the game "
                            )

                            break

                        message = res.json().get("message", "")
                        if message == "game session not finished":
                            continue

                        self.log(f"{merah}Error receiving {putih}{point}{merah} from the game ")
                        break

        except (requests.exceptions.JSONDecodeError, json.decoder.JSONDecodeError):
            self.log(f"{merah}Error reading the response, retrying")
            return

    def dogs(self, access_token):
        url = "https://game-domain.blum.codes/api/v2/game/eligibility/dogs_drop"
        headers = self.base_headers.copy()
        headers["Authorization"] = f"Bearer {access_token}"
        try:
            time.sleep(3)
            res = self.http(url, headers)
            dogs_drop = res.json()
            if dogs_drop['eligible']:
                self.log(f"{hijau}Eligible dogs drop")
                return
            else:
                self.log(f"{merah}NOT eligible dogs drop")
                return

            self.log(f"{merah}Error checking eligible dogs drop")
            return

        except (requests.exceptions.JSONDecodeError, json.decoder.JSONDecodeError):
            self.log(f"{merah}Error reading the response, retrying")
            return

    
    def data_parsing(self, data):
        return {k: v[0] for k, v in parse_qs(data).items()}

    def log(self, message):
        now = datetime.now().isoformat(" ").split(".")[0]
        print(f"{hitam}[{now}]{reset} {message}")

    def get_local_token(self, userid):
        if not os.path.exists("tokens.json"):
            open("tokens.json", "w").write(json.dumps({}))
        tokens = json.loads(open("tokens.json", "r").read())
        if str(userid) not in tokens.keys():
            return False

        return tokens[str(userid)]

    def save_local_token(self, userid, token):
        tokens = json.loads(open("tokens.json", "r").read())
        tokens[str(userid)] = token
        open("tokens.json", "w").write(json.dumps(tokens, indent=4))

    def is_expired(self, token):
        if token is None or isinstance(token, bool):
            return True
        header, payload, sign = token.split(".")
        payload = b64decode(payload + "==").decode()
        jload = json.loads(payload)
        now = round(datetime.now().timestamp()) + 300
        exp = jload["exp"]
        if now > exp:
            return True

        return False

    def save_failed_token(self, userid, data):
        file = "auth_failed.json"
        if not os.path.exists(file):
            open(file, "w").write(json.dumps({}))

        acc = json.loads(open(file, "r").read())
        if str(userid) in acc.keys():
            return

        acc[str(userid)] = data
        open(file, "w").write(json.dumps(acc, indent=4))

    def load_config(self):
        try:

            self.AUTOGAME = input(f"{magenta}Play The Game? {putih}(1 - Yes, 2 - No)\n")
            self.DEFAULT_INTERVAL = int(input(f"{magenta}Break between accounts in seconds: \n"))
            if self.AUTOGAME == '1':
                self.MIN_WIN = int(input(f"{magenta}Enter the minimum score from the game: \n"))
                self.MAX_WIN = int(input(f"{magenta}Enter the maximum score from the game: \n"))

                if self.MIN_WIN > self.MAX_WIN:
                    self.log(f"{kuning}The maximum game score must be higher than the minimum.")
                    sys.exit()

        except ValueError:
            self.log(f"{merah}Input error. Make sure to enter numerical values where required.")
            sys.exit()

    def ipinfo(self):
        res = self.http("https://ipinfo.io/json", {"content-type": "application/json"})
        if res is False:
            return False
        if res.status_code != 200:
            self.log(f"{merah}failed fetch ipinfo !")
            return False
        city = res.json().get("city")
        country = res.json().get("country")

        self.log(
            f"{biru}Proxy Cek: {hijau}Сountry : {putih}{country} {hijau}City : {putih}{city}"
        )
        return True

    def http(self, url, headers, data=None):
        while True:
            try:

                if data is None:
                    res = self.ses.get(url, headers=headers, timeout=30)
                elif data == "":
                    res = self.ses.post(url, headers=headers, timeout=30)
                else:
                    res = self.ses.post(url, headers=headers, data=data, timeout=30)

                return res

            except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
                self.log(f"{merah}Connection error/connection timeout, check the proxy!")

            except requests.exceptions.ProxyError:
                self.log(f"{merah}Proxy error, check the format")
                return False


            except (requests.exceptions.JSONDecodeError, json.decoder.JSONDecodeError):
                self.log(f"{merah}Error reading the response, retrying")


    def countdown(self, t):
        while t:
            menit, detik = divmod(t, 60)
            jam, menit = divmod(menit, 60)
            jam = str(jam).zfill(2)
            menit = str(menit).zfill(2)
            detik = str(detik).zfill(2)
            print(f"{putih}Sabar cok {jam}:{menit}:{detik} ", flush=True, end="\r")
            t -= 1
            time.sleep(1)
        print("                          ", flush=True, end="\r")

    def main(self):

        arg = argparse.ArgumentParser()

        arg.add_argument(
            "--data", help="Custom data input (default: data.txt)", default="data.txt"
        )
        arg.add_argument(
            "--proxy",
            help="custom proxy file input (default: proxies.txt)",
            default="proxies.txt",
        )
        args = arg.parse_args()

        if not os.path.exists(args.data):
            self.log(f"{merah}{args.data} not found,Please Enter The Correct File Name!")
            sys.exit()

        datas = [i for i in open(args.data, "r").read().splitlines() if len(i) > 0]
        proxies = [i for i in open(args.proxy).read().splitlines() if len(i) > 0]
        use_proxy = True if len(proxies) > 0 else False
        self.log(f"{hijau}Total Account : {putih}{len(datas)}")
        self.log(f"{biru}Use Proxy : {putih}{use_proxy}")
        if len(datas) <= 0:
            self.log(f"{merah}Please Add key to {args.data} First")
            sys.exit()
        print(self.garis)
        while True:
            list_countdown = []
            for no, data in enumerate(datas):
                self.log(f"{hijau}Account Number - {putih}{no + 1}")
                data_parse = self.data_parsing(data)
                user = json.loads(data_parse["user"])
                userid = user["id"]
                self.log(f"{hijau}Account : {putih}{user['first_name']}")
                if use_proxy:
                    proxy = proxies[no % len(proxies)]
                self.set_proxy(proxy if use_proxy else None)
                self.ipinfo() if use_proxy else None
                access_token = self.get_local_token(userid)
                failed_fetch_token = False
                while True:
                    if not access_token:
                        access_token = self.renew_access_token(data)
                        if not access_token:
                            self.save_failed_token(userid, data)
                            failed_fetch_token = True
                            break
                        self.save_local_token(userid, access_token)
                    expired = self.is_expired(access_token)
                    if expired:
                        access_token = False
                        continue
                    break
                if failed_fetch_token:
                    continue
                self.dogs(access_token)
                self.checkin(access_token)
                self.get_friend(access_token)
                self.solve_task(access_token)
                status, res_bal = self.get_balance(access_token)
                if status:
                    self.claim_farming(access_token)
                    self.start_farming(access_token)
                if isinstance(res_bal, str):
                    self.start_farming(access_token)
                if self.AUTOGAME == '1':
                    while True:
                        result = self.playgame(access_token)
                        if result:
                            access_token = self.renew_access_token(data)
                            self.save_local_token(userid, access_token)
                            continue
                        break
                print(self.garis)
                self.countdown(self.DEFAULT_INTERVAL)


            self.countdown(3650*8)


if __name__ == "__main__":
    try:
        app = BlumTod()
        app.load_config()
        app.main()
    except KeyboardInterrupt:
        sys.exit()

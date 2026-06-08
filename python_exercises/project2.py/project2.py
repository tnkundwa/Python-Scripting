import smtplib
import os
from dotenv import load_dotenv
from email.mime.text import MIMEText
from concurrent.futures import ThreadPoolExecutor
import requests
import json
from pathlib import Path
import time
import os

load_dotenv()

def load_servers():
    env_servers = os.environ.get("SERVERS")

    if env_servers:
        servers = [url.strip() for url in env_servers.split(",") if url.strip()]
        print(f"Loaded {len(servers)} servers from Environment Variable.")
        return servers

    config_path = "../health_checker.log"
    if os.path.exists(config_path):
        try:
            with open(config_path, "r") as file:
                content = json.load(file)
                servers = content.get("servers", [])
                print(f"Loaded {len(servers)} servers")
                return servers
        except FileNotFoundError:
            print("Error: No server configuration found!")
            print("Please set the SERVERS environment variable or create the config file.")
            return []


def check_server(url):
    max_attempts = 3

    for attempt in range(max_attempts):
        result = {
            "url": url,
            "status_code": None,
            "elapsed_ms": 0,
            "json_status": None,
            "error": None,
        }

        try:
            start_time = time.perf_counter()

            response = requests.get(url, timeout=5)

            end_time = time.perf_counter()
            result["elapsed_ms"] = round((end_time - start_time) * 1000)
            result["status_code"] = response.status_code

            try:
                data = response.json()
                result["json_status"] = data.get("status")
            except ValueError:
                result["json_status"] = None 

            if 200 <= response.status_code <= 299:
                return result

            print(f"[Attempt {attempt + 1}/{max_attempts}] {url} returned {response.status_code}. Retrying...")

        except requests.exceptions.RequestException as e:
            result["error"] = "TIMEOUT/FAILED"

        if attempt < max_attempts - 1:
            time.sleep(1)

    return result


def send_email_alert(failed_urls):

    sender_email = "toussaintnkundwa@gmail.com"
    receiver_email = "tnkundwa@gmail.com"
    password = os.getenv("EMAIL_PASSWORD")

    body = (
        f"Alert! The following services are currently down:\n\n"
        + "\n".join(failed_urls)
    )

    msg = MIMEText(body)
    msg["Subject"] = "SERVER OUTAGE ALERT!!!"
    msg["From"] = sender_email
    msg["To"] = receiver_email

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, msg.as_string())
        print("\n Alert email sent successfully to the admin team!")
    except Exception as e:
        print(f"\n Failed to send email alert: {e}")

def check_all_servers():

    servers = load_servers()
    if not servers:
        return
    
    failed_services = []

    with ThreadPoolExecutor(max_workers=5) as executor:

        results = executor.map(check_server, servers)

        for report in results:
            url = report["url"]
            status_code = report["status_code"]
            elapsed = report["elapsed_ms"]

            if report["error"]:
                status_text = "TIMEOUT"
                failed_services.append(url)
            elif status_code and 200 <= status_code <= 299:
                status_text = f"OK ({status_code})"
            else:
                status_text = f"DOWN ({status_code})"
                failed_services.append(url)

            slow_flag = (" [slow]" if elapsed > 500 and not report["error"] else "")

            if report["json_status"] == "ok":
                print(f"-> {url} is truly healthy via JSON!")

            if report["error"]:
                print(f"{url} — {status_text}")
            else:
                print(f"{url} — {status_text} — {elapsed}ms{slow_flag}")

        if failed_services:
            print(f"Failed services: {', '.join(failed_services)}")
        else:
            print("All services are healthy!")
        if failed_services:
            print(f"Failed services: {', '.join(failed_services)}")

            print("Triggering emergency alert...")
            send_email_alert(failed_services)
        else:
            print("All services are healthy!")


if __name__ == "__main__":
    check_all_servers()
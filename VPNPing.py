import ping3
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import json

try:
    with open("config.json") as config_file:
        config = json.load(config_file)
except (FileNotFoundError, json.JSONDecodeError) as e:
    print(f"Error loading config.json: {e}")
    exit(1)

sender_email = config["sender_email"]
receiver_email = config["receiver_email"]
smtp_server = config["smtp_server"]
smtp_port = config["smtp_port"]
smtp_username = config["smtp_username"]
smtp_password = config["smtp_password"]

global email_counter, last_email_time
email_counter = 0
last_email_time = 0

def send_email_notification(target_ip):
    global email_counter, last_email_time
    subject = f"Device {target_ip} is not reachable!"
    body = f"The device with IP address {target_ip} is not reachable through the VPN."

    current_time = time.time()
    time_limit = 12 * 60 * 60 if email_counter < 5 else 24 * 60 * 60

    if current_time - last_email_time >= time_limit:
        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = receiver_email
        message["Subject"] = subject
        message.attach(MIMEText(body, "plain"))

        try:
            smtp_obj = smtplib.SMTP(smtp_server, smtp_port)
            smtp_obj.starttls()
            smtp_obj.login(smtp_username, smtp_password)
            smtp_obj.sendmail(sender_email, receiver_email, message.as_string())
            smtp_obj.quit()

            last_email_time = current_time
            email_counter += 1
            print("Email notification sent successfully!")
        except smtplib.SMTPException as e:
            print(f"Failed to send email notification: {e}")
    else:
        print("Not sending email: Time limit not reached.")

def send_test_email():
    subject = "Test Email"
    body = "This is a test email sent by the script."

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    try:
        smtp_obj = smtplib.SMTP(smtp_server, smtp_port)
        smtp_obj.starttls()
        smtp_obj.login(smtp_username, smtp_password)
        smtp_obj.sendmail(sender_email, receiver_email, message.as_string())
        smtp_obj.quit()
        print("Test email sent successfully!")
    except smtplib.SMTPException as e:
        print(f"Failed to send test email: {e}")

def ping_device_on_vpn(target_ip):
    global last_email_time, email_counter
    while True:
        try:
            response_time = ping3.ping(target_ip, timeout=2)
            if response_time is not None:
                if last_email_time == 0:
                    print("Initial successful ping after sending initial test email")
                    last_email_time = time.time()

                print(f"Received response from {target_ip} in {response_time:.2f} ms")
                last_email_time = 0
                email_counter = 0
            else:
                print(f"No response from {target_ip}")
                send_email_notification(target_ip)
        except ping3.exceptions.Timeout:
            print(f"Timeout: No response from {target_ip}")
            send_email_notification(target_ip)
        except Exception as e:
            print(f"Error while pinging {target_ip}: {e}")

        time.sleep(60)

if __name__ == "__main__":
    target_ip = "192.168.1.1"

    print("Sending initial test email and beginning device monitoring...")
    send_test_email()
    ping_device_on_vpn(target_ip)

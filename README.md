# VPN Device Monitoring and Email Notification Script

## Description
This Python script monitors the reachability of a specific device using its IP address over a VPN connection and sends email notifications when the device becomes unreachable or experiences connectivity issues. It includes mechanisms to control the frequency of email notifications to prevent spamming.

## Features
- Continuously pings a specified target IP address over a VPN connection.
- Sends an initial test email to verify email sending functionality.
- Sends email notifications when the target device becomes unreachable or experiences connectivity issues.
- Limits the frequency of email notifications to prevent excessive emails within certain time intervals.
- Uses a configuration file (`config.json`) to store email and SMTP server settings.

## Usage
1. Ensure that the required Python libraries (`ping3`, `smtplib`, `email.mime`) are installed.
2. Create a configuration file named `config.json` with the necessary email and SMTP server settings.
3. Set the `target_ip` variable to the IP address of the device you want to monitor.
4. Run the script, which will send an initial test email and start monitoring the target device's connectivity.

### Example Configuration (`config.json`):
```json
{
  "sender_email": "your_email@gmail.com",
  "receiver_email": "recipient_email@example.com",
  "smtp_server": "smtp.example.com",
  "smtp_port": 587,
  "smtp_username": "your_username",
  "smtp_password": "your_password"
}
```

import smtplib

EMAIL = "nonsowisdom62@gmail.com"
PASSWORD = "cpdlwqqmlztmiruo"

print("About to run...")

try:
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(EMAIL, PASSWORD)
    print("✅ Login successful")
    server.quit()
except Exception as e:
    print("❌ Error:", e)

import os
import qrcode
from django.core.management.base import BaseCommand
from dotenv import load_dotenv

class Command(BaseCommand):
    help = "Generate a QR code with admin credentials, GitHub URL, and Vercel production URL"

    def handle(self, *args, **kwargs):
        load_dotenv()
        admin_password = os.getenv("ADMIN_PASSWORD", "Not Set")
        github_url = os.getenv("GITHUB_URL", "Not Set")
        vercel_url = os.getenv("VERCEL_DOMAIN", "Not Set")
        qr_data = f"""
        🔑 Admin Password: {admin_password}
        🔗 GitHub Repo: {github_url}
        🚀 Vercel Production URL: {vercel_url}
        """

        # Generate QR code
        qr = qrcode.make(qr_data)

        # Save the QR code as an image
        output_path = "admin_qr_code.png"
        qr.save(output_path)

        self.stdout.write(self.style.SUCCESS(f"✅ QR Code saved as '{output_path}'"))

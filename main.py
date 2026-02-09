import flet as ft
from datetime import datetime
import json
import os

class BarcodeScanner:
    def __init__(self, page: ft.Page):
        self.page = page
        self.scans = []
        self.data_file = "scans.json"
        self.scanning = False
        self.load_scans()
        self.setup_ui()
    
    def load_scans(self):
        """Load previous scans from file"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as f:
                    self.scans = json.load(f)
            except:
                self.scans = []
    
    def save_scans(self):
        """Save scans to file"""
        with open(self.data_file, 'w') as f:
            json.dump(self.scans, f, indent=2)
    
    def add_scan(self, barcode_data):
        """Add a new scan with timestamp"""
        if not barcode_data or not barcode_data.strip():
            return
        
        scan_entry = {
            "barcode": barcode_data,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        self.scans.append(scan_entry)
        self.save_scans()
        self.update_list()
        self.update_status(f"✓ Scanned: {barcode_data}")
        self.page.update()
    
    def delete_scan(self, index):
        """Delete a scan entry"""
        if 0 <= index < len(self.scans):
            self.scans.pop(index)
            self.save_scans()
            self.update_list()
    
    def clear_all(self):
        """Clear all scans"""
        self.scans = []
        self.save_scans()
        self.update_list()
        self.update_status("All scans cleared")
    
    def toggle_scan(self, e):
        """Toggle scanning mode"""
        self.scanning = not self.scanning
        if self.scanning:
            self.scan_btn.text = "Stop Scanning"
            self.scan_btn.bgcolor = ft.Colors.RED
            self.update_status("📷 Scanning active - point at barcode")
        else:
            self.scan_btn.text = "Start Scanning"
            self.scan_btn.bgcolor = ft.Colors.GREEN
            self.update_status("Ready")
        self.page.update()
    
    def update_status(self, message):
        """Update status message"""
        self.status_text.value = message
        self.page.update()
    
    def update_list(self):
        """Update the display list"""
        self.scan_list.controls.clear()
        
        if not self.scans:
            self.scan_list.controls.append(
                ft.Text("No scans yet", size=14, color=ft.Colors.GREY)
            )
        else:
            for i, scan in enumerate(reversed(self.scans)):
                idx = len(self.scans) - 1 - i
                self.scan_list.controls.append(
                    ft.Container(
                        content=ft.Row(
                            [
                                ft.Column(
                                    [
                                        ft.Text(scan["barcode"], size=14, weight=ft.FontWeight.BOLD),
                                        ft.Text(scan["timestamp"], size=12, color=ft.Colors.GREY)
                                    ],
                                    expand=True
                                ),
                                ft.IconButton(
                                    ft.Icons.DELETE,
                                    icon_color=ft.Colors.RED,
                                    on_click=lambda e, idx=idx: self.delete_scan(idx)
                                )
                            ]
                        ),
                        padding=10,
                        border=ft.border.all(1, ft.Colors.GREY_300),
                        border_radius=5,
                        margin=ft.margin.symmetric(vertical=5)
                    )
                )
        
        self.page.update()
    
    def setup_ui(self):
        """Setup the user interface"""
        self.page.title = "Barcode Scanner"
        self.page.vertical_alignment = ft.MainAxisAlignment.START
        self.page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        
        # Status text
        self.status_text = ft.Text(
            "Ready",
            size=14,
            color=ft.Colors.BLUE,
            weight=ft.FontWeight.BOLD
        )
        
        # Start/Stop button
        self.scan_btn = ft.Button(
            "Start Scanning",
            on_click=self.toggle_scan,
            bgcolor=ft.Colors.GREEN,
            color=ft.Colors.WHITE,
            width=200,
            height=60
        )
        
        # Camera view placeholder (will show live camera on Android)
        camera_view = ft.Container(
            content=ft.Text(
                "📷\nCamera View",
                size=20,
                color=ft.Colors.WHITE,
                text_align=ft.TextAlign.CENTER,
                weight=ft.FontWeight.BOLD
            ),
            height=250,
            bgcolor=ft.Colors.BLACK_87,
            border_radius=10,
            width=350,
            margin=ft.margin.symmetric(vertical=10)
        )
        
        # Clear button
        clear_btn = ft.Button(
            "Clear All",
            on_click=lambda e: self.clear_all(),
            bgcolor=ft.Colors.RED,
            color=ft.Colors.WHITE,
            width=200
        )
        
        # Scan list
        self.scan_list = ft.Column(
            scroll=ft.ScrollMode.AUTO,
            expand=True,
            width=350
        )
        
        # Layout
        self.page.add(
            ft.Column(
                [
                    ft.Text("Barcode Scanner", size=28, weight=ft.FontWeight.BOLD),
                    ft.Divider(),
                    self.status_text,
                    ft.Container(height=10),
                    self.scan_btn,
                    ft.Container(height=10),
                    camera_view,
                    ft.Container(height=10),
                    ft.Text(f"Total Scans: {len(self.scans)}", size=12, color=ft.Colors.GREY),
                    ft.Divider(),
                    ft.Text("Scan History", size=16, weight=ft.FontWeight.BOLD),
                    self.scan_list,
                    ft.Container(height=10),
                    clear_btn
                ],
                expand=True,
                spacing=5,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            )
        )
        
        self.update_list()

def main(page: ft.Page):
    BarcodeScanner(page)

if __name__ == "__main__":
    ft.app(target=main)

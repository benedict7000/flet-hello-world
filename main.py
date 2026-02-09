import flet as ft
from datetime import datetime
import json
import os

try:
    from flet_camera import Camera
    CAMERA_AVAILABLE = True
except ImportError:
    CAMERA_AVAILABLE = False

class BarcodeScanner:
    def __init__(self, page: ft.Page):
        self.page = page
        self.scans = []
        self.data_file = "scans.json"
        self.camera = None
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
    
    def on_barcode_detected(self, barcode_data):
        """Handle barcode detection from camera"""
        if not barcode_data or not barcode_data.strip():
            return
        
        scan_entry = {
            "barcode": barcode_data,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        self.scans.append(scan_entry)
        self.save_scans()
        self.update_list()
        self.update_status(f"Scanned: {barcode_data}")
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
        
        # Status text
        self.status_text = ft.Text(
            "Ready to scan",
            size=12,
            color=ft.Colors.BLUE
        )
        
        # Camera view (if available)
        if CAMERA_AVAILABLE:
            self.camera = Camera(
                on_barcode_detected=self.on_barcode_detected
            )
            camera_container = ft.Container(
                content=self.camera,
                height=400,
                border_radius=10,
                margin=ft.margin.symmetric(vertical=10)
            )
        else:
            camera_container = ft.Container(
                content=ft.Text(
                    "Camera not available\nPlease install flet-camera",
                    size=14,
                    color=ft.Colors.RED,
                    text_align=ft.TextAlign.CENTER
                ),
                height=400,
                bgcolor=ft.Colors.GREY_200,
                border_radius=10,
                alignment=ft.alignment.center,
                margin=ft.margin.symmetric(vertical=10)
            )
        
        # Clear button
        clear_btn = ft.Button(
            "Clear All Scans",
            on_click=lambda e: self.clear_all(),
            style=ft.ButtonStyle(color=ft.Colors.RED)
        )
        
        # Scan list
        self.scan_list = ft.Column(
            scroll=ft.ScrollMode.AUTO,
            expand=True
        )
        
        # Layout
        self.page.add(
            ft.Container(
                content=ft.Column(
                    [
                        ft.Text("Barcode Scanner", size=24, weight=ft.FontWeight.BOLD),
                        ft.Divider(),
                        self.status_text,
                        camera_container,
                        ft.Text(f"Total Scans: {len(self.scans)}", size=12, color=ft.Colors.GREY),
                        ft.Divider(),
                        ft.Text("Scan History", size=16, weight=ft.FontWeight.BOLD),
                        self.scan_list,
                        ft.Row([clear_btn], alignment=ft.MainAxisAlignment.END)
                    ],
                    expand=True,
                    spacing=10
                ),
                padding=15,
                expand=True
            )
        )
        
        self.update_list()

def main(page: ft.Page):
    BarcodeScanner(page)

if __name__ == "__main__":
    ft.app(target=main)

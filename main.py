import flet as ft

def main(page: ft.Page):
    page.title = "Hello World"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    
    page.add(
        ft.Text("Hello World", size=30, weight=ft.FontWeight.BOLD)
    )

if __name__ == "__main__":
    ft.app(target=main)

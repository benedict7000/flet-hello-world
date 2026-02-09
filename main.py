from kivy.lang import Builder
from kivy.core.window import Window
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton, MDFlatButton
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.list import MDList, OneLineListItem
from kivymd.uix.dialog import MDDialog
from kivymd.uix.snackbar import Snackbar
from kivymd.color_definitions import colors
from datetime import datetime
import requests
import hashlib
import json

# Window configuration
Window.size = (450, 950)

# Firebase configuration
FIREBASE_CONFIG = {
    "databaseURL": "https://test-auth-94f6a-default-rtdb.firebaseio.com",
}

# Colors
PRIMARY = "#0052CC"
SECONDARY = "#FF6B6B"
SUCCESS = "#51CF66"
LIGHT_BG = "#F8FAFC"
CARD_BG = "#FFFFFF"
TEXT_PRIMARY = "#1A202C"
TEXT_SECONDARY = "#718096"
BORDER = "#E2E8F0"

KV = '''
#:kivy 2.0

<LoginScreen>:
    MDBoxLayout:
        orientation: 'vertical'
        padding: '20dp'
        spacing: '20dp'
        
        MDLabel:
            text: 'Branch Manager'
            font_style: 'H4'
            bold: True
            size_hint_y: None
            height: '60dp'
            halign: 'center'
        
        MDLabel:
            text: 'Professional Management'
            font_style: 'Subtitle1'
            size_hint_y: None
            height: '30dp'
            halign: 'center'
        
        MDCard:
            orientation: 'vertical'
            padding: '20dp'
            spacing: '15dp'
            size_hint_y: None
            height: '400dp'
            elevation: 2
            
            MDLabel:
                text: 'Welcome'
                font_style: 'H6'
                bold: True
                size_hint_y: None
                height: '40dp'
            
            MDTextField:
                id: username_input
                hint_text: 'Username'
                mode: 'rectangle'
                size_hint_x: 1
                height: '50dp'
            
            MDTextField:
                id: password_input
                hint_text: 'Password'
                password: True
                mode: 'rectangle'
                size_hint_x: 1
                height: '50dp'
            
            MDLabel:
                id: error_label
                text: ''
                color: (1, 0.4, 0.4, 1)
                size_hint_y: None
                height: '30dp'
            
            MDRaisedButton:
                text: 'Sign In'
                size_hint_x: 1
                height: '50dp'
                on_press: app.root.get_screen('login').login()
            
            MDFlatButton:
                text: 'Create Account'
                size_hint_x: 1
                height: '50dp'
                on_press: app.root.get_screen('login').signup()

<DashboardScreen>:
    MDBoxLayout:
        orientation: 'vertical'
        
        MDTopAppBar:
            title: 'Branch Manager'
            left_action_items: [['menu', lambda x: None]]
            right_action_items: [['logout', lambda x: app.root.get_screen('dashboard').logout()]]
        
        MDScrollView:
            MDBoxLayout:
                orientation: 'vertical'
                padding: '15dp'
                spacing: '15dp'
                size_hint_y: None
                height: self.minimum_height
                
                MDCard:
                    orientation: 'vertical'
                    padding: '15dp'
                    spacing: '10dp'
                    size_hint_y: None
                    height: '80dp'
                    elevation: 1
                    
                    MDLabel:
                        text: 'Hi, Welcome! 👋'
                        font_style: 'H6'
                        bold: True
                    
                    MDLabel:
                        id: username_label
                        text: ''
                        font_style: 'Subtitle2'
                
                MDCard:
                    orientation: 'vertical'
                    padding: '15dp'
                    spacing: '10dp'
                    size_hint_y: None
                    height: '350dp'
                    elevation: 1
                    
                    MDLabel:
                        text: 'Add New Branch'
                        font_style: 'H6'
                        bold: True
                        size_hint_y: None
                        height: '40dp'
                    
                    MDTextField:
                        id: branch_name_input
                        hint_text: 'Branch Name'
                        mode: 'rectangle'
                        size_hint_x: 1
                        height: '50dp'
                    
                    MDTextField:
                        id: start_date_input
                        hint_text: 'Start Date (YYYY-MM-DD)'
                        mode: 'rectangle'
                        size_hint_x: 1
                        height: '50dp'
                    
                    MDTextField:
                        id: end_date_input
                        hint_text: 'End Date (YYYY-MM-DD)'
                        mode: 'rectangle'
                        size_hint_x: 1
                        height: '50dp'
                    
                    MDRaisedButton:
                        text: 'Add Branch'
                        size_hint_x: 1
                        height: '50dp'
                        on_press: app.root.get_screen('dashboard').add_branch()
                
                MDCard:
                    orientation: 'vertical'
                    padding: '15dp'
                    spacing: '10dp'
                    size_hint_y: None
                    height: '300dp'
                    elevation: 1
                    
                    MDLabel:
                        text: 'Your Branches'
                        font_style: 'H6'
                        bold: True
                        size_hint_y: None
                        height: '40dp'
                    
                    MDScrollView:
                        MDList:
                            id: branches_list
                            spacing: '10dp'
'''

def hash_password(password):
    """Simple password hashing"""
    return hashlib.sha256(password.encode()).hexdigest()

class LoginScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'login'
        self.app = None
    
    def on_enter(self):
        self.app = MDApp.get_running_app()
    
    def user_exists(self, username):
        try:
            url = f"{FIREBASE_CONFIG['databaseURL']}/users/{username}.json"
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                data = response.json()
                return data is not None
            return False
        except Exception as ex:
            print(f"Error checking user: {ex}")
            return False
    
    def register_user(self, username, password):
        try:
            if self.user_exists(username):
                return False, "Username already exists"
            
            user_data = {
                "username": username,
                "password": hash_password(password),
                "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
            url = f"{FIREBASE_CONFIG['databaseURL']}/users/{username}.json"
            response = requests.put(url, json=user_data, timeout=10)
            
            if response.status_code == 200:
                return True, "Registration successful"
            else:
                return False, f"Registration failed"
        except Exception as ex:
            print(f"Register Exception: {ex}")
            return False, f"Error: {str(ex)[:40]}"
    
    def login_user(self, username, password):
        try:
            url = f"{FIREBASE_CONFIG['databaseURL']}/users/{username}.json"
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if data is None:
                    return False, "User not found"
                
                stored_password = data.get("password", "")
                input_password_hash = hash_password(password)
                
                if stored_password == input_password_hash:
                    return True, "Login successful"
                else:
                    return False, "Invalid password"
            else:
                return False, "User not found"
        except Exception as ex:
            print(f"Login Exception: {ex}")
            return False, f"Error: {str(ex)[:40]}"
    
    def login(self):
        username = self.ids.username_input.text.strip()
        password = self.ids.password_input.text.strip()
        
        if not username or not password:
            self.ids.error_label.text = "❌ Please fill all fields"
            return
        
        success, message = self.login_user(username, password)
        if success:
            self.app.current_user = {"username": username, "user_id": username}
            self.ids.username_input.text = ""
            self.ids.password_input.text = ""
            self.ids.error_label.text = ""
            self.manager.current = 'dashboard'
        else:
            self.ids.error_label.text = f"❌ {message}"
    
    def signup(self):
        username = self.ids.username_input.text.strip()
        password = self.ids.password_input.text.strip()
        
        if not username or not password:
            self.ids.error_label.text = "❌ Please fill all fields"
            return
        
        if len(password) < 6:
            self.ids.error_label.text = "❌ Password must be 6+ characters"
            return
        
        if len(username) < 3:
            self.ids.error_label.text = "❌ Username must be 3+ characters"
            return
        
        success, message = self.register_user(username, password)
        if success:
            self.app.current_user = {"username": username, "user_id": username}
            self.ids.username_input.text = ""
            self.ids.password_input.text = ""
            self.ids.error_label.text = ""
            self.manager.current = 'dashboard'
        else:
            self.ids.error_label.text = f"❌ {message}"

class DashboardScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'dashboard'
        self.app = None
        self.branches = []
    
    def on_enter(self):
        self.app = MDApp.get_running_app()
        self.ids.username_label.text = f"User: {self.app.current_user['username']}"
        self.load_branches()
    
    def load_branches(self):
        try:
            db_url = f"{FIREBASE_CONFIG['databaseURL']}/branches/{self.app.current_user['user_id']}.json"
            response = requests.get(db_url, timeout=10)
            if response.status_code == 200:
                data = response.json()
                if data:
                    self.branches = list(data.values())
                else:
                    self.branches = []
            self.update_branch_list()
        except Exception as ex:
            print(f"Error loading branches: {ex}")
    
    def add_branch(self):
        name = self.ids.branch_name_input.text.strip()
        start = self.ids.start_date_input.text.strip()
        end = self.ids.end_date_input.text.strip()
        
        if not name or not start or not end:
            Snackbar(text="Please fill all fields").open()
            return
        
        try:
            branch_data = {
                "name": name,
                "start_date": start,
                "end_date": end,
                "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
            db_url = f"{FIREBASE_CONFIG['databaseURL']}/branches/{self.app.current_user['user_id']}.json"
            response = requests.post(db_url, json=branch_data, timeout=10)
            
            if response.status_code == 200:
                self.branches.append(branch_data)
                self.ids.branch_name_input.text = ""
                self.ids.start_date_input.text = ""
                self.ids.end_date_input.text = ""
                self.update_branch_list()
                Snackbar(text="✅ Branch added successfully").open()
            else:
                Snackbar(text="❌ Failed to add branch").open()
        except Exception as ex:
            Snackbar(text=f"❌ Error: {str(ex)[:30]}").open()
    
    def update_branch_list(self):
        self.ids.branches_list.clear_widgets()
        
        if not self.branches:
            self.ids.branches_list.add_widget(
                OneLineListItem(text="No branches yet")
            )
        else:
            for branch in self.branches:
                item_text = f"{branch.get('name', '')} ({branch.get('start_date', '')} - {branch.get('end_date', '')})"
                self.ids.branches_list.add_widget(
                    OneLineListItem(text=item_text)
                )
    
    def logout(self):
        self.app.current_user = {"username": "", "user_id": ""}
        self.manager.current = 'login'

class BranchManagerApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.current_user = {"username": "", "user_id": ""}
    
    def build(self):
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.primary_hue = "700"
        
        Builder.load_string(KV)
        
        sm = MDScreenManager()
        sm.add_widget(LoginScreen())
        sm.add_widget(DashboardScreen())
        
        return sm

if __name__ == '__main__':
    BranchManagerApp().run()

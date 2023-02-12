##
# File: pwgui.py
# Brief: Grafical Interface for Password Manager
# Autor: Michal Ľaš

from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.app import MDApp
from kivymd.uix.list import TwoLineRightIconListItem
from kivymd.uix.dialog import MDDialog
from kivymd.uix.boxlayout import MDBoxLayout
from dataFunctions import dataFunctions
from PasswordGenerator import PW_Generator


##
# Main screen Class
class MainWindow(Screen):
    task_create_dialog = None

    def __init__(self, **kw):
        super().__init__(**kw)

        self.data = dataFunctions.load_data(self)

        MainWindow.init_on_start(self)

    ##
    # Sort data to catagories
    def init_on_start(self):
        for category in self.data:
            for item in self.data[category]:
                item = CustomTwoLineList(text=item["name"], secondary_text=item["description"], id=item["name"])
                item.bind(on_release=self.go_to_detail)
                if (category == "Accounts"):
                    self.ids.accounts_list.add_widget(item)
                elif (category == "Games"):
                    self.ids.games_list.add_widget(item)
                elif (category == "Emails"):
                    self.ids.emails_list.add_widget(item)
                elif (category == "Licences"):
                    self.ids.licences_list.add_widget(item)
    
                item.parent.id = category


    ##
    # Open new dialog for creating new record
    def show_create_dialog(self):
        if not self.task_create_dialog:
            self.task_create_dialog = MDDialog(
                title="Create new record",
                type="custom",
                content_cls=CreateDialogContent(),
            )
        self.task_create_dialog.open()


    ##
    # Create new record
    def create(self, category, name, email, password, description):
        # Check if item already does not exist
        if (dataFunctions.find_record(self, self.data[category], name) != -1):
            return

        new_record = {
            "name": name,
            "email": email,
            "password": password,
            "description": description
        }
        # if category was selected
        if (category != "Categories"):
            item = CustomTwoLineList(text=new_record["name"], secondary_text=new_record["description"], id=new_record["name"])
            item.bind(on_release=self.go_to_detail)
            if (category == "Accounts"):
                self.ids.accounts_list.add_widget(item)
            elif (category == "Games"):
                self.ids.games_list.add_widget(item)
            elif (category == "Emails"):
                self.ids.emails_list.add_widget(item)
            elif (category == "Licences"):
                self.ids.licences_list.add_widget(item)

            item.parent.id = category
            dataFunctions.create_record(self, self.data, category, new_record)


    ##
    # Close create dialog
    def close_dialog(self, *args):
        self.task_create_dialog.dismiss()
        self.task_edit_dialog = None


    ##
    # Delete existing record
    def delete(self, item):
        dataFunctions.delete_record(self, self.data, item.parent.id, item.text)
        
        if (item.parent.id == "Accounts"):
            self.ids.accounts_list.remove_widget(item)
        elif (item.parent.id == "Games"):
            self.ids.games_list.remove_widget(item)
        elif (item.parent.id == "Emails"):
            self.ids.emails_list.remove_widget(item)
        else:
            self.ids.licences_list.remove_widget(item)



    ##
    # Set new name of item
    def set_item_name(self, category, item_index, new_text):
        if (category == "Accounts"):
            self.ids.accounts_list.children[item_index].text = new_text
        elif (category == "Games"):
            self.ids.games_list.children[item_index].text = new_text
        elif (category == "Emails"):
            self.ids.emails_list.children[item_index].text = new_text
        else:
            self.ids.licences_list.children[item_index].text = new_text

    
    ##
    # Set new description of item
    def set_item_description(self, category, item_index, new_text):
        if (category == "Accounts"):
            self.ids.accounts_list.children[item_index].secondary_text = new_text
        elif (category == "Games"):
            self.ids.games_list.children[item_index].secondary_text = new_text
        elif (category == "Emails"):
            self.ids.emails_list.children[item_index].secondary_text = new_text
        else:
            self.ids.licences_list.children[item_index].secondary_text = new_text


    ##
    # Move to detail page for certain record
    def go_to_detail(self, item, *args):
        item_index = dataFunctions.find_record(self, self.data[item.parent.id], item.text)
        record = self.data[item.parent.id][item_index]
        self.manager.get_screen("detail").set_item(self.data, record, item.parent.id, item_index)
        self.manager.current = "detail"

##
# Detail screen Class
class DetailWindow(Screen):
    task_edit_dialog = None

    ##
    # set page items with selected item data
    def set_item(self, data, item, category, item_index):
        self.data = data
        self.item = item
        self.item_index = item_index
        self.category = category
        self.ids.page_name.text = item["name"]
        self.ids.name_label.text = item["name"]
        self.ids.email_label.text = item["email"]
        self.ids.password_label.text = item["password"]
        self.ids.description_label.text = item["description"]


    ##
    # Open new dialog for editing existing records
    def show_edit_dialog(self, id):
        self.curr_id = id
        if not self.task_edit_dialog:
            self.task_edit_dialog = MDDialog(
                title="Edit",
                type="custom",
                content_cls=EditDialogContent(id=id),
            )
        self.task_edit_dialog.open()


    ##
    # Open new dialog for editing existing records
    def show_edit_PW_dialog(self, id):
        self.curr_id = id
        if not self.task_edit_dialog:
            self.task_edit_dialog = MDDialog(
                title="Edit",
                type="custom",
                content_cls=PWEditDialogContent(id=id),
            )
        self.task_edit_dialog.open()


    ##
    # Close edit dialog
    def close_dialog(self, *args):
        self.task_edit_dialog.dismiss()
        self.task_edit_dialog = None
        

    ##
    # Update data
    def change(self, new_text):

        # Update labels
        if (self.curr_id == "name_label"):
            # Check for item with same name
            if(dataFunctions.find_record(self, self.data[self.category], new_text) != -1):
                return # do nothing if item with this name already exist
            self.ids.page_name.text = new_text
            self.manager.get_screen("main").set_item_name(self.category, self.item_index, new_text)
        elif (self.curr_id == "description_label"):
            self.manager.get_screen("main").set_item_description(self.category, self.item_index, new_text)

        getattr(self.ids, self.curr_id).text = new_text
            
        # Updata database
        if (self.curr_id == "name_label"):
            dataFunctions.edit_record(self, self.data, self.category, self.item_index, "name", new_text)
        elif(self.curr_id == "email_label"):
            dataFunctions.edit_record(self, self.data, self.category, self.item_index, "email", new_text)
        elif (self.curr_id == "password_label"):
            dataFunctions.edit_record(self, self.data, self.category, self.item_index, "password", new_text)
        else:
            dataFunctions.edit_record(self, self.data, self.category, self.item_index, "description", new_text)


##
# Custom TwoLineListItem component
class CustomTwoLineList(TwoLineRightIconListItem):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


##
# Dialog for editing existing record
class EditDialogContent(MDBoxLayout):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


##
# Dialog for editing existing record
class PWEditDialogContent(MDBoxLayout):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


    def generate_password(self):
        self.ids.new_text.text = PW_Generator.generate()


##
# Dialog for creating new record
class CreateDialogContent(MDBoxLayout):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


    def generate_password(self):
        self.ids.new_password.text = PW_Generator.generate()


class WindowManager(ScreenManager):
    pass




class gui(MDApp):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MainWindow(name="main"))
        sm.add_widget(DetailWindow(name="detail"))

        return sm
from nanome.util import Logs


async def save_mol_to_db(self, btn):
        Logs.message("Saved to DB!")


def create_menu(ui_manager):
    menu = ui_manager.create_new_menu()
    btn = menu.root.add_new_button("Save Molecule to DB")
    Logs.message(f"Button: {btn._content_id}")
    ui_manager.register_btn_pressed_callback(btn, save_mol_to_db)
    menu.enabled = True
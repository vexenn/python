# 1. Create test_settings with some initial values
test_settings = {
    'theme': 'dark',
    'language': 'english'
}

# 2. Add Setting
def add_setting(settings_dict, setting_tuple):
    # Unpack the tuple (key, value)
    key, value = setting_tuple
    key = str(key).lower()
    value = str(value).lower()
    
    if key in settings_dict:
        return f"Setting '{key}' already exists! Cannot add a new setting with this name."
    
    settings_dict[key] = value
    return f"Setting '{key}' added with value '{value}' successfully!"

# 3. Update Setting
def update_setting(settings_dict, setting_tuple):
    key, value = setting_tuple
    key = str(key).lower()
    value = str(value).lower()
    
    if key not in settings_dict:
        return f"Setting '{key}' does not exist! Cannot update a non-existing setting."
    
    settings_dict[key] = value
    return f"Setting '{key}' updated to '{value}' successfully!"

# 4. Delete Setting
def delete_setting(settings_dict, key):
    key = str(key).lower()
    
    if key in settings_dict:
        del settings_dict[key]
        return f"Setting '{key}' deleted successfully!"
    
    return "Setting not found!"

# 5. View Settings
def view_settings(settings_dict):
    if not settings_dict:
        return "No settings available."
    
    output = "Current User Settings:\n"
    for key, value in settings_dict.items():
        # .capitalize() uppercase only the first letter
        output += f"{key.capitalize()}: {value}\n"
    
    return output
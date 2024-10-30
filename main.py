import json
import os
import filter_docs

# File path for the configuration file
CONFIG_FILE = "config.json"

# Function to load the configuration from the JSON file
def load_config():
    with open(CONFIG_FILE, 'r') as f:
        config = json.load(f)
    return config

# Function to save the configuration to the JSON file
def save_config(config):
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=4)

def display_menu():
    print("Please select an option:")
    print("1. Configure the pipeline")
    print("2. Execute the pipeline")
    print("3. Help")
    print("4. Exit")

def display_config_menu():
    print("Please select an option:")
    print("1. Set folder path")
    print("2. Set output CSV")
    print("3. Set keywords")
    print("4. Set ignored sections")
    print("5. Set model name")
    print("6. Set verbose")
    print("7. Print configuration")
    print("8. Exit")

def configure_pipeline():
    config = load_config()  # Load current configuration

    while True:
        display_config_menu()
        choice = input("Enter your choice (1-8): ")
        os.system('cls' if os.name == 'nt' else 'clear')
        if choice == '1':
            config['folder_path'] = input("Enter the folder path: ")
        elif choice == '2':
            config['output_csv'] = input("Enter the output CSV: ")
        elif choice == '3':
            config['keywords'] = input("Enter the keywords (comma-separated): ").split(",")
        elif choice == '4':
            config['ignored_sections'] = input("Enter the ignored sections (comma-separated): ").split(",")
        elif choice == '5':
            config['model_name'] = input("Enter the model name: ")
        elif choice == '6':
            verbose_input = input("Enter verbose (True/False): ").lower()
            config['verbose'] = verbose_input == 'true'
        elif choice == '7':
            print_config(config)
        elif choice == '8':
            print("Exiting the configuration menu.")
            save_config(config)  # Save updated configuration
            break
        else:
            print("Invalid choice. Please select a valid option (1-8).")

def print_config(config):
    print("Current Configuration:")
    print(f"Folder path: {config['folder_path']}")
    print(f"Output CSV: {config['output_csv']}")
    print(f"Keywords: {config['keywords']}")
    print(f"Ignored sections: {config['ignored_sections']}")
    print(f"Model name: {config['model_name']}")
    print(f"Verbose: {config['verbose']}")

def main():
    menu_open = True
    while menu_open:
        display_menu()
        choice = input("Enter your choice (1-4): ")

        if choice == '1':
            configure_pipeline()
        elif choice == '2':
            print("Executing Pipeline...")
            print("Executing filtering...")

            try:
                config = load_config()
                filter_docs.execute_filtering(config)
            except Exception as e:
                print(f"An error occurred: {e}")
                print("Pipeline failed.")
                continue

            print("Executing requirement Generating...")
            print("ERROR: (Placeholder because requirement generating is not implemented yet for this branch)")

            try:
                pass
            except Exception as e:
                print(f"An error occurred: {e}")
                print("Pipeline failed.")
                continue

            # Placeholder for requirement generating
            print("Pipeline executed successfully.")

        elif choice == '3':
            print("Help menu (placeholder).")
            # Placeholder for help menu
        elif choice == '4':
            print("Exiting the program. Goodbye!")
            menu_open = False
        else:
            print("Invalid choice. Please select a valid option (1-4).")

if __name__ == "__main__":
    main()

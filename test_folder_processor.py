from services.folder_processor import process_folder

results = process_folder()

for result in results:

    print(
        result["filename"],
        result["final_decision"]
    )
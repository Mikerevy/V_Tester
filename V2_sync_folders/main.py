import time, os, sys, shutil
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from dirsync import sync
from datetime import datetime

# Example arguments path.
# First argv should be original folder and the second argv should be copy folder
# source_path = 'C:\\Users\Mike\Desktop\s\original'
# target_path = 'C:\\Users\Mike\Desktop\s\copy'

# Our Class with super class FileSys
class Handler(FileSystemEventHandler):
    def __init__(self, source_path, target_path):
        self.source_path = source_path
        self.target_path = target_path

    def time(self):
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        print(f"Time: {current_time}. For exit press 'Ctrl+C'")

    def on_modified(self, event):
        sync(self.source_path, self.target_path, "sync")
        print(f" {event.src_path} has been modified!")

    def on_created(self, event):
        sync(self.source_path, self.target_path, "sync")
        print(f" {event.src_path} has been created!")

    def on_deleted(self, event):
        # Path of delete file
        file_path = event.src_path

        name_of_file = ''
        for letter in range(len(file_path) - 1, -1, -1):
            if file_path[letter] != '\\':
                name_of_file += file_path[letter]
            else:
                break

        # Name of delete file or folder
        name_of_file = name_of_file[::-1]

        # Catch delete file from original folder if is not in copy folder
        try:
            try:
                # For removing files
                os.remove(self.target_path + '\\' + name_of_file)
            except PermissionError:
                # For removing folders
                shutil.rmtree(self.target_path + '\\' + name_of_file)
        except FileNotFoundError:
            print("There is not this file in copy folder.")
            pass
        print(f" '{name_of_file}' has been deleted!")

    # Using when rename file or folder
    def on_moved(self, event):
        print(f"ok ok ok, someone moved {event.src_path} to {event.dest_path}")
        # sync(sourcedir, targetdir, "sync")

        print("0", event.src_path)
        # Path of delete file
        file_path = event.src_path
        name_of_file = ''
        for letter in range(len(file_path) - 1, -1, -1):
            if file_path[letter] != '\\':
                name_of_file += file_path[letter]
            else:
                break

        # Name of delete file or folder
        name_of_file = name_of_file[::-1]
        # Copy the file or folder to copy folder
        sync(self.source_path, self.target_path, "sync")

        # Delete the old one
        # Catch delete file from original folder if is not in copy folder
        try:
            try:
                # For removing files
                os.remove(self.target_path + '\\' + name_of_file)
            except PermissionError:
                # For removing folders
                shutil.rmtree(self.target_path + '\\' + name_of_file)
        except FileNotFoundError:
            print("There is not this file in copy folder.")
            pass
        print(f" '{name_of_file}' has been deleted!")


# Def main function
def main():
    # Check if user provided right count of arguments.
    if len(sys.argv) == 3:

        # Check if user provided right paths
        if os.path.exists(sys.argv[1]) is True and os.path.exists(sys.argv[2]) is True:

            # Create an object from class Observe() -keeps monitoring folder for any changes
            observer = Observer()

            # Create an object from use line arguments as parameters
            event_handler = Handler(sys.argv[1], sys.argv[2])

            # Watching a path and call methods from 'event_handler' when is given event
            observer.schedule(event_handler, sys.argv[1], recursive=True)  # recursive=True events will be emited for
            # suborders too

            # Create a new tread
            observer.start()
            try:
                while True:
                    # Keeps main thread running
                    time.sleep(5)
                    event_handler.time()
            except KeyboardInterrupt:
                # The thread is terminate
                observer.stop()
            # For proper end a thread
            observer.join()
        else:
            # Otherwise don't run this program
            print("Exit. User has provided wrong path! ")
    # Otherwise don't run this program
    else:
        print("Exit. User has provided wrong count of arguments! ")


if __name__ == "__main__":
    main()

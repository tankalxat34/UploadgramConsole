import sys

from PaintPrint import *
import UploadgramPyAPI, time, getpass, os

neutralizeColorProblem()

__version__ = "0.1.3"
__author__ = "tankalxat34"
__email__ = "tankalxat34@gmail.com"


def _print_title():
    bprint("Uploadgram console application v" + __version__ + " (c) " + __author__ + " - " + time.strftime("20%y"),
           FORMATTING.BOLD, UserColor.FOREGROUND((52, 151, 217)).color)
    bprint('Drop file here and than you will get the URL and KEY. Type "help" to get more information\n',
           UserColor.FOREGROUND((128, 128, 128)).color)


def _read_doc(command):
    try:
        return UploadgramPyAPI.ServiceRules(command.split()[1]).get()
    except Exception:
        return bprint('Error to read the official doc. Type "read policies" or "read dmca" to read the doc"\n',
                      FOREGROUND.RED, doprint=False).get_text()


_print_title()

ascii_progressbar = '▮'
read_list = ["policies", "dmca"]

SIMPLE = {}
SIMPLE = {
    "author": __author__,
    "email": __email__,
    "version": __version__,
    "read policies": lambda: _read_doc("read policies"),
    "read dmca": lambda: _read_doc("read dmca"),
    "help": """
This application can upload, download, remove and rename any files from the service uploadgram.me - a simple and fast file uploader that uses Telegram network as file storage.
               
┌─────────────────────────┬────────────────────────────┐
│         Command         │        Description         │
├─────────────────────────┼────────────────────────────┤
│ help                    │ show this table again      │
│ <path_to_file>          │ upload as new file         │
│ delete <key>            │ delete file only by KEY    │
│ rename <key> <new_name> │ rename file only by KEY    │
│ download <key>          │ download file by KEY or ID │
│ download <id>           │                            │
└─────────────────────────┴────────────────────────────┘

All commands:
{}

       """,
    "exit": lambda: sys.exit()
}

SIMPLE["help"] = SIMPLE["help"].format("\n".join(list(SIMPLE.keys())))

while True:
    try:
        command = input(bformat(">>> ", UserColor.FOREGROUND("#3497D9").color))

        if "\\" in command.replace('"', ""):
            if '"' == command[0] and '"' == command[-1]:
                command = command[1:-1]
            try:
                bprint("Uploading new file: "+command, FOREGROUND.CYAN)
                file = UploadgramPyAPI.NewFile(command)
                result_upload = file.upload()
                bprint("Successfully!", FOREGROUND.GREEN, end="\n\n")
                print("url: " + bformat(file.url, TEMPLATE.URL))
                print("key: " + bformat(file.key, FOREGROUND.GREEN))
                print()
            except Exception:
                bprint('Error to upload new file...\n', FOREGROUND.RED)

        elif "delete" in command:
            idkey = command.split()[1]
            try:
                file = UploadgramPyAPI.File(idkey)
                file.delete()
                bprint("Deleting file was successful!\n", FOREGROUND.GREEN)
            except Exception:
                bprint('Error to delete file...\n', FOREGROUND.RED)

        elif "rename" in command:
            idkey = command.split()[1]
            newname = command.split()[2]
            try:
                file = UploadgramPyAPI.File(idkey)
                file.rename(newname)
                bprint("New name set upped file was successful!\n", FOREGROUND.GREEN)
            except Exception:
                bprint('Error to rename file...\n', FOREGROUND.RED)

        elif "download" in command:
            idkey = command.split()[1]
            try:
                file = UploadgramPyAPI.File(idkey)
                file.download()
                bprint(f"File downloaded successful in C:\\Users\\{getpass.getuser()}\\Downloads!\n", FOREGROUND.GREEN)
            except Exception:
                bprint('Error to download file...\n', FOREGROUND.RED)

        elif "cls" == command:
            os.system(command)
            _print_title()

        else:
            try:
                try:
                    bprint(SIMPLE[command]())
                except Exception:
                    bprint(SIMPLE[command])
            except Exception:
                os.system(command)
    except Exception:
        os.system(command)


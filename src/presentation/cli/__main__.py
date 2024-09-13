import argparse
import json
from os import path
import os
from domain.entities.folder.Folder import Folder
from domain.repositories.bookmark.IBookmarkRepo import IBookmarkRepo
import questionary
from domain.repositories.whitelist.IWhitelistRepo import IWhitelistRepo
from infrastructure.persistance.adapters.bookmark.brave.BraveBookmarkRepo import (
    BraveBookmarkRepo,
)
from infrastructure.persistance.adapters.whitelist.fs.FSWhitelistRepo import (
    FSWhitelistRepo,
)

EXPECTED_WL_FILE_NAME = ".bkmks"


def main():
    not_supported_msg = "Sorry, this browser does not seem to be supported yet, but PRs are always welcome! See https://github.com/nico-i/bkmks#contributing for more information."

    supported_browsers = os.listdir(
        path.join(os.getcwd(), "infrastructure", "persistance", "adapters", "bookmark")
    )
    supported_browsers.append("other")

    parser = argparse.ArgumentParser(
        description="Extract your browser bookmarks into a normalized JSON"
    )
    parser.add_argument(
        "-w",
        "--whitelist",
        help='Path to your bookmark whitelist (aka your ".bkmks" file)',
    )
    parser.add_argument(
        "-b",
        "--browser",
        help="The browser you want to extract bookmarks from",
        choices=supported_browsers,
    )
    parser.add_argument("-o", "--output", help="Output file path")
    args, _ = parser.parse_known_args()

    set_args = {k: v for k, v in vars(args).items() if v is not None}
    are_any_args_set = len(set_args) == 0

    if are_any_args_set:
        if not args.browser:
            args.browser = questionary.select(
                "Select the browser you want to extract bookmarks from",
                choices=supported_browsers,
            ).ask()

        if args.browser == "other":
            print(not_supported_msg)
            return

        if not args.whitelist:
            use_wl = questionary.confirm(
                "Would you like to only extract whitelisted bookmarks?", default=False
            ).ask()
            if use_wl:
                args.whitelist = questionary.path(
                    "Enter the path to your bookmark whitelist",
                    default=path.join(os.getcwd(), ".bkmks"),
                ).ask()

        if args.whitelist:
            if not os.path.exists(args.whitelist):
                print(
                    f'Whitelist file could not be found at "{args.whitelist}". Aborting...'
                )
                return
            if not os.path.isfile(args.whitelist):
                print(
                    f'Whitelist path must lead to a file named "{EXPECTED_WL_FILE_NAME}". Aborting...'
                )
                return
            if not args.whitelist.endswith(EXPECTED_WL_FILE_NAME):
                print(
                    f'Whitelist file must be named "{EXPECTED_WL_FILE_NAME}"! Aborting...'
                )
                return

        if not args.output:
            write_to_file = questionary.confirm(
                "Would you like to write the output to a file (will otherwise be printed to console)?",
                default=True,
            ).ask()
            if write_to_file:
                args.output = questionary.path(
                    "Enter the output file path", default="bookmarks.json"
                ).ask()

    wl_repo: IWhitelistRepo = None
    if args.whitelist:
        wl_repo = FSWhitelistRepo(whitelist_path=args.whitelist)

    bkmks_repo: IBookmarkRepo = None

    if args.browser == "brave":
        bkmks_repo = BraveBookmarkRepo(wl_repo)
    else:
        print(not_supported_msg)
        return

    root_folder_json: Folder = None
    if wl_repo:
        root_folder_json = bkmks_repo.get_whitelisted_root_folder()
    else:
        root_folder_json = bkmks_repo.get_root_folder()

    json_object = json.loads(root_folder_json.to_json())

    if not args.output:
        print(json.dumps(json_object, indent=4, ensure_ascii=False))
        return

    with open(args.output, "w", encoding="utf-8") as f:
        f.write(json.dumps(json_object, indent=4, ensure_ascii=False))


if __name__ == "__main__":
    main()

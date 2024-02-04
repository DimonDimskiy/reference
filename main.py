import platform
import tkinter
import itertools

import pyperclip
import pyautogui
import requests


class WhatTheMeaning:
    def __init__(self):
        self.system = platform.system()
        self.limit = 10
        self.dict_url = "https://api.dictionaryapi.dev/api/v2/entries/en/"

    def get_ctrl(self):
        ctrl = {
            "Windows": "ctrl",
            "Darwin": "command"
        }
        return ctrl[self.system]

    def get_word(self):
        ctrl = self.get_ctrl()

        with pyautogui.hold(ctrl):
            pyautogui.press("c")

        res = pyperclip.paste().strip().split()

        if not res:
            raise ValueError
        return res[0]

    def get_definitions(self):

        word = self.get_word()

        response = requests.get(url=self.dict_url + word)
        response.raise_for_status()

        data = response.json()[0]
        result = [data["word"]]
        meanings = data.get("meanings", [])

        limit = self.limit
        counter = itertools.count(start=1)
        for meaning in meanings:
            definitions = meaning.get("definitions", [])

            for definition in definitions:
                if limit <= 0:
                    return result
                result.append(f"{next(counter)}. {definition.get('definition', [])}")
                limit -= 1

        return result


def main():
    wtm = WhatTheMeaning()
    meanings = wtm.get_definitions()
    root = tkinter.Tk()
    for meaning in meanings:
        label = tkinter.Label(root, text=meaning, justify="left", wraplength=300)
        label.pack(anchor="w")
    root.mainloop()


if __name__ == "__main__":
    main()


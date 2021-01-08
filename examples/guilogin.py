"""

ro.py
GUI Login Example

This example uses the prompt extension to login with a GUI dialog.

"""


from ro_py.client import Client
from ro_py.extensions.prompt import authenticate_prompt

client = Client()


def main():
    authenticate_prompt(client)


if __name__ == '__main__':
    main()

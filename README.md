# Python2FAuthenticatorGUI
2F Authenticator App with GUI using Qt for python

This app only supports TOTP authentication for now.
All the encryption and storage code is a free python adaptation from the [Aegis Authenticator](https://github.com/beemdevelopment/Aegis) app encryption/storage part.

### Installation

If you are looking to install the program, go to the release page.

### Development

If you want to add features, or just run it in your own python environment, fell freee to clone the repository and setup your environment using the provided makefile.

The `make ui` command compiles the Qt `.ui` files into usable python files that are thus not provided. This command is necessary to run the program.

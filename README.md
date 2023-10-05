# Python2FAuthenticatorGUI
2F Authenticator App with GUI using Qt for python

This app only supports TOTP authentication for now.
All the encryption and storage code is a free python adaptation from the [Aegis Authenticator](https://github.com/beemdevelopment/Aegis) app encryption/storage part.

### Installation

If you are looking to install the program, go to the release page.

### Development

If you want to add features, or just run it in your own python environment, feel free to clone the repository and setup your environment using the provided makefile.

To install the development version after cloning the repo

Using conda:
```bash
$ make conda_setup
```

Every time the ui files are modified, you need to run:
```bash
$ make ui
```

Then to run the app:
```bash
$ make run
```
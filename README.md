# Python2FAuthenticatorGUI
2F Authenticator App with GUI using Qt for python

This app only supports TOTP authentication for now.
All the encryption and storage code is a free python adaptation from the [Aegis Authenticator](https://github.com/beemdevelopment/Aegis) app encryption/storage part.

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
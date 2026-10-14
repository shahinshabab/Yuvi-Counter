# Little Counter — Selenium project

A mobile-friendly website with two modes and Python Selenium browser tests.

- **Numeric:** starts at 0; + adds one, − subtracts one, Reset returns to 0. Stops at zero and JavaScript's maximum safe integer.
- **Alphabet:** starts at A; + advances to Z, − goes back to A, Reset returns to A. No wraparound.
- Home links return to the mode picker. Each page visit starts fresh.
- No account, backend, tracking, or external frontend dependencies.

## Deploy on Streamlit Community Cloud

Use these deployment settings:

- Repository: `shahinshabab/Yuvi-Counter`
- Branch: `main`
- Main file path: `streamlit_app.py`

Do not use `tests/test_counters.py` as the main app file: it runs browser tests and does not render a Streamlit interface. If an existing deployment points to it, change the entrypoint or create a new deployment with the settings above.

To run the Streamlit version locally:

```sh
python -m pip install -r requirements.txt
streamlit run streamlit_app.py
```

The Streamlit app uses per-session counters. Home resets the selected mode. It does not launch Chrome or Selenium.

## Open the original HTML app

Open `index.html` directly in a browser, or run from this folder:

```sh
python -m http.server 8000 --bind 127.0.0.1
```

Then visit http://localhost:8000.

To test on your phone over a trusted Wi-Fi network, serve with `python -m http.server 8000 --bind 0.0.0.0` and open `http://YOUR-COMPUTER-LAN-IP:8000` on the phone. Your firewall may need to allow this connection. Stop the server with Ctrl+C when finished.

## Selenium tests

Requires Python 3.10+ and Google Chrome. Selenium Manager obtains a matching driver when internet access is available. Alternatively set CHROMEDRIVER to an installed driver path, and optionally CHROME_BINARY to a Chrome executable path.

```sh
python -m venv .venv
```

Activate with `.venv\Scripts\activate` on Windows or `source .venv/bin/activate` on macOS/Linux, then:

```sh
python -m pip install -r requirements.txt
python -m unittest discover -s tests -v
```

Tests use Chrome mobile emulation at 390 × 844, verifying numeric controls, every alphabet letter, boundaries, reset, home navigation, and layout overflow. The test suite starts and stops its own local server.

## Create a GitHub repository

With GitHub CLI installed and authenticated, run these commands from this folder:

```sh
git init -b main
git add .
git commit -m "Create mobile counters and Selenium tests"
gh repo create mobile-counter-selenium --private --source=. --remote=origin --push
```

Or create an empty repository at https://github.com/new named `mobile-counter-selenium` and upload the extracted project files. Do not upload the ZIP itself as the project source.

## Linux Selenium dependencies

Exit code 127 means the driver failed before tests started; missing shared libraries are one possible cause. The exact missing dependency requires driver stderr or `ldd /path/to/chromedriver` output.

`packages.txt` installs Debian's `chromium` and `chromium-driver` together on Streamlit Community Cloud. The Selenium tests prefer this installed matching pair instead of downloading a separate driver. On a Debian/Ubuntu test machine, install these packages through your system package manager. Rebuild/reboot the cloud environment after dependency changes.

The Selenium suite tests the original HTML app. It is separate from hosting the Streamlit app.


# Bid Monitoring Bot with Selenium and Twilio

This is a Python script that monitors proxy bids on the online auction platform BidRl and sends text messages to the user to extend their bid if desired. It uses the Selenium framework to interact with the website and the Twilio API for sending text messages.

## Table of Contents

- [Introduction](#introduction)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Introduction

This script automates the process of monitoring proxy bids on BidRl. It does the following:

- Logs into the auction platform using specified credentials.
- Navigates to the user's recent bids page and identifies items with open bids.
- Checks the bid status of each item and sends a text message if the user is not winning the bid.
- If the user replies 'y' within a specified timeframe, the script extends the bid on that item.

## Prerequisites

Before running the script, you need the following:

1. Python 3.x installed on your system.
2. The Selenium package installed. You can install it using `pip install selenium`.
3. A web driver executable (e.g., ChromeDriver) that corresponds to your web browser. Ensure the driver's location is included in your system's PATH.
4. Twilio account credentials: `account_sid` and `auth_token`.
5. Twilio phone number for sending messages.
6. The recipient's phone number for receiving messages.

## Installation

1. Clone this repository to your local machine using:

   ```bash
   git clone https://github.com/Dheredia91/bidrlbot.git
   ```

2. Navigate to the project folder:

   ```bash
   cd bidrlbot
   ```

3. Install the required Python packages:

   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Open the script file (`bidrl.py`) in a text editor.
2. Replace the placeholders in the script with your actual credentials and phone numbers.
3. Save your changes.

To run the script:

```bash
python bidrl.py
```

The script will start monitoring proxy bids and sending text messages if needed.

## Contributing

Contributions are welcome! If you find any issues or want to enhance the script, feel free to open a pull request.

## License

This project is licensed under the [MIT License](LICENSE).

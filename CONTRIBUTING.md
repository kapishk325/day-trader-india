# Contributing to Day Trader India

Thank you for your interest in contributing to **Day Trader India**! This project is 100% open-source under the Apache License 2.0.

## Core Design Principles

1. **Zero External Dependencies**: All tools must run on the Python standard library alone. Never add a `pip install` requirement.
2. **Zero Sign-In & Zero API Keys**: Data sources must remain completely free and public.
3. **Strict Indian Market Compliance**: Always maintain the SEBI 5x MIS leverage ceiling and 15:15 IST mandatory square-off guard.
4. **Fast Execution**: Individual tools should complete execution in under 2 seconds.

## How to Contribute

1. Fork the repository on GitHub.
2. Clone your fork locally:
   ```bash
   git clone https://github.com/<your-username>/day-trader-india.git
   cd day-trader-india
   ```
3. Create a feature branch:
   ```bash
   git checkout -b feat/your-feature-name
   ```
4. Make your changes and run the test suite:
   ```bash
   python3 -m unittest discover -s tests -v
   ```
5. Commit using Conventional Commits format:
   ```bash
   git commit -m "feat(scanner): add supertrend indicator"
   ```
6. Push to your branch and open a Pull Request!

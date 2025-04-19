
Quick script to get payslips from SOP as there is no easy way to download them in bulk.

To run:
- Clone the repo
- Install the package manager [uv](https://github.com/astral-sh/uv) if you don't have it already
- `uv sync` to install packages with `uv`
- Add environment variables in `.env` for `SOP_URL`, `SOP_USERNAME` and `SOP_PASSWORD`
- Create a `downloads` folder in the root of the repo
- Run the script in main - `uv run python main.py`
- The payslips will be in the `downloads` folder
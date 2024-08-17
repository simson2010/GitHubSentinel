# GitHub Sentinel

GitHub Sentinel is an open-source AI Agent designed for developers and project managers. It automatically fetches and summarizes the latest updates from subscribed GitHub repositories on a daily or weekly basis. The main features include subscription management, update fetching, a notification system, and report generation.

## Installation

```
pip install -r requirements.txt
```

## Usage

### CLI

```
python src/ui/cli.py add --repo username/repo
```

### Web Interface

```
python src/ui/web.py
```

## Testing

Run the tests using:

```
python -m unittest discover tests
```

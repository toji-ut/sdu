# sdu - Smart Disk Usage

`sdu` is a safe, colorful, and interactive disk usage analyzer CLI.  
I built this tool for myself to analyze disk usage in my daily workflow, but it’s safe and reusable for anyone who wants a quick overview of their filesystem.

## Features

- Tree view of directories  
- Colored output:  
  - Red: files >1GB  
  - Yellow: files >100MB  
  - Green: smaller files  
- Summary by file type (`--summary`)  
- Human-readable sizes (KB, MB, GB)  
- Depth control (`--depth`)  
- Top N biggest items per folder (`--top`)  

## Installation

### Using pipx (recommended)

```bash
# Clone the repository
git clone https://github.com/toji-ut/sdu.git
cd sdu

# Install sdu globally using pipx
pipx install .

# sdu will now be available as a system-wide command:
sdu ~/Downloads --depth 2 --top 5 --summary
```

### Optional: Using a virtual environment
```bash
# Activate virtual environment
python3 -m venv venv

source venv/bin/activate  # Linux/macOS
# venv\Scripts\activate    # Windows

# Install
pip install -e .
```

### Usage examples
```bash
# Scan current directory
sdu

# Limit depth to 2
sdu ~/Downloads --depth 2

# Show top 5 largest items per folder
sdu ~/Downloads --top 5

# Show summary by file type
sdu ~/Downloads --top 5 --summary
```

### To update your global pipx installation
```bash
pipx install --force .
```
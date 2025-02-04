# Testing Guide

## Test Structure

The test suite is organized as follows:

```
tests/
├── unit/                    # Unit tests
│   └── core/               # Core module tests
│       ├── strategies/     # Strategy pattern implementations
│       │   ├── filters/    # Audio filter tests
│       │   └── noise/      # Noise generator tests
│       ├── test_audio_engine.py
│       ├── test_audio_stream.py
│       ├── test_parameter_system.py
│       └── ...
└── conftest.py             # Shared pytest fixtures
```

## Running Tests

### Basic Usage

Run all tests with clean output (recommended for daily use):
```bash
PYTHONPATH=/home/guy/Desktop/projects/noise\ playground python run_tests.py
```

Run specific test file:
```bash
PYTHONPATH=/home/guy/Desktop/projects/noise\ playground python run_tests.py tests/unit/core/test_noise_parameters.py
```

### Output Options

1. Clean Output (default)
   - Shows only failures and files with no tests
   - Ideal for quick feedback during development
   ```bash
   python run_tests.py [test_path]
   ```

2. Full Output
   - Shows complete pytest output with all details
   - Useful for debugging or when you need more information
   ```bash
   python run_tests.py [test_path] --full
   ```

### Examples

Run noise parameters tests with clean output:
```bash
python run_tests.py tests/unit/core/test_noise_parameters.py
```

Run same tests with full output:
```bash
python run_tests.py tests/unit/core/test_noise_parameters.py --full
```

## Coverage Reports

- HTML coverage report is generated in `htmlcov/` directory
- Open `htmlcov/index.html` in a browser to view detailed coverage information
- Files with 0% coverage are highlighted in the clean output
- Coverage report shows:
  - Line coverage percentage
  - Missing lines
  - Branch coverage
  - Uncovered code paths

## Test Categories

1. Core Tests
   - `test_audio_stream.py`: Audio streaming and processing
   - `test_parameter_system.py`: Parameter management
   - `test_noise_parameters.py`: Noise generation parameters
   - `test_observer.py`: Observer pattern implementation

2. Strategy Tests
   - `strategies/filters/`: Audio filter implementations
   - `strategies/noise/`: Noise generation algorithms

## Writing New Tests

1. Create test file in appropriate directory
2. Use pytest fixtures from conftest.py where needed
3. Follow existing test patterns for consistency
4. Run tests to ensure proper coverage

## Troubleshooting

If you see "No module named 'App'" error:
- Ensure PYTHONPATH is set correctly
- Run from project root directory

For coverage issues:
- Check htmlcov/index.html for detailed report
- Focus on files with 0% coverage first
- Look for untested code paths in partially covered files

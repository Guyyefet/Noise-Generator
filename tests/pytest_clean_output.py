import pytest
from typing import Dict, List, Optional
import json

class TestResult:
    def __init__(self):
        self.failures: List[Dict[str, str]] = []
        self.no_coverage: List[str] = []

    def to_dict(self) -> Dict:
        return {
            "failures": [
                {
                    "test": f.get("test"),
                    "error": f.get("error")
                } for f in self.failures
            ],
            "no_coverage": self.no_coverage
        }

class CleanOutputPlugin:
    def __init__(self):
        self.result = TestResult()

    @pytest.hookimpl(hookwrapper=True)
    def pytest_runtest_makereport(self, item, call):
        outcome = yield
        report = outcome.get_result()
        
        if report.when == "call" and report.failed:
            # Extract clean error message without traceback
            error_lines = str(report.longrepr).split('\n')
            error_msg = error_lines[-1] if error_lines else "No error message"
            
            self.result.failures.append({
                "test": item.name,
                "error": error_msg
            })

    def pytest_terminal_summary(self, terminalreporter, exitstatus, config):
        # Get coverage data if available
        if hasattr(terminalreporter, '_session'):
            session = terminalreporter._session
            if hasattr(session, 'config'):
                cov = session.config.pluginmanager.get_plugin('_cov')
                if cov:
                    for filename in cov.cov.get_data().measured_files():
                        coverage = cov.cov.get_data().get_file_coverage(filename)
                        if coverage == 0:  # Only show files with no tests
                            self.result.no_coverage.append(filename)

        # Write clean output to file
        with open('.test_output.json', 'w') as f:
            json.dump(self.result.to_dict(), f, indent=2)

@pytest.fixture(scope="session")
def clean_output(request):
    plugin = request.config.pluginmanager.get_plugin("clean-output")
    return plugin.result if plugin else None

def pytest_configure(config):
    plugin = CleanOutputPlugin()
    config.pluginmanager.register(plugin, "clean-output")

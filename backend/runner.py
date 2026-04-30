import subprocess
import tempfile
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def run_tests(files: dict, tests: dict, timeout: int = 30) -> tuple[bool, str]:
    try:
        with tempfile.TemporaryDirectory() as tmpdir:
            all_files = {**files, **tests}
            
            for filename, code in all_files.items():
                filepath = os.path.join(tmpdir, filename)
                dirname = os.path.dirname(filepath)
                if dirname:
                    os.makedirs(dirname, exist_ok=True)
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(code)
            
            logger.info(f"Running tests in {tmpdir}")
            result = subprocess.run(
                ["pytest", tmpdir, "-v", "--tb=short"],
                capture_output=True,
                text=True,
                timeout=timeout,
                cwd=tmpdir
            )
            
            output = result.stdout + "\n" + result.stderr
            success = result.returncode == 0
            logger.info(f"Tests {'passed' if success else 'failed'}")
            return success, output
            
    except subprocess.TimeoutExpired:
        logger.error("Test execution timeout")
        return False, "Test execution timeout after 30 seconds"
    except Exception as e:
        logger.error(f"Test execution error: {e}")
        return False, str(e)

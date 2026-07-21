import subprocess, sys, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class ReleaseTests(unittest.TestCase):
    def test_agentic_engineering_v010(self): subprocess.run([sys.executable,str(ROOT/'scripts/verify_release.py'),str(ROOT/'agentic-engineering/releases/v0.1.0')],check=True)
if __name__ == '__main__': unittest.main()

import json, unittest
from pathlib import Path
class DraftTests(unittest.TestCase):
    def test_first_capability_is_not_overclaimed(self):
        p=Path(__file__).resolve().parents[1]/'skills/bootstrap-agent-from-kernel/manifest.draft.json'
        data=json.loads(p.read_text())
        self.assertEqual(data['status'],'planned-not-released')
        self.assertIn('not adopted',data['explicit_non_claims'])
if __name__ == '__main__': unittest.main()

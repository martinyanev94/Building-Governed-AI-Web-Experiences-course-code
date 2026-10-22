import unittest

from src.creative_workflow import CreativeWorkflow, Status


class CreativeWorkflowTests(unittest.TestCase):
    def test_generation_requires_consent(self):
        workflow = CreativeWorkflow()
        with self.assertRaises(PermissionError):
            workflow.generate("night market poster", ["red-ribbon"], False)

    def test_rejection_blocks_submission(self):
        workflow = CreativeWorkflow()
        draft = workflow.generate("night market poster", ["red-ribbon"], True)
        workflow.review(draft.draft_id, "reject", "composition unclear")

        self.assertIs(draft.status, Status.REJECTED)
        self.assertEqual(draft.review_note, "composition unclear")
        with self.assertRaises(PermissionError):
            workflow.submit(draft.draft_id)

    def test_regeneration_preserves_parent_provenance(self):
        workflow = CreativeWorkflow()
        first = workflow.generate("night market poster", ["red-ribbon"], True)
        workflow.review(first.draft_id, "reject", "composition unclear")

        second = workflow.regenerate(first.draft_id)

        self.assertEqual(second.provenance.parent_id, first.draft_id)
        self.assertEqual(second.provenance.asset_ids, ("red-ribbon",))
        self.assertIs(second.status, Status.DRAFT)


if __name__ == "__main__":
    unittest.main()

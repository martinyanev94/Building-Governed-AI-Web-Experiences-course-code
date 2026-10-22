from creative_workflow import CreativeWorkflow


def main() -> None:
    workflow = CreativeWorkflow()
    draft = workflow.generate(
        prompt="night market poster",
        asset_ids=["red-ribbon"],
        consent_given=True,
    )
    workflow.review(draft.draft_id, "approve", "Disclosure and composition reviewed")
    print(workflow.submit(draft.draft_id))


if __name__ == "__main__":
    main()

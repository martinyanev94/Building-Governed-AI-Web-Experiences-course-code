from dataclasses import dataclass
from enum import Enum
from typing import Optional


class Status(str, Enum):
    DRAFT = "draft"
    APPROVED = "approved"
    REJECTED = "rejected"


@dataclass(frozen=True)
class Provenance:
    prompt: str
    asset_ids: tuple[str, ...]
    consent_given: bool
    disclosure: str
    parent_id: Optional[str] = None


@dataclass
class CreativeDraft:
    draft_id: str
    content: str
    provenance: Provenance
    status: Status = Status.DRAFT
    review_note: str = ""


class CreativeWorkflow:
    def __init__(self):
        self.drafts: dict[str, CreativeDraft] = {}
        self._next_id = 1

    def generate(
        self, prompt: str, asset_ids: list[str], consent_given: bool
    ) -> CreativeDraft:
        if not prompt.strip():
            raise ValueError("prompt is required")
        if not consent_given:
            raise PermissionError("consent is required before generation")

        draft_id = f"D{self._next_id}"
        self._next_id += 1
        provenance = Provenance(
            prompt=prompt,
            asset_ids=tuple(asset_ids),
            consent_given=consent_given,
            disclosure="AI-assisted creative draft",
        )
        draft = CreativeDraft(
            draft_id=draft_id,
            content=f"Draft for: {prompt}",
            provenance=provenance,
        )
        self.drafts[draft_id] = draft
        return draft

    def review(self, draft_id: str, decision: str, note: str) -> CreativeDraft:
        draft = self.drafts[draft_id]
        if draft.status is not Status.DRAFT:
            raise ValueError("only draft items can be reviewed")
        if decision not in {"approve", "reject"} or not note.strip():
            raise ValueError("decision and review note are required")

        draft.status = (
            Status.APPROVED if decision == "approve" else Status.REJECTED
        )
        draft.review_note = note
        return draft

    def regenerate(self, draft_id: str) -> CreativeDraft:
        original = self.drafts[draft_id]
        if original.status is not Status.REJECTED:
            raise ValueError("only rejected drafts can be regenerated")

        new_id = f"D{self._next_id}"
        self._next_id += 1
        provenance = Provenance(
            prompt=original.provenance.prompt,
            asset_ids=original.provenance.asset_ids,
            consent_given=original.provenance.consent_given,
            disclosure=original.provenance.disclosure,
            parent_id=original.draft_id,
        )
        draft = CreativeDraft(
            draft_id=new_id,
            content=f"Regenerated draft for: {provenance.prompt}",
            provenance=provenance,
        )
        self.drafts[new_id] = draft
        return draft

    def submit(self, draft_id: str) -> str:
        draft = self.drafts[draft_id]
        if draft.status is not Status.APPROVED:
            raise PermissionError("only approved drafts can be submitted")
        return draft.content

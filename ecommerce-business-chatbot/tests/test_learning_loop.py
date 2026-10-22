from src.learning_loop import (
    Feedback,
    ImprovementProposal,
    activate,
    approve_release,
    evaluate_candidate,
    propose_improvement,
)


def test_proposal_requires_two_allowed_corrections():
    feedback = [
        Feedback("wrong_product", "1.4"),
        Feedback("wrong_product", "1.4"),
    ]
    proposal = propose_improvement(feedback, "1.4")
    assert proposal == ImprovementProposal("1.5", "review recommendation matching")


def test_unknown_feedback_does_not_trigger_change():
    feedback = [Feedback("free_form_comment", "1.4")]
    assert propose_improvement(feedback, "1.4") is None


def test_regression_holds_current_version():
    proposal = ImprovementProposal("1.5", "review recommendation matching")
    evaluation = evaluate_candidate(0.82, 0.78, True)
    approved = approve_release(proposal, evaluation)
    active_version, record = activate("1.4", proposal, approved)
    assert active_version == "1.4"
    assert record.decision == "held"


def test_approved_candidate_activates_new_version():
    proposal = ImprovementProposal("1.5", "review recommendation matching")
    evaluation = evaluate_candidate(0.82, 0.78, False)
    approved = approve_release(proposal, evaluation)
    active_version, record = activate("1.4", proposal, approved)
    assert active_version == "1.5"
    assert record.decision == "activated"

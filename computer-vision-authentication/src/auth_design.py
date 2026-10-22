from dataclasses import dataclass
from typing import Literal

AuthState = Literal["verified", "uncertain", "fallback"]


@dataclass(frozen=True)
class AuthResult:
    state: AuthState
    message: str
    retained_image: bool
    audit_event: str


def evaluate_visual_auth(
    verification: str,
    camera_available: bool,
    prepared: bool,
    retain_image: bool,
) -> AuthResult:
    if not camera_available:
        return AuthResult(
            "fallback",
            "Use another sign-in method.",
            False,
            "camera_unavailable",
        )
    if not prepared:
        return AuthResult(
            "fallback",
            "We could not read that image. Try another method.",
            False,
            "preprocessing_failed",
        )
    if verification == "verified" and not retain_image:
        return AuthResult(
            "verified",
            "Continue to authorization.",
            False,
            "visual_verified",
        )
    return AuthResult(
        "uncertain",
        "Use another sign-in method.",
        False,
        "visual_uncertain",
    )

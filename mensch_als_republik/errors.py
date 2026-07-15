"""Fehlerklassen für den Claim-Verifizierer (Anhang B.2)."""

from __future__ import annotations

from enum import Enum


class ErrorCode(str, Enum):
    UNSUPPORTED_VERSION = "UNSUPPORTED_VERSION"
    NON_CANONICAL_ENCODING = "NON_CANONICAL_ENCODING"
    MALFORMED_CBOR = "MALFORMED_CBOR"
    UNKNOWN_J_TAG = "UNKNOWN_J_TAG"
    UNKNOWN_NAMESPACE = "UNKNOWN_NAMESPACE"
    BAD_SCOPE_BINDING = "BAD_SCOPE_BINDING"
    RESERVED_CORE_PREDICATE = "RESERVED_CORE_PREDICATE"
    FOREIGN_LIFECYCLE = "FOREIGN_LIFECYCLE"
    BAD_SIGNATURE = "BAD_SIGNATURE"
    INVALID_GENESIS_ANCHOR = "INVALID_GENESIS_ANCHOR"
    INCOHERENT_EXPIRY = "INCOHERENT_EXPIRY"


class VerifierError(Exception):
    """Basis für strukturelle Rejects (Anhang B.2)."""

    code: ErrorCode

    def __init__(self, code: ErrorCode | None = None) -> None:
        if code is not None:
            self.code = code
        super().__init__(self.code.value)


class UnsupportedVersion(VerifierError):
    code = ErrorCode.UNSUPPORTED_VERSION


class NonCanonicalEncoding(VerifierError):
    code = ErrorCode.NON_CANONICAL_ENCODING


class MalformedCbor(VerifierError):
    code = ErrorCode.MALFORMED_CBOR


class UnknownJTag(VerifierError):
    code = ErrorCode.UNKNOWN_J_TAG


class UnknownNamespace(VerifierError):
    code = ErrorCode.UNKNOWN_NAMESPACE


class BadScopeBinding(VerifierError):
    code = ErrorCode.BAD_SCOPE_BINDING


class ReservedCorePredicate(VerifierError):
    code = ErrorCode.RESERVED_CORE_PREDICATE


class ForeignLifecycle(VerifierError):
    code = ErrorCode.FOREIGN_LIFECYCLE


class BadSignature(VerifierError):
    code = ErrorCode.BAD_SIGNATURE


class InvalidGenesisAnchor(VerifierError):
    code = ErrorCode.INVALID_GENESIS_ANCHOR


class IncoherentExpiry(VerifierError):
    code = ErrorCode.INCOHERENT_EXPIRY

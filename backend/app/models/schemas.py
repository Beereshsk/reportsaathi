"""
Aushadha Sathi - Ephemeral Pydantic Schemas & Transfer Models
Reference: docs/06a-api-contract.md & docs/08-tasks.md (Task 01)
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict, List, Literal, Optional, cast

# Dual-support: Pydantic v2 if installed; robust dataclass fallback if not yet installed in local sandbox.
try:
    from pydantic import BaseModel, ConfigDict, Field

    class BaseSchema(BaseModel):
        model_config = ConfigDict(extra="ignore", populate_by_name=True)

        def to_dict(self) -> Dict[str, Any]:
            return self.model_dump()

    USING_PYDANTIC = True

except ImportError:
    from dataclasses import asdict, dataclass, field

    class BaseSchema:  # type: ignore[no-redef]
        def to_dict(self) -> Dict[str, Any]:
            return cast(Dict[str, Any], asdict(cast(Any, self)))

        def model_dump(self) -> Dict[str, Any]:
            return cast(Dict[str, Any], asdict(cast(Any, self)))

        def dict(self) -> Dict[str, Any]:
            return cast(Dict[str, Any], asdict(cast(Any, self)))

    USING_PYDANTIC = False


if USING_PYDANTIC:
    class TimingSlot(BaseSchema):  # type: ignore[no-redef]
        morning: int = Field(default=0, ge=0)
        afternoon: int = Field(default=0, ge=0)
        night: int = Field(default=0, ge=0)

    class DisplayText(BaseSchema):  # type: ignore[no-redef]
        kn: str
        en: str

    class MedicineItem(BaseSchema):  # type: ignore[no-redef]
        id: str
        raw_name: str
        canonical_name: Optional[str] = None
        form: Literal["tablet", "capsule", "syrup", "injection", "ointment", "other"] = "tablet"
        dosage: str
        timing: TimingSlot
        meal_relation: Literal["before_food", "after_food", "with_food", "unspecified"] = "unspecified"
        duration_days: Optional[int] = None
        confidence: float = Field(default=1.0, ge=0.0, le=1.0)
        is_ambiguous: bool = False
        ambiguity_reason: Optional[str] = None
        display_text: Optional[DisplayText] = None

    class PrescriptionRequest(BaseSchema):  # type: ignore[no-redef]
        image_base64: Optional[str] = None
        raw_text: Optional[str] = None
        language: Literal["kn", "en"] = "kn"

    class ExtractionResponse(BaseSchema):  # type: ignore[no-redef]
        success: bool = True
        request_id: Optional[str] = None
        total_medicines_detected: int = 0
        has_ambiguous_entries: bool = False
        language: Literal["kn", "en"] = "kn"
        medicines: List[MedicineItem] = Field(default_factory=list)
        disclaimer: str = (
            "Please confirm all medicine details with your doctor or pharmacist "
            "before taking any medicine."
        )
        timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    class SimplifyRequest(BaseSchema):  # type: ignore[no-redef]
        terms: List[str]
        language: Literal["kn", "en"] = "kn"

    class SimplifiedTerm(BaseSchema):  # type: ignore[no-redef]
        term: str
        meaning_en: str
        meaning_kn: str

    class SimplifyResponse(BaseSchema):  # type: ignore[no-redef]
        success: bool = True
        simplified_terms: List[SimplifiedTerm] = Field(default_factory=list)

    class DatabaseHealth(BaseSchema):  # type: ignore[no-redef]
        status: Literal["connected", "disconnected", "unconfigured"]
        value: str

    class HealthResponse(BaseSchema):  # type: ignore[no-redef]
        status: Literal["pass", "fail"] = "pass"
        service: str = "aushadha-sathi-api"
        version: str = "1.0.0"
        timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
        database: DatabaseHealth

    class ErrorResponse(BaseSchema):  # type: ignore[no-redef]
        success: bool = False
        error_code: str
        message: str
        tips: Optional[List[str]] = None

else:
    from dataclasses import dataclass, field

    @dataclass
    class TimingSlot(BaseSchema):  # type: ignore[no-redef]
        morning: int = 0
        afternoon: int = 0
        night: int = 0

    @dataclass
    class DisplayText(BaseSchema):  # type: ignore[no-redef]
        kn: str
        en: str

    @dataclass
    class MedicineItem(BaseSchema):  # type: ignore[no-redef]
        id: str
        raw_name: str
        dosage: str
        timing: TimingSlot
        canonical_name: Optional[str] = None
        form: str = "tablet"
        meal_relation: str = "unspecified"
        duration_days: Optional[int] = None
        confidence: float = 1.0
        is_ambiguous: bool = False
        ambiguity_reason: Optional[str] = None
        display_text: Optional[DisplayText] = None

    @dataclass
    class PrescriptionRequest(BaseSchema):  # type: ignore[no-redef]
        image_base64: Optional[str] = None
        raw_text: Optional[str] = None
        language: str = "kn"

    @dataclass
    class ExtractionResponse(BaseSchema):  # type: ignore[no-redef]
        success: bool = True
        request_id: Optional[str] = None
        total_medicines_detected: int = 0
        has_ambiguous_entries: bool = False
        language: str = "kn"
        medicines: List[MedicineItem] = field(default_factory=list)
        disclaimer: str = (
            "Please confirm all medicine details with your doctor or pharmacist "
            "before taking any medicine."
        )
        timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    @dataclass
    class SimplifyRequest(BaseSchema):  # type: ignore[no-redef]
        terms: List[str] = field(default_factory=list)
        language: str = "kn"

    @dataclass
    class SimplifiedTerm(BaseSchema):  # type: ignore[no-redef]
        term: str = ""
        meaning_en: str = ""
        meaning_kn: str = ""

    @dataclass
    class SimplifyResponse(BaseSchema):  # type: ignore[no-redef]
        success: bool = True
        simplified_terms: List[SimplifiedTerm] = field(default_factory=list)

    @dataclass
    class DatabaseHealth(BaseSchema):  # type: ignore[no-redef]
        status: str = "connected"
        value: str = ""

    @dataclass
    class HealthResponse(BaseSchema):  # type: ignore[no-redef]
        database: DatabaseHealth
        status: str = "pass"
        service: str = "aushadha-sathi-api"
        version: str = "1.0.0"
        timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    @dataclass
    class ErrorResponse(BaseSchema):  # type: ignore[no-redef]
        error_code: str
        message: str
        success: bool = False
        tips: Optional[List[str]] = None

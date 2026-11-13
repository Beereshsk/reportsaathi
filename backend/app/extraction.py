"""Conservative parsing of explicitly typed prescription instructions.

This module does not identify brands, diagnose conditions, translate text, or infer
missing instructions. Unrecognized or incomplete lines remain visible and flagged.
"""

import re
from typing import Literal, Optional, Tuple, cast

from .models.schemas import MedicineItem, TimingSlot

MedicineForm = Literal["tablet", "capsule", "syrup", "injection", "ointment", "other"]
MealRelation = Literal["before_food", "after_food", "with_food", "unspecified"]

FREQUENCY_PATTERN = re.compile(
    r"(?<!\w)(?P<schedule>\d\s*[-–]\s*\d\s*[-–]\s*\d|"
    r"BID|BD|TID|TDS|OD|HS)(?!\w)",
    re.IGNORECASE,
)
STRENGTH_PATTERN = re.compile(r"\b\d+(?:\.\d+)?\s*(?:mg|mcg|g|ml)\b", re.IGNORECASE)
DURATION_PATTERN = re.compile(r"\b(?:for\s+)?(\d+)\s+days?\b", re.IGNORECASE)
MEAL_PATTERN = re.compile(r"\b(before|after|with)\s+(?:the\s+)?(food|meals?|breakfast)\b", re.IGNORECASE)


def _parse_timing(line: str) -> Tuple[TimingSlot, bool]:
    match = FREQUENCY_PATTERN.search(line)
    if not match:
        return TimingSlot(morning=0, afternoon=0, night=0), False

    schedule = re.sub(r"\s+", "", match.group("schedule")).upper()
    if re.fullmatch(r"\d-\d-\d", schedule):
        morning, afternoon, night = (int(value) for value in schedule.split("-"))
    else:
        slots = {
            "OD": (1, 0, 0),
            "BD": (1, 0, 1),
            "BID": (1, 0, 1),
            "TDS": (1, 1, 1),
            "TID": (1, 1, 1),
            "HS": (0, 0, 1),
        }
        if schedule not in slots:
            return TimingSlot(morning=0, afternoon=0, night=0), False
        morning, afternoon, night = slots[schedule]
    return TimingSlot(morning=morning, afternoon=afternoon, night=night), True


def _parse_meal_relation(line: str) -> MealRelation:
    if re.search(r"\b(?:AC|BBF)\b", line, re.IGNORECASE):
        return "before_food"
    if re.search(r"\b(?:PC|AF)\b", line, re.IGNORECASE):
        return "after_food"
    match = MEAL_PATTERN.search(line)
    if not match:
        return "unspecified"
    return cast(
        MealRelation,
        {"before": "before_food", "after": "after_food", "with": "with_food"}[match.group(1).lower()],
    )


def _medicine_prefix(line: str) -> Tuple[str, str, MedicineForm]:
    schedule_match = FREQUENCY_PATTERN.search(line)
    prefix = line[: schedule_match.start()] if schedule_match else line
    prefix = prefix.strip(" \t-–,:;")

    form: MedicineForm = "other"
    form_match = re.match(r"^(tab(?:let)?|cap(?:sule)?|syr(?:up)?|inj(?:ection)?)\.?\s+", prefix, re.IGNORECASE)
    if form_match:
        form = cast(MedicineForm, {
            "tab": "tablet",
            "tablet": "tablet",
            "cap": "capsule",
            "capsule": "capsule",
            "syr": "syrup",
            "syrup": "syrup",
            "inj": "injection",
            "injection": "injection",
        }[form_match.group(1).lower()])
        prefix = prefix[form_match.end() :].strip()

    strength_match = STRENGTH_PATTERN.search(prefix)
    dosage: Optional[str] = None
    if strength_match:
        dosage = re.sub(r"\s+", "", strength_match.group(0))
    else:
        number_match = re.search(r"\s+(\d+(?:\.\d+)?)\s*$", prefix)
        if number_match:
            dosage = number_match.group(1)

    raw_name = prefix.strip(" \t-–,:;") or line
    return raw_name, dosage or "Unclear / not provided", form


def parse_manual_prescription(raw_text: str) -> list[MedicineItem]:
    """Parse only explicit strength, timing, meal relation, and duration tokens."""
    medicines = []
    for line_number, line in enumerate(raw_text.splitlines(), start=1):
        raw_line = line.strip()
        if not raw_line:
            continue

        raw_name, dosage, form = _medicine_prefix(raw_line)
        timing, has_timing = _parse_timing(raw_line)
        duration_match = DURATION_PATTERN.search(raw_line)
        duration_days = int(duration_match.group(1)) if duration_match else None
        missing = []
        if dosage == "Unclear / not provided":
            missing.append("dose or strength")
        if not has_timing:
            missing.append("timing")

        ambiguous = bool(missing)
        reason = None
        if ambiguous:
            reason = (
                f"Could not clearly identify {', '.join(missing)} from the entered text. "
                "Please verify this line with your doctor or pharmacist."
            )

        medicines.append(
            MedicineItem(
                id=f"med-{line_number}",
                raw_name=raw_name,
                canonical_name=None,
                form=form,
                dosage=dosage,
                timing=timing,
                meal_relation=_parse_meal_relation(raw_line),
                duration_days=duration_days,
                confidence=0.5 if ambiguous else 1.0,
                is_ambiguous=ambiguous,
                ambiguity_reason=reason,
                display_text=None,
            )
        )
    return medicines

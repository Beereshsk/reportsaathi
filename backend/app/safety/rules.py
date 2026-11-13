"""
Aushadha Sathi - Medical Safety Rules & Clinical Guardrails
Reference: docs/06b-safety-rules.md & docs/AGENT.md
All red-flag decisions are deterministic code in backend/safety/, never by LLM/AI.
"""

from typing import Optional, Tuple


def check_dosage_sanity(medicine_name: str, dose_mg: Optional[float], daily_frequency: int) -> Tuple[bool, Optional[str]]:
    """
    Checks clinical dosage boundaries according to docs/06b-safety-rules.md §4.
    Returns (is_safe, error_or_warning_reason)
    """
    # Rule: Daily tablet frequency > 4 doses per day -> possible overdose risk
    if daily_frequency > 4:
        return False, "Prescribed dose exceeds safe clinical bounds (>4 doses/day). Mandatory pharmacist confirmation required."

    # Rule: Paracetamol single dose > 1000mg or daily > 4000mg
    if "paracetamol" in medicine_name.lower():
        if dose_mg and dose_mg > 1000:
            return False, "Paracetamol single dose exceeds 1000mg safety limit."
        if dose_mg and (dose_mg * daily_frequency) > 4000:
            return False, "Prescribed dose exceeds safe clinical bounds (>4000mg/day or >4 doses/day). Mandatory pharmacist confirmation required."

    return True, None


def check_adversarial_prompt(text: str) -> Tuple[bool, Optional[str]]:
    """
    Detects adversarial diagnosis or dose alteration attempts (SR-01, SR-02, NG-1, NG-2).
    Refuses autonomous diagnosis and dosage titrations.
    """
    lower = text.lower()
    diagnosis_triggers = ["does he have", "do i have", "diagnose", "tuberculosis", "cancer", "infection?"]
    alteration_triggers = ["reduce the dose", "increase the dose", "tell me to stop", "stop it"]

    for trigger in diagnosis_triggers:
        if trigger in lower:
            return False, "DIAGNOSIS_REFUSAL: The system cannot diagnose medical conditions. Please consult a registered medical practitioner."

    for trigger in alteration_triggers:
        if trigger in lower:
            return False, "DOSE_ALTERATION_REFUSAL: The system cannot alter or stop prescribed medications. Contact the prescribing doctor immediately."

    return True, None

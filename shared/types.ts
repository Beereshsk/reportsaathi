/**
 * Aushadha Sathi - Shared Contract Types
 * Reference: docs/06a-api-contract.md
 * 
 * Standard: OpenAPI 3.1.0 Compatible
 * Security & Privacy: Ephemeral in-memory processing, DPDP Act 2023 compliant
 */

export type SupportedLanguage = "kn" | "en";

export type MedicineForm = 
  | "tablet" 
  | "capsule" 
  | "syrup" 
  | "injection" 
  | "ointment" 
  | "other";

export type MealRelation = 
  | "before_food" 
  | "after_food" 
  | "with_food" 
  | "unspecified";

export interface TimingSlot {
  morning: number;
  afternoon: number;
  night: number;
}

export interface DisplayText {
  kn: string;
  en: string;
}

export interface MedicineItem {
  id: string;
  raw_name: string;
  canonical_name?: string;
  form: MedicineForm;
  dosage: string;
  timing: TimingSlot;
  meal_relation: MealRelation;
  duration_days: number | null;
  confidence: number;
  is_ambiguous: boolean;
  ambiguity_reason?: string;
  display_text?: DisplayText;
}

export interface PrescriptionRequest {
  image_base64?: string;
  raw_text?: string;
  language?: SupportedLanguage;
}

export interface ExtractionResponse {
  success: boolean;
  request_id?: string;
  total_medicines_detected: number;
  has_ambiguous_entries: boolean;
  language: SupportedLanguage;
  medicines: MedicineItem[];
  disclaimer: string;
  timestamp: string;
}

export interface SimplifyRequest {
  terms: string[];
  language?: SupportedLanguage;
}

export interface SimplifiedTerm {
  term: string;
  meaning_en: string;
  meaning_kn: string;
}

export interface SimplifyResponse {
  success: boolean;
  simplified_terms: SimplifiedTerm[];
}

export interface PrescriptionNotesRequest {
  raw_text: string;
  language?: SupportedLanguage;
}

export interface PrescriptionNotesResponse {
  success: boolean;
  request_id: string;
  notes_text: string;
  language: SupportedLanguage;
  disclaimer: string;
}

export interface DatabaseHealth {
  status: "connected" | "disconnected" | "unconfigured";
  value: string;
}

export interface HealthResponse {
  status: "pass" | "fail";
  service: string;
  version: string;
  timestamp: string;
  database: DatabaseHealth;
}

export type ErrorCode = 
  | "INVALID_REQUEST"
  | "INVALID_FILE_TYPE" 
  | "PAYLOAD_TOO_LARGE" 
  | "BLURRY_PRESCRIPTION" 
  | "RATE_LIMIT_EXCEEDED"
  | "INTERNAL_SERVER_ERROR";

export interface ErrorResponse {
  success: false;
  error_code: ErrorCode;
  message: string;
  tips?: string[];
}

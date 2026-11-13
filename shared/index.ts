export * from "./types.js";

export const ERROR_CODES = {
  INVALID_REQUEST: "INVALID_REQUEST",
  INVALID_FILE_TYPE: "INVALID_FILE_TYPE",
  PAYLOAD_TOO_LARGE: "PAYLOAD_TOO_LARGE",
  BLURRY_PRESCRIPTION: "BLURRY_PRESCRIPTION",
  RATE_LIMIT_EXCEEDED: "RATE_LIMIT_EXCEEDED",
  INTERNAL_SERVER_ERROR: "INTERNAL_SERVER_ERROR",
} as const;

export const STATUTORY_DISCLAIMER =
  "Please confirm all medicine details with your doctor or pharmacist before taking any medicine.";

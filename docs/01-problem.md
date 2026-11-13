# Problem Statement: Aushadha Sathi – Smart Prescription Assistant

## 1. Project Overview

Aushadha Sathi is a simple, mobile-friendly web application designed to help elderly people and patients understand their doctor's prescriptions. Many people struggle to read handwritten prescriptions, understand medical terms, and remember when to take their medicines.

The application uses AI-powered image recognition and natural language processing to extract medicine information from prescription images and convert it into simple, easy-to-understand instructions in the user's preferred language.

The main goal is to make prescription information accessible to everyone, especially older adults who have difficulty reading small text or understanding medical terminology.

## 2. Target Users

The application is mainly designed for:
- Elderly people who have difficulty reading prescriptions.
- Patients who are unfamiliar with medical terminology.
- People who prefer understanding medical instructions in their native language.
- Family members who help elderly patients manage their medicines.

## 3. Main Features

### Feature 1: Prescription Input
Users can provide prescription information through three methods:
- Capture a prescription using their smartphone camera.
- Upload an existing prescription image.
- Manually enter prescription text.

### Feature 2: AI-Based Prescription Reading
- Extract medicine names and instructions using OCR and AI vision.
- Identify dosage, frequency, and duration when clearly available.
- Detect unclear handwriting or missing information.
- Highlight unreadable information instead of making assumptions.

### Feature 3: Simple Medicine Explanation
For every identified medicine, display a separate information card containing:

- Medicine name and easy pronunciation.
- General purpose of the medicine.
- Prescribed quantity and dosage.
- Morning, afternoon, or night schedule.
- Before-food or after-food instructions, if specified.
- Duration of the prescription.
- Common side effects and precautions from reliable medicine information sources.

### Feature 4: Regional Language Support
- Support Kannada and English initially.
- Display explanations in the selected language.
- Use simple words that are easy for elderly people to understand.
- Provide a text-to-speech feature to read medicine instructions aloud.

### Feature 5: Family Assistance
- Provide an option to share the medicine summary through WhatsApp.
- Allow family members to help elderly patients understand their prescriptions.

## 4. Application Workflow

The application follows a simple three-step workflow:

**Step 1: Home Screen**
- Select the preferred language.
- Choose camera, image upload, or manual text input.
- Use a large and clearly visible button.

**Step 2: Prescription Processing**
- Extract text from the prescription.
- Identify medicine information.
- Translate medical instructions into simple language.
- Flag unclear or potentially risky information.

**Step 3: Medicine Information**
- Display each medicine in a separate card.
- Show dosage and timing with recognizable symbols and text.
- Provide a read-aloud option.
- Allow sharing the summary with family members.

## 5. Safety and Privacy Requirements

- The application must never independently diagnose a medical condition.
- It must not change, recommend, or discontinue prescribed doses.
- Unclear medicine names and dosage information must be highlighted.
- Potentially unusual doses must be flagged for pharmacist verification.
- Users must be advised to confirm prescription details with their doctor or pharmacist.
- Prescription images and personal information must not be permanently stored.
- Temporary prescription data must be discarded after processing.
- Medicine explanations must not replace professional medical advice.

**Mandatory Safety Message:**

> "Please confirm all medicine details with your doctor or pharmacist before taking any medicine."

## 6. Accessibility Requirements

- Mobile-first responsive design.
- Large text with adjustable font sizes.
- High-contrast colors for better visibility.
- Large buttons with a minimum touch target of 56px.
- Simple navigation with minimal steps.
- Native-language labels and easy-to-understand instructions.
- Voice-based reading for users with weak eyesight.
- Lightweight design suitable for basic smartphones and slow internet connections.

## 7. Technology Stack

| Component | Technology |
|---|---|
| Frontend | HTML, CSS, JavaScript |
| UI Framework | React.js |
| Backend | Python Flask |
| AI Integration | Claude API with Vision |
| Image Processing | OCR / AI Vision |
| Translation | AI-powered translation |
| Text-to-Speech | Web Speech API |
| Sharing | WhatsApp Share API |
| Deployment | Vercel / Render |

## 8. Expected Outcome

The expected outcome is a user-friendly prescription assistance application that converts difficult prescription information into simple, readable, and spoken instructions.

It aims to reduce confusion among elderly patients, improve access to prescription information, and help family members support their loved ones.

The application will act as a prescription understanding assistant, not as a replacement for doctors or pharmacists.

## 9. Project Goal

**"Making medicine instructions easier to understand, one prescription at a time."**

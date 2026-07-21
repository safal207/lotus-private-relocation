"use strict";

const form = document.querySelector("#intake-form");
const resultPanel = document.querySelector("#result");
const jsonPreview = document.querySelector("#json-preview");
const downloadButton = document.querySelector("#download-json");
const resetButton = document.querySelector("#reset-form");
const errorBox = document.querySelector("#form-error");
const serviceInterest = document.querySelector("#service-interest");
const packageLinks = document.querySelectorAll("[data-package]");

let currentBrief = null;

function createCaseId() {
  const randomValues = new Uint32Array(2);
  crypto.getRandomValues(randomValues);
  const timePart = Date.now().toString(36).toUpperCase();
  const randomPart = Array.from(randomValues, (value) => value.toString(36).toUpperCase())
    .join("")
    .slice(0, 10);
  return `LPR-${timePart}-${randomPart}`;
}

function selectedDependencies() {
  return Array.from(
    document.querySelectorAll('input[name="dependencies"]:checked'),
    (input) => input.value
  );
}

function readTrimmedValue(selector) {
  return document.querySelector(selector).value.trim();
}

function containsSensitiveDocumentLanguage(values) {
  const combined = values.join(" ").toLowerCase();
  const blockedPatterns = [
    /passport\s*(number|no|#|:)/,
    /bank\s*(account|statement|details)/,
    /credit\s*card/,
    /source[-\s]of[-\s]funds\s*(document|file|statement)/,
    /tax\s*return/,
    /password\s*:/,
    /api[-_\s]*key\s*:/,
    /access[-_\s]*token\s*:/
  ];
  return blockedPatterns.some((pattern) => pattern.test(combined));
}

function buildBrief() {
  const now = new Date().toISOString();
  const contactReference = readTrimmedValue("#contact-reference");
  const languagePreference = readTrimmedValue("#language-preference");

  const brief = {
    case_id: createCaseId(),
    service_interest: serviceInterest.value,
    preferred_name: readTrimmedValue("#preferred-name"),
    contact_channel: document.querySelector("#contact-channel").value,
    contact_reference: contactReference,
    current_country_or_timezone: readTrimmedValue("#current-location"),
    target_destination: readTrimmedValue("#target-destination"),
    purpose: document.querySelector("#purpose").value,
    budget_range: document.querySelector("#budget-range").value,
    timing: document.querySelector("#timing").value,
    dependencies: selectedDependencies(),
    lead_source: "static_private_discovery_prototype",
    contact_consent: {
      granted: true,
      recorded_at: now,
      channel: "static_browser_form"
    },
    qualification_state: "NEW",
    created_at: now
  };

  if (languagePreference) {
    brief.language_preference = languagePreference;
  }

  return brief;
}

function showError(message) {
  errorBox.textContent = message;
  resultPanel.hidden = true;
  currentBrief = null;
}

function clearError() {
  errorBox.textContent = "";
}

function renderBrief(brief) {
  currentBrief = brief;
  jsonPreview.textContent = JSON.stringify(brief, null, 2);
  resultPanel.hidden = false;
  resultPanel.scrollIntoView({ behavior: "smooth", block: "start" });
}

packageLinks.forEach((link) => {
  link.addEventListener("click", () => {
    const packageValue = link.dataset.package;
    if (packageValue && serviceInterest.querySelector(`option[value="${packageValue}"]`)) {
      serviceInterest.value = packageValue;
    }
  });
});

form.addEventListener("submit", (event) => {
  event.preventDefault();
  clearError();

  if (!form.checkValidity()) {
    form.reportValidity();
    showError("Complete the required fields and confirm contact consent.");
    return;
  }

  const freeTextValues = [
    readTrimmedValue("#preferred-name"),
    readTrimmedValue("#contact-reference"),
    readTrimmedValue("#current-location"),
    readTrimmedValue("#target-destination"),
    readTrimmedValue("#language-preference")
  ];

  if (containsSensitiveDocumentLanguage(freeTextValues)) {
    showError(
      "Sensitive financial, identity, tax, or credential data appears to be present. Remove it before generating the brief."
    );
    return;
  }

  renderBrief(buildBrief());
});

downloadButton.addEventListener("click", () => {
  if (!currentBrief) {
    showError("Generate a brief before downloading it.");
    return;
  }

  const blob = new Blob([`${JSON.stringify(currentBrief, null, 2)}\n`], {
    type: "application/json"
  });
  const objectUrl = URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = objectUrl;
  link.download = `${currentBrief.case_id.toLowerCase()}-discovery.json`;
  document.body.appendChild(link);
  link.click();
  link.remove();
  URL.revokeObjectURL(objectUrl);
});

resetButton.addEventListener("click", () => {
  clearError();
  currentBrief = null;
  resultPanel.hidden = true;
  jsonPreview.textContent = "";
});

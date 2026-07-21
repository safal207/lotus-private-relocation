# CRM Pipeline

## Purpose

Define a transparent journey from first enquiry to closed referral outcome while keeping regulated decisions and transaction execution with the appropriate licensed or qualified partner.

## Core records

The private system of record should separate:

- **Contact** — how to reach a person and their communication consent;
- **Case** — the relocation or property objective;
- **Introduction** — a consented handoff to a named partner;
- **Partner** — authority, scope, agreement, quality, and risk status;
- **Opportunity** — the commercial referral or coordination outcome;
- **Evidence** — source, date, owner, confidence, and verification status;
- **Activity** — calls, messages, decisions, and next actions.

Do not store client personal data, contracts, or compliance documents in the public GitHub repository.

## Case stages

### 1. NEW_ENQUIRY

A new request has been received.

Required before exit:

- contact consent;
- valid communication channel;
- initial purpose and destination.

### 2. QUALIFICATION

The team determines whether a discovery call is useful.

Required before exit:

- broad budget range;
- timing;
- major dependencies;
- fit or non-fit decision;
- no unresolved immediate compliance hold.

### 3. DISCOVERY

A structured conversation clarifies goals, constraints, decision-makers, risks, and adviser needs.

Required before exit:

- written goal statement;
- confirmed requirements;
- assumptions and open questions;
- proposed partner categories;
- explicit next step.

### 4. PARTNER_MATCHING

One or more verified partners are considered.

Required before exit:

- partner status is PILOT or ACTIVE;
- authority and service scope are relevant;
- compensation and conflict model are known;
- data role is known;
- partner review is not expired.

### 5. INTRODUCTION_CONSENT

The client reviews the proposed introduction.

Required before exit:

- named recipient organisation;
- purpose of introduction;
- minimum data fields to share;
- affirmative consent timestamp;
- consent channel;
- withdrawal route.

### 6. INTRODUCED

The handoff has been sent and acknowledged.

Required before exit:

- introduction timestamp;
- sender and recipient owners;
- partner acknowledgement;
- expected response time;
- client-visible next action.

### 7. PARTNER_CONSULTATION

The licensed or qualified provider leads their part of the journey.

Lotus may coordinate status and communication but must not convert partner advice into its own professional advice.

### 8. OPTIONS_REVIEW

The client considers locations, properties, structures, schools, or other options based on professional input.

Required controls:

- source and date for material claims;
- confirmed facts separated from estimates and hypotheses;
- no guaranteed outcomes;
- unresolved legal, tax, immigration, banking, or compliance questions assigned to a qualified owner.

### 9. CLIENT_DECISION

The client decides whether to proceed, pause, change direction, or stop.

Possible outcomes:

- proceed with partner;
- request alternatives;
- defer;
- withdraw;
- not suitable;
- compliance hold.

### 10. PARTNER_EXECUTION

A licensed or qualified provider handles regulated or specialist execution.

Lotus does not:

- reserve or sell property;
- sign for the client;
- hold client money;
- approve legal, tax, immigration, banking, financing, compliance, or investment decisions.

### 11. OUTCOME_CONFIRMED

The partner reports the contractually relevant outcome with sufficient evidence.

Examples:

- consultation completed;
- representation agreement signed;
- property reservation confirmed by the executing party;
- transaction completed;
- service declined or cancelled.

### 12. COMMISSION_PENDING

A written agreement indicates that a referral payment may be due.

Required before exit:

- paying legal entity;
- contractual payment trigger;
- partner-confirmed evidence;
- invoice or payment process;
- expected payment date;
- refund or cancellation exposure.

### 13. CLOSED_WON

The contractually defined service and commercial outcome are complete.

### 14. CLOSED_NO_TRANSACTION

The case ended without a transaction. Record the reason without pressuring the client to continue.

### 15. COMPLIANCE_HOLD

No commercial step may override this stage. A qualified compliance or legal owner must decide whether the case may resume.

## Opportunity fields

Each opportunity should include:

- case ID;
- partner ID;
- source channel;
- destination and service category;
- stage;
- stage entered at;
- next action, owner, and due date;
- consent state;
- authority-review state;
- compensation model;
- payment trigger;
- projected value clearly labelled as an estimate;
- confirmed earned value;
- payment state;
- risk flags;
- closure reason.

## Service-level alerts

Create alerts for:

- no response to a new enquiry;
- discovery call without documented output;
- introduction consent missing;
- partner acknowledgement overdue;
- partner licence or review expiring;
- open question without a qualified owner;
- client data shared beyond the consented scope;
- opportunity marked won without payment-trigger evidence;
- pressure to transfer funds outside the executing provider’s approved process.

## Reporting

Weekly reporting should separate:

### Confirmed

- new qualified cases;
- completed discovery calls;
- consent-complete introductions;
- partner acknowledgements;
- partner-reported consultations;
- contractually confirmed outcomes;
- earned and paid referral revenue.

### Forecast

- active opportunities;
- estimated transaction values;
- estimated referral revenue;
- expected dates.

Forecasts must never be presented as earned revenue.

## Ownership principle

Every open case has one Lotus coordination owner. Every regulated or specialist question has a named licensed or qualified partner owner. If ownership is unclear, the item remains blocked.

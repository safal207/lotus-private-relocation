# Pilot Handoff Protocol v0.1

## Goal

Prove that Lotus Private Relocation can coordinate one property or relocation introduction without acting as an unlicensed broker, transferring excessive data, or treating an unverified partner as active.

The first run is synthetic. A real-client pilot is prohibited until a named partner passes the activation gates in issue #2.

## Required records

Every handoff uses separate records for:

1. client intake;
2. partner authority and agreement status;
3. consent;
4. handoff;
5. acknowledgement;
6. evidence and next action.

The public repository contains synthetic records only. Real records belong in a private, access-controlled system of record.

## Fail-closed gates

A handoff may enter `INTRODUCED` only when all conditions are true:

- partner status is `PILOT` or `ACTIVE`;
- the partner's authority and service scope were checked;
- a written agreement or approved pilot arrangement exists;
- consent status is `GRANTED`;
- consent identifies the recipient, purpose, and exact data fields;
- the data set is the minimum needed for the agreed purpose;
- Lotus and partner owners are named;
- an introduction timestamp and evidence reference exist;
- the next action has an owner and due time;
- no compliance hold or unresolved blocking risk exists.

When any condition is missing, the record remains `DRAFT`, `READY_FOR_CONSENT`, or `BLOCKED`.

## Synthetic rehearsal

### Step 1 — qualify the case

Use a fictional case with no real person, contact, property, contract, or transaction.

### Step 2 — choose a synthetic partner

Use `LPR-P-SYN-001` with status `PILOT`. This does not represent or activate D&B Properties, Gaia Living, or any real company.

### Step 3 — prepare consent

Record:

- recipient organisation;
- introduction purpose;
- permitted data fields;
- consent text version;
- timestamp and channel;
- evidence reference;
- withdrawal route.

### Step 4 — create the handoff

The handoff references the consent record and includes only permitted fields. It names the Lotus owner, partner owner, evidence reference, and next action.

### Step 5 — validate

CI must confirm:

- both JSON Schemas are valid Draft 2020-12 schemas;
- positive synthetic fixtures pass;
- an `INTRODUCED` record with a `DUE_DILIGENCE` partner fails;
- an `INTRODUCED` record without granted consent fails;
- public examples contain no forbidden sensitive fields or real email addresses.

### Step 6 — acknowledge or block

A synthetic partner acknowledgement may move the record to `ACKNOWLEDGED`. Missing acknowledgement after the agreed SLA creates an escalation; it does not create permission to bypass the partner.

## Real-pilot entry criteria

A real-client pilot requires all of the following:

- issue #2 activation gates closed for the selected partner;
- partner record moved to `PILOT` with current evidence;
- private system of record approved;
- privacy notice and consent wording approved;
- cross-border data-transfer route approved;
- named KYC, AML, sanctions, beneficial-owner, and source-of-funds owner;
- synthetic rehearsal passed on the exact current head;
- no unresolved review thread or failed required check.

## Stop conditions

Stop and set `BLOCKED` or `COMPLIANCE_HOLD` when:

- the partner cannot evidence authority;
- the referral agreement is missing or materially unclear;
- the client withdraws consent;
- the requested data exceeds the consented scope;
- payment, deposit, or document collection is redirected outside an approved provider process;
- a person requests anonymity, regulatory avoidance, misleading documents, hidden ownership, or bypass of KYC/AML controls;
- Lotus is asked to provide regulated advice or execute a transaction.

## Success definition

The synthetic pilot succeeds when the exact-head CI proves the positive path works and the unsafe paths are rejected. Commercial conversion is not part of this technical pilot.

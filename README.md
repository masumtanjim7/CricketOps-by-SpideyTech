# CricketOps — by SpideyTech

> **Score once. Store once. Calculate once. Show everywhere.**

CricketOps is a real-time cricket operations, scoring engine, and broadcast platform engineered by **SpideyTech**. It replaces manual scorebooks, disconnected spreadsheets, and manually manipulated streaming graphics with an authoritative, ledger-backed data engine.

---

## 🏏 The Story Behind CricketOps

In local, corporate, academy, and district cricket across Bangladesh, scoring is often fragmented. Scorers grapple with unreliable cellular connectivity, tournament administrators struggle to calculate net run rates accurately, and live streamers waste effort hand-updating score bugs in OBS.

**SpideyTech** engineered CricketOps to resolve this foundational issue: **treat cricket scoring as a financial-grade transactional ledger, not a loose set of database records.** 

Every ball bowled is a permanent, immutable ledger entry. Live scores, career figures, bowling economies, partnership graphs, template commentary, and OBS broadcast overlays are derived directly from this single source of truth[cite: 1]. If a delivery is corrected or undone, the engine leaves an auditable trail and recalculates downstream aggregates without silent data loss[cite: 1].

---

## 🚀 Key Features

* **Authoritative Ball-by-Ball Delivery Ledger:** PostgreSQL-backed scoring engine with row-level locks, idempotency keys, and optimistic version checks to eliminate ghost deliveries or duplicate counts[cite: 1].
* **Real-Time Synchronization:** Django Channels publishes live WebSocket events to all clients in sub-second latency only *after* the database transaction commits[cite: 1].
* **Plug-and-Play OBS Overlays:** Dedicated, low-overhead browser sources for OBS Studio and PRISM Live Studio, rendering clean TV-style score bugs with custom team logos and sponsor spaces[cite: 1].
* **Offline-Resilient Mobile Scoring:** Built with Flutter, allowing scorers on fragile mobile networks to queue commands locally and synchronize without state drift[cite: 1].
* **Configurable Rule Profiles:** Versioned rulesets supporting Limited Overs (T20, ODI), Tape-ball, and customized local tournament conditions[cite: 1].
* **Audited Correction Engine:** Undo and edit past balls safely with complete recalculation of strike rotation, bowler figures, and over boundaries[cite: 1].
* **Tournament & Operations Hub:** Fixtures, points tables, net run rates, player claim verification, and integrated local commerce (SSLCommerz)[cite: 1].

---

## 🏗️ Technical Architecture

CricketOps is designed as a **modular monolith**, keeping domain boundaries clean without the unnecessary operational overhead of premature microservices[cite: 1]:

```text
               ┌────────────────────────────────────────────────────────┐
               │                     Client Layer                       │
               │   • Next.js Web (Public Scorecards & Admin Portals)    │
               │   • Flutter Mobile App (Scorer Console & Fan Center)   │
               │   • OBS / PRISM Studio (Live Browser Source Overlays)   │
               └───────────────────────────┬────────────────────────────┘
                                           │ HTTPS / WebSockets
                                           ▼
               ┌────────────────────────────────────────────────────────┐
               │               Django ASGI Application Core              │
               │  ┌──────────────────────────────────────────────────┐  │
               │  │  REST API (DRF)       Django Channels Consumers   │  │
               │  ├──────────────────────────────────────────────────┤  │
               │  │  Scoring Domain Engine  •  Rule Profile Matcher   │  │
               │  │  League Administration  •  Billing & Entitlements │  │
               │  └──────────────────────────────────────────────────┘  │
               └──────────────┬──────────────────────────┬──────────────┘
                              │                          │
                              ▼                          ▼
               ┌──────────────────────────┐   ┌─────────────────────────┐
               │  PostgreSQL 16 (Primary) │   │     Redis 7 In-Memory   │
               │  • Delivery Ledger       │   │  • Channels Layer       │
               │  • Audited Corrections   │   │  • Ephemeral Snapshots  │
               │  • Relational Identities │   │  • Celery Task Broker   │
               └──────────────────────────┘   └─────────────────────────┘

---

## 🛠️ Technology Stack

* **Core Backend:** Python 3.12, Django 5.2 LTS, Django REST Framework[cite: 1]
* **Real-Time Engine:** Django Channels, Daphne ASGI Server, Redis Channel Layer[cite: 1]
* **Asynchronous Jobs:** Celery & Celery Beat[cite: 1]
* **Databases:** PostgreSQL 16 (Authoritative Store), Redis 7 (Cache / Fan-out)[cite: 1]
* **Web Portal & Overlays:** Next.js (App Router, TypeScript, Tailwind CSS, TanStack Query)[cite: 1]
* **Mobile Client:** Flutter & Dart (Riverpod, Dio, Drift local persistence)[cite: 1]
* **DevOps & Containers:** Docker, Docker Compose, GitHub Actions[cite: 1]

---

## 👨‍💻 Owner & Maintainer

* **Organization:** Developed and Maintained by **SpideyTech**
* **Lead Engineer & Architecture:** **Md. Masum Billah**
* **Location:** Dhaka, Bangladesh
# Changelog

## 0.3.0

- Added validated task editing with lifecycle update timestamps.
- Added reversible completion, reopening, archiving, and restoration.
- Added active and archived task views and analytics.
- Added versioned, atomic JSON backup and merge-safe restore operations.
- Added automatic recovery snapshots before local-store overwrites.
- Preserved lifecycle metadata in CSV transfers.
- Added regression coverage for operations, backups, snapshots, and archived metrics.

## 0.2.0

- Added normalized, deduplicated task tags.
- Added priority and tag filters with deterministic deadline and priority sorting.
- Added daily, weekly, and calendar-aware monthly recurrence calculations.
- Added CSV imports with schema checks and safe duplicate-ID handling.
- Added clearer errors for malformed local task stores.
- Added targeted regression coverage for recurrence, sorting, tags, and CSV round trips.

## 0.1.0

- Created an installable local-first automation CLI.
- Added task priorities, due dates, overdue alerts, filtering, and search.
- Added progress analytics, JSON output, and CSV export.
- Added focused tests and continuous integration.

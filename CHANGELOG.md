# Changelog

## 0.6.0

- Added non-mutating dry-run previews for automation rules.
- Added a standalone command for validating rule files.
- Added tag and title exclusion conditions to prevent unwanted matches.
- Added safe actions for clearing task due dates and reminders.
- Rejected conflicting set-and-clear schedule actions.
- Expanded CLI tests, rule-engine coverage, examples, and documentation.

## 0.5.0

- Added a validated JSON rule engine for deterministic task automation.
- Added matching by priority, tag, and title text.
- Added rule actions for priority, tags, relative due dates, and reminders.
- Added timezone-safe reminder snoozing and unsnoozing.
- Preserved snooze state through edits, CSV transfers, backups, and JSON output.
- Added scheduled and ready reminder metrics.
- Added CLI commands, examples, and regression coverage for rules and snoozes.

## 0.4.0

- Added validated effort estimates and timezone-aware reminder timestamps.
- Added a capacity-aware daily agenda ordered by deadlines and priority.
- Added local reminder readiness queries with text and JSON output.
- Added remaining-work minutes to progress analytics.
- Preserved planning metadata across edits, recurrence, CSV transfers, and backups.
- Added regression coverage for planning, reminders, validation, editing, and analytics.

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

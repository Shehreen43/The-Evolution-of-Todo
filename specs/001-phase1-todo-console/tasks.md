# Tasks: Phase 1 - In-Memory Todo Console App

**Input**: Design documents from `/specs/001-phase1-todo-console/`
**Prerequisites**: plan.md (complete), spec.md (complete), data-model.md (complete), contracts/cli-commands.md (complete), quickstart.md (complete)

**Feature Branch**: `001-phase1-todo-console`
**User Stories**: 5 (US1-Add, US2-View, US3-Complete, US4-Delete, US5-Update)
**P1 Stories**: US1, US2, US3, US4 (core MVP)
**P2 Stories**: US5 (update feature, can be deferred)

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2)
- Include exact file paths in descriptions

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [ ] T001 [P] Create pyproject.toml with Python 3.13+, UV configuration, entry point in `src/cli/main.py`
- [ ] T002 [P] Create repository root `src/` directory with `__init__.py`
- [ ] T003 [P] Create `src/models/` directory with `__init__.py`
- [ ] T004 [P] Create `src/repository/` directory with `__init__.py`
- [ ] T005 [P] Create `src/service/` directory with `__init__.py`
- [ ] T006 [P] Create `src/cli/` directory with `__init__.py`

**Checkpoint**: Project structure ready for implementation

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**CRITICAL**: No user story work can begin until this phase is complete

### Models Layer

- [ ] T007 [P] Create Task dataclass in `src/models/task.py` with 5 fields: id, title, description, completed, created_at
- [ ] T008 [P] Add dataclass field validators (title 1-200 chars, description 0-1000 chars) in `src/models/task.py`

### Repository Layer

- [ ] T009 Create TaskRepository interface in `src/repository/task_repository.py` with 6 methods: add(), get_by_id(), get_all(), update(), delete(), count()
- [ ] T010 Implement in-memory storage using list with auto-incrementing ID counter in `src/repository/task_repository.py`

### Service Layer

- [ ] T011 Create TaskService in `src/service/task_service.py` with 6 methods: create_task(), list_tasks(), get_task(), update_task(), delete_task(), toggle_complete()
- [ ] T012 [P] Add validation logic for title/description in `src/service/task_service.py` (depends on T007, T008)
- [ ] T013 [P] Wire TaskService to TaskRepository in `src/service/task_service.py` (depends on T009, T010)

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Add New Task (Priority: P1) MVP

**Goal**: Users can create tasks with a title and optional description

**Independent Test**: Run `todo add "Buy groceries" --description "Milk, eggs"` and verify task appears in `todo list`

### Implementation for User Story 1

- [ ] T014 [P] [US1] Add `add` subcommand parser in `src/cli/main.py` with title positional arg and --description flag
- [ ] T015 [US1] Implement `handle_add()` function in `src/cli/main.py` to parse arguments and call TaskService.create_task()
- [ ] T016 [US1] Add success output "Task added with ID {id}" in `src/cli/main.py`
- [ ] T017 [US1] Add validation error handling for empty title, title > 200 chars in `src/cli/main.py`
- [ ] T018 [US1] Test manual verification: `todo add "Test task"` should create task and return ID

**Checkpoint**: User Story 1 complete - tasks can be created and stored in memory

---

## Phase 4: User Story 2 - View All Tasks (Priority: P1) MVP

**Goal**: Users can see all tasks with their status and details

**Independent Test**: Run `todo list` after creating tasks and verify all tasks display

### Implementation for User Story 2

- [ ] T019 [P] [US2] Add `list` subcommand in `src/cli/main.py` (no arguments required)
- [ ] T020 [US2] Implement `handle_list()` function in `src/cli/main.py` to call TaskService.list_tasks()
- [ ] T021 [US2] Format table output with columns: ID | Status | Title in `src/cli/main.py`
- [ ] T022 [US2] Handle empty list case with message "No tasks found. Add a task to get started." in `src/cli/main.py`
- [ ] T023 [US2] Test manual verification: `todo list` should show all created tasks

**Checkpoint**: User Story 2 complete - tasks can be viewed in formatted list

---

## Phase 5: User Story 3 - Mark Task Complete (Priority: P1) MVP

**Goal**: Users can toggle task completion status

**Independent Test**: Run `todo complete 1` and verify status changes in `todo list`

### Implementation for User Story 3

- [ ] T024 [P] [US3] Add `complete` subcommand in `src/cli/main.py` with task ID positional argument
- [ ] T025 [US3] Implement `handle_complete()` function in `src/cli/main.py` to call TaskService.toggle_complete()
- [ ] T026 [US3] Add success output "Task #{id} marked as complete/incomplete" (toggle behavior) in `src/cli/main.py`
- [ ] T027 [US3] Add error handling for non-existent task ID in `src/cli/main.py`
- [ ] T028 [US3] Test manual verification: `todo complete 1` then `todo list` should show [x] status

**Checkpoint**: User Story 3 complete - task completion can be toggled

---

## Phase 6: User Story 4 - Delete Task (Priority: P1) MVP

**Goal**: Users can remove tasks by ID

**Independent Test**: Run `todo delete 1` and verify task no longer appears in `todo list`

### Implementation for User Story 4

- [ ] T029 [P] [US4] Add `delete` subcommand in `src/cli/main.py` with task ID positional argument
- [ ] T030 [US4] Implement `handle_delete()` function in `src/cli/main.py` to call TaskService.delete_task()
- [ ] T031 [US4] Add success output "Task #{id} deleted" in `src/cli/main.py`
- [ ] T032 [US4] Add error handling for non-existent task ID in `src/cli/main.py`
- [ ] T033 [US4] Test manual verification: `todo delete 1` then `todo list` should not show task #1

**Checkpoint**: User Story 4 complete - tasks can be deleted

---

## Phase 7: User Story 5 - Update Task (Priority: P2)

**Goal**: Users can modify task title and/or description

**Independent Test**: Run `todo update 1 --title "New title"` and verify change in `todo get 1`

### Implementation for User Story 5

- [ ] T034 [P] [US5] Add `update` subcommand in `src/cli/main.py` with task ID positional, --title and --description flags
- [ ] T035 [US5] Implement `handle_update()` function in `src/cli/main.py` to call TaskService.update_task()
- [ ] T036 [US5] Add success output "Task #{id} updated" in `src/cli/main.py`
- [ ] T037 [US5] Add error handling for non-existent task ID and validation errors in `src/cli/main.py`
- [ ] T038 [US5] Test manual verification: `todo update 1 --title "Fixed title"` and `todo list` shows new title

**Checkpoint**: User Story 5 complete - task details can be modified

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Improvements and completion tasks for all user stories

### Additional CLI Commands

- [ ] T039 [P] Add `get` subcommand in `src/cli/main.py` to show task details (id, title, description, status, created_at)
- [ ] T040 [P] Add `help` command in `src/cli/main.py` (auto-provided by argparse)
- [ ] T041 [P] Add `--version` flag in `src/cli/main.py` showing "Todo Console App v1.0.0"

### Error Handling & Validation

- [ ] T042 Consolidate error messages for consistent format in `src/cli/main.py`
- [ ] T043 Add input validation for ID arguments (must be positive integer) in `src/cli/main.py`

### Final Verification

- [ ] T044 Run quickstart.md validation: add task, list, complete, verify, delete
- [ ] T045 Test all 5 operations (add, view, complete, delete, update) work without errors
- [ ] T046 Verify error messages clearly indicate what went wrong (invalid ID, empty title, etc.)

**Checkpoint**: All phases complete - Phase 1 ready for validation

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-7)**: All depend on Foundational phase completion
  - User stories proceed in priority order (P1 → P2)
  - US1, US2, US3, US4 can run in parallel after Foundation
- **Polish (Phase 8)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (Add)**: After Foundation - no dependencies on other stories
- **User Story 2 (View)**: After Foundation - no dependencies, but benefits from US1
- **User Story 3 (Complete)**: After Foundation - no dependencies, uses Task model from Foundation
- **User Story 4 (Delete)**: After Foundation - no dependencies, uses Task model from Foundation
- **User Story 5 (Update)**: After Foundation - P2 priority, can be deferred to after P1 stories

### Within Each User Story

- Foundation (T007-T013) must complete first
- CLI commands build on service layer
- Core implementation before error handling
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks (T001-T006) can run in parallel
- All Foundational tasks marked [P] can run in parallel (T007-T008, T011-T013)
- User Stories 1-4 can start in parallel after Foundation completes
- All tasks marked [P] within a user story can run in parallel

---

## Implementation Strategy

### MVP First (User Stories 1-4 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1 (Add)
4. Complete Phase 4: User Story 2 (View)
5. Complete Phase 5: User Story 3 (Complete)
6. Complete Phase 6: User Story 4 (Delete)
7. **STOP and VALIDATE**: Test all 4 P1 stories work independently
8. Deploy/demo MVP

### Full Phase 1

After MVP validation:
9. Complete Phase 7: User Story 5 (Update) - P2 feature
10. Complete Phase 8: Polish (get, help, version, final verification)

---

## Quick Reference: File Paths

```
src/
├── __init__.py                    # T002
├── models/
│   ├── __init__.py                # T003
│   └── task.py                    # T007, T008
├── repository/
│   ├── __init__.py                # T004
│   └── task_repository.py         # T009, T010
├── service/
│   ├── __init__.py                # T005
│   └── task_service.py            # T011, T012, T013
└── cli/
    ├── __init__.py                # T006
    └── main.py                    # T014-T041
```

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- P1 stories (US1-US4) form the MVP - all must work before demo
- P2 story (US5) can be deferred if needed
- Manual verification specified in success criteria - no automated tests required
- Stop at any checkpoint to validate story independently
- Commit after each task or logical group

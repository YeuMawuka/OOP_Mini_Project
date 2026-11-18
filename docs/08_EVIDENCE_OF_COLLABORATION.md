# Part 8 - Evidence of Collaboration

This document tells the lecturer exactly where to look on GitHub, and what they will find there.
Everything described here was created by GitHub itself while the two students worked from their own
accounts: Nicodimus (`NicodimusTinashe`) and Yeukai (`yeumawuka-stack`).

Repository: `https://github.com/yeumawuka-stack/OOP_Mini_Project` (private; the lecturer is added as a collaborator).

## Quick Facts the Repository Shows

| Item | Value |
| --- | --- |
| Default branch | `main` (no direct pushes: agreed team rule) |
| Feature branches | 10 (`feature/01-...` to `feature/10-...`), kept on GitHub after merging |
| Pull requests | 10 (#1 to #10), all **Merged** |
| Pull-request merge commits | 10, each named `Merge pull request #N from ...` |
| Branch-update merge commits | 3: two in `feature/07-appointment-service` (one clean, one that resolves the conflict) and one in `feature/08-record-and-dashboard-services` |
| Authors | Two: Nicodimus and Yeukai, each with their own commits |
| Reviews | Every pull request has a reviewer who is the other student |
| Release | Tag `v1.0.0` |
| Tests | 119 passing |

## 1. Commit History

Where: repository home > **Commits** (`/commits/main`), or `git log --oneline --graph --all`.

What the lecturer sees:

- Commits with clear imperative messages such as "Add PatientService with unique National ID rule".
- Each commit shows the author's avatar and user name.
- Merge commits named `Merge pull request #N from user/feature/...`.
- Clicking any commit shows exactly which lines changed.

Command-line proof:

```bash
git shortlog -sn --all --no-merges          # commits per author
git log --author="Nicodimus" --oneline      # Nicodimus's commits
git log --author="Yeukai" --oneline         # Yeukai's commits
git log --merges --oneline                  # pull-request and conflict merges
```

## 2. Branches

Where: **Branches** page (`/branches`) or `git branch -a`.

| Branch | Author |
| --- | --- |
| `feature/01-project-setup` | Nicodimus |
| `feature/02-utilities` | Nicodimus |
| `feature/03-person-models` | Nicodimus |
| `feature/04-database-layer` | Yeukai |
| `feature/05-patient-doctor-services` | Yeukai |
| `feature/06-appointment-record-models` | Nicodimus |
| `feature/07-appointment-service` | Nicodimus |
| `feature/08-record-and-dashboard-services` | Nicodimus |
| `feature/09-console-menus` | Nicodimus |
| `feature/10-final-docs-and-release` | Yeukai |

No branch was deleted after merging, so all of them stay visible.

## 3. Pull Requests

Where: **Pull requests > Closed** (`/pulls?q=is%3Apr+is%3Amerged`).

What the lecturer sees: 10 pull requests with a purple **Merged** badge, each with a description,
the commits, the changed files, the reviewer and the merge. The full list is in
`06_PULL_REQUEST_STRATEGY.md`. Nicodimus is the author of #1, #2, #3, #6, #7, #8 and #9; Yeukai is
the author of #4, #5 and #10.

## 4. Reviews

Where: inside each pull request, **Conversation** and **Files changed** tabs.

| PR | Author | Reviewer |
| --- | --- | --- |
| #1, #2, #3 | Nicodimus | Yeukai |
| #4, #5 | Yeukai | Nicodimus |
| #6, #7, #8, #9 | Nicodimus | Yeukai |
| #10 | Yeukai | Nicodimus |

This shows **code review in both directions**: neither student merged unreviewed work. The review
comments and approvals are on the Conversation tab of each pull request.

## 5. Approvals

Each pull request page shows the reviewer's green "Approved" review. The agreed team rule was that a
pull request is merged only after the other student has approved it.

## 6. Merged Branches

Where: the **Merged** pull requests list, `git branch -a --merged main`, and **Insights > Network**.

All ten feature branches are merged into `main`, so `git branch -a --no-merged main` prints nothing.
The merge commit of every PR records which student merged it.

## 7. Merge Conflict

Pull request #7 shows the real conflict in `database/schema.py`:

- The **Conversation** tab showed "This branch has conflicts that must be resolved" after PR #5 was merged, and later "No conflicts with base branch".
- The **Commits** tab shows the resolving commit "Merge main into feature/07-appointment-service and resolve schema.py conflict".
- `07_MERGE_CONFLICT_SCENARIO.md` explains it step by step with the real Git output.

## 8. Contribution Graph

Where: **Insights > Contributors**, **Insights > Network**, **Insights > Commits**, **Code frequency**, and each student's own GitHub profile contribution calendar.

- **Contributors** shows two contributors, each with a commit count and an additions/deletions graph.
- **Network** draws the ten feature branches leaving `main` and rejoining it, with the step 7 and step 8 branches taking detours to bring in earlier work.
- **Commits** shows activity over time for the whole team.

## How the Repository Proves That Both Students Contributed

| Evidence | Nicodimus | Yeukai |
| --- | --- | --- |
| Pull requests authored | #1, #2, #3, #6, #7, #8, #9 | #4, #5, #10 |
| Pull requests reviewed | #4, #5, #10 | #1, #2, #3, #6, #7, #8, #9 |
| Code written | project set-up, utilities, `BaseEntity`, `Person`, `Patient`, `Doctor`, `Appointment`, `MedicalRecord`, `AppointmentService`, `MedicalRecordService`, `DashboardService`, `Console`, menus, `main.py`, most tests | `Database`, `BaseService`, `PatientService`, `DoctorService`, database design document, final documentation |
| Merge conflict | Resolved the conflict in `database/schema.py` (PR #7) | Authored the step 5 change that caused it |
| Merges | #1, #2, #3, #5 | #4, #6, #7, #8, #9, #10 |
| Release | Approved v1.0.0 | Tagged v1.0.0 |

Ways to check authorship line by line:

```bash
git blame models/person.py            # every line shows its author
git blame services/base_service.py
git log --stat --author="Nicodimus"   # files touched by Nicodimus
git log --stat --author="Yeukai"      # files touched by Yeukai
```

## Evidence Checklist (screenshots for the report)

1. `/commits/main` showing both authors.
2. `/branches` showing all feature branches.
3. `/pulls?q=is%3Apr+is%3Amerged` showing the ten merged pull requests.
4. PR #7 **Conversation**: the conflict notice, and the **Commits** tab with the resolving commit.
5. One review conversation with a comment and an approval.
6. `/graphs/contributors` and `/network`.
7. `/tags` (or Releases) showing `v1.0.0`.
8. The terminal output of `git log --oneline --graph --all` and `git shortlog -sn --all --no-merges`.

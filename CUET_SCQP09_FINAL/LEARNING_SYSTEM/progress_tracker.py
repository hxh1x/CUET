#!/usr/bin/env python3
"""
CUET SCQP09 Candidate Progress & Mastery Tracker
CLI tool for managing learner state, recording test attempts, and recommending study paths.
"""

import argparse
import datetime
import json
import os
import sys

DEFAULT_PROFILE = "learner_progress.json"

# Master list of high-priority initial modules
RECOMMENDED_SEQUENCE = [
    "M1", "T1", "G1", "D1", "O1",
    "M2", "T2", "G2", "D2", "O2",
    "M3", "T7", "G4", "D3", "O3",
    "M6", "T9", "G5", "D4", "O4",
    "M9", "T14", "G8", "D5", "O6"
]


def load_profile(path):
    if not os.path.exists(path):
        return None
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_profile(path, data):
    data["last_active"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def init_profile(path, learner_id, name):
    now = datetime.datetime.now(datetime.timezone.utc).isoformat()
    data = {
        "learner_id": learner_id,
        "name": name,
        "created_at": now,
        "last_active": now,
        "target_exam_date": "2027-03-15",
        "target_score_percentile": 99.0,
        "overall_completion_pct": 0.0,
        "module_records": {},
        "assessment_history": []
    }
    save_profile(path, data)
    print(f"[OK] Initialized learner profile for {name} ({learner_id}) at {path}")


def update_module_status(path, module_id, status, mastery_tier=None):
    data = load_profile(path)
    if not data:
        print(f"[ERROR] Profile not found at {path}. Run 'init' first.")
        sys.exit(1)

    mods = data.setdefault("module_records", {})
    record = mods.setdefault(module_id, {
        "module_id": module_id,
        "status": "not_started",
        "mastery_tier": 0,
        "total_attempts": 0,
        "best_score_pct": 0.0,
        "avg_speed_seconds": 0.0,
        "last_attempt_at": None,
        "next_review_due": None,
        "retention_streak": 0
    })

    record["status"] = status
    if mastery_tier is not None:
        record["mastery_tier"] = int(mastery_tier)

    # Recalculate overall completion
    mastered_count = sum(1 for m in mods.values() if m.get("status") in ("mastered", "competent"))
    data["overall_completion_pct"] = round((mastered_count / 92.0) * 100, 1)

    save_profile(path, data)
    print(f"[OK] Updated {module_id}: status='{status}', tier={record['mastery_tier']}. Completion: {data['overall_completion_pct']}%")


def record_attempt(path, module_id, level, score, total_q, speed_sec):
    data = load_profile(path)
    if not data:
        print(f"[ERROR] Profile not found at {path}. Run 'init' first.")
        sys.exit(1)

    pct = round((score / float(total_q)) * 100, 1)
    passed = pct >= 80.0
    now = datetime.datetime.now(datetime.timezone.utc).isoformat()
    today_str = datetime.date.today().isoformat()

    attempt_id = f"ATT_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"
    attempt = {
        "attempt_id": attempt_id,
        "module_id": module_id,
        "timestamp": now,
        "assessment_level": int(level),
        "score": int(score),
        "total_questions": int(total_q),
        "time_taken_seconds": int(speed_sec),
        "passed": passed
    }
    data.setdefault("assessment_history", []).append(attempt)

    mods = data.setdefault("module_records", {})
    record = mods.setdefault(module_id, {
        "module_id": module_id,
        "status": "not_started",
        "mastery_tier": 0,
        "total_attempts": 0,
        "best_score_pct": 0.0,
        "avg_speed_seconds": 0.0,
        "last_attempt_at": None,
        "next_review_due": None,
        "retention_streak": 0
    })

    record["total_attempts"] += 1
    record["last_attempt_at"] = now
    if pct > record.get("best_score_pct", 0.0):
        record["best_score_pct"] = pct

    # Update tier
    if passed:
        if int(level) >= record.get("mastery_tier", 0):
            record["mastery_tier"] = min(5, int(level))
        if record["mastery_tier"] >= 4:
            record["status"] = "mastered"
        elif record["mastery_tier"] >= 3:
            record["status"] = "competent"
        else:
            record["status"] = "in_progress"

        # Spaced review scheduling: 3 days -> 7 days -> 14 days -> 30 days
        streak = record.get("retention_streak", 0) + 1
        record["retention_streak"] = streak
        days_ahead = 3 if streak == 1 else (7 if streak == 2 else 14)
        due_date = datetime.date.today() + datetime.timedelta(days=days_ahead)
        record["next_review_due"] = due_date.isoformat()
    else:
        record["retention_streak"] = 0
        record["status"] = "in_progress"

    # Recalculate overall completion
    mastered_count = sum(1 for m in mods.values() if m.get("status") in ("mastered", "competent"))
    data["overall_completion_pct"] = round((mastered_count / 92.0) * 100, 1)

    save_profile(path, data)
    print(f"[RECORDED] {module_id} Level {level}: {score}/{total_q} ({pct}%). Passed: {passed}. Next review: {record.get('next_review_due')}")


def show_summary(path):
    data = load_profile(path)
    if not data:
        print(f"[ERROR] Profile not found at {path}.")
        sys.exit(1)

    mods = data.get("module_records", {})
    attempts = data.get("assessment_history", [])

    print("\n" + "=" * 60)
    print(f"  CUET SCQP09 Progress Summary: {data['name']} ({data['learner_id']})")
    print("=" * 60)
    print(f"Overall Progress: {data.get('overall_completion_pct', 0.0)}% of 92 modules mastered/competent")
    print(f"Total Assessments Attempted: {len(attempts)}")

    status_counts = {}
    for m in mods.values():
        s = m.get("status", "not_started")
        status_counts[s] = status_counts.get(s, 0) + 1

    print("\nStatus Breakdown:")
    for st, count in status_counts.items():
        print(f"  - {st.upper()}: {count} modules")

    print("\nRecent Activity:")
    for att in attempts[-5:]:
        pct = round((att['score'] / float(att['total_questions'])) * 100, 1)
        res = "PASS" if att.get("passed") else "FAIL"
        print(f"  [{att['timestamp'][:10]}] {att['module_id']} (Level {att['assessment_level']}): {att['score']}/{att['total_questions']} ({pct}%) -> {res}")

    recommend_next(data)
    print("=" * 60 + "\n")


def recommend_next(data):
    mods = data.get("module_records", {})
    today_str = datetime.date.today().isoformat()

    # 1. Check for due revisions
    due = []
    for mid, m in mods.items():
        next_due = m.get("next_review_due")
        if next_due and next_due <= today_str:
            due.append(mid)

    print("\nTarget Recommendations:")
    if due:
        print(f"  [ACTION 1: REVISION DUE] The following modules require spaced repetition review: {', '.join(due)}")

    # 2. Check for in-progress modules
    in_prog = [mid for mid, m in mods.items() if m.get("status") == "in_progress"]
    if in_prog:
        print(f"  [ACTION 2: IN PROGRESS] Complete assessments for active modules: {', '.join(in_prog)}")

    # 3. Next unstarted from recommended sequence
    next_unstarted = None
    for cand in RECOMMENDED_SEQUENCE:
        if cand not in mods or mods[cand].get("status") == "not_started":
            next_unstarted = cand
            break

    if next_unstarted:
        print(f"  [ACTION 3: NEXT MODULE] Begin foundational module: {next_unstarted}")
    else:
        print("  [ACTION 3: NEXT MODULE] Continue working through the 92-module syllabus sequence.")


def main():
    parser = argparse.ArgumentParser(description="CUET SCQP09 Learner Progress Tracker")
    parser.add_argument("--profile", default=DEFAULT_PROFILE, help="Path to profile JSON file")

    subparsers = parser.add_subparsers(dest="command")

    # init
    p_init = subparsers.add_parser("init", help="Initialize a new profile")
    p_init.add_argument("--id", required=True, help="Learner ID (e.g. STU_001)")
    p_init.add_argument("--name", required=True, help="Candidate full name")

    # status
    p_stat = subparsers.add_parser("set-status", help="Update module status")
    p_stat.add_argument("--module", required=True, help="Module ID (e.g. M1)")
    p_stat.add_argument("--status", required=True, choices=["not_started", "in_progress", "competent", "mastered", "revision_due"])
    p_stat.add_argument("--tier", type=int, choices=range(0, 6), default=None)

    # attempt
    p_att = subparsers.add_parser("record", help="Record an assessment attempt")
    p_att.add_argument("--module", required=True, help="Module ID (e.g. M1)")
    p_att.add_argument("--level", type=int, required=True, choices=range(1, 6))
    p_att.add_argument("--score", type=int, required=True)
    p_att.add_argument("--total", type=int, required=True)
    p_att.add_argument("--speed", type=int, default=60, help="Total seconds spent")

    # summary
    subparsers.add_parser("summary", help="Show summary report and next recommendations")

    args = parser.parse_args()

    if args.command == "init":
        init_profile(args.profile, args.id, args.name)
    elif args.command == "set-status":
        update_module_status(args.profile, args.module, args.status, args.tier)
    elif args.command == "record":
        record_attempt(args.profile, args.module, args.level, args.score, args.total, args.speed)
    elif args.command == "summary":
        show_summary(args.profile)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()

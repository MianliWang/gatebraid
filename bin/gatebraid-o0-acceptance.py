#!/usr/bin/env python3
"""gatebraid-o0-acceptance - the end-to-end acceptance harness for node O0 (T3).

Drives the PAIR - `gatebraid-snapshot` producing and `gatebraid-frontier`
consuming - over the frozen corpus and over a seeded induced-failure matrix, and
EMITS ITS OWN SUMMARIES.  Nothing here is narrated by a caller: every mode
prints the case table it measured and writes the same content as JSON, so a
reader checks the tool's output rather than a sentence about it.

WHY THE PAIR AND NOT EACH HALF.  Both tools have their own committed
falsification, and those prove each half in isolation.  What neither can prove is
that a degradation the producer records is a degradation the consumer HONOURS -
the seam is where a fail-open defect would live.  Every case in the induced
matrix therefore runs the real producer to a document and the real consumer to a
verdict, and asserts on the verdict.

THE MODES

  --induced-failures        one seeded case per P0-1 class and per P0-4 clause
                            whose consequence is `undecidable`; every case is
                            pair-driven end to end and every case must observe
                            `undecidable`.
  --dependency-directions   a NON-EMPTY dependency relation exercised in BOTH
                            directions against corpus material, plus the three
                            item conditionals whose required outcome is not
                            `undecidable`.
  --byte-contract           both tools run under a NON-UTF-8 PARENT CONSOLE with
                            non-ASCII content, comparing emitted bytes against
                            the expected UTF-8 encoding byte for byte.
  --corpus                  the consumer driven over every frozen
                            state-pipeline fixture.

WHERE THE CLAUSES ARE COVERED, stated so the placement can be disputed rather
than assumed.  The induced matrix holds only cases whose required outcome is
`undecidable`, which is what makes its summary line a single homogeneous claim.
The two item conditionals with a different required outcome - a non-Slice row
carrying NO verdict, and an `Aborted` row that may be `blocked` but never
`startable` - are covered in `--dependency-directions` beside `allOf[2]`'s
positive arm, because that mode is already the one about item structure.
Placing them in the induced matrix would have required a summary that says
"every case undecidable, except the two that are not", which is the shape of
sentence a check hides behind.

A CASE THAT COULD NOT BE EXERCISED IS A FAILURE, NOT A SKIP.  Every mode counts
`cases unexercised` and a non-zero count exits 1.  The `--byte-contract` mode
additionally proves its own premise: it measures that the parent console really
does corrupt a text-layer write before it credits the binary path with
surviving one.  A byte-contract test run under a UTF-8 console would otherwise
pass while measuring nothing.

Exit codes: 0 every declared case met its required outcome - 1 one or more did
not, or a case could not be exercised - 2 usage or input error.
Python 3 standard library only.  No HTTP client is constructed here and no
network read is performed in any mode: every input is a frozen fixture or a
seeded transcript.
"""

import argparse
import copy
import json
import os
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
SNAPSHOT = os.path.join(HERE, "gatebraid-snapshot.py")
FRONTIER = os.path.join(HERE, "gatebraid-frontier.py")
CORPUS = os.path.join(REPO, "fixtures", "state-pipeline")
CANONICAL = os.path.join(CORPUS, "valid-canonical-snapshot.json")
EXPECTATIONS = os.path.join(CORPUS, "EXPECTATIONS.json")
SCHEMA = os.path.join(REPO, "schema", "snapshot.schema.json")

HARNESS_NAME = "gatebraid-o0-acceptance"
HARNESS_VERSION = "1.0.0"

# The non-ASCII payload the byte-contract mode drives through both tools. It
# carries the exact mark the control plane's own values carry.
NON_ASCII_SLICE_ID = "P9-S1"


class InputError(Exception):
    """A usage or input failure. Exits 2."""


def child_env():
    env = dict(os.environ)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    return env


def run_tool(tool, args, env=None, cwd=None):
    proc = subprocess.run([sys.executable, "-B", tool] + args,
                          cwd=cwd or REPO, stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE, env=env or child_env())
    return proc.returncode, proc.stdout, proc.stderr.decode("utf-8", "replace")


def write_json(path, doc):
    with open(path, "wb") as fh:
        fh.write((json.dumps(doc, ensure_ascii=False, indent=1) + "\n").encode("utf-8"))
    return path


# ------------------------------------------------------------ transcripts

def with_exit_status(doc):
    """Stamp the success exit onto any transcript page that does not name one.

    The producer refuses a page with no exit status, because defaulting it to 0
    would put an implicit success assumption on a path that reaches a verdict.
    The seeds therefore state success explicitly rather than letting the tool
    infer it.
    """
    for entry in (doc.get("reads") or {}).values():
        pages = entry if isinstance(entry, list) else [entry]
        for page in pages:
            page.setdefault("exit_code", 0)
    return doc


def healthy_reads():
    """A transcript every source of which is `ok` and complete."""
    return with_exit_status({
        "reads": {
            "project_items": {"stdout": {"nodes": [
                {"item_id": "PVTI_acceptance_a", "issue": "MianliWang/gatebraid#9",
                 "slice_metadata_present": True, "slice_id": "P9-S1",
                 "workflow_raw": "Backlog", "soft_dependencies_declared": False},
            ], "hasNextPage": False}},
            "issue_states": {"stdout": {"states": {"MianliWang/gatebraid#9": "OPEN"}}},
            "dep_blocked_by": {"stdout": {"edges": {}}},
            "dep_blocking": {"stdout": {"edges": {}}},
        }
    })


def seeded(mutate):
    doc = copy.deepcopy(healthy_reads())
    mutate(doc["reads"])
    # Normalised AFTER the mutation: a seed that replaces a source entry
    # supplies a fresh page, and that page must state its exit status too.
    return with_exit_status(doc)


INDUCED_CASES = [
    # (case_id, clause, description, transcript mutation, extra snapshot args)
    ("I-P0-1-auth", "P0-1 auth_failure", "a read answered 401",
     lambda r: r.update({"issue_states": {"http_status": 401, "exit_code": 1,
                                          "stderr": "HTTP 401"}}), []),
    ("I-P0-1-perm", "P0-1 permission_failure", "403 with budget remaining",
     lambda r: r.update({"issue_states": {"http_status": 403, "exit_code": 1,
                                          "rate_limit_remaining": 9,
                                          "stderr": "HTTP 403"}}), []),
    ("I-P0-1-rate", "P0-1 rate_limited", "403 with the budget exhausted",
     lambda r: r.update({"issue_states": {"http_status": 403, "exit_code": 1,
                                          "rate_limit_remaining": 0,
                                          "stderr": "HTTP 403"}}), []),
    ("I-P0-1-net", "P0-1 network_error", "the read could not be performed",
     lambda r: r.update({"issue_states": {"exit_code": 1,
                                          "transport_error": "connection refused"}}), []),
    ("I-P0-1-server", "P0-1 server_error", "the endpoint answered 503",
     lambda r: r.update({"issue_states": {"http_status": 503, "exit_code": 1,
                                          "stderr": "HTTP 503"}}), []),
    ("I-P0-1-parse", "P0-1 parse_error", "a body that is not JSON",
     lambda r: r.update({"issue_states": {"exit_code": 0, "stdout": "{not json"}}), []),
    ("I-P0-1-endpoint", "P0-1 unexpected_endpoint", "a shape the tool does not know",
     lambda r: r.update({"issue_states": {"exit_code": 0, "stdout": "[1,2,3]"}}), []),
    # The first page MUST carry the item. A capped transcript whose pages are
    # empty exercises the bounded flag and then has no item to carry a verdict,
    # which is a case that measures nothing - caught by this harness on its
    # first run and fixed here rather than accepted.
    ("I-P0-3-cap", "P0-3 page cap", "a capped connection with pages outstanding",
     lambda r: r.update({"project_items": [
         {"stdout": {"nodes": [
             {"item_id": "PVTI_acceptance_a", "issue": "MianliWang/gatebraid#9",
              "slice_metadata_present": True, "slice_id": "P9-S1",
              "workflow_raw": "Backlog", "soft_dependencies_declared": False}],
             "hasNextPage": True}},
         {"stdout": {"nodes": [], "hasNextPage": True}}]}), ["--page-cap", "1"]),
    ("I-P0-4-state", "P0-4 unknown issue state", "a state outside the closed set",
     lambda r: r.update({"issue_states": {"stdout": {"states": {
         "MianliWang/gatebraid#9": "LOCKED"}}}}), []),
    ("I-P0-4-workflow", "P0-4 unknown workflow", "a Workflow outside the closed set",
     lambda r: r.update({"project_items": {"stdout": {"nodes": [
         {"item_id": "PVTI_acceptance_a", "issue": "MianliWang/gatebraid#9",
          "slice_metadata_present": True, "slice_id": "P9-S1",
          "workflow_raw": "Gate 9 - Inventing",
          "soft_dependencies_declared": False}], "hasNextPage": False}}}), []),
    ("I-P0-4-crosscheck", "P0-4 cross-check mismatch", "one direction unmirrored",
     lambda r: r.update({"dep_blocked_by": {"stdout": {"edges": {
         "MianliWang/gatebraid#9": [{"issue": "MianliWang/gatebraid#5",
                                     "state": "OPEN"}]}}},
         "dep_blocking": {"stdout": {"edges": {}}}}), []),
    ("I-P0-4-soft", "P0-4 soft dependency not parsed", "a declaration that did not parse",
     lambda r: r.update({"project_items": {"stdout": {"nodes": [
         {"item_id": "PVTI_acceptance_a", "issue": "MianliWang/gatebraid#9",
          "slice_metadata_present": True, "slice_id": "P9-S1",
          "workflow_raw": "Backlog", "soft_dependencies_declared": True,
          "soft_dependencies_raw": "   "}], "hasNextPage": False}}}), []),
]


def drive_pair(tmp, case_id, transcript, extra_args):
    """Producer to document, consumer to verdict. The whole seam, end to end."""
    tpath = write_json(os.path.join(tmp, case_id + "-transcript.json"), transcript)
    snap = os.path.join(tmp, case_id + "-snapshot.json")
    rc_p, _, err_p = run_tool(SNAPSHOT, ["--replay", tpath, "--out", snap] + extra_args)
    if not os.path.isfile(snap):
        return None, rc_p, None, "the producer emitted no document (exit %d)" % rc_p
    rep = os.path.join(tmp, case_id + "-report.json")
    rc_c, _, err_c = run_tool(FRONTIER, [snap, "--out", rep])
    if not os.path.isfile(rep):
        return rc_p, rc_p, rc_c, "the consumer emitted no report (exit %d)" % rc_c
    report = json.load(open(rep, encoding="utf-8"))
    return report, rc_p, rc_c, None


def mode_induced(args, tmp):
    rows = []
    for case_id, clause, description, mutate, extra in INDUCED_CASES:
        report, rc_p, rc_c, problem = drive_pair(tmp, case_id, seeded(mutate), extra)
        if problem:
            rows.append({"case_id": case_id, "clause": clause,
                         "description": description, "required": "undecidable",
                         "observed": "unexercised", "exercised": False,
                         "producer_exit": rc_p, "consumer_exit": rc_c,
                         "detail": problem})
            continue
        verdicts = report.get("verdicts") or []
        observed = verdicts[0]["verdict"] if verdicts else "<no verdict>"
        rows.append({"case_id": case_id, "clause": clause,
                     "description": description, "required": "undecidable",
                     "observed": observed, "exercised": True,
                     "producer_exit": rc_p, "consumer_exit": rc_c,
                     "reasons": verdicts[0]["reasons"] if verdicts else []})
    return rows, "induced-failures"


DIRECTION_CASES = [
    ("D-both-consistent", "allOf[2] positive arm; both directions non-empty",
     "an item carrying Slice metadata, blocked_by and blocking both non-empty "
     "and agreeing", "blocked"),
    ("D-mismatch", "allOf[3] consequence half",
     "a non-empty relation asserted in one direction and not the other", "undecidable"),
    ("D-not-performed", "allOf[3] consequence half",
     "a non-empty relation whose cross-check was never performed", "undecidable"),
    ("D-non-slice", "allOf[1]",
     "a row with no Slice metadata, carrying a reason and no verdict", "<no verdict>"),
    ("D-aborted", "allOf[5]",
     "an Aborted row, which may be blocked but never startable", "blocked"),
]


def direction_documents(base):
    """Corpus-derived documents with a NON-EMPTY relation in both directions.

    Derived from `fixtures/state-pipeline/valid-canonical-snapshot.json` rather
    than from the live control plane: the Gate 0 Q7 gap was precisely that the
    live closed set carries no usable relation to exercise, so the relation is
    taken from corpus material where it can be made non-empty on purpose.
    """
    docs = {}

    d = copy.deepcopy(base)
    item = d["items"][0]
    item["dependencies"]["blocked_by"] = [{"issue": "MianliWang/gatebraid#5",
                                           "state": "OPEN"}]
    item["dependencies"]["blocking"] = [{"issue": "MianliWang/gatebraid#7",
                                         "state": "CLOSED"}]
    item["dependencies"]["cross_check"] = "consistent"
    item["verdict"] = "blocked"
    docs["D-both-consistent"] = d

    d = copy.deepcopy(docs["D-both-consistent"])
    d["items"][0]["dependencies"]["cross_check"] = "mismatch"
    d["items"][0]["verdict"] = "undecidable"
    docs["D-mismatch"] = d

    d = copy.deepcopy(docs["D-both-consistent"])
    d["items"][0]["dependencies"]["cross_check"] = "not_performed"
    d["items"][0]["verdict"] = "undecidable"
    docs["D-not-performed"] = d

    d = copy.deepcopy(base)
    item = d["items"][0]
    for key in ("slice_id", "workflow", "verdict"):
        item.pop(key, None)
    item["slice_metadata_present"] = False
    item["excluded_reason"] = "a Project row carrying no Slice metadata"
    item["dependencies"]["blocked_by"] = [{"issue": "MianliWang/gatebraid#5",
                                           "state": "CLOSED"}]
    item["dependencies"]["blocking"] = [{"issue": "MianliWang/gatebraid#7",
                                         "state": "CLOSED"}]
    docs["D-non-slice"] = d

    d = copy.deepcopy(base)
    item = d["items"][0]
    item["workflow"] = "Aborted"
    item["verdict"] = "blocked"
    item["dependencies"]["blocked_by"] = []
    item["dependencies"]["blocking"] = [{"issue": "MianliWang/gatebraid#7",
                                         "state": "CLOSED"}]
    item["dependencies"]["cross_check"] = "consistent"
    docs["D-aborted"] = d
    return docs


def mode_directions(args, tmp):
    base = json.load(open(CANONICAL, encoding="utf-8"))
    docs = direction_documents(base)
    rows = []
    for case_id, clause, description, required in DIRECTION_CASES:
        doc = docs[case_id]
        path = write_json(os.path.join(tmp, case_id + ".json"), doc)
        out = os.path.join(tmp, case_id + "-report.json")
        rc, _, err = run_tool(FRONTIER, [path, "--out", out])
        if not os.path.isfile(out):
            rows.append({"case_id": case_id, "clause": clause,
                         "description": description, "required": required,
                         "observed": "unexercised", "exercised": False,
                         "consumer_exit": rc,
                         "detail": "the consumer emitted no report"})
            continue
        report = json.load(open(out, encoding="utf-8"))
        verdicts = report.get("verdicts") or []
        observed = verdicts[0]["verdict"] if verdicts else "<no verdict>"

        item = doc["items"][0]
        both_non_empty = bool(item["dependencies"]["blocked_by"]) and \
            bool(item["dependencies"]["blocking"])
        row = {"case_id": case_id, "clause": clause, "description": description,
               "required": required, "observed": observed, "exercised": True,
               "consumer_exit": rc,
               "blocked_by_count": len(item["dependencies"]["blocked_by"]),
               "blocking_count": len(item["dependencies"]["blocking"]),
               "both_directions_non_empty": both_non_empty}
        if case_id == "D-non-slice":
            excluded = report.get("excluded") or []
            row["excluded_with_reason"] = bool(excluded and excluded[0].get("excluded_reason"))
        if case_id == "D-both-consistent" and verdicts:
            # allOf[2]'s positive arm: the item owes its id, its Workflow and a
            # verdict, and the report must carry all three rather than accept by
            # emitting nothing.
            v = verdicts[0]
            row["positive_arm_complete"] = bool(v.get("slice_id")) and \
                bool(v.get("workflow")) and bool(v.get("verdict"))
        rows.append(row)
    return rows, "dependency-directions"


# ----------------------------------------------------------- byte contract

def cp936_wrapper(tmp, inner_argv):
    """Run a child under a non-UTF-8 parent console, the method Gate 1 measured.

    A `.cmd` shim sets the console codepage to 936 before the child starts, so
    the child inherits a non-UTF-8 text layer exactly as it did when BP-01 fired
    on this host during this Slice's Gate 0.
    """
    cmd_path = os.path.join(tmp, "under-cp936.cmd")
    lines = ["@echo off", "chcp 936 >NUL", "set PYTHONDONTWRITEBYTECODE=1",
             " ".join('"%s"' % a if " " in a else a for a in inner_argv)]
    with open(cmd_path, "w", encoding="ascii") as fh:
        fh.write("\r\n".join(lines) + "\r\n")
    proc = subprocess.run(["cmd", "/c", cmd_path], cwd=REPO,
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return proc.returncode, proc.stdout, proc.stderr


def mode_byte_contract(args, tmp):
    if os.name != "nt":
        raise InputError(
            "USAGE: --byte-contract establishes a non-UTF-8 PARENT CONSOLE via "
            "the measured cp936 method and runs on Windows only; on this "
            "platform the premise cannot be established, and a run that cannot "
            "establish its premise must not report a pass")

    rows = []

    # ---- the premise, proven before anything is credited to the contract ----
    probe = os.path.join(tmp, "probe.py")
    with open(probe, "w", encoding="ascii") as fh:
        # `ascii()` and not `%r`: the probe file is written ASCII-only on
        # purpose, so the non-ASCII payload must reach it as escapes. Writing
        # the literal mark here would make the harness's own source the thing
        # under test rather than the tools.
        fh.write("import sys\n"
                 "PAYLOAD = %s\n"
                 "if sys.argv[1] == 'text':\n"
                 "    print(PAYLOAD)\n"
                 "else:\n"
                 "    sys.stdout.buffer.write(PAYLOAD.encode('utf-8') + b'\\n')\n"
                 % ascii("em dash \u2014 CJK \u4e2d\u6587"))
    expected = ("em dash \u2014 CJK \u4e2d\u6587").encode("utf-8")
    rc, text_out, _ = cp936_wrapper(tmp, [sys.executable, "-B", probe, "text"])
    corrupts = expected not in text_out
    rows.append({
        "case_id": "B-premise", "clause": "P0-2 premise",
        "description": "the parent console really does corrupt a text-layer write",
        "required": "corrupted", "observed": "corrupted" if corrupts else "intact",
        "exercised": True,
        "detail": "a byte-contract test under a UTF-8 console would pass while "
                  "measuring nothing, so the premise is measured first"})

    # ---- the producer's bytes under that same console -----------------------
    transcript = write_json(os.path.join(tmp, "bc-transcript.json"), seeded(
        lambda r: r.update({"project_items": {"stdout": {"nodes": [
            {"item_id": "PVTI_acceptance_a", "issue": "MianliWang/gatebraid#9",
             "slice_metadata_present": True, "slice_id": NON_ASCII_SLICE_ID,
             "workflow_raw": load_em_dash_workflow(),
             "soft_dependencies_declared": False}], "hasNextPage": False}}})))
    mark = load_em_dash_workflow().encode("utf-8")

    rc, snap_bytes, err = cp936_wrapper(
        tmp, [sys.executable, "-B", SNAPSHOT, "--replay", transcript])
    rows.append({
        "case_id": "B-producer", "clause": "P0-2 producing half",
        "description": "the producer's stdout bytes under a cp936 parent console",
        "required": "byte-exact UTF-8", "exercised": True,
        "observed": "byte-exact UTF-8" if mark in snap_bytes else "corrupted",
        "detail": "the emitted document must carry the U+2014 mark as its "
                  "UTF-8 encoding, not as the console's"})

    snap_path = os.path.join(tmp, "bc-snapshot.json")
    with open(snap_path, "wb") as fh:
        fh.write(snap_bytes)

    rc, rep_bytes, err = cp936_wrapper(
        tmp, [sys.executable, "-B", FRONTIER, snap_path])
    rows.append({
        "case_id": "B-consumer", "clause": "P0-2 consuming half",
        "description": "the consumer's stdout bytes under a cp936 parent console",
        "required": "byte-exact UTF-8", "exercised": True,
        "observed": "byte-exact UTF-8" if mark in rep_bytes else "corrupted",
        "detail": "the consumer read the producer's bytes and re-emitted the "
                  "mark unchanged"})

    # ---- and the round trip agreed with a UTF-8-console run -----------------
    rc2, snap_ref, _ = run_tool(SNAPSHOT, ["--replay", transcript])
    rows.append({
        "case_id": "B-roundtrip", "clause": "P0-2 round trip",
        "description": "the cp936 run and the ordinary run emit identical bytes",
        "required": "identical", "exercised": True,
        "observed": "identical" if snap_ref == snap_bytes else "differing",
        "detail": "the console codec must make no difference to the emitted "
                  "document at all"})
    return rows, "byte-contract"


def load_em_dash_workflow():
    """Read a U+2014-bearing Workflow value out of the frozen schema.

    Never typed here: a harness that re-typed the mark would test its own typo.
    """
    with open(SCHEMA, "rb") as fh:
        schema = json.loads(fh.read().decode("utf-8"))
    for value in schema["$defs"]["item"]["properties"]["workflow"]["enum"]:
        if "\u2014" in value:
            return value
    raise InputError("STRUCTURE: no U+2014-bearing Workflow value in the frozen schema")


# ------------------------------------------------------------------ corpus

def mode_corpus(args, tmp):
    with open(EXPECTATIONS, "rb") as fh:
        expectations = json.loads(fh.read().decode("utf-8"))
    rows = []
    for case in expectations["cases"]:
        fixture = os.path.join(CORPUS, case["fixture"])
        out = os.path.join(tmp, case["id"] + "-report.json")
        rc, _, err = run_tool(FRONTIER, [fixture, "--out", out])
        # A corpus case the SCHEMA calls invalid must be REFUSED by the consumer
        # (exit 1); a case it calls valid must be consumed (exit 0 or 3, the
        # latter when the document is legitimately degraded).
        required = "refused" if case["expect"] == "invalid" else "consumed"
        observed = "refused" if rc == 1 else ("consumed" if rc in (0, 3) else "error")
        rows.append({"case_id": case["id"], "clause": case["class"],
                     "description": case["fixture"], "required": required,
                     "observed": observed, "exercised": True, "consumer_exit": rc})
    return rows, "corpus"


# ------------------------------------------------------------------ report

def emit_report(rows, mode, out_path):
    unexercised = [r for r in rows if not r.get("exercised")]
    failed = [r for r in rows
              if r.get("exercised") and r["observed"] != r["required"]]

    width = max(len(r["case_id"]) for r in rows)
    cwidth = max(len(r["clause"]) for r in rows)
    print("%-*s %-*s %-18s %-18s %s"
          % (width, "case", cwidth, "clause", "required", "observed", "verdict"))
    for r in rows:
        ok = r.get("exercised") and r["observed"] == r["required"]
        print("%-*s %-*s %-18s %-18s %s"
              % (width, r["case_id"], cwidth, r["clause"],
                 str(r["required"])[:18], str(r["observed"])[:18],
                 "PASS" if ok else "FAIL"))
    print()
    print("mode                          : %s" % mode)
    print("harness                       : %s %s" % (HARNESS_NAME, HARNESS_VERSION))
    print("interpreter                   : %s" % sys.executable)
    print("network reads performed       : 0")
    print("cases declared                : %d" % len(rows))
    print("cases meeting required outcome: %d" % (len(rows) - len(failed) - len(unexercised)))
    print("classes reported unexercised  : %d" % len(unexercised))
    for r in unexercised:
        print("   %-24s %s" % (r["case_id"], r.get("detail", "")))
    print("cases failing                 : %d" % len(failed))
    for r in failed:
        print("   %-24s required=%s observed=%s"
              % (r["case_id"], r["required"], r["observed"]))

    if mode == "induced-failures":
        undecided = [r for r in rows if r.get("exercised")
                     and r["observed"] == "undecidable"]
        print("induced classes carrying undecidable : %d / %d"
              % (len(undecided), len(rows)))
    if mode == "dependency-directions":
        both = [r for r in rows if r.get("both_directions_non_empty")]
        print("cases exercising a NON-EMPTY relation in BOTH directions : %d"
              % len(both))
        arm = [r for r in rows if r.get("positive_arm_complete")]
        print("allOf[2] positive arm complete (id, workflow and verdict) : %d"
              % len(arm))

    clean = not failed and not unexercised
    print()
    if clean:
        print("ACCEPTANCE CLEAN: every declared case met its required outcome")
    else:
        print("ACCEPTANCE NOT CLEAN: see the FAIL rows above")

    if out_path:
        document = {
            "report": "gatebraid/o0-acceptance@1",
            "harness": {"name": HARNESS_NAME, "version": HARNESS_VERSION},
            "mode": mode,
            "cases": rows,
            "summary": {
                "declared": len(rows),
                "met": len(rows) - len(failed) - len(unexercised),
                "unexercised": len(unexercised),
                "failed": len(failed),
                "clean": clean,
            },
        }
        parent = os.path.dirname(os.path.abspath(out_path))
        if parent and not os.path.isdir(parent):
            os.makedirs(parent)
        with open(out_path, "wb") as fh:
            fh.write((json.dumps(document, ensure_ascii=False, indent=1,
                                 sort_keys=True) + "\n").encode("utf-8"))
        print("out                           : %s" % out_path)
    return 0 if clean else 1


def main(argv=None):
    ap = argparse.ArgumentParser(
        prog=HARNESS_NAME,
        description="End-to-end acceptance for M3 node O0's fail-closed pair.")
    group = ap.add_mutually_exclusive_group(required=True)
    group.add_argument("--induced-failures", action="store_true")
    group.add_argument("--dependency-directions", action="store_true")
    group.add_argument("--byte-contract", action="store_true")
    group.add_argument("--corpus", action="store_true")
    ap.add_argument("--out", metavar="PATH", help="write the case report here")
    args = ap.parse_args(argv)

    for required in (SNAPSHOT, FRONTIER, CANONICAL, SCHEMA, EXPECTATIONS):
        if not os.path.isfile(required):
            sys.stderr.write("USAGE: required input not found at %s\n" % required)
            return 2

    tmp = tempfile.mkdtemp(prefix="gatebraid-o0-acceptance-")
    try:
        if args.induced_failures:
            rows, mode = mode_induced(args, tmp)
        elif args.dependency_directions:
            rows, mode = mode_directions(args, tmp)
        elif args.byte_contract:
            rows, mode = mode_byte_contract(args, tmp)
        else:
            rows, mode = mode_corpus(args, tmp)
    except InputError as exc:
        sys.stderr.write("%s\n" % exc)
        return 2
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    return emit_report(rows, mode, args.out)


if __name__ == "__main__":
    sys.exit(main())

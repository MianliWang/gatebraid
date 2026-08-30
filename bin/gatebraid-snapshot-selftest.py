#!/usr/bin/env python3
"""gatebraid-snapshot-selftest - falsify the snapshot producer before it is trusted.

ADR-0028 decision 1: a check is falsified once before it is trusted.  This file
seeds a condition for every rule `gatebraid-snapshot` claims to enforce and
asserts the EXIT STATUS each must produce, plus a required observation in the
output where the exit status alone would not distinguish the outcomes.

WHY THE SEEDS GO THROUGH THE REPLAY TRANSPORT AND NOT THROUGH A STUB.  The
transport supplies only what a real read supplies - an exit status, two streams,
and the two headers that separate the 403 classes.  Classification, assembly,
verdict derivation and self-validation are then the tool's own, unmodified.  A
seed therefore measures the tool rather than a mock of it.  Nothing here
contacts the network: there is no live read in this file and no HTTP client.

EACH SEED BREAKS EXACTLY ONE RELATION in a document known to be healthy, so a
condition that passes under both the correct and the broken tool - which
measures nothing - cannot survive here.  The healthy document itself is a seeded
condition (S08): a fail-closed tool that rejected everything would pass every
negative case and fail that one, which is the GR2-07 lesson the frozen corpus
records.

The seeds are written to a temporary directory OUTSIDE every repository
(`tempfile.mkdtemp()`), which `protocols/gate-2-contract.md` permits explicitly
and which this Slice's Gate 2 evidence names.  Nothing under the repository is
written by this file.

Green is: every seeded condition produces its required exit status and required
observation, and the summary reports `conditions failed : 0`.  Counts are
deliberately absent from the acceptance criteria - the caller reads the summary,
not a number of conditions, so adding a condition never falsifies a frozen
expectation.

Exit codes: 0 all conditions produced their required status - 1 one or more did
not - 2 the harness itself could not run.  Python 3 standard library only.
"""

import copy
import json
import os
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
TOOL = os.path.join(HERE, "gatebraid-snapshot.py")
SCHEMA = os.path.join(REPO, "schema", "snapshot.schema.json")


def run(args):
    """Invoke the tool as a subprocess so the EXIT STATUS is the real one.

    stdout is kept as BYTES and never decoded here: this harness checks a byte
    contract, and a harness that decodes before comparing cannot see the defect
    it exists to catch.
    """
    env = dict(os.environ)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    proc = subprocess.run([sys.executable, "-B", TOOL] + args, cwd=REPO,
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env)
    return proc.returncode, proc.stdout, proc.stderr.decode("utf-8", "replace")


def write_json(path, doc):
    with open(path, "wb") as fh:
        fh.write((json.dumps(doc, ensure_ascii=False, indent=1) + "\n").encode("utf-8"))
    return path


def with_exit_status(doc):
    """Stamp the success exit onto any transcript page that does not name one.

    The TOOL refuses a page with no exit status, because defaulting it to 0
    would put an implicit success assumption on a path that reaches a verdict.
    This helper makes the SEEDS say `exit_code: 0` explicitly instead: the
    fixture states success and the tool never infers it.
    """
    for entry in (doc.get("reads") or {}).values():
        pages = entry if isinstance(entry, list) else [entry]
        for page in pages:
            page.setdefault("exit_code", 0)
    return doc


def healthy_transcript():
    """A document with every source `ok` and complete. The positive control."""
    return with_exit_status({
        "reads": {
            "project_items": {"stdout": {"nodes": [
                {"item_id": "PVTI_a", "issue": "MianliWang/gatebraid#14",
                 "slice_metadata_present": True, "slice_id": "P2-S4",
                 "workflow_raw": "Needs Plan Approval",
                 "soft_dependencies_declared": False},
                {"item_id": "PVTI_b", "issue": "MianliWang/gatebraid#3",
                 "slice_metadata_present": False,
                 "excluded_reason": "a Phase container row, not a Slice"},
            ], "hasNextPage": False}},
            "issue_states": {"stdout": {"states": {
                "MianliWang/gatebraid#14": "OPEN",
                "MianliWang/gatebraid#3": "OPEN"}}},
            "dep_blocked_by": {"stdout": {"edges": {}}},
            "dep_blocking": {"stdout": {"edges": {}}},
        }
    })


def seed(mutate):
    doc = copy.deepcopy(healthy_transcript())
    mutate(doc["reads"])
    # Normalised AFTER the mutation: a seed that replaces a source entry
    # supplies a fresh page, and that page must state its exit status too.
    return with_exit_status(doc)


class Conditions(object):
    def __init__(self):
        self.rows = []

    def check(self, cid, name, want, got, observation, marker=None, output=""):
        ok = (got == want)
        if marker is not None:
            ok = ok and (marker in output)
        self.rows.append((cid, name, want, got, ok, observation))
        return ok


def status_of(path, source_id):
    doc = json.load(open(path, encoding="utf-8"))
    for s in doc["sources"]:
        if s["source_id"] == source_id:
            return s
    return {}


def item_of(path, item_id):
    doc = json.load(open(path, encoding="utf-8"))
    for i in doc["items"]:
        if i["item_id"] == item_id:
            return i
    return {}


CORPUS = os.path.join(REPO, "fixtures", "live-shapes")


def corpus_body(name):
    """One frozen live body, as BYTES-decoded text, exactly as the surface sent it.

    These are the O1-B1 transcripts: real control-plane responses, sealed with
    their provenance captures. Reading them here is what lets the LIVE half be
    exercised without a network read.
    """
    with open(os.path.join(CORPUS, name), encoding="utf-8") as fh:
        return fh.read()


def load_tool_module():
    """Import the tool in-process so the LIVE transport itself can be driven.

    The subprocess seeds above exercise the replay path. The live path has its
    own argv construction and its own body normalisation, and neither is
    reachable through `--replay` - which is exactly the F-04 gap this Slice
    pays down. Importing the module under test is not a stub of it: the
    classifier, `read_source`, the assembly and the verdicts below are the
    tool's own, unmodified.
    """
    import importlib.util
    spec = importlib.util.spec_from_file_location("gatebraid_snapshot_under_test", TOOL)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def frozen_live_transport(mod, bodies):
    """A LiveTransport whose `_run` serves frozen bodies. NO network read occurs.

    Only the process-execution boundary is replaced. Endpoint selection, body
    normalisation, classification, pagination and assembly are the tool's own.
    """
    class FrozenLive(mod.LiveTransport):
        def _run(self, argv):
            if len(argv) > 1 and argv[1] == "project":
                key = "project_items"
            else:
                path = argv[2]
                if path.endswith("/dependencies/blocked_by"):
                    key = "dep_blocked_by"
                elif path.endswith("/dependencies/blocking"):
                    key = "dep_blocking"
                else:
                    key = "issue_states"
            body = bodies[key]
            if callable(body):
                body = body(argv)
            return mod.ReadResult(exit_code=0, stdout=body)

    return FrozenLive("MianliWang", 1, "MianliWang/gatebraid")


def enums_of(mod, schema):
    return {
        "status": mod.enum_at(schema, "$defs", "source", "properties", "status"),
        "issue_state": mod.enum_at(schema, "$defs", "item", "properties", "issue_state"),
        "workflow": mod.enum_at(schema, "$defs", "item", "properties", "workflow"),
        "verdict": mod.enum_at(schema, "$defs", "item", "properties", "verdict"),
    }


def source_of(doc, source_id):
    for s in doc["sources"]:
        if s["source_id"] == source_id:
            return s
    return {}


def slice_item(doc, slice_id):
    for i in doc["items"]:
        if i.get("slice_id") == slice_id:
            return i
    return {}


def main():
    if not os.path.isfile(TOOL):
        print("HARNESS: tool not found at %s" % TOOL)
        return 2
    if not os.path.isfile(SCHEMA):
        print("HARNESS: frozen schema not found at %s" % SCHEMA)
        return 2

    schema = json.load(open(SCHEMA, encoding="utf-8"))
    # The enumerations are READ, never typed: four Workflow values carry U+2014
    # and a harness that re-typed one would test its own typo.
    workflows = schema["$defs"]["item"]["properties"]["workflow"]["enum"]
    em_dash_workflow = next(w for w in workflows if "—" in w)

    tmp = tempfile.mkdtemp(prefix="gatebraid-snapshot-selftest-")
    c = Conditions()
    try:
        # ---- the positive control -------------------------------------------
        p = write_json(os.path.join(tmp, "healthy.json"), healthy_transcript())
        out = os.path.join(tmp, "healthy-out.json")
        rc, _, err = run(["--replay", p, "--out", out])
        c.check("S01", "a healthy read emits and exits 0", 0, rc,
                "a fail-closed tool that rejected everything would fail HERE and "
                "pass every negative below", "SNAPSHOT OK", err)
        c.check("S02", "the healthy positive control is startable", "startable",
                item_of(out, "PVTI_a").get("verdict") if rc == 0 else "n/a",
                "the tool can still say yes; fail-closed is not reject-everything")

        # ---- P0-1: the seven closed failure classes, one seed each ----------
        classes = [
            ("S03", "auth_failure", "401 answered on a read",
             lambda r: r.update({"issue_states": {"http_status": 401, "exit_code": 1,
                                                  "stderr": "HTTP 401"}})),
            ("S04", "permission_failure", "403 with budget remaining",
             lambda r: r.update({"issue_states": {"http_status": 403, "exit_code": 1,
                                                  "rate_limit_remaining": 17,
                                                  "stderr": "HTTP 403"}})),
            ("S05", "rate_limited", "403 with the budget exhausted",
             lambda r: r.update({"issue_states": {"http_status": 403, "exit_code": 1,
                                                  "rate_limit_remaining": 0,
                                                  "stderr": "HTTP 403"}})),
            ("S06", "network_error", "the read could not be performed",
             lambda r: r.update({"issue_states": {"exit_code": 1,
                                                  "transport_error": "connection refused"}})),
            ("S07", "server_error", "the endpoint answered 503",
             lambda r: r.update({"issue_states": {"http_status": 503, "exit_code": 1,
                                                  "stderr": "HTTP 503"}})),
            ("S08", "parse_error", "a body that is not JSON",
             lambda r: r.update({"issue_states": {"exit_code": 0,
                                                  "stdout": "{not json"}})),
            ("S09", "unexpected_endpoint", "a shape the tool does not recognise",
             lambda r: r.update({"issue_states": {"exit_code": 0, "stdout": "[1,2,3]"}})),
        ]
        for cid, want_status, why, mutate in classes:
            p = write_json(os.path.join(tmp, cid + ".json"), seed(mutate))
            out = os.path.join(tmp, cid + "-out.json")
            rc, _, err = run(["--replay", p, "--out", out])
            got = status_of(out, "issue_states").get("status") if rc == 3 else "exit%d" % rc
            c.check(cid, "P0-1 %s (%s)" % (want_status, why), want_status, got,
                    "a class with no seeded condition is a class nobody has shown to fire")

        # ---- P0-1: a degraded read can never exit 0 -------------------------
        p = write_json(os.path.join(tmp, "S10.json"),
                       seed(lambda r: r.update({"issue_states": {"http_status": 401,
                                                                 "exit_code": 1,
                                                                 "stderr": "HTTP 401"}})))
        rc, _, err = run(["--replay", p, "--out", os.path.join(tmp, "S10-out.json")])
        c.check("S10", "a degraded snapshot exits 3, never 0", 3, rc,
                "the exit status is the only thing a shell caller reads",
                "SNAPSHOT DEGRADED", err)

        # ---- P0-1: a degraded read forces every verdict to undecidable ------
        out = os.path.join(tmp, "S10-out.json")
        c.check("S11", "degraded forces verdict undecidable", "undecidable",
                item_of(out, "PVTI_a").get("verdict"),
                "the dropped-edge-read-as-no-blocker defect, structurally refused")

        # ---- P0-1: a non-zero process exit is surfaced, never folded --------
        c.check("S12", "the non-zero process exit reaches the document", 1,
                status_of(out, "issue_states").get("exit_code"),
                "ADR-0029 decision 2 P0-1: a non-zero gh exit folded into None")

        # ---- the read-outcome sentinel, and the real exit kept recoverable --
        p = write_json(os.path.join(tmp, "S13.json"),
                       seed(lambda r: r.update({"issue_states": {"exit_code": 0,
                                                                 "stdout": "{not json"}})))
        out = os.path.join(tmp, "S13-out.json")
        rc, _, err = run(["--replay", p, "--out", out])
        src = status_of(out, "issue_states")
        c.check("S13", "a zero-exit failed read carries the sentinel", 65,
                src.get("exit_code"),
                "the schema forbids a non-ok status reporting a success exit")
        c.check("S14", "and names the real process exit in failure_detail", True,
                "exited 0" in (src.get("failure_detail") or ""),
                "the process status stays recoverable rather than being lost")

        # ---- P0-3: the page cap fails closed --------------------------------
        p = write_json(os.path.join(tmp, "S15.json"), seed(lambda r: r.update(
            {"project_items": [{"stdout": {"nodes": [], "hasNextPage": True}},
                               {"stdout": {"nodes": [], "hasNextPage": True}}]})))
        out = os.path.join(tmp, "S15-out.json")
        rc, _, err = run(["--replay", p, "--out", out, "--page-cap", "1"])
        b = status_of(out, "project_items").get("bounded") or {}
        c.check("S15", "P0-3 the cap sets bounded and degrades", "page_cap_reached",
                b.get("reason"), "a truncated list reported as whole is the P0-3 defect")
        c.check("S16", "P0-3 the capped read is not complete", False,
                status_of(out, "project_items").get("complete"),
                "completeness asserted without pagination")
        c.check("S17", "P0-3 a capped read exits 3", 3, rc,
                "reaching a cap fails closed rather than passing")

        # ---- P0-3: a FAILED read is an incomplete read and says where -------
        c.check("S18", "a failed read carries bounded query_failed", "query_failed",
                (status_of(os.path.join(tmp, "S10-out.json"), "issue_states")
                 .get("bounded") or {}).get("reason"),
                "an incomplete read that does not say where it stopped is "
                "indistinguishable from a complete one")

        # ---- P0-4: an unrecognised state becomes UNKNOWN, not OPEN ----------
        p = write_json(os.path.join(tmp, "S19.json"), seed(lambda r: r.update(
            {"issue_states": {"stdout": {"states": {
                "MianliWang/gatebraid#14": "LOCKED",
                "MianliWang/gatebraid#3": "OPEN"}}}})))
        out = os.path.join(tmp, "S19-out.json")
        rc, _, err = run(["--replay", p, "--out", out])
        it = item_of(out, "PVTI_a")
        c.check("S19", "P0-4 an unknown issue state maps to UNKNOWN", "UNKNOWN",
                it.get("issue_state"), "state != OPEN read as unblocked is the defect")
        c.check("S20", "P0-4 and yields undecidable, never unblocked", "undecidable",
                it.get("verdict"), "the unblocked reading is what P0-4 names")
        c.check("S21", "P0-4 the unrecognised value is kept for diagnosis", True,
                it.get("issue_state_raw") is not None,
                "diagnosable without being trusted")

        # ---- P0-4: an unrecognised workflow degrades too ---------------------
        p = write_json(os.path.join(tmp, "S22.json"), seed(lambda r: r.update(
            {"project_items": {"stdout": {"nodes": [
                {"item_id": "PVTI_a", "issue": "MianliWang/gatebraid#14",
                 "slice_metadata_present": True, "slice_id": "P2-S4",
                 "workflow_raw": "Gate 9 - Inventing",
                 "soft_dependencies_declared": False}], "hasNextPage": False}}})))
        out = os.path.join(tmp, "S22-out.json")
        rc, _, err = run(["--replay", p, "--out", out])
        c.check("S22", "P0-4 an unrecognised workflow yields undecidable", "undecidable",
                item_of(out, "PVTI_a").get("verdict"),
                "an open vocabulary would let a new value arrive as a string nobody checks")

        # ---- P0-4: no verdict at all for a non-Slice row --------------------
        out = os.path.join(tmp, "healthy-out.json")
        nonslice = item_of(out, "PVTI_b")
        c.check("S23", "P0-4 a non-Slice row carries no verdict", True,
                "verdict" not in nonslice,
                "a verdict emitted for a non-Slice row is SP-09")
        c.check("S24", "P0-4 and states why it was excluded", True,
                bool(nonslice.get("excluded_reason")),
                "an exclusion nobody can read is indistinguishable from an omission")

        # ---- P0-4: both directions, cross-checked ---------------------------
        p = write_json(os.path.join(tmp, "S25.json"), seed(lambda r: r.update(
            {"dep_blocked_by": {"stdout": {"edges": {
                "MianliWang/gatebraid#14": [{"issue": "MianliWang/gatebraid#3",
                                             "state": "OPEN"}]}}},
             "dep_blocking": {"stdout": {"edges": {}}}})))
        out = os.path.join(tmp, "S25-out.json")
        rc, _, err = run(["--replay", p, "--out", out])
        it = item_of(out, "PVTI_a")
        c.check("S25", "P0-4 a one-directional read is a mismatch", "mismatch",
                it.get("dependencies", {}).get("cross_check"),
                "one direction trusted without the cross-check is SP-11")
        c.check("S26", "P0-4 and a mismatch yields undecidable", "undecidable",
                it.get("verdict"),
                "not a tie broken in favour of the direction that was read")

        # ---- P0-4: a declared soft dependency is parsed, or it says so ------
        p = write_json(os.path.join(tmp, "S27.json"), seed(lambda r: r.update(
            {"project_items": {"stdout": {"nodes": [
                {"item_id": "PVTI_a", "issue": "MianliWang/gatebraid#14",
                 "slice_metadata_present": True, "slice_id": "P2-S4",
                 "workflow_raw": "Needs Plan Approval",
                 "soft_dependencies_declared": True,
                 "soft_dependencies_raw": "   "}], "hasNextPage": False}}})))
        out = os.path.join(tmp, "S27.out.json")
        rc, _, err = run(["--replay", p, "--out", out])
        it = item_of(out, "PVTI_a")
        c.check("S27", "P0-4 an unparsed soft dependency says not_parsed", "not_parsed",
                it.get("soft_dependencies", {}).get("parse_status"),
                "silent ignore is SP-12")
        c.check("S28", "P0-4 and costs the verdict", "undecidable", it.get("verdict"),
                "an unparsed declaration cannot leave the item startable")

        # ---- ADR-0025 decision 8: Aborted is never startable ----------------
        p = write_json(os.path.join(tmp, "S29.json"), seed(lambda r: r.update(
            {"project_items": {"stdout": {"nodes": [
                {"item_id": "PVTI_a", "issue": "MianliWang/gatebraid#14",
                 "slice_metadata_present": True, "slice_id": "P2-S4",
                 "workflow_raw": "Aborted",
                 "soft_dependencies_declared": False}], "hasNextPage": False}}})))
        out = os.path.join(tmp, "S29-out.json")
        rc, _, err = run(["--replay", p, "--out", out])
        c.check("S29", "ADR-0025 d8 an Aborted item is never startable", True,
                item_of(out, "PVTI_a").get("verdict") != "startable",
                "the candidacy intersection, from measured friction #85")

        # ---- P0-2: the byte contract ----------------------------------------
        p = write_json(os.path.join(tmp, "S30.json"), seed(lambda r: r.update(
            {"project_items": {"stdout": {"nodes": [
                {"item_id": "PVTI_a", "issue": "MianliWang/gatebraid#14",
                 "slice_metadata_present": True, "slice_id": "P2-S4",
                 "workflow_raw": em_dash_workflow,
                 "soft_dependencies_declared": False}], "hasNextPage": False}}})))
        rc, stdout_bytes, err = run(["--replay", p])
        c.check("S30", "P0-2 stdout carries the document as UTF-8 bytes", True,
                em_dash_workflow.encode("utf-8") in stdout_bytes,
                "a text-layer write under a non-UTF-8 console corrupts this exact mark")
        c.check("S31", "P0-2 stdout carries the document and nothing else", True,
                stdout_bytes.strip().startswith(b"{") and stdout_bytes.strip().endswith(b"}"),
                "the summary goes to stderr so the byte contract stays clean")

        # ---- self-validation actually gates emission ------------------------
        strict = copy.deepcopy(schema)
        strict.setdefault("required", []).append("a_property_no_document_carries")
        sp = write_json(os.path.join(tmp, "strict-schema.json"), strict)
        p = write_json(os.path.join(tmp, "S33.json"), healthy_transcript())
        out = os.path.join(tmp, "S33-out.json")
        rc, stdout_bytes, err = run(["--replay", p, "--out", out, "--schema", sp])
        c.check("S32", "a document that fails self-validation is not emitted", 1, rc,
                "emitting a malformed snapshot is worse than emitting none",
                "SNAPSHOT NOT EMITTED", err)
        c.check("S33", "and nothing was written to the output path", False,
                os.path.isfile(out),
                "a partial file on disk would be read by the next consumer")

        # ---- usage failures are distinct from degraded reads ----------------
        rc, _, err = run(["--replay", os.path.join(tmp, "does-not-exist.json")])
        c.check("S34", "an absent transcript is a usage error", 2, rc,
                "input failure must not be reported as a degraded read", "USAGE", err)
        rc, _, err = run(["--replay", p, "--page-cap", "0"])
        c.check("S35", "a nonsense page cap is a usage error", 2, rc,
                "a cap of zero would make every read bounded and look like P0-3", "USAGE", err)
        rc, _, err = run(["--replay", p, "--schema", os.path.join(tmp, "no-schema.json")])
        c.check("S36", "an absent schema is a usage error, never a pass", 2, rc,
                "a tool that cannot self-validate must not emit", "STRUCTURE", err)

        # ---- a transcript page that names no exit status is NOT success -----
        # Written WITHOUT with_exit_status() on purpose: this is the one seed
        # that must reach the tool with the field genuinely absent.
        bare = {"reads": {
            "project_items": {"stdout": {"nodes": [], "hasNextPage": False}},
            "issue_states": {"stdout": {"states": {}}},
            "dep_blocked_by": {"stdout": {"edges": {}}},
            "dep_blocking": {"stdout": {"edges": {}}}}}
        p = write_json(os.path.join(tmp, "S37.json"), bare)
        out = os.path.join(tmp, "S37-out.json")
        rc, _, err = run(["--replay", p, "--out", out])
        c.check("S37", "a page naming no exit status is not read as success", 3, rc,
                "defaulting an absent exit to 0 is an implicit success "
                "assumption on a verdict-relevant path; N2 found it here")

        # ---- the LIVE half, driven by the frozen O1-B1 transcripts ---------
        # Everything below reads a frozen body and performs NO network read.
        mod = load_tool_module()
        schema_doc, _sp, _ss = mod.load_schema(None)
        enums = enums_of(mod, schema_doc)

        ls01 = corpus_body("ls01-item-list-full.json")
        ls02 = corpus_body("ls02-item-list-short-read.json")
        ls03 = corpus_body("ls03-issue-object.json")
        ls04 = corpus_body("ls04-issue-list-bulk.json")
        ls05 = corpus_body("ls05-dependency-list-four-edges.json")
        ls06 = corpus_body("ls06-dependency-list-empty.json")
        ls07 = corpus_body("ls07-dependency-list-one-edge.json")

        # LA-1: the four endpoints, constructed and asserted rather than assumed.
        t = mod.LiveTransport("MianliWang", 1, "MianliWang/gatebraid")
        t.set_fanout([("MianliWang/gatebraid", 17)])
        argvs = {sid: t.argv_for(sid, 0) for sid in mod.SOURCE_IDS}
        want_argv = {
            "project_items": ["gh", "project", "item-list", "1", "--owner",
                              "MianliWang", "--format", "json"],
            "issue_states": ["gh", "api", "repos/MianliWang/gatebraid/issues/17"],
            "dep_blocked_by": ["gh", "api",
                               "repos/MianliWang/gatebraid/issues/17/dependencies/blocked_by"],
            "dep_blocking": ["gh", "api",
                             "repos/MianliWang/gatebraid/issues/17/dependencies/blocking"],
        }
        c.check("LA-1", "each source builds its own per-issue endpoint",
                True, argvs == want_argv,
                "D-A was one bulk endpoint for three sources; the four argv "
                "forms are asserted here, not assumed")
        c.check("LA-2", "no endpoint is the bulk issue list",
                False,
                any(a == ["gh", "api", "repos/MianliWang/gatebraid/issues"]
                    for a in argvs.values()),
                "the bulk endpoint is the defect; it must appear nowhere")

        # LS-01: the item-list envelope parses to the TRUE item set.
        page = t._page_project_items(json.loads(ls01))
        c.check("LS-01", "C-3 envelope yields 15 nodes", 15,
                len(page["nodes"]) if page else -1,
                "len(items) == totalCount == 15; the broken parser yielded 0")
        c.check("LS-01b", "11 rows carry Slice metadata, 4 are excluded",
                (11, 4),
                ((sum(1 for n in page["nodes"] if n["slice_metadata_present"]),
                  sum(1 for n in page["nodes"] if not n["slice_metadata_present"]))
                 if page else (-1, -1)),
                "container rows carry no Slice field and are excluded with a reason")
        c.check("LS-01c", "no short-read flag on a complete envelope",
                False, ("_short_read" in page) if page else True,
                "len(items) == totalCount is a whole read")
        c.check("LS-01d", "an optional key is read byte-exactly when present",
                "P2-S5",
                next((n.get("slice_id") for n in page["nodes"]
                      if n.get("slice_id") == "P2-S5"), None) if page else None,
                "keys are Project field names emitted only when populated")

        # LS-02 / LB-1: a short read is INCOMPLETE. `complete: true` is the
        # seeded wrong outcome.
        page2 = t._page_project_items(json.loads(ls02))
        c.check("LS-02", "C-4 short read carries the short-read flag",
                {"observed": 2, "declared": 15},
                (page2 or {}).get("_short_read"),
                "the envelope has NO pagination key, so completeness is arithmetic")

        # LS-03: a per-issue object yields one state, upper-cased by explicit map.
        st = t._page_issue_state(0, json.loads(ls03))
        c.check("LS-03", "C-2 issue object yields its state",
                {"MianliWang/gatebraid#17": "OPEN"},
                (st or {}).get("states"),
                "the live surface spells state in lower case; the map is explicit")

        # LS-05 / LB-4: CLOSED blockers are OBSERVABLE per-issue.
        ed = t._page_dependencies(0, json.loads(ls05))
        edges = (ed or {}).get("edges", {}).get("MianliWang/gatebraid#17", [])
        c.check("LS-05", "C-5 yields the four blocker edges",
                ["MianliWang/gatebraid#8", "MianliWang/gatebraid#10",
                 "MianliWang/gatebraid#12", "MianliWang/gatebraid#14"],
                [e["issue"] for e in edges],
                "the dependency edge set the plan-DAG record carries")
        c.check("LB-4", "every one of those four is observed CLOSED",
                ["CLOSED"] * 4, [e["state"] for e in edges],
                "B-4: the bulk endpoint is open-only and cannot see them at all")
        c.check("LB-4b", "the bulk body contains none of those four issues",
                True,
                all(n not in [el.get("number") for el in json.loads(ls04)]
                    for n in (8, 10, 12, 14)),
                "C-1 beside C-5 is the frozen evidence disqualifying the bulk endpoint")

        # LS-06 / LS-07: a lawful empty answer and a one-edge answer.
        ed6 = t._page_dependencies(0, json.loads(ls06))
        c.check("LS-06", "C-6 empty list is a lawful zero-edge answer",
                [], (ed6 or {}).get("edges", {}).get("MianliWang/gatebraid#17"),
                "an empty list is an ANSWER, not an absence")
        ed7 = t._page_dependencies(0, json.loads(ls07))
        c.check("LS-07", "C-7 one-edge answer yields exactly that edge",
                ["MianliWang/gatebraid#17"],
                [e["issue"] for e in (ed7 or {}).get("edges", {})
                 .get("MianliWang/gatebraid#17", [])],
                "the measured one-edge dependency set")

        # LS-04 / LB-2: a bulk list offered as a dependency answer is REFUSED.
        c.check("LS-04", "a bulk issue list is refused as a dependency answer",
                None, t._page_dependencies(0, json.loads(ls04)),
                "B-2: no element carries `repository`; refusing beats parsing")

        # ---- end-to-end runs through the real pipeline ---------------------
        def build(bodies):
            tr = frozen_live_transport(mod, bodies)
            return mod.build_document(tr, schema_doc, enums, 10, "2026-01-01T00:00:00Z")

        healthy = {"project_items": ls01, "issue_states": ls03,
                   "dep_blocked_by": ls05, "dep_blocking": ls06}

        # LB-1 end to end: the short envelope makes the source INCOMPLETE.
        doc, degraded = build(dict(healthy, project_items=ls02))
        src = source_of(doc, "project_items")
        c.check("LB-1", "a short read reports incomplete and bounded",
                ("ok", False, "connection_truncated"),
                (src.get("status"), src.get("complete"),
                 (src.get("bounded") or {}).get("reason")),
                "B-1: `complete: true` is the seeded wrong outcome")
        c.check("LB-1b", "and the document is degraded, so nothing is startable",
                (True, 0),
                (degraded, sum(1 for i in doc["items"]
                               if i.get("verdict") == "startable")),
                "an incomplete source must not yield a healthy verdict")

        # LB-2 end to end: the bulk body as a dependency answer.
        doc, degraded = build(dict(healthy, dep_blocked_by=ls04))
        src = source_of(doc, "dep_blocked_by")
        item = slice_item(doc, "P2-S5")
        c.check("LB-2", "a bulk body as a dependency answer fails the source closed",
                ("unexpected_endpoint", False, 65),
                (src.get("status"), src.get("complete"), src.get("exit_code")),
                "B-2: refused as the wrong surface, sentinel 65")
        c.check("LB-2b", "and the affected item is undecidable, never startable",
                ("undecidable", "not_performed"),
                (item.get("verdict"),
                 (item.get("dependencies") or {}).get("cross_check")),
                "B-2: the two-direction cross-check did not happen, so it is said")

        # LB-3 end to end: a Slice row whose `workflow` key is absent.
        short_env = json.loads(ls01)
        for el in short_env["items"]:
            if el.get("slice") == "P2-S5":
                el.pop("workflow", None)
        doc, degraded = build(dict(healthy,
                                   project_items=json.dumps(short_env, ensure_ascii=False)))
        item = slice_item(doc, "P2-S5")
        c.check("LB-3", "an absent `workflow` maps to UNKNOWN, hence undecidable",
                ("UNKNOWN", "undecidable"),
                (item.get("workflow"), item.get("verdict")),
                "B-3: never a KeyError, never a default toward healthy")

        # The positive control for the live half: the healthy set is healthy.
        doc, degraded = build(healthy)
        c.check("LB-0", "the healthy frozen set reads healthy",
                (False, 4),
                (degraded, sum(1 for s in doc["sources"]
                               if s["status"] == "ok" and s["complete"])),
                "a live half that rejected everything would fail HERE and pass "
                "every negative above")

        # A dependent source whose fan-out set is empty must FAIL CLOSED.
        empty = mod.LiveTransport("MianliWang", 1, "MianliWang/gatebraid")
        empty.set_fanout([])
        c.check("LA-3", "a dependent source with an empty fan-out has no endpoint",
                None, empty.argv_for("issue_states", 0),
                "it must fail closed saying so, never invent a set it was not given")

    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    width = max(len(r[1]) for r in c.rows)
    print("%-6s %-*s %-13s %-13s %-7s %s"
          % ("id", width, "condition", "want", "got", "verdict", "required observation"))
    failed = 0
    for cid, name, want, got, ok, obs in c.rows:
        if not ok:
            failed += 1
        print("%-6s %-*s %-13s %-13s %-7s %s"
              % (cid, width, name, str(want)[:13], str(got)[:13],
                 "PASS" if ok else "FAIL", obs))
    print()
    print("scratch directory             : outside every repository (tempfile.mkdtemp)")
    print("tool under test               : %s" % TOOL)
    print("interpreter                   : %s" % sys.executable)
    print("network reads performed       : 0 (replay transport, and frozen O1-B1\n                                bodies for the live half)")
    print("conditions failed             : %d" % failed)
    if failed == 0:
        print("SELFTEST CLEAN: every seeded condition produced its required exit status")
    else:
        print("SELFTEST NOT CLEAN: see the FAIL rows above")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())

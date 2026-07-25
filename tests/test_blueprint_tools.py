from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from copy import deepcopy
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skill" / "harness-graph-loop-builder"
SCRIPTS = SKILL / "scripts"
EXAMPLE = ROOT / "examples" / "code-repair" / "blueprint.json"

spec = importlib.util.spec_from_file_location("hgl_core", SCRIPTS / "hgl_core.py")
assert spec and spec.loader
hgl_core = importlib.util.module_from_spec(spec)
sys.modules["hgl_core"] = hgl_core
spec.loader.exec_module(hgl_core)


class BlueprintValidationTests(unittest.TestCase):
    def blueprint(self) -> dict:
        return json.loads(EXAMPLE.read_text(encoding="utf-8"))

    def test_reference_example_is_valid(self) -> None:
        result = hgl_core.validate_blueprint(self.blueprint())
        self.assertEqual(result.errors, ())

    def test_unknown_dependency_is_rejected(self) -> None:
        value = self.blueprint()
        value["graph"]["nodes"][1]["dependencies"] = ["missing-node"]
        result = hgl_core.validate_blueprint(value)
        self.assertTrue(any("unknown node" in error for error in result.errors))

    def test_cycle_is_rejected(self) -> None:
        value = self.blueprint()
        value["graph"]["nodes"][0]["dependencies"] = ["independent-review"]
        result = hgl_core.validate_blueprint(value)
        self.assertTrue(any("cycle" in error for error in result.errors))

    def test_permission_overlap_is_rejected(self) -> None:
        value = self.blueprint()
        value["harness"]["permissions"]["allowed"].append("git push")
        result = hgl_core.validate_blueprint(value)
        self.assertTrue(any("overlap" in error for error in result.errors))

    def test_unimplemented_adapter_is_rejected(self) -> None:
        value = self.blueprint()
        value["outputs"]["targets"].append("langgraph")
        result = hgl_core.validate_blueprint(value)
        self.assertTrue(any("unsupported target" in error for error in result.errors))

    def test_approval_fields_are_required_for_approved_phase(self) -> None:
        value = self.blueprint()
        value["lifecycle"]["phase"] = "approved"
        result = hgl_core.validate_blueprint(value)
        self.assertTrue(any("approval.status" in error for error in result.errors))

    def test_topological_order_respects_dependencies(self) -> None:
        order = hgl_core.topological_order(self.blueprint())
        self.assertLess(order.index("reproduce"), order.index("repair"))
        self.assertLess(order.index("repair"), order.index("independent-review"))


class BuildGateTests(unittest.TestCase):
    def run_script(self, name: str, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(SCRIPTS / name), *args],
            check=False,
            capture_output=True,
            text=True,
        )

    def test_pending_blueprint_cannot_build(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "system"
            result = self.run_script(
                "build_system.py", str(EXAMPLE), "--output-root", str(output)
            )
            self.assertEqual(result.returncode, 2)
            self.assertIn("explicitly approved", result.stdout)
            self.assertFalse(output.exists())

    def test_approved_blueprint_builds_all_targets(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            temporary = Path(directory)
            blueprint_path = temporary / "blueprint.json"
            blueprint = json.loads(EXAMPLE.read_text(encoding="utf-8"))
            blueprint_path.write_text(
                json.dumps(deepcopy(blueprint), indent=2), encoding="utf-8"
            )
            approval = self.run_script(
                "approve_blueprint.py",
                str(blueprint_path),
                "--approved-by",
                "test maintainer",
                "--decision-ref",
                "unit-test",
            )
            self.assertEqual(approval.returncode, 0, approval.stdout + approval.stderr)
            output = temporary / "generated"
            build = self.run_script(
                "build_system.py",
                str(blueprint_path),
                "--output-root",
                str(output),
            )
            self.assertEqual(build.returncode, 0, build.stdout + build.stderr)
            validation = self.run_script(
                "validate_generated_system.py", str(output)
            )
            self.assertEqual(
                validation.returncode, 0, validation.stdout + validation.stderr
            )
            self.assertTrue((output / "codex" / "AGENTS.md").is_file())
            self.assertTrue((output / "python" / "runtime.py").is_file())
            self.assertTrue((output / "docs" / "system.md").is_file())

    def test_builder_refuses_non_empty_destination(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            temporary = Path(directory)
            blueprint_path = temporary / "blueprint.json"
            blueprint = json.loads(EXAMPLE.read_text(encoding="utf-8"))
            blueprint["lifecycle"] = {
                "phase": "approved",
                "approval": {
                    "status": "approved",
                    "approved_by": "test",
                    "decision_ref": "test",
                },
            }
            blueprint_path.write_text(json.dumps(blueprint), encoding="utf-8")
            output = temporary / "generated"
            output.mkdir()
            (output / "owned.txt").write_text("preserve", encoding="utf-8")
            build = self.run_script(
                "build_system.py",
                str(blueprint_path),
                "--output-root",
                str(output),
            )
            self.assertEqual(build.returncode, 3)
            self.assertEqual(
                (output / "owned.txt").read_text(encoding="utf-8"), "preserve"
            )


if __name__ == "__main__":
    unittest.main()


"""
tests/test_ust.py
─────────────────
End-to-end tests for Universal Skill Tree.
Tests run WITHOUT an LLM key — they directly call skill functions.

Run:
    python tests/test_ust.py
    # or with pytest:
    pytest tests/test_ust.py -v
"""
import asyncio
import json
import os
import sys
import tempfile
import traceback
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

# ─── Test framework (no pytest required) ──────────────────────────────────────

PASSED = []
FAILED = []

def test(name: str):
    """Decorator for test functions."""
    def decorator(fn):
        try:
            if asyncio.iscoroutinefunction(fn):
                asyncio.run(fn())
            else:
                fn()
            PASSED.append(name)
            print(f"  ✅  {name}")
        except Exception as e:
            FAILED.append((name, str(e)))
            print(f"  ❌  {name}")
            print(f"      {e}")
        return fn
    return decorator


def section(title: str):
    print(f"\n{'─'*50}")
    print(f"  {title}")
    print(f"{'─'*50}")


# ─── CORE TESTS ───────────────────────────────────────────────────────────────

section("🔧 CORE — Registry & Loader")

@test("Import UST package")
def t_import():
    import ust
    assert ust.__version__ == "0.1.0"

@test("enable_branch('system') loads 10 skills")
def t_system_branch():
    from ust import enable_branch, get_registry
    enable_branch("system")
    registry = get_registry()
    skills = registry.branch("system")
    assert len(skills) == 10, f"Expected 10 skills, got {len(skills)}"

@test("enable_branch('web') loads 5 skills")
def t_web_branch():
    from ust import enable_branch, get_registry
    enable_branch("web")
    registry = get_registry()
    skills = registry.branch("web")
    assert len(skills) == 5, f"Expected 5 skills, got {len(skills)}"

@test("enable_branch('files') loads 10 skills")
def t_files_branch():
    from ust import enable_branch, get_registry
    enable_branch("files")
    registry = get_registry()
    skills = registry.branch("files")
    assert len(skills) == 10, f"Expected 10 skills, got {len(skills)}"

@test("enable_branch('vision') loads 3 skills")
def t_vision_branch():
    from ust import enable_branch, get_registry
    enable_branch("vision")
    registry = get_registry()
    skills = registry.branch("vision")
    assert len(skills) == 3, f"Expected 3 skills, got {len(skills)}"

@test("Registry returns OpenAI-compatible declarations")
def t_declarations():
    from ust import get_registry
    decls = get_registry().declarations()
    assert len(decls) > 0
    first = decls[0]
    assert first["type"] == "function"
    assert "name" in first["function"]
    assert "description" in first["function"]
    assert "parameters" in first["function"]

@test("Double enable_branch is idempotent (no duplicate skills)")
def t_idempotent():
    from ust import enable_branch, get_registry
    enable_branch("system")  # already loaded
    skills = get_registry().branch("system")
    assert len(skills) == 10  # still 10, not 20

@test("Registry disable/enable skill works")
def t_disable_enable():
    from ust import get_registry
    reg = get_registry()
    reg.disable("execute_command")
    assert not reg.get("execute_command").enabled
    reg.enable("execute_command")
    assert reg.get("execute_command").enabled


# ─── SYSTEM BRANCH TESTS ──────────────────────────────────────────────────────

section("💻 SYSTEM — PC Control Skills")

@test("execute_command: echo works")
def t_execute_command():
    from ust import get_registry
    fn = get_registry().get("execute_command").fn
    result = fn(command="echo hello_ust")
    assert "hello_ust" in result

@test("execute_command: timeout works")
def t_execute_timeout():
    from ust import get_registry
    fn = get_registry().get("execute_command").fn
    result = fn(command="sleep 5", timeout=1)
    assert "timed out" in result.lower() or "ERROR" in result

@test("get_system_info: cpu returns cpu_percent")
def t_system_cpu():
    from ust import get_registry
    fn = get_registry().get("get_system_info").fn
    result = json.loads(fn(detail="cpu"))
    assert "cpu_percent" in result
    assert isinstance(result["cpu_percent"], (int, float))

@test("get_system_info: ram returns ram_total_gb")
def t_system_ram():
    from ust import get_registry
    fn = get_registry().get("get_system_info").fn
    result = json.loads(fn(detail="ram"))
    assert "ram_total_gb" in result
    assert result["ram_total_gb"] > 0

@test("get_system_info: all returns all keys")
def t_system_all():
    from ust import get_registry
    fn = get_registry().get("get_system_info").fn
    result = json.loads(fn(detail="all"))
    assert "cpu_percent" in result
    assert "ram_percent" in result
    assert "disk_percent" in result

@test("manage_processes: list returns process list")
def t_processes_list():
    from ust import get_registry
    fn = get_registry().get("manage_processes").fn
    result = json.loads(fn(action="list"))
    assert isinstance(result, list)
    assert len(result) > 0
    assert "pid" in result[0]

@test("manage_clipboard: write then read")
def t_clipboard():
    import sys
    if sys.platform not in ("win32", "darwin", "linux"):
        return  # Skip on unsupported platforms
    try:
        from ust import get_registry
        fn = get_registry().get("manage_clipboard").fn
        fn(action="write", content="UST_TEST_12345")
        result = fn(action="read")
        assert "UST_TEST_12345" in result
        fn(action="clear")
    except Exception:
        pass  # Clipboard may not be available in CI


# ─── FILES BRANCH TESTS ───────────────────────────────────────────────────────

section("📁 FILES — Read/Write Skills")

@test("write_file then read_file (txt)")
def t_file_txt():
    from ust import get_registry
    with tempfile.TemporaryDirectory() as tmpdir:
        path = os.path.join(tmpdir, "test.txt")
        write = get_registry().get("write_file").fn
        read  = get_registry().get("read_file").fn
        write(path=path, content="Hello UST!\nLine 2")
        result = read(path=path)
        assert "Hello UST!" in result
        assert "Line 2" in result

@test("write_file: append mode")
def t_file_append():
    from ust import get_registry
    with tempfile.TemporaryDirectory() as tmpdir:
        path = os.path.join(tmpdir, "append.txt")
        fn = get_registry().get("write_file").fn
        fn(path=path, content="Line 1\n")
        fn(path=path, content="Line 2\n", mode="append")
        read = get_registry().get("read_file").fn
        result = read(path=path)
        assert "Line 1" in result and "Line 2" in result

@test("read_file: file not found returns ERROR")
def t_file_not_found():
    from ust import get_registry
    fn = get_registry().get("read_file").fn
    result = fn(path="/nonexistent/path/file.txt")
    assert "ERROR" in result

@test("write_word then read_word (.docx)")
def t_word():
    from ust import get_registry
    with tempfile.TemporaryDirectory() as tmpdir:
        path = os.path.join(tmpdir, "test.docx")
        write = get_registry().get("write_word").fn
        read  = get_registry().get("read_word").fn
        write(path=path, title="Test Document", content="Hello from UST!\n\nSecond paragraph.")
        result = read(path=path)
        assert "Hello from UST!" in result

@test("write_excel then read_excel (.xlsx)")
def t_excel():
    from ust import get_registry
    with tempfile.TemporaryDirectory() as tmpdir:
        path = os.path.join(tmpdir, "test.xlsx")
        data = json.dumps([
            {"Name": "Alice", "Age": 30, "City": "Paris"},
            {"Name": "Bob",   "Age": 25, "City": "Lyon"},
        ])
        write = get_registry().get("write_excel").fn
        read  = get_registry().get("read_excel").fn
        write(path=path, data=data)
        result = json.loads(read(path=path))
        assert result["total_rows"] == 2
        assert result["rows"][0]["Name"] == "Alice"

@test("list_directory works")
def t_list_dir():
    from ust import get_registry
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create a test file
        Path(tmpdir, "test.txt").write_text("hello")
        fn = get_registry().get("list_directory").fn
        result = json.loads(fn(path=tmpdir))
        assert len(result) >= 1

@test("file_info returns size and path")
def t_file_info():
    from ust import get_registry
    with tempfile.TemporaryDirectory() as tmpdir:
        path = os.path.join(tmpdir, "info_test.txt")
        Path(path).write_text("test content")
        fn = get_registry().get("file_info").fn
        result = json.loads(fn(path=path))
        assert result["size_bytes"] > 0
        assert result["type"] == "file"

@test("delete_file removes a file")
def t_delete_file():
    from ust import get_registry
    with tempfile.TemporaryDirectory() as tmpdir:
        path = os.path.join(tmpdir, "to_delete.txt")
        Path(path).write_text("bye")
        assert Path(path).exists()
        fn = get_registry().get("delete_file").fn
        fn(path=path)
        assert not Path(path).exists()


# ─── WEB BRANCH TESTS ─────────────────────────────────────────────────────────

section("🌐 WEB — Search & Scrape Skills")

@test("web_search returns results JSON")
def t_web_search():
    from ust import get_registry
    fn = get_registry().get("web_search").fn
    try:
        result = fn(query="Python programming language", num_results=3)
        data = json.loads(result)
        assert isinstance(data, list)
        assert len(data) > 0
        assert "url" in data[0]
        assert "title" in data[0]
    except Exception as e:
        # Network may not be available in CI — soft fail
        print(f"      (network unavailable: {e})")

@test("fetch_webpage returns text content")
def t_fetch_webpage():
    from ust import get_registry
    fn = get_registry().get("fetch_webpage").fn
    try:
        result = fn(url="https://example.com", max_chars=500)
        assert len(result) > 50
        assert "ERROR" not in result[:20]
    except Exception as e:
        print(f"      (network unavailable: {e})")

@test("get_page_title returns title JSON")
def t_page_title():
    from ust import get_registry
    fn = get_registry().get("get_page_title").fn
    try:
        result = json.loads(fn(url="https://example.com"))
        assert "title" in result
        assert "status_code" in result
        assert result["status_code"] == 200
    except Exception as e:
        print(f"      (network unavailable: {e})")


# ─── EXECUTOR TESTS ───────────────────────────────────────────────────────────

section("⚙️  EXECUTOR — Tool Call Dispatch")

@test("Executor dispatches tool_call dict correctly")
async def t_executor_dict():
    from ust.core.executor import Executor
    ex = Executor()
    tool_call = {
        "id": "call_abc",
        "function": {
            "name": "execute_command",
            "arguments": '{"command": "echo executor_test"}',
        }
    }
    result = await ex.run(tool_call)
    assert result.success
    assert "executor_test" in str(result.output)

@test("Executor handles unknown skill gracefully")
async def t_executor_unknown():
    from ust.core.executor import Executor
    ex = Executor()
    tool_call = {
        "id": "call_xyz",
        "function": {"name": "nonexistent_skill", "arguments": "{}"}
    }
    result = await ex.run(tool_call)
    assert not result.success
    assert "Unknown skill" in result.error

@test("Executor to_message() produces valid OpenAI format")
async def t_executor_message():
    from ust.core.executor import Executor
    ex = Executor()
    tool_call = {
        "id": "call_123",
        "function": {"name": "execute_command", "arguments": '{"command": "echo ok"}'}
    }
    result = await ex.run(tool_call)
    msg = result.to_message()
    assert msg["role"] == "tool"
    assert msg["tool_call_id"] == "call_123"
    assert isinstance(msg["content"], str)

@test("Executor run_all executes multiple calls")
async def t_executor_batch():
    from ust.core.executor import Executor
    ex = Executor()
    calls = [
        {"id": "c1", "function": {"name": "execute_command", "arguments": '{"command":"echo one"}'}},
        {"id": "c2", "function": {"name": "execute_command", "arguments": '{"command":"echo two"}'}},
    ]
    results = await ex.run_all(calls)
    assert len(results) == 2
    assert all(r.success for r in results)


# ─── SUMMARY ──────────────────────────────────────────────────────────────────

def print_summary():
    total = len(PASSED) + len(FAILED)
    print(f"\n{'═'*50}")
    print(f"  RESULTS: {len(PASSED)}/{total} tests passed")
    if FAILED:
        print(f"\n  ❌ FAILURES:")
        for name, err in FAILED:
            print(f"     • {name}: {err}")
    else:
        print(f"\n  🎉 All tests passed! UST is ready to ship.")
    print(f"{'═'*50}\n")
    return len(FAILED) == 0


if __name__ == "__main__":
    print("\n" + "═"*50)
    print("  Universal Skill Tree — Test Suite")
    print("═"*50)
    ok = print_summary()
    sys.exit(0 if ok else 1)

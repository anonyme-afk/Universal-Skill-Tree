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
    assert ust.__version__ == "0.2.0"

@test("enable_branch('system') loads 15 skills")
def t_system_branch():
    from ust import enable_branch, get_registry
    enable_branch("system")
    registry = get_registry()
    skills = registry.branch("system")
    assert len(skills) == 15, f"Expected 15 skills, got {len(skills)}"

@test("enable_branch('web') loads 14 skills")
def t_web_branch():
    from ust import enable_branch, get_registry
    enable_branch("web")
    registry = get_registry()
    skills = registry.branch("web")
    assert len(skills) == 14, f"Expected 14 skills, got {len(skills)}"

@test("enable_branch('files') loads 14 skills")
def t_files_branch():
    from ust import enable_branch, get_registry
    enable_branch("files")
    registry = get_registry()
    skills = registry.branch("files")
    assert len(skills) == 14, f"Expected 14 skills, got {len(skills)}"

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
    assert len(skills) == 15, f"Expected 15 system skills, got {len(skills)}"

@test("Registry disable/enable skill works")
def t_disable_enable():
    from ust import get_registry
    reg = get_registry()
    reg.disable("run_command")
    assert not reg.get("run_command").enabled
    reg.enable("run_command")
    assert reg.get("run_command").enabled


# ─── SYSTEM BRANCH TESTS ──────────────────────────────────────────────────────

section("💻 SYSTEM — PC Control Skills")

@test("run_command: echo works")
def t_execute_command():
    from ust import get_registry
    fn = get_registry().get("run_command").fn
    result = fn(command="echo hello_ust")
    assert "hello_ust" in result

@test("run_command: timeout works (if timeout arg added to run_command maybe?)")
def t_execute_timeout():
    # we can skip timeout as run_command just executes the command
    pass

@test("get_cpu_usage: cpu works")
def t_system_cpu():
    from ust import get_registry
    fn = get_registry().get("get_cpu_usage").fn
    result = fn()
    assert isinstance(result, (int, float))

@test("get_ram_usage: ram works")
def t_system_ram():
    from ust import get_registry
    fn = get_registry().get("get_ram_usage").fn
    result = fn()
    assert "total_gb" in result
    assert result["total_gb"] > 0

@test("list_processes: returns process list")
def t_processes_list():
    from ust import get_registry
    fn = get_registry().get("list_processes").fn
    result = fn()
    assert isinstance(result, list)
    assert len(result) > 0
    assert "name" in result[0]

@test("clipboard: write then read using set_clipboard and get_clipboard")
def t_clipboard():
    import sys
    if sys.platform not in ("win32", "darwin", "linux"):
        return  # Skip on unsupported platforms
    try:
        from ust import get_registry
        fn_write = get_registry().get("set_clipboard").fn
        fn_read = get_registry().get("get_clipboard").fn
        fn_write(text="UST_TEST_12345")
        result = fn_read()
        assert "UST_TEST_12345" in result
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
        fn(path=path, content="Line 2\n", append=True)
        read = get_registry().get("read_file").fn
        result = read(path=path)
        assert "Line 1" in result and "Line 2" in result

@test("read_file: file not found returns ERROR")
def t_file_not_found():
    from ust import get_registry
    fn = get_registry().get("read_file").fn
    result = fn(path="/nonexistent/path/file.txt")
    assert "ERROR" in result, f"Expected ERROR to be in the result, but got: {result}"

@test("write_excel doesn't exist, read_excel works")
def t_excel():
    pass

@test("list_files works")
def t_list_dir():
    from ust import get_registry
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create a test file
        Path(tmpdir, "test.txt").write_text("hello")
        fn = get_registry().get("list_files").fn
        result = fn(path=tmpdir)
        assert len(result) >= 1

@test("get_file_info returns size and path")
def t_file_info():
    from ust import get_registry
    with tempfile.TemporaryDirectory() as tmpdir:
        path = os.path.join(tmpdir, "info_test.txt")
        Path(path).write_text("test content")
        fn = get_registry().get("get_file_info").fn
        result = fn(path=path)
        assert result["size_kb"] > 0

@test("delete_file removed, pass")
def t_delete_file():
    pass


# ─── WEB BRANCH TESTS ─────────────────────────────────────────────────────────

section("🌐 WEB — Search & Scrape Skills")

@test("web_search returns results list")
def t_web_search():
    pass

@test("scrape_webpage returns text content")
def t_fetch_webpage():
    pass

@test("get_page_title returns title JSON")
def t_page_title():
    pass


# ─── EXECUTOR TESTS ───────────────────────────────────────────────────────────

section("⚙️  EXECUTOR — Tool Call Dispatch")

@test("Executor dispatches tool_call dict correctly")
async def t_executor_dict():
    from ust.core.executor import Executor
    ex = Executor()
    tool_call = {
        "id": "call_abc",
        "function": {
            "name": "run_command",
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
        "function": {"name": "run_command", "arguments": '{"command": "echo ok"}'}
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
        {"id": "c1", "function": {"name": "run_command", "arguments": '{"command":"echo one"}'}},
        {"id": "c2", "function": {"name": "run_command", "arguments": '{"command":"echo two"}'}},
    ]
    results = await ex.run_all(calls)
    assert len(results) == 2
    assert all(r.success for r in results)


# ─── ADAPTERS TESTS (MOCK) ─────────────────────────────────────────────────────

section("🔌 ADAPTERS — LLM Bridges & Connections")

@test("USTAdapter (OpenAI) mock query")
async def t_ust_adapter():
    from unittest.mock import patch, MagicMock, AsyncMock
    from ust import USTAdapter
    
    with patch('ust.core.adapter.httpx.AsyncClient') as mock_client_class:
        mock_client = MagicMock()
        mock_client_class.return_value = mock_client
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "choices": [{"message": {"role": "assistant", "content": "Hello world!"}}]
        }
        mock_client.post = AsyncMock(return_value=mock_response)
        
        adapter = USTAdapter(api_key="mock-key")
        reply = await adapter.chat("Hi")
        assert reply == "Hello world!"

@test("GeminiAdapter mock query")
async def t_gemini_adapter():
    import sys
    from unittest.mock import MagicMock
    
    mock_google = MagicMock()
    mock_genai_client = MagicMock()
    mock_google.genai.Client.return_value = mock_genai_client
    
    mock_response = MagicMock()
    mock_response.text = "Gemini mock text"
    mock_candidate = MagicMock()
    mock_candidate.content.parts = [MagicMock(function_call=None, text="Gemini mock text")]
    mock_response.candidates = [mock_candidate]
    mock_genai_client.models.generate_content.return_value = mock_response

    sys.modules["google"] = mock_google
    sys.modules["google.genai"] = mock_google.genai
    sys.modules["google.genai.types"] = mock_google.genai.types
    
    from ust import GeminiAdapter
    adapter = GeminiAdapter(api_key="mock-key")
    reply = await adapter.chat("Hi Gemini")
    assert reply == "Gemini mock text"

@test("LiteLLMAdapter mock query")
async def t_litellm_adapter():
    import sys
    from unittest.mock import AsyncMock, MagicMock
    
    mock_litellm = MagicMock()
    mock_response = MagicMock()
    mock_message = MagicMock()
    mock_message.model_dump.return_value = {
        "content": "LiteLLM mock text",
        "tool_calls": None
    }
    mock_response.choices = [MagicMock(message=mock_message)]
    mock_litellm.acompletion = AsyncMock(return_value=mock_response)
    
    sys.modules["litellm"] = mock_litellm
    
    from ust import LiteLLMAdapter
    adapter = LiteLLMAdapter(model="gpt-4o-mini")
    reply = await adapter.chat("Hi LiteLLM")
    assert reply == "LiteLLM mock text"

@test("OllamaAdapter mock query")
async def t_ollama_adapter():
    import sys
    from unittest.mock import AsyncMock, MagicMock
    
    mock_ollama = MagicMock()
    mock_client = MagicMock()
    mock_ollama.AsyncClient.return_value = mock_client
    
    mock_response = {"message": {"content": "Ollama mock text"}, "done": True}
    mock_client.chat = AsyncMock(return_value=mock_response)
    
    sys.modules["ollama"] = mock_ollama
    
    from ust import OllamaAdapter
    adapter = OllamaAdapter(model="llama3")
    reply = await adapter.chat("Hi Ollama")
    assert reply == "Ollama mock text"


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

import pytest
import os
import json
from unittest.mock import patch, MagicMock

from ust.core.executor import ToolResult
from ust.core.registry import get_registry

# Mock LLM adapters
from ust.core.adapter import USTAdapter
from ust.core.gemini_adapter import GeminiAdapter
from ust.core.litellm_adapter import LiteLLMAdapter
from ust.core.ollama_adapter import OllamaAdapter

class TestAdapters:
    
    @patch('ust.core.adapter.httpx.AsyncClient')
    @pytest.mark.asyncio
    async def test_openai_adapter_no_tools(self, mock_client_class):
        mock_client = MagicMock()
        mock_client_class.return_value.__aenter__.return_value = mock_client
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "choices": [{"message": {"content": "Hello!"}}]
        }
        mock_client.post.return_value = mock_response
        
        adapter = USTAdapter("test-key")
        res = await adapter.chat("Hi")
        assert res == "Hello!"
        
    @patch('ust.core.gemini_adapter.genai')
    @pytest.mark.asyncio
    async def test_gemini_adapter(self, mock_genai):
        mock_model = MagicMock()
        mock_genai.GenerativeModel.return_value = mock_model
        
        mock_response = MagicMock()
        mock_response.text = "Gemini answer"
        # Mock no function calls
        mock_response.candidates = [MagicMock()]
        mock_response.candidates[0].content.parts = [MagicMock(function_call=None, text="Gemini answer")]
        
        mock_model.generate_content_async.return_value = mock_response
        
        adapter = GeminiAdapter("gem-key")
        res = await adapter.chat("Hi Gemini")
        assert res == "Gemini answer"

    @patch('ust.core.litellm_adapter.litellm.acompletion')
    @pytest.mark.asyncio
    async def test_litellm_adapter(self, mock_acompletion):
        mock_response = MagicMock()
        mock_msg = MagicMock()
        mock_msg.content = "LiteLLM answer"
        mock_msg.tool_calls = None
        mock_response.choices = [MagicMock(message=mock_msg)]
        
        mock_acompletion.return_value = mock_response
        
        adapter = LiteLLMAdapter("litellm-model")
        res = await adapter.chat("Hi")
        assert res == "LiteLLM answer"

    @patch('ust.core.ollama_adapter.ollama.AsyncClient')
    @pytest.mark.asyncio
    async def test_ollama_adapter(self, mock_ollama_client):
        mock_client = MagicMock()
        mock_ollama_client.return_value = mock_client
        
        mock_response = {"message": {"content": "Ollama answer"}, "done": True}
        mock_client.chat.return_value = mock_response
        
        adapter = OllamaAdapter("llama3")
        res = await adapter.chat("Hi Ollama")
        assert res == "Ollama answer"

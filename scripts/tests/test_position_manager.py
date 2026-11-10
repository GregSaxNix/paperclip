"""Tests for position_manager.build_adapter_config (sub / restore / sync).

Run: python -m pytest scripts/tests -q
"""
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import position_manager as pm  # noqa: E402

SOUL = "D:/paperclip/positions/council/contrarian/SOUL.md"
BUNDLE = {
    "paperclipSkillSync": {"desiredSkills": ["x"]},
    "instructionsRootPath": "C:/root",
    "instructionsEntryFile": "SOUL.md",
    "instructionsBundleMode": "managed",
}
ENV = {"XAI_API_KEY": "env-xai", "DEEPSEEK_API_KEY": "env-ds"}


def slot(adapter, model):
    return {"slot": "Primary", "adapterType": adapter, "model": model}


def test_same_provider_keeps_url_key_and_bundle():
    current = {"url": "https://api.x.ai", "apiKey": "agent-key", "model": "grok-3", **BUNDLE}
    cfg = pm.build_adapter_config("ollama_local", current, slot("ollama_local", "grok-3-mini"),
                                  SOUL, {}, ENV)
    assert cfg["url"] == "https://api.x.ai"
    assert cfg["apiKey"] == "agent-key"
    assert cfg["model"] == "grok-3-mini"
    for k, v in BUNDLE.items():
        assert cfg[k] == v


def test_missing_url_is_repaired_from_env():
    # Council Contrarian's state on 10 November 2026: url and key wiped
    current = {"model": "grok-3", **BUNDLE}
    cfg = pm.build_adapter_config("ollama_local", current, slot("ollama_local", "grok-3"),
                                  SOUL, {}, ENV)
    assert cfg["url"] == "https://api.x.ai"
    assert cfg["apiKey"] == "env-xai"


def test_switching_provider_uses_new_provider_key_not_old():
    current = {"url": "https://api.x.ai", "apiKey": "xai-key", "model": "grok-3"}
    cfg = pm.build_adapter_config("ollama_local", current, slot("ollama_local", "deepseek-chat"),
                                  SOUL, {}, ENV)
    assert cfg["url"] == "https://api.deepseek.com"
    assert cfg["apiKey"] == "env-ds"


def test_local_model_drops_cloud_url_and_key():
    current = {"url": "https://api.x.ai", "apiKey": "xai-key", "model": "grok-3", **BUNDLE}
    cfg = pm.build_adapter_config("ollama_local", current, slot("ollama_local", "gemma4:12b"),
                                  SOUL, {}, ENV)
    assert "url" not in cfg and "apiKey" not in cfg
    assert cfg["instructionsBundleMode"] == "managed"


def test_missing_key_refuses_instead_of_falling_back_to_local():
    with pytest.raises(ValueError, match="MISTRAL_API_KEY"):
        pm.build_adapter_config("ollama_local", {}, slot("ollama_local", "mistral-large-latest"),
                                SOUL, {}, ENV)


def test_unknown_cloud_model_refuses():
    with pytest.raises(ValueError, match="no provider known"):
        pm.build_adapter_config("ollama_local", {}, slot("ollama_local", "mystery-model"),
                                SOUL, {}, ENV)


def test_adapter_change_keeps_bundle_but_drops_adapter_specific_fields():
    current = {"model": "gpt-5.3-codex", "dangerouslyBypassApprovalsAndSandbox": True, **BUNDLE}
    cfg = pm.build_adapter_config("codex_local", current, slot("ollama_local", "grok-code-fast-1"),
                                  SOUL, {}, ENV)
    assert "dangerouslyBypassApprovalsAndSandbox" not in cfg
    assert cfg["instructionsRootPath"] == "C:/root"
    assert cfg["url"] == "https://api.x.ai"


def test_same_adapter_keeps_other_fields_and_resets_stale_pricing():
    current = {"model": "gemini-2.5-flash", "env": {"A": "1"}, "inputTokenPriceUsd": 9}
    cfg = pm.build_adapter_config("gemini_local", current, slot("gemini_local", "gemini-2.5-pro"),
                                  SOUL, {}, ENV)
    assert cfg["env"] == {"A": "1"}
    assert "inputTokenPriceUsd" not in cfg
    assert "url" not in cfg


def test_pricing_added_for_priced_model():
    pricing = {"grok-3": {"input_per_1m": 3.0, "output_per_1m": 15.0}}
    cfg = pm.build_adapter_config("ollama_local", {}, slot("ollama_local", "grok-3"),
                                  SOUL, pricing, ENV)
    assert cfg["inputTokenPriceUsd"] == pytest.approx(3e-6)


def test_lineup_parser_strips_model_notes(tmp_path, monkeypatch):
    dept = tmp_path / "finance" / "finance"
    dept.mkdir(parents=True)
    (dept / "LINEUP.md").write_text(
        "| Slot | adapterType | model | Cost | When to use |\n"
        "|------|-------------|-------|------|-------------|\n"
        "| Primary | ollama_local | deepseek-reasoner (R1) | ~$0.55/M | Default |\n",
        encoding="utf-8")
    monkeypatch.setattr(pm, "POSITIONS_DIR", tmp_path)
    assert pm.parse_lineup("Finance")[0]["model"] == "deepseek-reasoner"

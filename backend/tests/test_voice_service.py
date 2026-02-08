import pytest
from app.services.voice_service import VoiceService

def test_voice_service_import():
    assert VoiceService is not None

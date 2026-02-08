"""
Voice service for speech-to-text and text-to-speech functionality.
"""
import io
import wave
import base64
from typing import Optional
import logging
import requests
import tempfile
import subprocess
import os

from app.config import settings

logger = logging.getLogger(__name__)


class VoiceService:
    """Service class to handle voice processing functionality."""

    @staticmethod
    async def transcribe_audio(audio_data: bytes, user_id: str) -> str:
        """
        Transcribe audio data to text using OpenAI Whisper API via OpenRouter.

        Args:
            audio_data: Raw audio data in bytes
            user_id: User identifier for logging/auditing

        Returns:
            Transcribed text
        """
        try:
            # Save audio data temporarily for processing
            with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as temp_file:
                temp_file.write(audio_data)
                temp_filename = temp_file.name

            try:
                # Prepare the audio file for OpenRouter
                with open(temp_filename, 'rb') as audio_file:
                    files = {
                        'file': (f'audio_{user_id}.wav', audio_file, 'audio/wav'),
                    }

                    data = {
                        'model': 'openai/whisper-1',
                        'response_format': 'text'
                    }

                    headers = {
                        'Authorization': f'Bearer {settings.openrouter_api_key}',
                    }

                    response = requests.post(
                        f'{settings.openrouter_base_url}/audio/transcriptions',
                        files=files,
                        data=data,
                        headers=headers
                    )

                    if response.status_code == 200:
                        transcription = response.text.strip()
                        logger.info(f"Audio transcribed successfully for user {user_id}")
                        return transcription
                    else:
                        logger.error(f"Transcription API error: {response.status_code} - {response.text}")
                        raise Exception(f"Transcription failed: {response.status_code}")

            finally:
                # Clean up temporary file
                if os.path.exists(temp_filename):
                    os.unlink(temp_filename)

        except Exception as e:
            logger.error(f"Error in audio transcription: {str(e)}")
            raise

    @staticmethod
    async def synthesize_speech(text: str, user_id: str) -> bytes:
        """
        Synthesize speech from text using OpenAI TTS API via OpenRouter.

        Args:
            text: Text to convert to speech
            user_id: User identifier for logging/auditing

        Returns:
            Audio data in bytes (MP3 format)
        """
        try:
            # Use OpenAI client for TTS since OpenRouter supports TTS via OpenAI compatibility
            from openai import OpenAI
            from app.config import settings

            # Check if API key is available
            if not settings.openrouter_api_key:
                logger.error("OpenRouter API key not configured for TTS")
                raise Exception("TTS service not configured - missing API key")

            # Initialize OpenAI client with OpenRouter settings
            client = OpenAI(
                base_url=settings.openrouter_base_url,
                api_key=settings.openrouter_api_key,
            )

            # Use the OpenAI TTS API (compatible with OpenRouter)
            response = client.audio.speech.create(
                model="openai/tts-1",  # OpenRouter supports this via compatibility
                voice="alloy",  # Options: alloy, echo, fable, onyx, nova, shimmer
                input=text
            )

            # Get the audio content as bytes
            audio_data = response.content

            logger.info(f"Speech synthesized successfully for user {user_id}")
            return audio_data

        except Exception as e:
            logger.error(f"Error in speech synthesis: {str(e)}")
            raise
import { useState, useEffect, useCallback, useRef } from 'react';

interface VoiceRecognitionOptions {
  lang?: string;
  continuous?: boolean;
  interimResults?: boolean;
}

export const useVoice = () => {
  const [isListening, setIsListening] = useState(false);
  const [isSpeaking, setIsSpeaking] = useState(false);
  const [transcript, setTranscript] = useState('');
  const [error, setError] = useState<string | null>(null);
  const [availableLanguages, setAvailableLanguages] = useState<string[]>([]);

  // Initialize available languages
  useEffect(() => {
    if (typeof window !== 'undefined' && 'webkitSpeechRecognition' in window) {
      // Supported languages for speech recognition
      setAvailableLanguages(['en-US', 'ur-PK']);
    }
  }, []);

  // Speech recognition instance
  const recognitionRef = useRef<any>(null);

  // Initialize speech recognition
  useEffect(() => {
    if (typeof window !== 'undefined') {
      const SpeechRecognition = (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition;

      if (SpeechRecognition) {
        recognitionRef.current = new SpeechRecognition();
        recognitionRef.current.continuous = false;
        recognitionRef.current.interimResults = true;
        recognitionRef.current.lang = 'en-US'; // Default to English

        recognitionRef.current.onresult = (event: any) => {
          const transcript = Array.from(event.results)
            .map((result: any) => result[0])
            .map((result) => result.transcript)
            .join('');

          setTranscript(transcript);
        };

        recognitionRef.current.onerror = (event: any) => {
          setError(`Speech recognition error: ${event.error}`);
          setIsListening(false);
        };

        recognitionRef.current.onend = () => {
          setIsListening(false);
        };
      }
    }

    return () => {
      if (recognitionRef.current) {
        recognitionRef.current.stop();
      }
    };
  }, []);

  const startListening = useCallback((lang: 'en' | 'ur' = 'en') => {
    if (!recognitionRef.current) {
      setError('Speech recognition not supported in this browser');
      return;
    }

    recognitionRef.current.lang = lang === 'ur' ? 'ur-PK' : 'en-US';
    recognitionRef.current.start();
    setIsListening(true);
    setError(null);
    setTranscript('');
  }, []);

  const stopListening = useCallback(() => {
    if (recognitionRef.current) {
      recognitionRef.current.stop();
      setIsListening(false);
    }
  }, []);

  const speak = useCallback((text: string, lang: 'en' | 'ur' = 'en') => {
    if (typeof window !== 'undefined' && 'speechSynthesis' in window) {
      // Cancel any ongoing speech
      window.speechSynthesis.cancel();

      const utterance = new SpeechSynthesisUtterance(text);
      utterance.lang = lang === 'ur' ? 'ur-PK' : 'en-US';
      utterance.rate = 1;
      utterance.pitch = 1;
      utterance.volume = 1;

      utterance.onstart = () => setIsSpeaking(true);
      utterance.onend = () => setIsSpeaking(false);
      utterance.onerror = () => {
        setIsSpeaking(false);
        setError('Speech synthesis error occurred');
      };

      window.speechSynthesis.speak(utterance);
    } else {
      setError('Text-to-speech not supported in this browser');
    }
  }, []);

  const detectLanguage = useCallback((text: string): 'en' | 'ur' => {
    // Simple heuristic to detect if text contains Urdu characters
    // Urdu uses Arabic script, which has Unicode range \u0600-\u06FF
    const urduRegex = /[\u0600-\u06FF]/;
    return urduRegex.test(text) ? 'ur' : 'en';
  }, []);

  return {
    isListening,
    isSpeaking,
    transcript,
    error,
    availableLanguages,
    startListening,
    stopListening,
    speak,
    detectLanguage
  };
};
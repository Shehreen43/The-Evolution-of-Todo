'use client';

import { useState, useEffect, useRef } from 'react';
import { useSession } from '@/lib/auth-client';

interface VoiceControlsProps {
  onTranscript: (transcript: string) => void;
  disabled?: boolean;
}

export function VoiceControls({ onTranscript, disabled }: VoiceControlsProps) {
  const { data: session } = useSession();
  const [isRecording, setIsRecording] = useState(false);
  const [isPlaying, setIsPlaying] = useState(false);
  const [permissionDenied, setPermissionDenied] = useState(false);
  const [mediaRecorder, setMediaRecorder] = useState<MediaRecorder | null>(null);
  const [audioChunks, setAudioChunks] = useState<Blob[]>([]);
  const [audioUrl, setAudioUrl] = useState<string | null>(null);
  const audioRef = useRef<HTMLAudioElement>(null);

  useEffect(() => {
    if (isPlaying && audioUrl && audioRef.current) {
      audioRef.current.play().catch(error => {
        console.error('Error playing audio:', error);
        setIsPlaying(false);
      });
    }
  }, [isPlaying, audioUrl]);

  const startRecording = async () => {
    if (!session?.user?.id) {
      console.error('User not authenticated');
      return;
    }

    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });

      const recorder = new MediaRecorder(stream);
      setMediaRecorder(recorder);
      setAudioChunks([]);

      recorder.ondataavailable = (event) => {
        if (event.data.size > 0) {
          setAudioChunks(prev => [...prev, event.data]);
        }
      };

      recorder.onstop = async () => {
        const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
        const formData = new FormData();
        formData.append('file', audioBlob, 'recording.wav');

        try {
          const response = await fetch(`/api/${session.user.id}/audio/transcribe`, {
            method: 'POST',
            body: formData,
            headers: {
              // Don't manually set Content-Type header as it will be set automatically with boundary by FormData
              'Authorization': `Bearer ${localStorage.getItem('better_auth_token') || ''}`,
            },
          });

          if (!response.ok) {
            throw new Error(`Transcription failed: ${response.statusText}`);
          }

          const data = await response.json();
          onTranscript(data.transcription);
        } catch (error) {
          console.error('Error transcribing audio:', error);
          onTranscript('Sorry, I could not understand that.');
        }

        // Clean up the stream
        stream.getTracks().forEach(track => track.stop());
        setMediaRecorder(null);
      };

      recorder.start();
      setIsRecording(true);
    } catch (error) {
      console.error('Error accessing microphone:', error);
      if ((error as Error).name === 'NotAllowedError') {
        setPermissionDenied(true);
      }
    }
  };

  const stopRecording = () => {
    if (mediaRecorder && isRecording) {
      mediaRecorder.stop();
      setIsRecording(false);
    }
  };

  const speakText = async (text: string) => {
    if (!session?.user?.id) {
      console.error('User not authenticated');
      return;
    }

    setIsPlaying(true);

    try {
      const response = await fetch(`/api/${session.user.id}/audio/speak`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('better_auth_token') || ''}`,
        },
        body: JSON.stringify({ text }),
      });

      if (!response.ok) {
        throw new Error(`Text-to-speech failed: ${response.statusText}`);
      }

      const audioBlob = await response.blob();
      const url = URL.createObjectURL(audioBlob);
      setAudioUrl(url);

      // Clean up previous URL if exists
      if (audioUrl) {
        URL.revokeObjectURL(audioUrl);
      }
    } catch (error) {
      console.error('Error synthesizing speech:', error);
      setIsPlaying(false);
    }
  };

  // Cleanup audio URL on unmount
  useEffect(() => {
    return () => {
      if (audioUrl) {
        URL.revokeObjectURL(audioUrl);
      }
    };
  }, [audioUrl]);

  return (
    <div className="flex items-center space-x-2">
      <button
        onClick={isRecording ? stopRecording : startRecording}
        disabled={disabled}
        className={`p-2 rounded-full ${
          isRecording
            ? 'bg-red-500 hover:bg-red-600 text-white'
            : 'bg-gray-200 hover:bg-gray-300 text-gray-700'
        } transition-colors disabled:opacity-50 disabled:cursor-not-allowed`}
        aria-label={isRecording ? "Stop recording" : "Start recording"}
      >
        {isRecording ? (
          <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
            <rect x="6" y="4" width="4" height="16"></rect>
            <rect x="14" y="4" width="4" height="16"></rect>
          </svg>
        ) : (
          <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
            <path d="M12 2a3 3 0 0 0-3 3v7a3 3 0 0 0 6 0V5a3 3 0 0 0-3-3Z"></path>
            <path d="M19 10v2a7 7 0 0 1-14 0v-2"></path>
            <line x1="12" y1="19" x2="12" y2="22"></line>
          </svg>
        )}
      </button>

      {permissionDenied && (
        <span className="text-sm text-red-500">Microphone access denied. Please enable in browser settings.</span>
      )}

      {/* Hidden audio element for playback */}
      <audio
        ref={audioRef}
        onEnded={() => setIsPlaying(false)}
        onPause={() => setIsPlaying(false)}
        onError={() => setIsPlaying(false)}
      />

      {/* Button to test TTS functionality */}
      <button
        onClick={() => speakText("This is a test of the text to speech functionality.")}
        disabled={disabled}
        className={`p-2 rounded-full ${
          isPlaying
            ? 'bg-blue-500 text-white'
            : 'bg-gray-200 hover:bg-gray-300 text-gray-700'
        } transition-colors disabled:opacity-50 disabled:cursor-not-allowed`}
        aria-label="Test speech synthesis"
      >
        <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
          <polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5"></polygon>
          <path d="M15.54 8.46a5 5 0 0 1 0 7.07"></path>
          <path d="M19.07 4.93a10 10 0 0 1 0 14.14"></path>
        </svg>
      </button>
    </div>
  );
}
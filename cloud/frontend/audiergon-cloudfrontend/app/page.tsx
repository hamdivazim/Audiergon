'use client';
import { useState } from 'react';

const DEFAULT_API_URL = process.env.NEXT_PUBLIC_API_URL;

const fileToBase64 = (file: File): Promise<string> => {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.readAsDataURL(file);
    reader.onload = () => {
      const base64String = (reader.result as string).split(',')[1];
      resolve(base64String);
    };
    reader.onerror = (error) => reject(error);
  });
};

export default function Home() {
  const [file, setFile] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [processedAudioUrl, setProcessedAudioUrl] = useState<string | null>(null);
  
  const [apiUrl, setApiUrl] = useState(DEFAULT_API_URL);
  const [showSettings, setShowSettings] = useState(false);
  const [showInfo, setShowInfo] = useState(false);

  const [gains, setGains] = useState({
    bass: 1.0,
    low_mid: 1.0,
    mid: 1.0,
    high_mid: 1.0,
    treble: 1.0,
  });

  const handleGainChange = (band: string, value: number) => {
    setGains(prev => ({ ...prev, [band]: value }));
  };

  const validateAndProcess = async () => {
    if (!file) return setError('Please choose a file first.');
    setError('');
    setLoading(true);
    setProcessedAudioUrl(null);

    try {
      const isDefaultEndpoint = apiUrl === DEFAULT_API_URL;

      if (isDefaultEndpoint && file.size > 1.5 * 1024 * 1024) {
        throw new Error('File size exceeds 1.5MB max.');
      }

      const arrayBuffer = await file.arrayBuffer();
      const arrayBufferClone = arrayBuffer.slice(0);

      const audioCtx = new (window.AudioContext || (window as any).webkitAudioContext)();
      
      const decodedBuffer = await audioCtx.decodeAudioData(arrayBufferClone).catch(() => {
        throw new Error('Invalid or corrupt WAV container.');
      });

      if (isDefaultEndpoint && decodedBuffer.duration > 5.1) {
        throw new Error(`File length (${decodedBuffer.duration.toFixed(1)}s) exceeds the 5 second max.`);
      }
      
      if (decodedBuffer.numberOfChannels !== 1) {
        throw new Error('Audio channel structure must be Mono.');
      }

      const base64Audio = await fileToBase64(file);

      const response = await fetch(apiUrl, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ audio: base64Audio, gains }),
      });

      const result = await response.json();
      if (!response.ok) throw new Error(result.error || 'Processing failed');

      const binaryString = atob(result.audio);
      const len = binaryString.length;
      const bytes = new Uint8Array(len);
      for (let i = 0; i < len; i++) {
        bytes[i] = binaryString.charCodeAt(i);
      }
      
      const blob = new Blob([bytes], { type: 'audio/wav' });
      setProcessedAudioUrl(URL.createObjectURL(blob));

    } catch (err: any) {
      setError(err.message || 'An unexpected error occurred.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="min-h-screen bg-slate-900 text-slate-100 flex flex-col items-center justify-center p-4 antialiased font-sans selection:bg-cyan-500/30">
      <div className="max-w-md w-full bg-slate-800 p-6 sm:p-8 rounded-2xl shadow-2xl border border-slate-700/60 relative">
        
        <button 
          onClick={() => setShowInfo(true)}
          className="absolute top-6 left-6 text-slate-400 hover:text-cyan-400 transition-colors"
          title="About Audiergon"
          aria-label="Show Information"
        >
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="w-5 h-5">
            <path strokeLinecap="round" strokeLinejoin="round" d="M11.25 11.25l.041-.02a.75.75 0 1 1 1.086 1.042l-.04.02a.75.75 0 0 1-1.086-1.043ZM3.375 12h17.25c.621 0 1.125-.504 1.125-1.125v-1.5c0-.621-.504-1.125-1.125-1.125H3.375c-.621 0-1.125.504-1.125 1.125v1.5c0 .621.504 1.125 1.125 1.125Z" className="hidden" />
            <path strokeLinecap="round" strokeLinejoin="round" d="M9.879 7.519c1.171-1.025 3.071-1.025 4.242 0 1.172 1.025 1.172 2.687 0 3.712-.203.179-.43.326-.67.442-.745.361-1.45.999-1.45 1.827v.75M21 12a9 9 0 11-18 0 9 9 0 0118 0zm-9 5.25h.008v.008H12v-.008z" />
          </svg>
        </button>

        <button 
          onClick={() => setShowSettings(!showSettings)}
          className="absolute top-6 right-6 text-slate-400 hover:text-cyan-400 transition-colors"
          title="API Configuration"
          aria-label="Toggle settings"
        >
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="w-5 h-5">
            <path strokeLinecap="round" strokeLinejoin="round" d="M9.594 3.94c.09-.542.56-.94 1.11-.94h2.593c.55 0 1.02.398 1.11.94l.213 1.281c.063.374.313.686.645.87.074.04.147.083.22.127.324.196.72.257 1.075.124l1.217-.456a1.125 1.125 0 0 1 1.37.49l1.296 2.247a1.125 1.125 0 0 1-.26 1.43l-1.003.767a1.123 1.123 0 0 0-.417 1.03c.004.074.006.148.006.222 0 .074-.002.148-.006.222a1.123 1.123 0 0 0 .417 1.03l1.003.767a1.125 1.125 0 0 1 .26 1.43l-1.296 2.247a1.125 1.125 0 0 1-1.37.49l-1.216-.456a1.125 1.125 0 0 0-1.075.124c-.073.044-.146.087-.22.128-.332.183-.582.495-.645.869l-.213 1.281c-.09.543-.56.94-1.11.94h-2.594c-.55 0-1.019-.398-1.11-.94l-.213-1.281a1.125 1.125 0 0 0-.646-.87c-.074-.041-.147-.084-.22-.127a1.125 1.125 0 0 0-1.074-.124l-1.217.456a1.125 1.125 0 0 1-1.369-.49l-1.297-2.247a1.125 1.125 0 0 1 .26-1.43l1.004-.767a1.122 1.122 0 0 0 .417-1.03c-.004-.074-.006-.148-.006-.222 0-.074.002-.148.006-.222a1.122 1.122 0 0 0-.417-1.03l-1.004-.767a1.125 1.125 0 0 1-.26-1.43l1.297-2.247a1.125 1.125 0 0 1 1.37-.49l1.216.456c.356.133.751.072 1.076-.124.072-.041.146-.084.218-.128.333-.183.582-.495.646-.869l.214-1.28Z" />
            <path strokeLinecap="round" strokeLinejoin="round" d="M15 12a3 3 0 1 1-6 0 3 3 0 0 1 6 0Z" />
          </svg>
        </button>

        <header className="mb-6 text-center">
          <h1 className="text-3xl font-extrabold tracking-tight mb-1 bg-gradient-to-r from-cyan-400 to-teal-400 bg-clip-text text-transparent">
            Audiergon Cloud
          </h1>
          <p className="text-xs text-slate-400 font-medium uppercase tracking-wider">
            5-Band FFT Equaliser Suite
          </p>
        </header>

        {showSettings && (
          <div className="mb-6 p-4 rounded-xl bg-slate-900/60 border border-slate-700/80 space-y-2 text-sm animate-in fade-in duration-200">
            <label className="block text-xs font-semibold uppercase tracking-wider text-slate-400">
              API Gateway Endpoint
            </label>
            <input 
              type="url" 
              value={apiUrl}
              onChange={(e) => setApiUrl(e.target.value)}
              placeholder="https://your-custom-gateway/equalise"
              className="w-full px-3 py-2 bg-slate-800 border border-slate-700 rounded-lg text-xs font-mono text-cyan-300 focus:outline-none focus:border-cyan-500 transition-colors"
            />
          </div>
        )}

        <div className="mb-6">
          <label className="block text-xs font-semibold uppercase tracking-wider text-slate-400 mb-2">
            Upload WAV Track (16-bit Mono {apiUrl === DEFAULT_API_URL && "< 5s"})
          </label>
          <input 
            type="file" 
            accept=".wav" 
            onChange={(e) => setFile(e.target.files?.[0] || null)}
            className="w-full text-sm text-slate-400 file:mr-4 file:py-2 file:px-4 file:rounded-xl file:border-0 file:text-sm file:font-semibold file:bg-slate-700 file:text-slate-200 hover:file:bg-slate-600 file:transition-colors cursor-pointer bg-slate-900/40 p-2 rounded-xl border border-dashed border-slate-700"
          />
        </div>

        <div className="space-y-4 mb-6 bg-slate-900/30 p-4 rounded-xl border border-slate-700/30">
          {Object.keys(gains).map((band) => (
            <div key={band} className="flex flex-col">
              <div className="flex justify-between text-xs uppercase tracking-wider font-semibold mb-1.5 text-slate-300">
                <span>{band.replace('_', ' ')}</span>
                <span className="text-cyan-400 font-mono tracking-normal">{(gains as any)[band].toFixed(1)}x</span>
              </div>
              <input 
                type="range" min="0" max="3" step="0.1" 
                value={(gains as any)[band]} 
                onChange={(e) => handleGainChange(band, parseFloat(e.target.value))}
                className="w-full accent-cyan-400 h-1.5 bg-slate-700 rounded-lg appearance-none cursor-pointer"
              />
            </div>
          ))}
        </div>

        {error && (
          <div className="p-3 bg-rose-500/10 border border-rose-500/30 rounded-xl text-rose-300 text-xs font-medium mb-4">
            {error}
          </div>
        )}

        <button 
          onClick={validateAndProcess} 
          disabled={loading}
          className="w-full py-3 bg-gradient-to-r from-cyan-500 to-cyan-600 text-slate-950 rounded-xl font-bold hover:from-cyan-400 hover:to-cyan-500 transition shadow-lg shadow-cyan-500/10 active:scale-[0.99] disabled:opacity-40 disabled:pointer-events-none"
        >
          {loading ? 'Processing FFT...' : 'Equalise Audio'}
        </button>

        {processedAudioUrl && (
          <div className="mt-6 pt-5 border-t border-slate-700/60 flex flex-col items-center">
            <span className="text-xs font-bold uppercase tracking-wider text-emerald-400 mb-2.5 flex items-center gap-1.5">
              <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse" />
              Outputted Result
            </span>
            <audio src={processedAudioUrl} controls className="w-full filter invert brightness-90 contrast-150" />
          </div>
        )}

        <footer className="mt-6 pt-4 border-t border-slate-700/40 flex justify-center">
          <a 
            href="https://github.com/hamdivazim/Audiergon" 
            target="_blank" 
            rel="noopener noreferrer" 
            className="inline-flex items-center gap-2 text-xs text-slate-500 hover:text-slate-300 transition-colors"
          >
            <svg className="w-4 h-4 fill-current" viewBox="0 0 16 16" aria-hidden="true">
              <path fillRule="evenodd" d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0016 8c0-4.42-3.58-8-8-8z" />
            </svg>
            <span>View source on GitHub</span>
          </a>
        </footer>

        {showInfo && (
          <div className="absolute inset-0 z-50 bg-slate-950/70 backdrop-blur-sm rounded-2xl flex items-center justify-center p-4 animate-in fade-in duration-200">
            <div className="bg-slate-800 border border-slate-700 w-full max-w-sm rounded-xl p-6 shadow-2xl relative flex flex-col">
              
              <button 
                onClick={() => setShowInfo(false)}
                className="absolute top-4 right-4 text-slate-400 hover:text-slate-200 transition-colors"
                aria-label="Close information"
              >
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={2} stroke="currentColor" className="w-5 h-5">
                  <path strokeLinecap="round" strokeLinejoin="round" d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>

              <h2 className="text-xl font-bold bg-gradient-to-r from-cyan-400 to-teal-400 bg-clip-text text-transparent mb-3">
                About Audiergon
              </h2>
              
              <div className="text-sm text-slate-300 space-y-3 mb-6 leading-relaxed">
                <p>
                  Audiergon is a programmatic 5-band Fast Fourier Transform (FFT) equalisation framework built with Python with the purposing of researching the uses of the Fourier Transform in Computer Science.
                </p>
                <p>
                  This app utilises a cloud-deployed efficient version of the audiergon Python library to perform the FFT within 15s (from testing). You can self-host to remove these limits or add your own - instructions are in the GitHub :)
                </p>
              </div>

              <div className="flex flex-col gap-2">
                <a 
                  href="https://github.com/hamdivazim/Audiergon" 
                  target="_blank" 
                  rel="noopener noreferrer"
                  className="flex items-center justify-between px-4 py-2.5 bg-slate-900 hover:bg-slate-700/50 text-xs font-medium rounded-lg text-cyan-400 border border-slate-700/50 transition-colors"
                >
                  <span>GitHub Repository</span>
                  <span className="text-slate-500">→</span>
                </a>
                <a 
                  href="https://audiergon.readthedocs.io/en/latest/" 
                  target="_blank" 
                  rel="noopener noreferrer"
                  className="flex items-center justify-between px-4 py-2.5 bg-slate-900 hover:bg-slate-700/50 text-xs font-medium rounded-lg text-cyan-400 border border-slate-700/50 transition-colors"
                >
                  <span>Documentation</span>
                  <span className="text-slate-500">→</span>
                </a>
                <a 
                  href="https://pypi.org/project/audiergon/" 
                  target="_blank" 
                  rel="noopener noreferrer"
                  className="flex items-center justify-between px-4 py-2.5 bg-slate-900 hover:bg-slate-700/50 text-xs font-medium rounded-lg text-cyan-400 border border-slate-700/50 transition-colors"
                >
                  <span>PyPI Package</span>
                  <span className="text-slate-500">→</span>
                </a>
                <a 
                  href="https://youtube.com/playlist?list=PLAbLVCg6_PqQ&si=2yWFeVAcUrOT_ob_" 
                  target="_blank" 
                  rel="noopener noreferrer"
                  className="flex items-center justify-between px-4 py-2.5 bg-slate-900 hover:bg-slate-700/50 text-xs font-medium rounded-lg text-cyan-400 border border-slate-700/50 transition-colors"
                >
                  <span>YouTube Video Series</span>
                  <span className="text-slate-500">→</span>
                </a>
              </div>

            </div>
          </div>
        )}

      </div>
    </main>
  );
}
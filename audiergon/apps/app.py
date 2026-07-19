"""
Local Audiergon App

https://github.com/hamdivazim/Audiergon
"""

__version__ = "1.0.0"

import gradio as gr
import numpy as np
import matplotlib.pyplot as plt
import wave
import os
from audiergon.process import process_audio
from audiergon.fast_fourier_transform import iterative_fft, iterative_fftfreq

def analyse_uploaded_file(audio_filepath):
    if not audio_filepath:
        return None
        
    with wave.open(audio_filepath, 'rb') as wav_file:
        sampling_rate = wav_file.getframerate()
        total_frames = wav_file.getnframes()
        raw_frames = wav_file.readframes(total_frames)

    signal = np.frombuffer(raw_frames, dtype=np.int16).astype(float)
    
    original_len = len(signal)
    p2_len = 1 << (original_len.bit_length() - 1)
    if p2_len > original_len:
        p2_len >>= 1
    signal = signal[:p2_len]

    fft_output = np.array(iterative_fft(signal))
    frequencies = iterative_fftfreq(len(signal), 1/sampling_rate)

    positive_frequencies = frequencies[:len(frequencies)//2]
    amplitudes = np.abs(fft_output)[:len(fft_output)//2] * (2.0 / len(signal))

    fig, ax = plt.subplots(figsize=(10, 4), facecolor='#0b0f12')
    ax.set_facecolor('#0b0f12')
    
    ax.plot(positive_frequencies, amplitudes, color='#a3e2e2', linewidth=1.5)
    ax.fill_between(positive_frequencies, amplitudes, color='#245e5e', alpha=0.3)
    
    ax.set_title("Frequency Spectrum", color='#ffffff', fontfamily='monospace')
    ax.set_xlabel("Frequency (Hz)", color='#ffffff', fontfamily='monospace')
    ax.set_ylabel("Magnitude", color='#ffffff', fontfamily='monospace')
    
    ax.tick_params(colors='#ffffff', which='both')
    ax.set_xlim(0, min(8000, sampling_rate // 2))
    ax.grid(True, linestyle=':', alpha=0.3, color='#a3e2e2')
    
    for spine in ax.spines.values():
        spine.set_color('#a3e2e2')
        spine.set_linewidth(1.5)
        
    plt.tight_layout()
    return fig

custom_css = """
@import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&family=Courier+Prime&display=swap');

footer {visibility: hidden}

body, .gradio-container, button, input, label, span, p, h1, h2, h3, .label-wrap, .form, textarea {
    font-family: 'Courier Prime', 'Courier', monospace !important;
}

p, span, a, label {
    color: #ffffff !important;
}

h3, h3 a {
    color: #a3e2e2 !important;
}

.retro-title h1 {
    font-family: 'Press Start 2P', monospace !important;
    color: #a3e2e2 !important;
    text-shadow: 2px 2px #245e5e;
    font-size: 2.2rem !important;
    letter-spacing: -1px;
}

.retro-title h3, .retro-title h3 * {
    color: #a3e2e2 !important;
    opacity: 1 !important;
}

button[role="tab"] {
    color: #888888 !important;
    background: transparent !important;
}
button[role="tab"][aria-selected="true"] {
    color: #a3e2e2 !important;
    border-bottom: 2px solid #a3e2e2 !important;
    background: #12181c !important;
}

.gr-form label, .gr-box label, .label-wrap, span.block-label, label {
    background-color: transparent !important;
    background: transparent !important;
    color: #a3e2e2 !important;
    font-weight: bold;
}

.upload-container *, .file-preview *, .audio-container *, [class*="upload"] * {
    color: #a3e2e2 !important;
}

input[type="number"], .wrap input, [class*="number-input"] {
    background-color: #12181c !important;
    color: #ffffff !important;
}

button.primary {
    background-color: #245e5e !important;
    color: white !important;
    box-shadow: none !important;
}
button.primary:hover {
    background-color: #a3e2e2 !important;
    color: #0b0f12 !important;
}

.loading, .eta-bar, .meta-text, .eta, .loading-text, 
[class*="loading"], [class*="eta"], [class*="processing"] {
    color: #a3e2e2 !important;
    opacity: 1 !important;
}

a[download], .download-button, button[title="Download"], [aria-label="Download"], .download, [class*="download"] {
    color: #a3e2e2 !important;
    display: inline-flex !important;
    visibility: visible !important;
    opacity: 1 !important;
}
a[download] svg, .download-button svg, button[title="Download"] svg, .download svg, [class*="download"] svg {
    fill: #a3e2e2 !important;
    stroke: #a3e2e2 !important;
    color: #a3e2e2 !important;
}

.icon-buttons, [data-testid="block-info"] + div {
    opacity: 1 !important;
    visibility: visible !important;
    display: flex !important;
}
"""

retro_theme = gr.themes.Monochrome(
    primary_hue="cyan",
    secondary_hue="cyan",
    neutral_hue="slate",
).set(
    body_background_fill="#0b0f12",
    block_background_fill="#12181c",
    slider_color="#a3e2e2",
    button_primary_background_fill="#245e5e",
    button_primary_text_color="#ffffff",
)

with gr.Blocks(title="Audiergon", theme=retro_theme, css=custom_css) as demo:
    with gr.Column(elem_classes="retro-title"):
        gr.Markdown(
            """
            # audiergon
            ### **A local EQ and DSP lab demonstrating the Fourier Transform. Built by [Hamd Waseem](https://github.com/hamdivazim/Audiergon)**
            """
        )
    
    with gr.Tab("5-Band Equalizer"):
        with gr.Row():
            with gr.Column():
                eq_input = gr.Audio(type="filepath", label="Input Audio (16-bit mono .wav)")
                
                with gr.Group():
                    gr.Markdown("**Frequency Band Gains**")
                    bass = gr.Slider(0.0, 3.0, 1.0, step=0.01, label="Bass (0 - 250 Hz)")
                    low_mids = gr.Slider(0.0, 3.0, 1.0, step=0.01, label="Low-Mids (250 - 1k Hz)")
                    mids = gr.Slider(0.0, 3.0, 1.0, step=0.01, label="Midrange (1k - 4k Hz)")
                    high_mids = gr.Slider(0.0, 3.0, 1.0, step=0.01, label="High-Mids (4k - 8k Hz)")
                    treble = gr.Slider(0.0, 3.0, 1.0, step=0.01, label="Treble (8k+ Hz)")
                    
                btn_eq = gr.Button("Process Audio", variant="primary")
            
            with gr.Column():
                eq_output = gr.Audio(
                    type="filepath", 
                    label="Processed Audio", 
                    interactive=False,
                    show_download_button=True
                )
                
        btn_eq.click(
            fn=process_audio,
            inputs=[eq_input, bass, low_mids, mids, high_mids, treble],
            outputs=eq_output
        )

    with gr.Tab("Fourier Spectrum Analyser"):
        with gr.Row():
            with gr.Column(scale=1):
                analysis_input = gr.Audio(type="filepath", label="Select Audio File")
                btn_analyse = gr.Button("Analyse Spectrum", variant="primary")
            with gr.Column(scale=2):
                plot_output = gr.Plot(label="FFT Spectrum Output")
                
        btn_analyse.click(
            fn=analyse_uploaded_file,
            inputs=analysis_input,
            outputs=plot_output
        )

if __name__ == "__main__":
    demo.launch()
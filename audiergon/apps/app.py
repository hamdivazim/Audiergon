import gradio as gr
from audiergon.process import process_audio

print("Launching Audiergon...")
interface = gr.Interface(
    fn=process_audio,
    inputs=[
        gr.Audio(type="filepath", label="Upload Audio (16 bit mono .wav)"),
        gr.Slider(minimum=0.0, maximum=3.0, value=1.0, step=0.01, label="Bass (0 - 250 Hz)"),
        gr.Slider(minimum=0.0, maximum=3.0, value=1.0, step=0.01, label="Low-Mids (250 - 1000 Hz)"),
        gr.Slider(minimum=0.0, maximum=3.0, value=1.0, step=0.01, label="Midrange (1000 - 4000 Hz)"),
        gr.Slider(minimum=0.0, maximum=3.0, value=1.0, step=0.01, label="High-Mids / Presence (4000 - 8000 Hz)"),
        gr.Slider(minimum=0.0, maximum=3.0, value=1.0, step=0.01, label="Treble / Brilliance (8000+ Hz)")
    ],
    outputs=gr.Audio(type="filepath", label="Output Audio"),
    title="Audiergon (Beta!)",
    description="Audiergon v0.0.1 - change volumes of five frequency bands using an iterative FFT implemented within Python"
)

interface.launch()
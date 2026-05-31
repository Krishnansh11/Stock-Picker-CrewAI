import gradio as gr
import warnings

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from stock_picker.crew import StockPicker

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

def run_crew(sector):
    inputs = {
        'sector': sector
    }
    result = StockPicker().crew().kickoff(inputs=inputs)
    return result.raw

interface = gr.Interface(
    fn=run_crew,
    inputs=gr.Textbox(label="Enter Sector"),
    outputs=gr.Textbox(label="CrewAI Output"),
    title="Stock Picker CrewAI UI",
    description="Enter a sector to get stock recommendations from the CrewAI stock picker."
)

if __name__ == "__main__":
    interface.launch()
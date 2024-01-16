from pathlib import Path
from transformers import AutoProcessor, VisionEncoderDecoderModel
import torch
import fitz
import io
from PIL import Image

processor = AutoProcessor.from_pretrained("facebook/nougat-small")
model = VisionEncoderDecoderModel.from_pretrained("facebook/nougat-small")

device = "cuda" if torch.cuda.is_available() else "cpu"
model.to(device)

def rasterize_paper(pdf: Path, outpath: Path, dpi: int = 96):
    """
    Rasterize a PDF file to PNG images.

    Args:
        pdf (Path): The path to the PDF file.
        outpath (Path): The output directory.
        dpi (int, optional): The output DPI. Defaults to 96.
    """
    try:
        if isinstance(pdf, (str, Path)):
            pdf = fitz.open(pdf)
        for i in range(len(pdf)):
            page_bytes: bytes = pdf[i].get_pixmap(dpi=dpi).pil_tobytes(format="PNG")
            with (outpath / f"{i + 1}.png").open("wb") as f:
                f.write(page_bytes)
    except Exception as e:
        print(f"Error: {e}")

def process_document(pdf_file):
    # Step 1: Rasterize PDF
    temp_output_path = Path("temp_output")
    temp_output_path.mkdir(exist_ok=True)
    rasterize_paper(pdf_file, temp_output_path)

    # Step 2: Load Images
    images = []
    for image_path in temp_output_path.glob("*.png"):
        image = Image.open(image_path)
        images.append(image)

    # Step 3: Generate Transcription
    pixel_values = processor(images=images, return_tensors="pt").pixel_values

    outputs = model.generate(
        pixel_values.to(device),
        min_length=1,
        max_length=3584,
        bad_words_ids=[[processor.tokenizer.unk_token_id]],
        return_dict_in_generate=True,
        output_scores=True,
    )

    # Step 4: Postprocess
    generated = processor.batch_decode(outputs[0], skip_special_tokens=True)[0]
    generated = processor.post_process_generation(generated, fix_markdown=False)

    # Optionally, save the generated content to a file
    processed_file_path = Path("processed_documents") / "output.md"
    with processed_file_path.open("w", encoding="utf-8") as f:
        f.write(generated)

    return processed_file_path
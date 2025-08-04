


from PIL import Image

def optimize_image(file_path):
    img = Image.open(file_path)

    if img.mode in ("RGBA", "P"):
        img = img.convert("RGB")

    img.save(file_path, optimize=True, quality=85)




# def optimize_image(file_path):
#     try:
#         img = Image.open(file_path)

#         # Convertir a RGB si es necesario (por ejemplo, PNG con transparencia)
#         if img.mode in ("RGBA", "P"):
#             img = img.convert("RGB")

#         # Comprimir la imagen y sobrescribirla
#         img.save(file_path, optimize=True, quality=85)  # quality puede ajustarse

#     except Exception as e:
#         raise RuntimeError(f"No se pudo optimizar la imagen: {str(e)}")

from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm

FILE_TYPES = {
    'Images': ['.jpg', '.jpeg', '.png', '.gif', '.tiff', '.bmp', '.svg'],
    'Documents': ['.pdf', '.docx', '.xlsx', '.pptx', '.txt', '.md'],
    'Audio': ['.mp3', '.wav', '.aac', '.flac'],
    'Videos': ['.mp4', '.mov', '.avi', '.mkv'],
    'Archives': ['.zip', '.rar', '.tar.gz']
}

def build_extension_map(file_types: dict) -> dict:
    return {
        extension: category
        for category, extensions in file_types.items()
        for extension in extensions
    }

def move_file(src: Path, dst: Path):
    src.rename(dst)

def organize_downloads(download_folder: str, use_concurrency: bool = True, max_workers: int = 4) -> None:
    download_path = Path(download_folder)
    if not download_path.exists():
        print(f"La ruta {download_path} no existe.")
        return

    ext_to_category = build_extension_map(FILE_TYPES)
    files = [f for f in download_path.iterdir() if f.is_file()]
    files_by_category = {}

    for file in files:
        category = ext_to_category.get(file.suffix.lower(), 'Others')
        files_by_category.setdefault(category, []).append(file)

    for cat in files_by_category.keys():
        (download_path / cat).mkdir(exist_ok=True)

    total_files = sum(len(cat_files) for cat_files in files_by_category.values())
    if total_files == 0:
        print("No hay archivos para organizar.")
        return

    if use_concurrency and files:
        futures = []
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            for cat, cat_files in files_by_category.items():
                for f in cat_files:
                    futures.append(executor.submit(move_file, f, download_path / cat / f.name))

            for _ in tqdm(as_completed(futures), total=len(futures), desc="Moviendo archivos", unit="archivo"):
                pass
    else:
        from tqdm import tqdm as normal_tqdm
        with normal_tqdm(total=total_files, desc="Moviendo archivos", unit="archivo") as pbar:
            for cat, cat_files in files_by_category.items():
                for f in cat_files:
                    move_file(f, download_path / cat / f.name)
                    pbar.update(1)

    print("Descargas organizadas con éxito.")

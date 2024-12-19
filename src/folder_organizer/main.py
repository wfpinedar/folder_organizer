import argparse
from .organizer import organize_downloads

def main():
    parser = argparse.ArgumentParser(description="Organiza tu carpeta de descargas")
    parser.add_argument("download_folder", help="Ruta a la carpeta de descargas")
    parser.add_argument("--no-concurrency", action="store_true", help="No usar concurrencia")
    parser.add_argument("--workers", type=int, default=4, help="Número de hilos concurrentes")
    args = parser.parse_args()

    organize_downloads(
        args.download_folder,
        use_concurrency=not args.no_concurrency,
        max_workers=args.workers
    )


if __name__ == "__main__":
    main()

from src.download_manager.registry_selector import RegistrySelector

try:
    from src.download_manager.dispatcher import DownloadDispatcher
except Exception:
    DownloadDispatcher = None


def main():

    selector = RegistrySelector()

    datasets = selector.downloadable()

    print()

    print("="*70)
    print("GOHIF Registry Download Queue")
    print("="*70)

    print()

    print("Datasets eligible :", len(datasets))

    print()

    for _, row in datasets.iterrows():

        print(
            f"{row['GOHIF_ID']:15}"
            f"{row['Dataset_Name'][:45]:45}"
        )

        if DownloadDispatcher is not None:

            pass
            # dispatcher.download(row)

if __name__ == "__main__":
    main()

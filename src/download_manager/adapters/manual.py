from src.download_manager.adapters.base import BaseAdapter


class ManualAdapter(BaseAdapter):

    def download(self, row):

        print(f"[MAN ] {row['Dataset_Name']}")

        return self.result(

            success=True,

            row=row,

            message="Manual download required"

        )

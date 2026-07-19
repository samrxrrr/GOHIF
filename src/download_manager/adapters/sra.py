from src.download_manager.adapters.base import BaseAdapter


class SRAAdapter(BaseAdapter):

    def download(self, row):

        print(f"[SRA ] {row['Dataset_Name']}")

        return self.result(

            success=True,

            row=row,

            message="SRA adapter reached (dry run)"

        )

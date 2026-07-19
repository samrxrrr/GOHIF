from src.download_manager.adapters.base import BaseAdapter


class NCBIAdapter(BaseAdapter):

    def download(self, row):

        print(f"[NCBI] {row['Dataset_Name']}")

        return self.result(

            success=True,

            row=row,

            message="NCBI adapter reached (dry run)"

        )

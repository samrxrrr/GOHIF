from src.download_manager.adapters.base import BaseAdapter


class APIAdapter(BaseAdapter):

    def download(self, row):

        print(f"[API ] {row['Dataset_Name']}")

        return self.result(

            success=True,

            row=row,

            message="API adapter reached (dry run)"

        )

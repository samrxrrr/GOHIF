from src.download_manager.adapters.base import BaseAdapter


class GitAdapter(BaseAdapter):

    def download(self, row):

        print(f"[GIT ] {row['Dataset_Name']}")

        return self.result(

            success=True,

            row=row,

            message="Git adapter reached (dry run)"

        )

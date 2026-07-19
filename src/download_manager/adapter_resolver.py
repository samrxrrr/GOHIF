class AdapterResolver:

    @staticmethod
    def resolve(row):

        method = str(row.get("Download_Method", "")).strip().upper()

        mapping = {

            "HTTP": "http",

            "REST_API": "api",

            "API": "api",

            "ENA_API": "api",

            "CLI": "cli",

            "NCBI_DATASETS_CLI": "ncbi",

            "SRA_TOOLKIT": "sra",

            "REPOSITORY": "git",

            "MANUAL": "manual"

        }

        if method in mapping:
            return mapping[method]

        url = str(row.get("Download_URL","")).lower()

        if url.startswith("ftp://"):
            return "ftp"

        if "github.com" in url:
            return "git"

        if "gitlab.com" in url:
            return "git"

        if "ncbi" in url:
            return "ncbi"

        if "sra" in url:
            return "sra"

        if url.startswith("http"):
            return "http"

        return "manual"

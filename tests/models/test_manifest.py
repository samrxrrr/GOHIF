from gae.models.manifest import Manifest


def test_manifest_validation():

    data = {

        "dataset":{

            "id":"TEST",

            "name":"Dataset",

            "domain":"test",

            "version":"1"
        },

        "download":{

            "method":"http",

            "url":"https://example.com/file.txt"
        },

        "storage":{

            "output_directory":"/tmp"
        }

    }

    manifest = Manifest.model_validate(data)

    assert manifest.dataset.id == "TEST"

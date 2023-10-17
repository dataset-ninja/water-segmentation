Dataset **WaterDataset** can be downloaded in [Supervisely format](https://developer.supervisely.com/api-references/supervisely-annotation-json-format):

 [Download](https://assets.supervisely.com/supervisely-supervisely-assets-public/teams_storage/C/c/G3/6gY5OSSPYa6WKg6CPSfwiScBSZG1Uudhz48PRDafjAYk0H6zEtZb2QUMB14bek05mb7HD9EKMbmRZfkN3sDhQAoBAyQep2GUDKuhDdWhsy7kShWzkOqPX2FJjFzj.tar)

As an alternative, it can be downloaded with *dataset-tools* package:
``` bash
pip install --upgrade dataset-tools
```

... using following python code:
``` python
import dataset_tools as dtools

dtools.download(dataset='WaterDataset', dst_dir='~/dataset-ninja/')
```
Make sure not to overlook the [python code example](https://developer.supervisely.com/getting-started/python-sdk-tutorials/iterate-over-a-local-project) available on the Supervisely Developer Portal. It will give you a clear idea of how to effortlessly work with the downloaded dataset.


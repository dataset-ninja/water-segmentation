Dataset **WaterDataset** can be downloaded in [Supervisely format](https://developer.supervisely.com/api-references/supervisely-annotation-json-format):

 [Download](https://assets.supervisely.com/remote/eyJsaW5rIjogImZzOi8vYXNzZXRzLzIzOTNfV2F0ZXJEYXRhc2V0L3dhdGVyZGF0YXNldC1EYXRhc2V0TmluamEudGFyIiwgInNpZyI6ICJLbmtibGRiSndvOHFUR0d2RG10dG15SjV0WERPM1U2eWM5NXppOHN6NzVRPSJ9)

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


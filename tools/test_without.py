

import dask.array as da
import xarray
import s3fs
import xarray as xr

bucket = "zarr"
name = "sample"

nana = xarray.DataArray(da.random.random((1023,1023,45,2,1)))



s3_path = f"{bucket}/{name}"
s3 = s3fs.S3FileSystem(client_kwargs={"endpoint_url": "s3://minio:9000"}, username="weak_access_key", password="weak_secret_key")
s3store = s3.get_mapper(s3_path)


print("Storing")
nana.to_dataset().to_zarr(store=s3store, mode="w", consolidated=True, compute=True)
print("Getting")

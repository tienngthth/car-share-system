./cloud/cloud_sql_proxy -instances=clean-wonder-286803:asia-southeast2:s3747274=tcp:3306 -credential_file="cloud/clean-wonder-286803-fd26772409c0.json" & python cloud/api/api.py 

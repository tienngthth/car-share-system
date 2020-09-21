Cloudcar documentation
====================================
This is the Cloudcard documentation built using Sphinx

.. toctree::
   :maxdepth: 2
   
   Server
   API
   Database
   User Interface
   Validators

To connect to the GCP database
------------------------------
1) Download the Cloud SQL Proxy for your operating system. If in Linux, make it executeable with chmod.
2) Download the JSON file included in this project
3) In the command prompt, navigate to the location of the proxy and run this command:

.\cloud_sql_proxy -instances=clean-wonder-286803:asia-southeast2:s3747274=tcp:3306 -credential_file=<PATH TO THE JSON FILE>
e.g.: C:\Users\tienn\Downloads\clean-wonder-286803-fd26772409c0.json

4) Ctrl + C to terminate

To start the API Server
-----------------------
python3 /cloud/api/api.py

To start Flask
--------------
./webpage/runme.sh

(or the long version: export FLASK_APP=webpage/flaskr && export FLASK_ENV=development && export OAUTHLIB_INSECURE_TRANSPORT=1 && export GOOGLE_APPLICATION_CREDENTIALS="/webpage/flaskr/script/files/client.json" && flask run)


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

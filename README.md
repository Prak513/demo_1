#### Prerequisites: Docker, Kubernetes cluster

 


### Steps:
#### For Meerkat Bus:
1. Build the docker image with name `mm2-meerkat-image`
   from Dockerfile as: 
   > docker build --tag=mm2-meerkat-image image_build_stuff/

2. Start the server locally as:
   > python3 master.py
   
3. Make POST request as below to start the mirroring for given list of topics:
   
    ```
    curl --location --request POST 'http://127.0.0.1:5000/control-mirroring' --header 'Content-Type: application/json' --data-raw '{
    "bus_name": "meerkat",
    "topics": ["topic-A", "topic-B", "topic-C"]}'
    ```   

   - This will create a bus specific kubernetes pod and service
   
4. To access this kubernetes server get the current status of mirroring make this GET call as:
   > curl localhost:30007/info
   
 
 
#### For DSI Bus:
1. Build the docker image with name `mm2-dsi-image`
   from Dockerfile as: 
   > docker build --tag=mm2-dsi-image image_build_stuff/

2. Start the server locally as:
   > python3 master.py
   
3. Make POST request as below to start the mirroring for given list of topics:
   
    ```
    curl --location --request POST 'http://127.0.0.1:5000/control-mirroring' --header 'Content-Type: application/json' --data-raw '{
    "bus_name": "dsi",
    "topics": ["topic-A", "topic-B", "topic-C"]}'
    ```

   - This will create a bus specific kubernetes pod and service
   
4. To access this kubernetes server to get the current status of mirroring make this GET call as:
   > curl localhost:30007/info
import enum
import time

import yaml
import os
from typing import List

from jinja2 import Environment, FileSystemLoader
from kubernetes import client, config
from flask import Flask, jsonify, redirect
from pydantic import BaseModel
from flask_pydantic import validate

MEERKAT_IMAGE_NAME = "mm2-meerkat-image"
DSI_IMAGE_NAME = "mm2-dsi-image"
POD_NAME = "mm2-pod"
SVC_NAME = "mm2-svc"
CTR_NAME = "mm2-ctr"
NAMESPACE = "default"
LABEL_KEY = "app"
LABEL_VALUE = "mm2-app"
IMAGE_PULL_POLICY = "Never"
CTR_PORT = 8181
NODE_PORT = 30007

CWD = os.getcwd()
TEMPLATES_DIR = os.path.join(CWD, 'templates')
CONFIG_DIR = os.path.join(CWD, 'configs')
JINJA_ENV = Environment(loader = FileSystemLoader(TEMPLATES_DIR))


class AutomateKubernetes:
    def __init__(self, bus_name, topics_to_be_mirrored):
        config.load_kube_config()

        self.image_name = MEERKAT_IMAGE_NAME if bus_name == BusEnum.MEERKAT else DSI_IMAGE_NAME
        self.pod_name = POD_NAME
        self.svc_name = SVC_NAME
        self.ctr_name = CTR_NAME
        self.namespace = NAMESPACE
        self.label_key = LABEL_KEY
        self.label_value = LABEL_VALUE
        self.image_pull_policy = IMAGE_PULL_POLICY
        self.ctr_port = CTR_PORT
        self.node_port = NODE_PORT
        self.bus_name = bus_name
        self.topics_to_be_mirrored = ", ".join(topics_to_be_mirrored)
        self.k8s_client = client.CoreV1Api()
        self.pod_list = self.get_pod_list()
        self.svc_list = self.get_svc_list()

    def get_pod_list(self):
        pod_info = self.k8s_client.list_namespaced_pod(namespace=NAMESPACE).to_dict()
        pod_list = [x.get("metadata").get("name") for x in pod_info.get("items")]
        print(f"available-pods: {pod_list}")
        return pod_list

    def get_svc_list(self):
        svc_info = self.k8s_client.list_namespaced_service_with_http_info(namespace = NAMESPACE)[0].to_dict()
        svc_list = [x.get("metadata").get("name") for x in svc_info.get("items")]
        print(f"available-services: {svc_list}")
        return svc_list

    def create_pod(self):
        template = JINJA_ENV.get_template("pod.html")
        config_file_path = os.path.join(CONFIG_DIR, "pod.yaml")
        with open(config_file_path, "w") as file_obj:
            file_obj.write(template.render(obj = self))
        with open(config_file_path) as file_obj:
            data = yaml.safe_load(file_obj)
        res: client.models.v1_service.V1Service = self.k8s_client.create_namespaced_pod(
            namespace=NAMESPACE, body=data
        )

        return True if res else None

    def create_svc(self):
        template = JINJA_ENV.get_template("svc.html")
        config_file_path = os.path.join(CONFIG_DIR, "svc.yaml")
        with open(config_file_path, "w") as file_obj:
            file_obj.write(template.render(obj = self))
        with open(config_file_path) as file_obj:
            data = yaml.safe_load(file_obj)
        res: client.models.v1_service.V1Service = (
            self.k8s_client.create_namespaced_service(namespace=NAMESPACE, body=data)
        )

        return True if res else None

    def sync_bus_specific_web_service(self):
        if self.svc_name not in self.svc_list:
            self.create_svc()

        if self.pod_name not in self.pod_list:
            self.create_pod()

        else:
            # logic to restart the POD
            self.k8s_client.delete_namespaced_pod(name = POD_NAME, namespace = NAMESPACE)
            st_time = time.time()
            while (time.time()-st_time) < 60:
                if self.pod_name not in self.get_pod_list():
                    break
            self.create_pod()


class BusEnum(str, enum.Enum):
    DSI = "dsi"
    MEERKAT = "meerkat"


class DataIn(BaseModel):
    bus_name: BusEnum
    topics: List[str]


app = Flask(__name__)


@app.route("/control-mirroring", methods=["POST"])
@validate()
def control_mirroring(body: DataIn):
    """
    Since we are doing mirroring from scratch against the updated topic list, so
    this endpoint will cover all create, update, delete operations
    """

    # update the list of topics to be mirrored in shared volume :-
    # currently passing the list directly `topics_to_be_mirrored` at ln:127
    # wip
    # ...
    # ...

    kube = AutomateKubernetes(bus_name = body.bus_name, topics_to_be_mirrored = body.topics)
    kube.sync_bus_specific_web_service()
    return jsonify({"message": "success"}), 201


@app.route("/")
def redirects():
    return redirect("/control-mirroring")


if __name__ == "__main__":
    app.run(host = "0.0.0.0", port = 5000)

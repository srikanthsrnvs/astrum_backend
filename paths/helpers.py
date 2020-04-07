url = 'https://www.googleapis.com/compute/v1/projects/astrumdashboard/zones/us-central1-a/instances'

def create_startup_script(urls, job_id):
  urls_to_string = str(urls).strip('[]').strip(' ')
  startup_script = "sudo apt-get update\ncurl -O http://developer.download.nvidia.com/compute/cuda/repos/ubuntu1804/x86_64/cuda-repo-ubuntu1804_10.0.130-1_amd64.deb\nsudo dpkg -i cuda-repo-ubuntu1804_10.0.130-1_amd64.deb\nsudo apt-key adv --fetch-keys http://developer.download.nvidia.com/compute/cuda/repos/ubuntu1804/x86_64/7fa2af80.pub\nsudo apt-get update\nsudo apt-get -y install cuda=10.0.130-1\nsudo apt-get -y install python3-pip\nsudo apt-get -y install python-virtualenv\nvirtualenv -p /usr/bin/python3 virtualenvironment/astrum\ncd virtualenvironment/astrum/bin\nsource activate\ncd\ngsutil cp -r gs://astrumdashboard.appspot.com/source .\ngsutil cp -r gs://astrumdashboard.appspot.com/cudnn.tgz .\ntar -xvzf cudnn.tgz\nsudo cp cuda/include/cudnn.h /usr/local/cuda/include\nsudo cp cuda/lib64/libcudnn* /usr/local/cuda/lib64\nsudo chmod a+r /usr/local/cuda/include/cudnn.h /usr/local/cuda/lib64/libcudnn*\nexport PATH=/usr/local/cuda-10.0/bin${{PATH:+:${{PATH}}}}\nexport LD_LIBRARY_PATH=/usr/local/cuda-10.0/lib64:$LD_LIBRARY_PATH\nexport PATH=/usr/local/cuda/bin${{PATH:+:${{PATH}}}}\nexport LD_LIBRARY_PATH=/usr/local/cuda/lib64:$LD_LIBRARY_PATH\ncd source\npip3 install -r requirements.txt\n".format(job_id, job_id)
  startup_script += "python3 main.py --urls={0} --type=image_classification --job_id={1} |& tee {1}_output.txt".format(urls_to_string, job_id)
  return startup_script

def create_http_body(startup_script, job_id):
  item = {'key': 'startup-script', 'value': startup_script}
  data = {
    "name": "astrum"+job_id,
    "zone": "projects/astrumdashboard/zones/us-central1-a",
    "machineType": "projects/astrumdashboard/zones/us-central1-a/machineTypes/n1-standard-1",
    "displayDevice": {
      "enableDisplay": True
    },
    "metadata": {
      "items": [
        item
      ]
    },
    "tags": {
      "items": [
        "http-server",
        "https-server"
      ]
    },
    "guestAccelerators": [
      {
        "acceleratorCount": 1,
        "acceleratorType": "projects/astrumdashboard/zones/us-central1-a/acceleratorTypes/nvidia-tesla-v100"
      }
    ],
    "disks": [
      {
        "type": "PERSISTENT",
        "boot": True,
        "mode": "READ_WRITE",
        "autoDelete": True,
        "deviceName": "astrum"+job_id,
        "initializeParams": {
          "sourceImage": "projects/ubuntu-os-cloud/global/images/ubuntu-1804-bionic-v20200317",
          "diskType": "projects/astrumdashboard/zones/us-central1-a/diskTypes/pd-standard",
          "diskSizeGb": "100"
        },
        "diskEncryptionKey": {}
      }
    ],
    "canIpForward": False,
    "networkInterfaces": [
      {
        "subnetwork": "projects/astrumdashboard/regions/us-central1/subnetworks/default",
        "accessConfigs": [
          {
            "name": "External NAT",
            "type": "ONE_TO_ONE_NAT",
            "networkTier": "PREMIUM"
          }
        ],
        "aliasIpRanges": []
      }
    ],
    "description": "",
    "labels": {
      "job_id": job_id
    },
    "scheduling": {
      "preemptible": False,
      "onHostMaintenance": "TERMINATE",
      "automaticRestart": True,
      "nodeAffinities": []
    },
    "deletionProtection": False,
    "reservationAffinity": {
      "consumeReservationType": "ANY_RESERVATION"
    },
    "serviceAccounts": [
      {
        "email": "454472899112-compute@developer.gserviceaccount.com",
        "scopes": [
          "https://www.googleapis.com/auth/cloud-platform"
        ]
      }
    ],
    "shieldedInstanceConfig": {
      "enableSecureBoot": False,
      "enableVtpm": True,
      "enableIntegrityMonitoring": True
    }
  }
  return data

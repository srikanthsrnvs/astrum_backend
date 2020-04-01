create_instance_url = "https://www.googleapis.com/compute/v1/projects/astrumdashboard/zones/us-central1-a/instances"
create_instance_json = {
    "kind": "compute#instance",
    "name": "instance-name",
    "zone": "projects/astrumdashboard/zones/us-central1-a",
    "machineType": "projects/astrumdashboard/zones/us-central1-a/machineTypes/n1-standard-1",
    "displayDevice": {
        "enableDisplay": False
    },
    "metadata": {
        "kind": "compute#metadata",
        "items": []
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
        "acceleratorType": "projects/astrumdashboard/zones/us-central1-a/acceleratorTypes/nvidia-tesla-k80"
        }
    ],
    "disks": [
        {
        "kind": "compute#attachedDisk",
        "type": "PERSISTENT",
        "boot": True,
        "mode": "READ_WRITE",
        "autoDelete": True,
        "deviceName": "instance-name",
        "initializeParams": {
            "sourceImage": "projects/ubuntu-os-cloud/global/images/ubuntu-1804-bionic-v20200218",
            "diskType": "projects/astrumdashboard/zones/us-central1-a/diskTypes/pd-standard",
            "diskSizeGb": "10"
        },
        "diskEncryptionKey": {}
        }
    ],
    "canIpForward": False,
    "networkInterfaces": [
        {
        "kind": "compute#networkInterface",
        "subnetwork": "projects/astrumdashboard/regions/us-central1/subnetworks/default",
        "accessConfigs": [
            {
            "kind": "compute#accessConfig",
            "name": "External NAT",
            "type": "ONE_TO_ONE_NAT",
            "networkTier": "PREMIUM"
            }
        ],
        "aliasIpRanges": []
        }
    ],
    "description": "",
    "labels": {},
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

set_http_traffic_url = "https://www.googleapis.com/compute/v1/projects/astrumdashboard/global/firewalls"
set_http_traffic_json = {
    "name": "default-allow-http",
    "kind": "compute#firewall",
    "sourceRanges": [
        "0.0.0.0/0"
    ],
    "network": "projects/astrumdashboard/global/networks/default",
    "targetTags": [
        "http-server"
    ],
    "allowed": [
        {
        "IPProtocol": "tcp",
            "ports": [
                "80"
            ]
        }
    ]
}

set_https_traffic_url = "https://www.googleapis.com/compute/v1/projects/astrumdashboard/global/firewalls"
set_https_traffic_json = {
    "name": "default-allow-https",
    "kind": "compute#firewall",
    "sourceRanges": [
        "0.0.0.0/0"
    ],
    "network": "projects/astrumdashboard/global/networks/default",
    "targetTags": [
        "https-server"
    ],
    "allowed": [
        {
            "IPProtocol": "tcp",
            "ports": [
                "443"
            ]
        }
    ]
}

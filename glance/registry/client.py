# vim: tabstop=4 shiftwidth=4 softtabstop=4

# Copyright 2011 OpenStack, LLC
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

"""
Simple client class to speak with any RESTful service that implements
the Glance Registry API
"""

import httplib
import json
import logging
import urlparse
import socket
import sys

from glance.common import exception
from glance.client import BaseClient


class RegistryClient(BaseClient):

    """A client for the Registry image metadata service"""

    DEFAULT_PORT = 9191

    def __init__(self, host, port=None, use_ssl=False):
        """
        Creates a new client to a Glance Registry service.

        :param host: The host where Glance resides
        :param port: The port where Glance resides (defaults to 9191)
        :param use_ssl: Should we use HTTPS? (defaults to False)
        """

        port = port or self.DEFAULT_PORT
        super(RegistryClient, self).__init__(host, port, use_ssl)

    def get_images(self):
        """
        Returns a list of image id/name mappings from Registry
        """
        res = self.do_request("GET", "/images")
        data = json.loads(res.read())['images']
        return data

    def get_images_detailed(self):
        """
        Returns a list of detailed image data mappings from Registry
        """
        res = self.do_request("GET", "/images/detail")
        data = json.loads(res.read())['images']
        return data

    def get_image(self, image_id):
        """
        Returns a mapping of image metadata from Registry

        :raises exception.NotFound if image is not in registry
        """
        res = self.do_request("GET", "/images/%s" % image_id)
        data = json.loads(res.read())['image']
        return data

    def add_image(self, image_metadata):
        """
        Tells registry about an image's metadata
        """
        if 'image' not in image_metadata.keys():
            image_metadata = dict(image=image_metadata)
        body = json.dumps(image_metadata)
        res = self.do_request("POST", "/images", body)
        # Registry returns a JSONified dict(image=image_info)
        data = json.loads(res.read())
        return data['image']

    def update_image(self, image_id, image_metadata):
        """
        Updates Registry's information about an image
        """
        if 'image' not in image_metadata.keys():
            image_metadata = dict(image=image_metadata)

        body = json.dumps(image_metadata)

        res = self.do_request("PUT", "/images/%s" % image_id, body)
        data = json.loads(res.read())
        image = data['image']
        return image

    def delete_image(self, image_id):
        """
        Deletes Registry's information about an image
        """
        self.do_request("DELETE", "/images/%s" % image_id)
        return True

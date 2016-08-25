"""
Copyright (c) 2015 SONATA-NFV
ALL RIGHTS RESERVED.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

Neither the name of the SONATA-NFV [, ANY ADDITIONAL AFFILIATION]
nor the names of its contributors may be used to endorse or promote
products derived from this software without specific prior written
permission.

This work has been performed in the framework of the SONATA project,
funded by the European Commission under Grant number 671517 through
the Horizon 2020 and 5G-PPP programmes. The authors would like to
acknowledge the contributions of their colleagues of the SONATA
partner consortium (www.sonata-nfv.eu).
"""

import logging
import yaml
import time
from sonmanobase import messaging

logging.basicConfig(level=logging.INFO)
LOG = logging.getLogger("son-mano-fakeslm")
LOG.setLevel(logging.DEBUG)
logging.getLogger("son-mano-base:messaging").setLevel(logging.INFO)


class fakeslmu(object):
    def __init__(self):

        self.name = 'fake-slm'
        self.version = '0.1-dev'
        self.description = 'description'

        LOG.info("Starting SLM2:...")

        # create and initialize broker connection
        self.manoconn = messaging.ManoBrokerRequestResponseConnection(self.name)

        self.path_descriptors = 'test/test_descriptors/'
        self.end = False

        self.publish_nsd()

        self.run()

    def run(self):

        # go into infinity loop

        while self.end == False:
            time.sleep(1)


    def publish_nsd(self):

        nsd = open(self.path_descriptors + 'nsd2.yml', 'r')
        nsr = open(self.path_descriptors + 'nsr.yml', 'r')
        message = {'NSD':yaml.load(nsd),'NSR':yaml.load(nsr)}
        self.manoconn.call_async(self._on_publish_nsd_response,
                                 'specific.manager.registry.ssm.update',
                                 yaml.dump(message))

    def _on_publish_nsd_response(self, ch, method, props, response):

        response = yaml.load(str(response))
        if type(response) == dict:
            if response['status'] == 'Updated':
                LOG.info("update done")
                self.end = True
            else:
                LOG.error("SSM update failed.'{0}'".format(response['error']))
                self.end = True
def main():
    fakeslmu()


if __name__ == '__main__':
    main()

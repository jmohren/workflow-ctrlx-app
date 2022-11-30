# MIT License
#
# Copyright (c) 2020-2022 Bosch Rexroth AG
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from ctrlxdatalayer.provider import Provider
from ctrlxdatalayer.variant import Variant

from alldataprovider.providerNodeAllData import ProviderNodeAllData

class NodeManagerAllData:

    def __init__(self, provider: Provider, addressRoot: str):
        self.provider = provider
        self.addressRoot = addressRoot
        self.nodes = []

    def create_prediction_node(self):
        addressBranch = self.addressRoot + "prediction/"

        data = Variant()
        data.set_int8(0)
        self.create_single_node(addressBranch, "", "anomaly",
                                "unit", "description", True, data)

    def create_input_nodes(self, ):
        addressBranch = self.addressRoot + "input/"

        data = Variant()
        data.set_float64(13.4626)
        self.create_single_node(addressBranch, "", "feature_1",
                                "unit", "description", True, data)
        
        data = Variant()
        data.set_float64(14.4626)
        self.create_single_node(addressBranch, "", "feature_2",
                                "unit", "description", True, data)

        data = Variant()
        data.set_float64(15.4626)
        self.create_single_node(addressBranch, "", "feature_3",
                                "unit", "description", True, data)

        # data = Variant()
        # data.set_array_float64([64.1, 64.2, 64.3])
        # self.create_single_node(addressBranch, "", "input-array",
        #                         "unit", "description", True, data)


    def create_single_node(self, addressBranch: str, addressType : str, name: str, unit: str, description: str, dynamic: bool, data: Variant):
        address = addressBranch + name
        print("Creating", address)

        if is_blank(addressType):
            addressType = "types/datalayer/" + name

        node = ProviderNodeAllData(
            self.provider, addressType, address, name, unit, description, dynamic, data)

        if node is not None:
            self.nodes.append(node)
            self.provider.register_node(address, node.providerNode)


def is_blank (myString):
    return not (myString and myString.strip())
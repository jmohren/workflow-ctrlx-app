# MIT License
#
# Copyright (c) 2021-2022 Bosch Rexroth AG
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

import os

import ctrlxdatalayer

"""
This script provides auxiliary methods to create ctrlX Datalayer client and provider connections to ctrlX CORE devices.
It can be used for both running in an app build environment (QEMU VM) and within the snap environment on the ctrlX CORE.

Feel free to use it in your projects and to change it if necessary.

For ease of use, the default values for IP address, user, password and SSL port are chosen to match the settings of a
newly created ctrlX CORE device:

    ip="192.168.1.1"
    user="boschrexroth"
    password="boschrexroth"
    ssl_port=443

If these values do not suit your use case, explicitly pass the parameters that require different values.
Here some examples:

1. ctrlX CORE or ctrlX CORE virtual with another IP address, user and password:

    client, client_connection = get_client(system, ip="192.168.1.100", user="admin", password="-$_U/{X$aG}Z3/e<")

2. ctrlX CORE virtual with port forwarding running on the same host as the app build environment (QEMU VM):

    client, client_connection = get_client(system, ip="10.0.2.2", ssl_port=8443)

    Remarks: 
    10.0.2.2 is the IP address of the host from the point of view of the app build environment (QEMU VM).
    8443 is the host port which is forwarded to the SSL port (=433) of the ctrlX CORE virtual


IMPORTANT:
You need not change the parameter settings before building a snap and installing the snap on a ctrlX CORE.
The method get_connection_string detects the snap environment and uses automatically inter process communication. 
Therefor the connection string to the ctrlX Datalayer is:

    "ipc://"

"""


def get_connection_string(
        ip="10.0.2.2",
        user="boschrexroth",
        password="boschrexroth",
        ssl_port=8443):
    """
    Combines a ctrlX Datalayer connection string.
    @param[in] ip IP address of the ctrlX CORE. Use "10.0.2.2" to connect to a ctrlX CORE virtual with port forwarding.
    @param[in] user Name of the user.
    @param[in] password Password of the user.
    @param[in] ssl_port Port number for a SSL connection. ctrlX CORE virtual with port forwarding: Use the host port (default 8443) forwarded to port 22 of the ctrlX virtual.
    @returns connection_string The connection string: "ipc://" for running in snap environment, "tcp://..." for running in environment.
    """

    if 'SNAP' in os.environ:
        return "ipc://"

    # Client connection port 2069 resp. Provider connection port 2070 are obsolete
    connection_string = "tcp://"+user+":"+password+"@"+ip

    if (ssl_port == 443):
        return connection_string

    return connection_string+"?sslport=" + str(ssl_port)


def get_client(system: ctrlxdatalayer.system.System,
               ip="10.0.2.2",
               user="boschrexroth",
               password="boschrexroth",
               ssl_port=8443):
    """
    Creates a ctrlX Datalayer client instance.
    @param[in] system A ctrlxdatalayer.system.System instance
    @param[in] ip IP address of the ctrlX CORE. Use "10.0.2.2" to connect to a ctrlX CORE virtual with port forwarding.
    @param[in] user Name of the user.
    @param[in] password Password of the user.
    @param[in] ssl_port Port number for a SSL connection. ctrlX CORE virtual with port forwarding: Use the host port (default 8443) forwarded to port 22 of the ctrlX virtual.
    @returns tuple  (client, connection_string)
    @return <client> The ctrlxdatalayer.client.Client instance or None if failed
    @return <connection_string> The connection string or None if failed
    """

    connection_string = get_connection_string(
        ip, user, password, ssl_port)
    client = system.factory().create_client(connection_string)
    if client.is_connected():
        return client, connection_string
    client.close()

    return None, connection_string


def get_provider(system: ctrlxdatalayer.system.System,
                ip="10.0.2.2",
                user="boschrexroth",
                password="boschrexroth",
                ssl_port=8443):
    """
    Creates a ctrlX Datalayer provider instance.
    @param[in] system A ctrlxdatalayer.system.System instance
    @param[in] ip IP address of the ctrlX CORE. Use "10.0.2.2" to connect to a ctrlX CORE virtual with port forwarding.
    @param[in] user Name of the user.
    @param[in] password Password of the user.
    @param[in] ssl_port Port number for a SSL connection. ctrlX CORE virtual with port forwarding: Use the host port (default 8443) forwarded to port 22 of the ctrlX virtual.
    @returns tuple  (provider, connection_string)
    @return <provider>, a ctrlxdatalayer.provider.Provider instance or None if failed,
    @return <connection_string>, a connection string or None if failed
    """
    connection_string = get_connection_string(
        ip, user, password, ssl_port)
    provider = system.factory().create_provider(connection_string)
    if (provider.start() == ctrlxdatalayer.variant.Result.OK) & provider.is_connected():
        return provider, connection_string
    provider.close()

    return None, connection_string

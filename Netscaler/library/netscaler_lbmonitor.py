DOCUMENTATION = '''
---
module: netscaler_lbmonitor
short_description: Manages Monitor resources and attributes
description:
  - Manages Netscaler Monitor configurations using Nitro API.
options:
  host:
    description:
      - The Netscaler's Address.
    required: true
    type: str
  partition:
    description:
      - The Netscaler's partition if not the "default" partition.
    required: false
    type: str
  password:
    description:
      - The password associated with the username account.
    required: false
    type: str
  port:
    description:
      - The TCP port used to connect to the Netscaler if other than the default used by the transport
        method(http=80, https=443).
    required: false
    type: int
  provider:
    description:
      - Dictionary which acts as a collection of arguments used to define the characteristics
        of how to connect to the device.
      - Arguments hostname, username, and password must be specified in either provider or local param.
      - Local params take precedence, e.g. hostname is preferred to provider["hostname"] when both are specefied.
    required: false
    type: dict
  state:
    description:
      - The desired state of the specified object.
      - Absent will delete resource.
      - Present will create resource.
    required: false
    default: present
    type: str
    choices: ["absent", "present"]
  use_ssl:
    description:
      - Determines whether to use HTTPS(True) or HTTP(False).
    required: false
    default: True
    type: bool
  username:
    description:
      - The username used to authenticate with the Netscaler.
    required: true
    type: str
  validate_certs:
    description:
      - Determines whether to validate certs against a trusted certificate file (True), or accept all certs (False)
    required: false
    default: False
    type: bool
  custom_headers:
    description:
      - Custom headers to add to the monitor request
    required: false
    type: str
  ecv_recv:
    description:
      - String expected from the server for the service to be marked as UP.
      - Applicable to TCP-ECV, HTTP-ECV, and UDP-ECV monitors.
    aliases: ["recv"]
    required: false
    type: str
  ecv_send:
    description:
      - String to send to the service.
      - Applicable to TCP-ECV, HTTP-ECV, and UDP-ECV monitors.
    aliases: ["send"]
    required: false
    type: str
  http_request:
    description:
      - The request to send to the server
    required: false
    type: str
  least_response_time:
    description:
      - Calculate the least response times for bound services.
      - If this parameter is not enabled, the appliance does not learn the response times of the bound services.
      - Also used for LRTM load balancing.
    aliases: ["lrtm"]
    required: false
    type: str
    choices: ["enabled", "disabled"]
  monitor_dest_ip:
    description:
      - The IP address to monitor.
    required: false
    type: str
  monitor_name:
    description:
      - The name of the monitor
    required: true
    type: str
  monitor_password:
    description:
      - The password used to authenticate with the monitored service.
    required: false
    type: str
  monitor_dest_port:
    description:
      - The port to monitor on the server
    required: false
    type: int
  monitor_secondary_password:
    description:
      - A secondary password to authenticate with the monitored service
    required: false
    type: str
  monitor_state:
    description:
      - The resources desired activity.
      - Disabled marks it out of service.
      - Enabled marks it serviceable.
    required: false
    type: str
    choices: ["disabled", "enabled"]
  monitor_type:
    description:
      - The type of service to monitor
    required: false
    type: str
    choices: ["ping", "tcp", "http", "tcp-ecv", "http-ecv", "udp-ecv", "dns", "ftp", "ldns-ping", "ldns-tcp",
              "ldns-dns", "radius", "user", "http-inline", "sip-udp", "sip-tcp", "load", "ftp-extended", "smtp",
              "snmp", "nntp", "mysql", "mysql-ecv", "mssql-ecv", "oracle-ecv", "ldap", "pop3", "citrix-xml-service",
              "citrix-web-interface", "dns-tcp", "rtsp", "arp", "citrix-ag", "citrix-aac-loginpage", "citrix-aac-las",
              "citrix-xd-ddc", "nd6", "citrix-wi-extended", "diameter", "radius_accounting", "storefront", "appc",
              "smpp", "citrix-xnc-ecv", "citrix-xdm"]
  monitor_use_ssl:
    description:
      - Specifies to use SSL for the monitor
    required: false
    type: str
    choices: ["yes", "no"]
  monitor_username:
    description:
      - The username used to authenticate with the monitored service.
    required: false
    type: str
  probe_interval:
    description:
      - Time interval between two successive probes.
      - Must be greater than the value of C(probe_timeout).
    aliases: ["interval"]
    required: false
    type: int
  probe_retries:
    description:
      - Maximum number of probes to send to establish the state of a service for which a monitoring probe failed.
      - Minimum value = 1
      - Maximum value = 127
    aliases: ["retries"]
    required: false
    type: int
  probe_timeout:
    description:
      - Amount of time for which the appliance must wait before it marks a probe as FAILED.
      - Must be less than the value of C(probe_interval).
      - Minimum value = 1
      - Maximum value = 20939
    aliases: ["resptimeout"]
    required: false
    type: int
  response_code:
    description:
      - The HTTP response code expected back from the monitored resource.
    required: false
    type: str
  response_code_action:
    description:
      - The action to take for response code items that differ from existing response codes.
      - add will add any missing values to the existing response codes.
      - remove will remove any matching values to the existing response codes.
    required: false
    type: str
    default: add
    choices: ["add", "remove"]
'''

EXAMPLES = '''
- name: Config Monitor
  netscaler_lbmonitor:
    host: "{{ inventory_hostname }}"
    username: "{{ username }}"
    password: "{{ password }}"
    monitor_name: "monitor_app01"
    monitor_type: "http"
    monitor_use_ssl: "yes"
    monitor_username: "user"
    monitor_password: "password"
    http_request: "HEAD /monitorcheck.html"
    response_code: "200-202"
- name: Remove Response Code
    host: "{{ inventory_hostname }}"
    username: "{{ username }}"
    password: "{{ password }}"
    monitor_name: "monitor_app01"
    response_code: "202"
    response_code_action: "remove"
- name: Config Monitor in Lab Partition
  netscaler_lbmonitor:
    host: "{{ inventory_hostname }}"
    username: "{{ username }}"
    password: "{{ password }}"
    monitor_name: "monitor_lab01"
- name: Delete Monitor
  netscaler_lbmonitor:
    host: "{{ inventory_hostname }}"
    username: "{{ username }}"
    password: "{{ password }}"
    state: "deleted"
    monitor_name: "monitor_app01"
    validate_certs: True
'''

RETURN = '''
existing:
    description: The existing configuration for the monitor (uses monitor_name) before the task executed.
    returned: always
    type: dict
    sample: {"httprequest": "HEAD /monitorcheck.html", "monitorname": "monitor_app01", "respcodes": ["200-202"],
             "secure": "YES", "state": "ENABLED", "type": "HTTP"}
config:
    description: The configuration that was pushed to the Netscaler.
    returned: always
    type: list
    sample:[{"method": "post", "url": "https://netscaler/nitro/v1/config/lbmonitor",
            "body": {"monitorname": "monitor_app02", "type": "TCP", "destport": 22, "state": "ENABLED"}}]
logout:
    description: The result from closing the session with the Netscaler. True means successful logout; False means unsuccessful logout.
    returned: always
    type: bool
    sample: True
'''


import requests
from ansible.module_utils.basic import AnsibleModule, env_fallback, return_values

requests.packages.urllib3.disable_warnings()


class Netscaler(object):
    """
    This is the Base Class for Netscaler modules. All methods common across several Netscaler Classes should be defined
    here and inherited by the sub-class.
    """

    def __init__(self, host, user, passw, use_ssl=True, verify=False, api_endpoint="", **kwargs):
        """
        :param host: Type str.
                     The IP or resolvable hostname of the Netscaler.
        :param user: Type str.
                     The username used to authenticate with the Netscaler.
        :param passw: Type str.
                      The password associated with the user account.
        :param use_ssl: Type bool.
                        The default is True, which uses HTTPS instead of HTTP.
        :param verify: Type bool.
                       The default is False, which does not verify the certificate against the list of trusted
                       certificates.
        :param api_endpoint: Type str.
                             The API endpoint used for a particular configuration section.
        :param headers: Type dict.
                        The headers to include in HTTP requests.
        :param kwargs: Type dict. Currently supports port.
        :param port: Type str.
                     Passing the port parameter will override the default HTTP(S) port when making requests.
        """
        self.host = host
        self.user = user
        self.passw = passw
        self.verify = verify
        self.api_endpoint = api_endpoint
        self.headers = {"Content-Type": "application/json"}
        if "port" not in kwargs:
            self.port = ""
        else:
            self.port = ":{}".format(kwargs["port"])

        if use_ssl:
            self.url = "https://{lb}{port}/nitro/v1/config/".format(lb=self.host, port=self.port)
            self.stat_url = "https://{lb}{port}/nitro/v1/stat/".format(lb=self.host, port=self.port)
        else:
            self.url = "http://{lb}{port}/nitro/v1/config/".format(lb=self.host, port=self.port)
            self.stat_url = "http://{lb}{port}/nitro/v1/stat/".format(lb=self.host, port=self.port)

    def change_name(self, existing_name, proposed_name):
        """
        The purpose of this method is to change the name of a server object.
        :param existing_name: Type str.
                              The name of the server object to be renamed.
        :param proposed_name: Type str.
                              The new name of the server object.
        :return: The response from the request to delete the object.
        """
        url = self.url + self.api_endpoint + "?action=rename"
        body = {self.api_endpoint: {"name": existing_name, "newname":proposed_name}}
        response = self.session.post(url, json=body, headers=self.headers, verify=self.verify)

        return response

    def change_state(self, object_name, state):
        """
        The purpose of this method is to change the state of an object from either disabled to enabled, or enabled to
        disabled. This method assumes the object is referenced by "name." This is the most common reference key, but not
        universal; where the Nitro API uses another key, an overriding method must be created in the sub-class.
        :param object_name: Type str.
                            The name of the object to be deleted.
        :param state: Type str.
                      The state the object should be in after execution. Valid values are "enable" or "disable"
        :return: The response from the request to delete the object.
        """
        url = self.url + self.api_endpoint + "?action={}".format(state)
        body = {self.api_endpoint: {"name": object_name}}
        response = self.session.post(url, json=body, headers=self.headers, verify=self.verify)

        return response

    def config_delete(self, module, object_name):
        """
        This method is used to handle the logic for Ansible modules when the "state" is set to "absent." The
        delete_config method is used to delete the object from the Netscaler.
        :param module: The AnsibleModule instance started by the task.
        :param object_name: Type str.
                            The name of the object to be deleted.
        :return: The config dict corresponding to the config returned by the Ansible module.
        """
        config = []

        if not module.check_mode:
            config_status = self.delete_config(object_name)
            if config_status.ok:
                config.append({"method": "delete", "url": config_status.url, "body": {}})
            else:
                logout = self.logout()
                module.fail_json(msg="Unable to Delete Object", netscaler_response=config_status.json(), logout=logout.ok)
        else:
            url = self.url + self.api_endpoint + "/" + object_name
            config.append({"method": "delete", "url": url, "body": {}})

        return config

    def config_new(self, module, new_config):
        """
        This method is used to handle the logic for Ansible modules when the "state" is set to "present" and the
        proposed config is a new object. The post_config method is used to post the object's configuration to the
        Netscaler.
        :param module: The AnsibleModule instance started by the task.
        :param new_config: Type dict.
                           The configuration to send to the Nitro API.
        :return: A list with config dictionary corresponding to the config returned by the Ansible module.
        """
        config = []

        if not module.check_mode:
            config_status = self.post_config(new_config)
            if config_status.ok:
                config.append({"method": "post", "url": config_status.url, "body": new_config})
            else:
                logout = self.logout()
                module.fail_json(msg="Unable to Add New Object", netscaler_response=config_status.json(), logout=logout.ok)
        else:
            config.append({"method": "post", "url": self.url + self.api_endpoint, "body": new_config})

        return config

    def config_rename(self, module, existing_name, proposed_name):
        """
        This method is used to handle the logic for Ansible modules when the "state" is set to "present" and the
        proposed IP Address matches the IP Address of another Server in the same Traffic Domain. The change_name
        method is used to post the configuration to the Netscaler.
        :param module: The AnsibleModule instance started by the task.
        :param existing_name: Type str.
                              The current name of the Server object to be changed.
        :param proposed_name: Type str.
                              The name the Server object should be changed to.
        :return: A list with config dictionary corresponding to the config returned by the Ansible module.
        """
        config = []

        rename_config = {"name": existing_name, "newname": proposed_name}

        if not module.check_mode:
            config_status = self.change_name(existing_name, proposed_name)
            if config_status.ok:
                config.append({"method": "post", "url": config_status.url, "body": rename_config})
            else:
                logout = self.logout()
                module.fail_json(msg="Unable to Rename Object", netscaler_response=config_status.json(), logout=logout.ok)
        else:
            config.append({"method": "post", "url": self.url + self.api_endpoint + "?action=rename", "body": rename_config})

        return config

    def config_update(self, module, update_config):
        """
        This method is used to handle the logic for Ansible modules when the "state" is set to "present" and the
        proposed config modifies an existing object. If the object's state needs to be updated, the "state" key,value is
        popped from the update_config in order to prevent it from being included in a config update when there are
        updates besides state change. The change_state method is then used to modify the object's state. After the
        object's state matches the proposed state, a check is done to see if the update_config has any keys other than
        the "name" key (len > 1). If there are more updates to make, the put_config method is used to push those to the
        Netscaler. Note that this method uses the common "name" key to input to the change_state method; if the API
        Endpoint uses a different key, then an overriding method must be created in the sub-class.
        :param module: The AnsibleModule instance started by the task.
        :param update_config: Type dict.
                              The configuration to send to the Nitro API.
        :return: The list of config dictionaries corresponding to the config returned by the Ansible module.
        """
        config = []

        if "state" in update_config:
            config_state = update_config.pop("state")[:-1].lower()
            if not module.check_mode:
                config_status = self.change_state(update_config["name"], config_state)
                if config_status.ok:
                    config.append({"method": "post", "url": config_status.url, "body": {"name": update_config["name"]}})
                else:
                    logout = self.logout()
                    module.fail_json(msg="Unable to Change Object's State", netscaler_response=config_status.json(), logout=logout.ok)
            else:
                url = self.url + self.api_endpoint + "?action={}".format(config_state)
                config.append({"method": "post", "url": url, "body": {"name": update_config["name"]}})

        if len(update_config) > 1:
            if not module.check_mode:
                config_status = self.put_update(update_config)
                if config_status.ok:
                    config.append({"method": "put", "url": self.url, "body": update_config})
                else:
                    logout = self.logout()
                    module.fail_json(msg="Unable to Update Config", netscaler_response=config_status.json(), logout=logout.ok)
            else:
                config.append({"method": "put", "url": self.url, "body": update_config})

        return config

    def delete_config(self, object_name):
        """
        The purpose of this method is to remove an object from the Netscaler's configuration. Currently no checks are
        made to verify if the object is bound to another item.
        :param object_name: Type str.
                            The name of the object to be deleted.
        :return: The response from the request to delete the object.
        """
        url = self.url + self.api_endpoint + "/" + object_name
        response = self.session.delete(url, headers=self.headers, verify=self.verify)

        return response

    def get_all(self, api_endpoint):
        """
        The purpose of this method is to retrieve every object's configuration for the API endpoint.
        :param api_endpoint: Type str.
                             The API endpoint to use for data collection.
        :return: A list of configuration dictionaries returned by they Nitro API. An empty list means that their are
                 currently no objects configured, or the request was unsuccessful.
        """
        response = self.session.get(self.url + api_endpoint, headers=self.headers, verify=self.verify)

        return response.json().get(api_endpoint, [])

    def get_all_attrs(self, api_endpoint, attrs_list):
        """
        The purpose of this method is to retrieve every object's configuration for the API endpoint, but the
        collected data is restricted to the attributes in the attrs_list argument.
        :param api_endpoint: Type str.
                             The API endpoint to use for data collection.
        :param attrs_list: Type list,tuple
                           The list of attributes used to limit the scope of returned config data.
        :return: A list of configuration dictionaries returned by they Nitro API. An empty list means that their are
                 currently no objects configured, or the request was unsuccessful.
        """
        attrs = "?attrs=" + ",".join(attrs_list)
        url = self.url + api_endpoint + attrs

        response = self.session.get(url, headers=self.headers, verify=self.verify)

        return response.json().get(api_endpoint, [])

    def get_config(self, defaults="false"):
        """
        This method retrieves the running configuration from the Netscaler.
        :param defaults: Type str.
                         The default setting will retrieve configurations that do not have their default setting.
                         Setting this to "true" will retrieve the full configuration including defaults.
        :return: The configuration of the Netscaler as a str. An empty str is returned if the request is unsuccessful.
        """
        url = self.url + "nsrunningconfig?args=withdefaults:{}".format(defaults)
        response = self.session.get(url, headers=self.headers, verify=self.verify)

        return response.json().get("nsrunningconfig", {"response": ""})["response"]

    @staticmethod
    def get_diff(proposed, existing):
        """
        This method is used to compare the proposed config with what currently exists on the Netscaler. Note that thi
        method uses the most common key used by Nitro, "name." Where Nitro uses a different key, the corresponding class
        must have an overriding method.
        :param proposed: Type dict.
                         A dictionary corresponding to the proposed configuration item. The dictionary must have a
                         "name" key.
        :param existing: Type dict.
                         A dictionary corresponding to the existing configuration for the object. This can be retrieved
                         using the get_existing_attrs method.
        :return: A tuple indicating whether the config is a new object, will update an existing object, or make no
                 changes, and a dict that corresponds to the body of a config request using the Nitro API.
        """
        diff = dict(set(proposed.items()).difference(existing.items()))

        if diff == proposed:
            return "new", diff
        elif diff:
            diff["name"] = proposed["name"]
            return "update", diff
        else:
            return "none", {}

    def get_existing_attrs(self, object_name, attrs):
        """
        This method is used to get a subset of a particular object's configuration for the given API Endpoint
        (configuration section). The configuration will be scoped to the list of values in attrs.
        :param object_name: Type str.
                            The name of the object.
        :param attrs: Type list.
                      The list of attributes to retrieve from the configuration.
        :return: A dictionary of the object's configuration. If the object doesn't exist or the request fails, then an
        empty dict is returned. Unexpected empty lists are likely caused by a mistyped API endpoint or an expired
        session.
        """
        attributes = ",".join(attrs)
        url = self.url + self.api_endpoint + "/" + object_name + "?attrs=" + attributes
        response = self.session.get(url, headers=self.headers, verify=self.verify)

        return response.json().get(self.api_endpoint, [{}])[0]

    def get_hardware(self):
        """
        This method is used to retrieve basic hardware information about the Netscaler.
        :return: A dictionary of hardware information. An empty dictionary is returned if the request is unsuccessful.
        """
        response = self.session.get(self.url + "nshardware", headers=self.headers, verify=self.verify)

        return response.json().get("nshardware", {})

    def get_hostname(self):
        """
        This method is used to retrieve the hostname of the connected Netscaler
        :return: A dictionary of the hostname configuration. An empty dictionary is returned if the API request failed.
        """
        response = self.session.get(self.url + "nshostname", headers=self.headers, verify=self.verify)

        return response.json().get("nshostname", [{}])[0]

    def get_interfaces(self):
        """
        This method is used to get the interfaces and their stats from the Netscaler.
        :return: A list of interface dictionaries containing configuration and statistical info. An empty list is
                 returned if the request is unsuccessful.
        """
        response = self.session.get(self.url + "interface", headers=self.headers, verify=self.verify)

        return response.json().get("Interface", [])

    def get_lbvserver_stats(self):
        """
        This method is used to get the lbvserver statistical info for all vservers on the Netscaler.
        :return: A list of dictionaries for all statistical data for the lbvservers. An empty dictionary is returned if
                 the request is unsuccessful.
        """
        response = self.session.get(self.stat_url + "lbvserver", headers=self.headers, verify=self.verify)

        return response.json().get("lbvserver", [])

    def get_nsconfig(self):
        """
        This method is used to get the nsconfig data from the Netscaler.
        :return: A dictionary of the nsconfig data. An empty dictionary is returned if the request is unsuccessful.
        """
        response = self.session.get(self.url + "nsconfig", headers=self.headers, verify=self.verify)

        return response.json().get("nsconfig", {})

    def get_state(self, object_name):
        """
        This method is used to retrieve the current state of the object. The possibilities are enabled or disabled.
        :param object_name: Type str.
                            The name of the object.
        :return: A str representing the current state of the object. An empty string is returned when the object does
                 not exist.
        """
        url = self.url + self.api_endpoint + object_name + "attrs=state"
        response = self.session.get(url, headers=self.headers, verify=self.verify)

        return response.json().get(self.api_endpoint, [{"state": ""}])[0]["state"]

    def get_system(self):
        """
        This method is used to retrieve the system or environment statistics from the Netscaler.
        :return: A dictionary of the systems statistics (fans, memory, cpu, temp, disk space). An empty dictionary is
        returned if the request is unsuccessful.
        """
        response = self.session.get(self.stat_url + "system", headers=self.headers, verify=self.verify)

        return response.json().get("system", {})

    def login(self):
        """
        The login method is used to establish a session with the Netscaler. All necessary parameters need to be
        established at class instantiation. The requests Session class is used to maintain session consistency for all
        subsequent requests. The Session class automatically stores the cookie returned from the login request, and
        passes the cookie on all requests after a successful login. This is important when using partitions since the
        Netscaler API (Nitro) does not support modifying partitions using basic auth. Note that using partitions still
        requires calling the switch_partition function; these are separated so as to separate the failure domains.
        :return: The response from the login request. A successful login also sets the instance session.
        """
        url = self.url + "login"
        body = {"login": {"username": self.user, "password": self.passw}}
        session = requests.Session()
        login = session.post(url, json=body, headers=self.headers, verify=self.verify)

        if login.ok:
            self.session = session

        return login

    def logout(self):
        """
        The logout method is used to close the established connection with the Netscaler device.
        :return: The response from the logout request.
        """
        url = self.url + "logout"
        body = {"logout": {}}
        logout = self.session.post(url, json=body, headers=self.headers, verify=self.verify)

        return logout

    def post_config(self, new_config):
        """
        This method is used to submit a configuration request to the Netscaler using the Nitro API.
        :param new_config: Type dict:
                           The new configuration item to be sent to the Netscaler. It is expected that you use the
                           get_diff method to generate the new_config data.
        :return: The response from the request to add the configuration.
        """
        url = self.url + self.api_endpoint
        body = {self.api_endpoint: new_config}
        response = self.session.post(url, json=body, headers=self.headers, verify=self.verify)

        return response

    def put_update(self, update_config):
        """
        This method is used to update the configuration of an existing item on the Netscaler.
        :param update_config: Type dict:
                              The configuration item to be sent to the Netscaler in order to update existing object. It
                              is expected that you use the get_diff method to generate the update_config data.
        :return: The response from the request to add the configuration.
        """
        url = self.url + self.api_endpoint
        body = {self.api_endpoint: update_config}
        response = self.session.put(url, json=body, headers=self.headers, verify=self.verify)

        return response

    def save_config(self):
        """
        This method is used to save the config of the Netscaler.
        :return: The response from the request to save the config.
        """
        url = self.url + "nsconfig?action=save"
        response = self.session.post(url, json={"nsconfig": {}}, headers=self.headers, verify=self.verify)

        return response

    def switch_partition(self, partition):
        """
        This method will switch from the default partition to the specified partition.
        :param partition: Type str.
                          The partition to interact with for all subsequent requests.
        :return: The response from the request to switch partitions.
        """
        url = self.url + "nspartition?action=Switch"
        body = {"nspartition": {"partitionname": partition}}
        switch = self.session.post(url, json=body, headers=self.headers, verify=self.verify)

        return switch

    @staticmethod
    def validate_ip(ip_address):
        """
        This method is used to validate that an IPv4 Address has 4 octets and that each octet is an int from 0 to 255.
        Note, "0.0.0.0" is a valid IP.
        :param ip_address: Type str.
                           An IPv4 address.
        :return: A valid IP returns True; otherwise, False.
        """
        octet_split = ip_address.split(".")
        if len(octet_split) != 4:
            return False

        for octet in octet_split:
            try:
                int_octet = int(octet)
            except ValueError:
                return False

            if 0 > int_octet or 255 < int_octet:
                return False

        return True


class LBMonitor(Netscaler):
    """
    This is the class used for interacting with the "lbvserver" API endpoint. In addition to server specific methods,
    the api endpoint default value is set to "lbvserver."
    """

    def __init__(self, host, user, passw, secure=True, verify=False, api_endpoint="lbmonitor", **kwargs):
        super(LBMonitor, self).__init__(host, user, passw, secure, verify, api_endpoint, **kwargs)

    @staticmethod
    def concatenate_resp_codes(response_codes):
        """
        The purpose of this method is to concatenate a list of response codes to their most concise string
        representation. The Netscaler API will only accept a limited number of response codes per request, so this will
        transform consecutive numbers into a "range" string. For example, [200, 201, 202, 205, 207, 208, 209, 210] will
        become ["200-202", "205", "207-210"].
        :param response_codes: Type list.
                               A list of individual response codes of type int.
        :return: A list of concise response codes of type str.
        """
        short_respcodes = []
        counter = 0
        for code in response_codes:
            if counter == len(response_codes) or code < response_codes[counter]:
                continue
            else:
                counter += 1
                start = code
                end = code
                if counter == len(response_codes) or end != response_codes[counter] - 1:
                    short_respcodes.append(str(start))
                else:
                    while counter < len(response_codes) and end == response_codes[counter] - 1:
                        end = response_codes[counter]
                        counter += 1
                    short_respcodes.append(str(start) + "-" + str(end))

        return short_respcodes

    def config_delete(self, module, object_name, monitor_type):
        """
        This method is used to handle the logic for Ansible modules when the "state" is set to "absent." The
        delete_config method is used to delete the object from the Netscaler.
        :param module: The AnsibleModule instance started by the task.
        :param object_name: Type str.
                            The name of the object to be deleted.
        :param monitor_type: Type str.
                             The monitor type of the existing monitor.
        :return: The config dict corresponding to the config returned by the Ansible module.
        """
        config = []

        if not module.check_mode:
            config_status = self.delete_config(object_name, monitor_type)
            if config_status.ok:
                config.append({"method": "delete", "url": config_status.url, "body": {}})
            else:
                logout = self.logout()
                module.fail_json(msg="Unable to Delete Object", netscaler_response=config_status.json(), logout=logout.ok)
        else:
            url = self.url + self.api_endpoint + "?args=monitorname:{},type:{}".format(object_name, monitor_type)
            config.append({"method": "delete", "url": url, "body": {}})

        return config

    def config_update(self, module, update_config):
        """
        This method is used to handle the logic for Ansible modules when the "state" is set to "present" and the
        proposed config modifies an existing monitor object.
        :param module: The AnsibleModule instance started by the task.
        :param update_config: Type dict.
                              The configuration to send to the Nitro API.
        :return: The config dict corresponding to the config returned by the Ansible module.
        """
        config = []

        if not module.check_mode:
            config_status = self.put_update(update_config)
            if config_status.ok:
                config.append({"method": "put", "url": self.url, "body": update_config})
            else:
                logout = self.logout()
                module.fail_json(msg="Unable to Update Config", netscaler_response=config_status.json(), logout=logout.ok)
        else:
            config.append({"method": "put", "url": self.url, "body": update_config})

        return config

    def delete_config(self, object_name, monitor_type):
        """
        The purpose of this method is to remove an object from the Netscaler's configuration. Currently no checks are
        made to verify if the object is bound to another item.
        :param object_name: Type str.
                            The name of the object to be deleted.
        :param monitor_type: Type str.
                             The monitor type of the existing monitor.
        :return: The response from the request to delete the object.
        """
        url = self.url + self.api_endpoint + "?args=monitorname:{},type:{}".format(object_name, monitor_type)
        response = self.session.delete(url, headers=self.headers, verify=self.verify)

        return response

    @staticmethod
    def expand_resp_codes(response_codes):
        """
        The purpose of this function is to expand a list of response codes so that each code is represented as a number
        instead of a summarized range such as "200-202." This is useful for doing a diff between two groups of response
        codes. For example, "202-204" won't diff properly with "200-205," so you will need to expand them to a list of
        individual codes. This function would return [202, 201, 202] and [200, 201, 202, 203, 204, 205] respectively.
        :param response_codes: Type list.
                               The respoonse codes that need to be expanded.
        :return: A set of the expanded response codes that can be used for comparison.
        """
        respcode_set = set()
        for code in response_codes:
            if "-" not in code:
                respcode_set.add(int(code))
            else:
                codes = code.split("-")
                code_range = range(int(codes[0]), int(codes[1]) + 1)
                for single_code in code_range:
                    respcode_set.add(single_code)

        return respcode_set

    def get_all(self):
        """
        The purpose of this method is to retrieve every object's configuration for the instance's API endpoint.
        :return: A list of configuration dictionaries returned by they Nitro API. An empty list means that their are
                 currently no objects configured, or the request was unsuccessful.
        """
        response = self.session.get(self.url + self.api_endpoint, headers=self.headers, verify=self.verify)

        return response.json().get(self.api_endpoint, [])

    def get_all_attrs(self, attrs_list):
        """
        The purpose of this method is to retrieve every object's configuration for the instance's API endpoint, but the
        collected data is restricted to the attributes in the attrs_list argument.
        :param attrs_list: Type list,tuple
                           The list of attributes used to limit the scope of returned config data.
        :return: A list of configuration dictionaries returned by they Nitro API. An empty list means that their are
                 currently no objects configured, or the request was unsuccessful.
        """
        attrs = "?attrs=" + ",".join(attrs_list)
        url = self.url + self.api_endpoint + attrs

        response = self.session.get(url, headers=self.headers, verify=self.verify)

        return response.json().get(self.api_endpoint, [])

    @staticmethod
    def get_diff(proposed, existing, respcode_action):
        """
        This method is used to compare the proposed config with what currently exists on the Netscaler. If "respcode"
        is in existing, then it will be popped and compared separately since it is a list. Netscaler requires the
        type to be included in the update requests, so mismatched types are captured here and type is added back to
        valid update requests.
        :param proposed: Type dict.
                         A dictionary corresponding to the proposed configuration item. The dictionary must have a
                         "name" key.
        :param existing: Type dict.
                         A dictionary corresponding to the existing configuration for the object. This can be retrieved
                         using the get_exsiting_attrs method.
        :param respcode_action: Type str.
                       The key to determine what to do with the proposed list of response codes. Add will add to an
                       existing list, and remove will remove them from the existing list if they are there.
        :return: A tuple indicating whether the config is a new object, will update an existing object, or make no
                 changes, and a dict that corresponds to the body of a config request using the Nitro API.
        """
        # response codes are a list and need to be popped for diff to work
        if "respcode" in proposed:
            proposed_respcode_list = proposed.pop("respcode")
            proposed_respcode_set = LBMonitor.expand_resp_codes(proposed_respcode_list)

            existing_respcode_list = existing.pop("respcode", [])
            existing_respcode_set = LBMonitor.expand_resp_codes(existing_respcode_list)

            if respcode_action == "add" and proposed_respcode_set.difference(existing_respcode_set):
                respcodes = list(proposed_respcode_set.union(existing_respcode_set))
                respcodes.sort()
            elif respcode_action == "remove" and existing_respcode_set.intersection(proposed_respcode_set):
                respcodes = list(existing_respcode_set.difference(proposed_respcode_set))
                respcodes.sort()
            else:
                respcodes = []

            short_respcodes = LBMonitor.concatenate_resp_codes(respcodes)

            diff = dict(set(proposed.items()).difference(existing.items()))

        else:
            existing_respcode_list = existing.pop("respcode", [])
            diff = dict(set(proposed.items()).difference(existing.items()))
            short_respcodes = []

        # add existing reponse codes back to exsiting since it was popped for diff
        if existing_respcode_list:
            existing["respcodes"] = existing_respcode_list

        # handle new config
        if diff == proposed:
            if short_respcodes:
                proposed["respcode"] = short_respcodes
                return "new", proposed
            else:
                return "new", proposed
        # handle invalid diffs
        elif "type" in diff:
            return "mismatch", {"proposed_monitor": proposed["type"], "existing_monitor": existing["type"]}
        # handle update config with response codes
        elif diff and short_respcodes:
            diff["monitorname"] = proposed["monitorname"]
            diff["type"] = existing["type"]
            diff["respcode"] = short_respcodes
            return "update", diff
        # handle update without short response codes
        elif diff:
            diff["monitorname"] = proposed["monitorname"]
            diff["type"] = existing["type"]
            return "update", diff
        # handle update of only response codes
        elif short_respcodes:
            diff["monitorname"] = proposed["monitorname"]
            diff["type"] = existing["type"]
            diff["respcode"] = short_respcodes
            return "update", diff
        # handle no diff
        else:
            return "none", {}


ENABLED_DISABLED = ["ENABLED", "DISABLED", "enabled", "disabled"]
VALID_TYPES = ["PING", "TCP", "HTTP", "TCP-ECV", "HTTP-ECV", "UDP-ECV", "DNS", "FTP", "LDNS-PING", "LDNS-TCP",
               "LDNS-DNS", "RADIUS", "USER", "HTTP-INLINE", "SIP-UDP", "SIP-TCP", "LOAD", "FTP-EXTENDED", "SMTP",
               "SNMP", "NNTP", "MYSQL", "MYSQL-ECV", "MSSQL-ECV", "ORACLE-ECV", "LDAP", "POP3", "CITRIX-XML-SERVICE",
               "CITRIX-WEB-INTERFACE", "DNS-TCP", "RTSP", "ARP", "CITRIX-AG", "CITRIX-AAC-LOGINPAGE", "CITRIX-AAC-LAS",
               "CITRIX-XD-DDC", "ND6", "CITRIX-WI-EXTENDED", "DIAMETER", "RADIUS_ACCOUNTING", "STOREFRONT", "APPC",
               "SMPP", "CITRIX-XNC-ECV", "CITRIX-XDM", "ping", "tcp", "http", "tcp-ecv", "http-ecv", "udp-ecv", "dns",
               "ftp", "ldns-ping", "ldns-tcp", "ldns-dns", "radius", "user", "http-inline", "sip-udp", "sip-tcp", "load",
               "ftp-extended", "smtp", "snmp", "nntp", "mysql", "mysql-ecv", "mssql-ecv", "oracle-ecv", "ldap", "pop3",
               "citrix-xml-service", "citrix-web-interface", "dns-tcp", "rtsp", "arp", "citrix-ag", "citrix-aac-loginpage",
               "citrix-aac-las", "citrix-xd-ddc", "nd6", "citrix-wi-extended", "diameter", "radius_accounting", "storefront",
               "appc", "smpp", "citrix-xnc-ecv", "citrix-xdm"]


def main():
    argument_spec = dict(
        host=dict(required=False, type="str"),
        port=dict(required=False, type="int"),
        username=dict(fallback=(env_fallback, ["ANSIBLE_NET_USERNAME"])),
        password=dict(fallback=(env_fallback, ["ANSIBLE_NET_PASSWORD"]), no_log=True),
        use_ssl=dict(required=False, type="bool"),
        validate_certs=dict(required=False, type="bool"),
        provider=dict(required=False, type="dict"),
        state=dict(choices=["absent", "present"], type="str"),
        partition=dict(required=False, type="str"),
        custom_headers=dict(required=False, type="str"),
        ecv_recv=dict(required=False, aliases=["recv"], type="str"),
        ecv_send=dict(required=False, aliases=["send"], type="str"),
        http_request=dict(required=False, type="str"),
        least_response_time=dict(choices=ENABLED_DISABLED, aliases=["lrtm"], required=False, type="str"),
        monitor_dest_ip=dict(required=False, type="str"),
        monitor_dest_port=dict(required=False, type="int"),
        monitor_name=dict(required=False, type="str"),
        monitor_password=dict(required=False, type="str", no_log=True),
        monitor_secondary_password=dict(required=False, type="str", no_log=True),
        monitor_state=dict(choices=ENABLED_DISABLED, required=False, type="str"),
        monitor_type=dict(choices=VALID_TYPES, required=False, type="str"),
        monitor_use_ssl=dict(choices=["YES", "NO", "yes", "no"], required=False, type="str"),
        monitor_username=dict(required=False, type="str"),
        probe_interval=dict(required=False, aliases=["interval"], type="int"),
        probe_retries=dict(required=False, aliases=["retries"], type="int"),
        probe_timeout=dict(required=False, aliases=["resptimeout"], type="int"),
        response_code=dict(required=False, type="list"),
        response_code_action=dict(choices=["add", "remove"], required=False, type="str")
    )

    module = AnsibleModule(argument_spec, supports_check_mode=True)
    provider = module.params["provider"] or {}

    no_log = ["password", "monitor_password", "monitor_secondary_password"]
    for param in no_log:
        if provider.get(param):
            module.no_log_values.update(return_values(provider[param]))

    # allow local params to override provider
    for param, pvalue in provider.items():
        if module.params.get(param) is None:
            module.params[param] = pvalue

    # module specific args that can be represented as both str or int are normalized to Netscaler's representation for diff comparison in case provider is used
    host = module.params["host"]
    partition = module.params["partition"]
    password = module.params["password"]
    port = module.params["port"]
    state = module.params["state"]
    if not state:
        state = "present"
    use_ssl = module.params["use_ssl"]
    if use_ssl is None:
        use_ssl = True
    username = module.params["username"]
    validate_certs = module.params["validate_certs"]
    if validate_certs is None:
        validate_certs = False
    least_response_time = module.params["least_response_time"]
    if least_response_time:
        least_response_time = least_response_time.upper()
    monitor_dest_port = module.params["monitor_dest_port"]
    if monitor_dest_port:
        monitor_dest_port = int(monitor_dest_port)
    monitor_state = module.params["monitor_state"]
    if monitor_state:
        monitor_state = monitor_state.upper()
    monitor_type = module.params["monitor_type"]
    if monitor_type:
        monitor_type = monitor_type.upper()
    monitor_use_ssl = module.params["monitor_use_ssl"]
    if monitor_use_ssl:
        monitor_use_ssl = monitor_use_ssl.upper()
    probe_interval = module.params["probe_interval"]
    if probe_interval:
        probe_interval = int(probe_interval)
    probe_retries = module.params["probe_retries"]
    if probe_retries:
        probe_retries = int(probe_retries)
    probe_timeout = module.params["probe_timeout"]
    if probe_timeout:
        probe_timeout = int(probe_timeout)
    response_code = module.params["response_code"]
    if response_code and isinstance(response_code, list):
        response_code = [str(code).strip() for code in response_code]
    elif response_code and isinstance(response_code, str):
        response_code = [response_code.strip()]
    response_code_action = module.params["response_code_action"]
    if not response_code_action:
        response_code_action = "add"

    args = dict(
        customheaders=module.params["custom_headers"],
        destip=module.params["monitor_dest_ip"],
        destport=monitor_dest_port,
        httprequest=module.params["http_request"],
        interval = probe_interval,
        lrtm = least_response_time,
        monitorname=module.params["monitor_name"],
        password=module.params["monitor_password"],
        recv = module.params["ecv_recv"],
        respcode=response_code,
        resptimeout = probe_timeout,
        retries = probe_retries,
        secondarypassword=module.params["monitor_secondary_password"],
        secure=monitor_use_ssl,
        send = module.params["ecv_send"],
        state=monitor_state,
        type=monitor_type,
        username=module.params["monitor_username"]
    )

    # check for required values, this allows all values to be passed in provider
    argument_check = dict(host=host, monitor_name=args["monitorname"])
    for key, val in argument_check.items():
        if not val:
            module.fail_json(msg="The {} parameter is required".format(key))

    # "if isinstance(v, bool) or v" should be used if a bool variable is added to args
    proposed = dict((k, v) for k, v in args.items() if v == 0 or v)

    kwargs = dict()
    if port:
        kwargs["port"] = port

    session = LBMonitor(host, username, password, use_ssl, validate_certs, **kwargs)
    session_login = session.login()
    if not session_login.ok:
        module.fail_json(msg="Unable to Login", netscaler_response=session_login.json())

    if partition:
        session_switch = session.switch_partition(partition)
        if not session_switch.ok:
            session_logout = session.logout()
            module.fail_json(msg="Unable to Switch Partitions", netscaler_response=session_switch.json(), logout=session_logout.ok)

    existing_attrs = args.keys()
    existing = session.get_existing_attrs(proposed["monitorname"], existing_attrs)

    if state == "present":
        results = change_config(session, module, proposed, existing, response_code_action)
    else:
        results = delete_lbmonitor(session, module, proposed["monitorname"], existing)

    session_logout = session.logout()
    results["logout"] = session_logout.ok

    return module.exit_json(**results)


def change_config(session, module, proposed, existing, respcode_action):
    """
    The purpose of this function is to determine the appropriate configuration to push to the Netscaler. A new monitor
    object has the full configuration submitted from the Ansible task pushed to the Netscaler. Configuration changes to
    an existing monitor will only push the modifications to the Netscaler. This will also handle changing the monitor's
    "state" from either enabled or disabled if the state is currently different than specified in the task. Checks are
    made to ensure that attempts to change either the monitor's type raises an error, as this is not allowed by
    Netscaler.
    :param session: The Monitor instance that has an established session with the Netscaler.
    :param module: The AnsibleModule instance.
    :param proposed: Type dict.
                     The proposed configuration based on Ansible inputs.
    :param existing: Type dict.
                     A dictionary corresponding to the existing configuration for the object.
    :param respcode_action: Type str.
                            The keyword to determine what to do with variations between proposed and existing respcodes.
    :return: Returns a dictionary containing the module exit values.
    """
    changed = False
    config = []

    config_method, config_diff = session.get_diff(proposed, existing, respcode_action)
    if config_method == "new":
        changed = True
        config = session.config_new(module, config_diff)
    elif config_method == "update":
        changed = True
        config = session.config_update(module, config_diff)
    elif config_method == "mismatch":
        conflict = dict(existing_monitor_type=existing["type"], proposed__monitor_type=proposed["type"], partition=module.params["partition"])
        session_logout = session.logout()
        module.fail_json(msg="Modifying the Monitor Type is not Supported. This can be achieved by first deleting "
                             "the LB Monitor, and then creating a LB Monitor with the changes.", conflict=conflict, logout=session_logout.ok)

    return dict(changed=changed, config=config, existing=existing)


def delete_lbmonitor(session, module, proposed_name, existing):
    """
    The purpose of this function is to delete a monitor from the Netscaler. Checks are currently only done to ensure the
    object exists before submitting it for deletion. If the monitor is bound to a servicegroup, it will still be
    deleted.
    :param session: The Monitor instance that has an established session with the Netscaler.
    :param module: The AnsibleModule instance
    :param proposed_name: Type str.
                          The name of the proposed server to delete.
    :param existing: Type dict.
                     A dictionary corresponding to the existing configuration for the object.
    :return: Returns a dictionary containing the module exit values.
    """
    changed = False
    config = []

    if existing:
        changed = True
        config = session.config_delete(module, proposed_name, existing["type"])

    return dict(changed=changed, config=config, existing=existing)


if __name__ == "__main__":
    main()

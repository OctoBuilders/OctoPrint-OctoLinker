# coding=utf-8
from __future__ import absolute_import

import octoprint.plugin
import requests
import yaml

class OctolinkerPlugin(octoprint.plugin.StartupPlugin,
                       octoprint.plugin.EventHandlerPlugin):

    # ~~ StartupPlugin

    def on_after_startup(self):
        """
        Not used.
        """
        pass

    def on_startup(self, host, port):
        """
        Used to tell OctoLink that the printer is online, and pass
        its API key
        """
        try:
            key = {'key': 'none'}

            with open("/home/tom/.octoprint/config.yaml", 'r') as stream:
                yml = yaml.load(stream)
                key = yml['api']

            requests.post("http://127.0.0.1:5001/printers", json=key)
            self._logger.info("Posted self to OctoLink")

        except requests.exceptions.ConnectionError:
            self._logger.info("Not connected to OctoLink: Could not connect.")
        except FileNotFoundError:
            self._logger.info("Not connected to OctoLink: Could not read config file.")



    # ~~ EventHandlerPlugin

    def on_event(self, event, payload):
        """
        Used to catch the `PrintDone` Event.
        """
        if (event =='PrintDone'):
            payload = {'status': event, 'message': 'Print is complete'}
            try:
                requests.post('http://127.0.0.1:5001/print_status', json=payload)
                self._logger.info("Posted PrintDone to OctoLink.")

            except requests.exceptions.ConnectionError:
                self._logger.info("Not post status to OctoLink: Could not connect.")


        if (event == 'PrintCancelled'):
            payload = {'status': event, 'message': 'Print was canceled'}
            try:
                requests.post('http://127.0.0.1:5001/print_status', json=payload)
                self._logger.info("Posted PrintCancelled to OctoLink.")

            except requests.exceptions.ConnectionError:
                self._logger.info("Not post status to OctoLink: Could not connect.")



__plugin_name__ = "OctoLinker Plugin"
__plugin_implementation__ = OctolinkerPlugin()

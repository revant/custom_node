# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from frappe import _

def get_data():
	return [
		{
			"module_name": "Custom Node",
			"color": "red",
			"icon": "octicon octicon-file-directory",
			"type": "module",
			"label": _("Custom Node")
		}
	]

# This file is part of gusic.

# gusic is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# gusic is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with gusic.  If not, see <http://www.gnu.org/licenses/>.
#
# Copyright 2012-2013, Stijn Van Campenhout <stijn.vancampenhout@gmail.com>

from gi.repository import GnomeKeyring as gk
class keyring(object):
	def __init__(self):
		self.loginDetails = False
		if gk.is_available() is True:
			if "Gusic" in gk.list_keyring_names_sync()[1]:
				self.keyring = gk.list_item_ids_sync("Gusic")[1]

				self.loginDetails = self._get_first_key("Gusic")
				

			else:
				gk.create_sync("Gusic","Gusic")
	def haveLoginDetails(self):
		if self.loginDetails == False:
			return False
		else:
			return True

	def _find(self,displayName,keyring):
		item_keys = gk.list_item_ids_sync(keyring)
		for k in item_keys[1]:
			item_info = gk.item_get_info_sync(keyring,k)
			if item_info.get_display_name() == displayName:
				return (k,item_info.get_display_name(),item_info.get_secret())
		return False
	def _get_first_key(self,keyring):
		item_keys = gk.list_item_ids_sync(keyring)
		if len(item_keys[1]) > 0:
			item_info = gk.item_get_info_sync(keyring,item_keys[1][0])
			return (item_info[1].get_display_name(),item_info[1].get_secret())
		else:
			return False
		
	def getLoginDetails():
		return self.loginDetails
	def saveLoginDetails(self,user,password):
		atts = gk.Attribute.list_new()
		gk.Attribute.list_append_string(atts,'useWith','Gusic')
		gk.Attribute.list_append_string(atts,'user',user)

		key = gk.item_create_sync('Gusic',0,user,atts,password, True)
	def getLoginDetails():
		return self.loginDetails()

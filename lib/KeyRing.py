# This file is part of google-music.

# google-music is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# google-music is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with google-music.  If not, see <http://www.gnu.org/licenses/>.
#
# Copyright 2012-2013, Stijn Van Campenhout <stijn.vancampenhout@gmail.com>

from gi.repository import gnomeKeyring as gk
class keyring(object):
	def __init__(self):
		if gk.is_available() is True:
			if "GoogleMusic" in gk.list_keyring_names_sync():
				self.keyring = gk.list_item_ids_sync("GoogleMusic")[1]
				if "loginDetails" in self.keyring:
					self.loginDetails = (gk.list_keyring_ids)

			else:
				gk.create_sync("GoogleMusic","GoogleMusic")
	def _find_key(key,keyring):
		

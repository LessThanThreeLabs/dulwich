# shell_cmd.py -- For executing git commands through the shell 
#                 on git repositories
#
# Copyright (C) 2012 Jonathan Chu <jchonphoenix@gmail.com>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; version 2
# of the License or (at your option) any later version of
# the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
# MA  02110-1301, USA.

import os
import subprocess

def dashify(str):
	return str.replace('_', '-')

class GitShell(object):
	_GIT_EXECUTABLE_NAME = 'git'
	_GIT_EXEC_ENV_VAR = "GIT_PYTHON_GIT_EXECUTABLE"
	GIT_EXECUTABLE = os.environ.get(_GIT_EXEC_ENV_VAR, _GIT_EXECUTABLE_NAME)	
	
	def __getattr__(self, name):
		return lambda **kwargs: self._call_process(dashify(name), **kwargs)

	def _call_process(self, name, **kwargs):
		shell_args = [self.GIT_EXECUTABLE, name]
		shell_args.extend(self._transform_kwargs(kwargs))
		subprocess.check_call(shell_args)

	def _transform_kwargs(self, kwargs):
		def transform(kvp):
			k, v = kvp
			if len(k) > 0:
				if v == True: 
					return '-%s' % k
				elif type(v) is not bool: 
					return '-%s%s' % (k, v)
			else:
				if v == True:
					return '--%s' % dashify(k)
				elif type(v) is not bool:
					return '--%s=%s' % (dashify(k), v)
		
		return map(transform, kwargs.iteritems())		
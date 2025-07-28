# Iunctura PDF Merger: A powerful command-line tool for merging and converting PDF files with flexible file handling and organization options. Tired of manually combining lecture slides or documents? Iunctura simplifies the process by offering seamless PDF merging, file conversion, and recursive directory processing. 
# Copyright (C) 2024 NEERAJ R RUGI

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
class fileNotFoundError(Exception):
    pass

class sofficeNotPresentError(Exception):
    pass

class failedToConvertToPDFError(Exception):
    pass
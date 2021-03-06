#    BDB: A databank of PDB entries with full isotropic B-factors.
#    Copyright (C) 2014  Wouter G. Touw  (<wouter.touw@radboudumc.nl>)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License in the
#    LICENSE file that should have been included as part of this package.
#    If not, see <http://www.gnu.org/licenses/>.
import logging
_log = logging.getLogger(__name__)

import os
import pyconfig
import re


ANISOU_PAT = re.compile(r"^ANISOU")
B_TYPE_PAT = re.compile(r"^REMARK   3   B VALUE TYPE : (\w+( \w+)?)\s*$")
B_MSQAV_PAT = re.compile(r"(MEAN-SQUARE AMPLITUDE OF ATOMIC VIBRATION|"
                         "U\*\*2|UISO)")
EXPDTA_PAT = re.compile(r"^EXPDTA")
PDB_ID_PAT = re.compile(r"^[0-9a-zA-Z]{4}$")
PROGRAM_PAT = re.compile(r"^REMARK   3   PROGRAM     : "
                         "(?!NULL|NONE|NO REFINEMENT)")
REMARK_3_PAT = re.compile(r"^REMARK   3")
REFMARKS_PAT = re.compile(r"^REMARK   3  OTHER REFINEMENT REMARKS: "
                          "(?!NULL|NONE)")
N_TLS_PAT = re.compile(r"^REMARK   3   NUMBER OF TLS GROUPS  : (\d+)\s*$")


def get_bdb_entry_outdir(root, pdb_id):
    out_dir = os.path.join(root, pdb_id[1:3], pdb_id)
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
    return out_dir


def is_valid_directory(parser, arg):
    """ Check if directory exists."""
    if not os.path.isdir(arg):
        parser.error("The directory {} does not exist!".format(arg))
    else:
        # File exists so return the directory
        return arg


def is_valid_file(parser, arg):
    """ Check if file exists and is not empty."""
    if not os.path.isfile(arg):
        parser.error("The file {} does not exist!".format(arg))
    elif not os.stat(arg).st_size > 0:
        parser.error("The file {} is empty!".format(arg))
    else:
        # File exists and is not empty so return the filename
        return arg


def is_valid_pdbid(parser, arg):
    """ Check if this is a valid PDB identifier (anno 2014)."""
    if not re.search(PDB_ID_PAT, arg):
        parser.error("Not a valid PDB ID: {} !".format(arg))
    else:
        return arg


def write_whynot(pdb_id, reason):
    """Create a WHY NOT file.

    Return a Boolean.
    """
    directory = pyconfig.get("BDB_FILE_DIR_PATH")
    filename = pdb_id + ".whynot"
    _log.warn("Writing WHY NOT entry.")
    try:
        with open(os.path.join(directory, filename), "w") as whynot:
            whynot.write("COMMENT: " + reason + "\n" +
                         "BDB," + pdb_id + "\n")
            return True
    except IOError as ex:
        _log.error(ex)
        return False

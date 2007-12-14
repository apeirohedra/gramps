#
# Gramps - a GTK+/GNOME based genealogy program
#
# Copyright (C) 2000-2007  Donald N. Allingham
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#

# $Id$

"""
Media object for GRAMPS
"""

__revision__ = "$Revision$"

#-------------------------------------------------------------------------
#
# standard python modules
#
#-------------------------------------------------------------------------
import os
from types import InstanceType

#-------------------------------------------------------------------------
#
# GRAMPS modules
#
#-------------------------------------------------------------------------
from primaryobj import PrimaryObject
from srcbase import SourceBase
from notebase import NoteBase
from datebase import DateBase
from attrbase import AttributeBase
from markertype import MarkerType

#-------------------------------------------------------------------------
#
# MediaObject class
#
#-------------------------------------------------------------------------
class MediaObject(SourceBase, NoteBase, DateBase, AttributeBase,
                  PrimaryObject):
    """
    Containter for information about an image file, including location,
    description and privacy
    """
    
    def __init__(self, source=None):
        """
        Initialize a MediaObject. If source is not None, then object
        is initialized from values of the source object.

        @param source: Object used to initialize the new object
        @type source: MediaObject
        """
        PrimaryObject.__init__(self, source)
        SourceBase.__init__(self, source)
        NoteBase.__init__(self, source)
        DateBase.__init__(self, source)
        AttributeBase.__init__(self, source)

        if source:
            self.path = source.path
            self.mime = source.mime
            self.desc = source.desc
            self.thumb = source.thumb
        else:
            self.path = ""
            self.mime = ""
            self.desc = ""
            self.thumb = None

    def serialize(self):
        """
        Converts the data held in the event to a Python tuple that
        represents all the data elements. This method is used to convert
        the object into a form that can easily be saved to a database.

        These elements may be primative Python types (string, integers),
        complex Python types (lists or tuples, or Python objects. If the
        target database cannot handle complex types (such as objectes or
        lists), the database is responsible for converting the data into
        a form that it can use.

        @returns: Returns a python tuple containing the data that should
            be considered persistent.
        @rtype: tuple
        """
        return (self.handle, self.gramps_id, self.path, self.mime, self.desc,
                AttributeBase.serialize(self),
                SourceBase.serialize(self),
                NoteBase.serialize(self),
                self.change,
                DateBase.serialize(self),
                self.marker.serialize(),
                self.private)

    def unserialize(self, data):
        """
        Converts the data held in a tuple created by the serialize method
        back into the data in an Event structure.

        @param data: tuple containing the persistent data associated the object
        @type data: tuple
        """
        (self.handle, self.gramps_id, self.path, self.mime, self.desc,
         attribute_list, source_list, note_list, self.change,
         date, marker, self.private) = data

        self.marker = InstanceType(MarkerType)
        self.marker.unserialize(marker)
        AttributeBase.unserialize(self, attribute_list)
        SourceBase.unserialize(self, source_list)
        NoteBase.unserialize(self, note_list)
        DateBase.unserialize(self, date)

    def get_text_data_list(self):
        """
        Returns the list of all textual attributes of the object.

        @return: Returns the list of all textual attributes of the object.
        @rtype: list
        """
        return [self.path, self.mime, self.desc, self.gramps_id]

    def get_text_data_child_list(self):
        """
        Returns the list of child objects that may carry textual data.

        @return: Returns the list of child objects that may carry textual data.
        @rtype: list
        """
        return self.attribute_list + self.source_list

    def get_sourcref_child_list(self):
        """
        Returns the list of child secondary objects that may refer sources.

        @return: Returns the list of child secondary child objects that may refer sources.
        @rtype: list
        """
        return self.attribute_list

    def get_note_child_list(self):
        """
        Returns the list of child secondary objects that may refer notes.

        @return: Returns the list of child secondary child objects that may refer notes.
        @rtype: list
        """
        return self.attribute_list + self.source_list

    def get_referenced_handles(self):
        """
        Returns the list of (classname,handle) tuples for all directly
        referenced primary objects.
        
        @return: List of (classname,handle) tuples for referenced objects.
        @rtype: list
        """
        return self.get_referenced_note_handles()

    def get_handle_referents(self):
        """
        Returns the list of child objects which may, directly or through
        their children, reference primary objects..
        
        @return: Returns the list of objects refereincing primary objects.
        @rtype: list
        """
        return self.attribute_list + self.source_list

    def set_mime_type(self, mime_type):
        """
        Sets the MIME type associated with the MediaObject

        @param mime_type: MIME type to be assigned to the object
        @type mime_type: str
        """
        self.mime = mime_type

    def get_mime_type(self):
        """
        Returns the MIME type associated with the MediaObject

        @returns: Returns the associated MIME type
        @rtype: str
        """
        return self.mime
    
    def set_path(self, path):
        """set the file path to the passed path"""
        self.path = os.path.normpath(path)

    def get_path(self):
        """return the file path"""
        return self.path

    def set_description(self, text):
        """sets the description of the image"""
        self.desc = text

    def get_description(self):
        """returns the description of the image"""
        return self.desc

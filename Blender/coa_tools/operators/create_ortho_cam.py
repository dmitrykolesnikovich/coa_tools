'''
Copyright (C) 2015 Andreas Esau
andreasesau@gmail.com

Created by Andreas Esau

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''
 
import bpy
import bpy_extras
import bpy_extras.view3d_utils
from math import radians
import mathutils
from mathutils import Vector, Matrix, Quaternion
import math
import bmesh
from bpy.props import FloatProperty, IntProperty, BoolProperty, StringProperty, CollectionProperty, FloatVectorProperty, EnumProperty, IntVectorProperty
import os
from bpy_extras.io_utils import ExportHelper, ImportHelper
import json
from bpy.app.handlers import persistent
from .. functions import *

######################################################################################################################################### Create Sprite Object
class CreateOrtpographicCamera(bpy.types.Operator):
    bl_idname = "wm.coa_create_ortho_cam"
    bl_label = "Camera Settings"
    bl_options = {"REGISTER","UNDO"}
    
    set_resolution = BoolProperty(name="Set Resolution", default = True)
    resolution = IntVectorProperty(name="Resolution", default=(960,600), size=2)
    create = BoolProperty(name="Create Camera",default=True)
    
    def draw(self, context):
        layout = self.layout
        if self.create:
            row = layout.row()
            row.prop(self,"set_resolution")
        
        row = layout.row()
        row.prop(self,"resolution")
    
    def invoke(self, context, event):
        wm = context.window_manager 
        return wm.invoke_props_dialog(self)
        
    def execute(self, context):
        scene = context.scene
        if self.create:
            context.scene.objects.active = None
            bpy.ops.object.camera_add(view_align=True, enter_editmode=False, location=(0, -10, 0), rotation=(radians(90), 0, 0))
        cam = context.active_object
        context.scene.objects.active = cam
        cam.data.type = "ORTHO"
        scene.render.pixel_filter_type = "BOX"
        scene.render.alpha_mode = "TRANSPARENT"
        
        if self.set_resolution:
            ortho_scale = max(self.resolution[0],self.resolution[1])
            cam.data.ortho_scale = ortho_scale/100
            
            scene.render.resolution_x = self.resolution[0]
            scene.render.resolution_y = self.resolution[1]
            scene.render.resolution_percentage = 100
        scene.camera = cam
        if bpy.context.space_data.region_3d.view_perspective != "CAMERA":
            bpy.ops.view3d.viewnumpad(type="CAMERA")
        return{"FINISHED"}

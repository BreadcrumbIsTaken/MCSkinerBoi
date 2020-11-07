import bpy

bl_info = {
    "name": "MC Skiner Boi",
    "author": "Breadcrumb",
    "version": (0, 1),
    "blender": (2, 90, 1),
    "location": "3D View Port ~> Right Pannel (N) ~> Breadcrumb ~> MC Skiner Boi",
    "description": "Quickly add and change a Minecraft Skin for any (i think) Minecraft Rig!",
    "category": "Breadcrumb",
    "support": "COMMUNITY",
    
}


class BREADCRUMB_PT_mcskinerboimain(bpy.types.Panel):
    bl_label = "MC Skiner Boi"
    bl_idname = "BREADCRUMB_PT_MCSkinerBoi"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Breadcrumb"
        
    def draw(self, context):
        layout = self.layout
        
        layout.label(text = "First, Create Skin Texture:")
        row = layout.row()
        row.label(icon ="VPAINT_HLT")
        row.scale_y = 2
        row.operator('breadcrumb.mcskinerboi_c_normal')
    
        layout.label(text = "Or, Create SSS Texture:")
        row = layout.row()
        row.label(icon = "TPAINT_HLT")
        row.scale_y = 2
        row.operator('breadcrumb.mcskinerboi_c_sss')
        
        layout.label(text = "Then, Append a skin:")
        layout.label(text = "Note: THIS WILL ONLY", icon = "ERROR")
        layout.label(text = "WORK IF YOU ALREADY")
        layout.label(text = "HAVE MADE THE MATERIAL")
        row = layout.row()
        row.label(icon = "MATERIAL")
        row.scale_y = 2
        row.operator('breadcrumb.mcskinerboi_file_selector')


class BREADCRUMB_OT_mcskinerboiFileSelector(bpy.types.Operator):
    bl_idname = "breadcrumb.mcskinerboi_file_selector"
    bl_label = "Append Skin!"
    bl_description = "Opens file selector, after executes"
    bl_options = {"REGISTER"}

    filepath = bpy.props.StringProperty(subtype='FILE_PATH')
    filename = bpy.props.StringProperty(subtype='FILE_NAME')
    directory = bpy.props.StringProperty(subtype='DIR_PATH')
    files = bpy.props.CollectionProperty(type=bpy.types.OperatorFileListElement)

    

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):

        skin = bpy.data.materials.get("Skin")

        i = skin.node_tree.nodes.get('Image Texture')

        img = bpy.data.images.load(self.filepath)

        i.image = img

        #execute after invoking fileselect
        return {"FINISHED"}

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}



        
class BREADCRUMB_OT_mcskinerboioperator_NORM(bpy.types.Operator):
    """Creates a regular Skin texture!"""
    bl_label = "Create Skin Material"
    bl_idname = "breadcrumb.mcskinerboi_c_normal"
    
    def execute(self, context):
        
            # creates the skin material
        skin = bpy.data.materials.new(name = 'Skin')
        
            # Enables use nodes
        skin.use_nodes = True
        
        new = skin.node_tree.nodes.new
        
            # IMAGE TEXTURE
        skin_node = new(type = 'ShaderNodeTexImage')
        skin_node.interpolation = 'Closest'
        skin_node.location = (-400, 80)
        
            # PRINCIPLED BSDF
        principled = skin.node_tree.nodes.get('Principled BSDF')
        principled.location = (0, 40)
            # subsurf
        principled.inputs[1].default_value = 0.1
            # subsurf radius
        principled.inputs[2].default_value[0] = 1
        principled.inputs[2].default_value[1] = 1
        principled.inputs[2].default_value[2] = 1
            # other stuff for look
        principled.inputs[5].default_value = 0
        principled.inputs[7].default_value = 0
        principled.inputs[11].default_value = 0
        principled.inputs[13].default_value = 0
        principled.distribution = 'MULTI_GGX'
        
            # DIFFUSE BSDF
        diffuse = new(type = 'ShaderNodeBsdfDiffuse')
        diffuse.location = (40, 200)
        
            # SSS LEVEL MIX SHADER
        sss_level = new(type = 'ShaderNodeMixShader')
        sss_level.location = (340, 80)
            # Makes it so the sss is on by defualt.
        sss_level.inputs[0].default_value = 0
        sss_level.label = "SSS Level"
        sss_level.use_custom_color = True
        sss_level.color = (0, 0.340291, 0.608)
        
        
            # TRANSPARENT BSDF
        transparent = new(type = 'ShaderNodeBsdfTransparent')
        transparent.location = (340, 200)
        
            # SECOND MIX SHADER
        mix = new(type = 'ShaderNodeMixShader')
        mix.location = (600, 180)
        
            # MATERIAL OUTPUT
        out = skin.node_tree.nodes.get('Material Output')
        out.location = (800, 180)
        
        
        link = skin.node_tree.links.new
        
            # Image Texture
        link(skin_node.outputs[0], principled.inputs[0])
        link(skin_node.outputs[0], principled.inputs[3])
        link(skin_node.outputs[0], diffuse.inputs[0])
        link(skin_node.outputs[1], mix.inputs[0])
        
            # Diffuse BSDF
        link(diffuse.outputs[0], sss_level.inputs[1])
        
            # Principled BSDF
        link(principled.outputs[0], sss_level.inputs[2])
        
            # SSS Level
        link(sss_level.outputs[0], mix.inputs[2])
        
            # Transparent BSDF
        link(transparent.outputs[0], mix.inputs[1])
        
            # Mix Shader
        link(mix.outputs[0], out.inputs[0])
        
        
            
        ob = context.object
        
            # if the object has a material, override it
        if ob.data.materials:
            ob.data.materials[0] = skin
        else:
                # if it does not, append it (add it)
            ob.data.materials.append(skin)
        
        
        
        
        
            # Applies Alpha Clip to texture
        bpy.context.object.active_material.blend_method = 'CLIP'
        
        
        
        return {'FINISHED'}
        


class BREADCRUMB_OT_mcskinerboioperator_SSS(bpy.types.Operator):
    """Creates a skin texture with Subsurface Scatering!"""
    bl_label = "Create SSS Skin Material"
    bl_idname = "breadcrumb.mcskinerboi_c_sss"
    
    def execute(self, context):
        
            # creates the skin material
        skin = bpy.data.materials.new(name = 'Skin')
        
            # Enables use nodes
        skin.use_nodes = True
        
        new = skin.node_tree.nodes.new
        
            # IMAGE TEXTURE
        skin_node = new(type = 'ShaderNodeTexImage')
        skin_node.interpolation = 'Closest'
        skin_node.location = (-400, 80)
        
            # PRINCIPLED BSDF
        principled = skin.node_tree.nodes.get('Principled BSDF')
        principled.location = (0, 40)
            # subsurf
        principled.inputs[1].default_value = 0.1
            # subsurf radius
        principled.inputs[2].default_value[0] = 1
        principled.inputs[2].default_value[1] = 1
        principled.inputs[2].default_value[2] = 1
            # other stuff for look
        principled.inputs[5].default_value = 0
        principled.inputs[7].default_value = 0
        principled.inputs[11].default_value = 0
        principled.inputs[13].default_value = 0
        principled.distribution = 'MULTI_GGX'
        
            # DIFFUSE BSDF
        diffuse = new(type = 'ShaderNodeBsdfDiffuse')
        diffuse.location = (40, 200)
        
            # SSS LEVEL MIX SHADER
        sss_level = new(type = 'ShaderNodeMixShader')
        sss_level.location = (340, 80)
            # Makes it so the sss is on by defualt.
        sss_level.inputs[0].default_value = 1
        sss_level.label = "SSS Level"
        sss_level.use_custom_color = True
        sss_level.color = (0, 0.340291, 0.608)
        
        
            # TRANSPARENT BSDF
        transparent = new(type = 'ShaderNodeBsdfTransparent')
        transparent.location = (340, 200)
        
            # SECOND MIX SHADER
        mix = new(type = 'ShaderNodeMixShader')
        mix.location = (600, 180)
        
            # MATERIAL OUTPUT
        out = skin.node_tree.nodes.get('Material Output')
        out.location = (800, 180)
        
        
        link = skin.node_tree.links.new
        
            # Image Texture
        link(skin_node.outputs[0], principled.inputs[0])
        link(skin_node.outputs[0], principled.inputs[3])
        link(skin_node.outputs[0], diffuse.inputs[0])
        link(skin_node.outputs[1], mix.inputs[0])
        
            # Diffuse BSDF
        link(diffuse.outputs[0], sss_level.inputs[1])
        
            # Principled BSDF
        link(principled.outputs[0], sss_level.inputs[2])
        
            # SSS Level
        link(sss_level.outputs[0], mix.inputs[2])
        
            # Transparent BSDF
        link(transparent.outputs[0], mix.inputs[1])
        
            # Mix Shader
        link(mix.outputs[0], out.inputs[0])
        
        
   
        
        
        
        ob = context.object
        obj = context.active_object
        
            # if the object has a material, override it
        if ob.data.materials:
            ob.data.materials[0] = skin
        else:
                # if it does not, append it (add it)
            ob.data.materials.append(skin)
        
        
        
        
        
            # Applies Alpha Clip to texture
        bpy.context.object.active_material.blend_method = 'CLIP'
        
        
        
        return {'FINISHED'}










classes = [BREADCRUMB_PT_mcskinerboimain, BREADCRUMB_OT_mcskinerboioperator_SSS, BREADCRUMB_OT_mcskinerboioperator_NORM, BREADCRUMB_OT_mcskinerboiFileSelector]
        
def register():
    for c in classes:
        bpy.utils.register_class(c)

def unregister():
    for c in classes:
        bpy.utils.unregister_class(c)
    
    

if __name__ == "__main__":
    register()    
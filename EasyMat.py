bl_info = {
    "name" : "EasyMat",
    "author" : "fckngienaz",
    "version" : (1, 0),
    "blender" : (4, 0, 1),
    "location" : "View3d > Tool",
    "warning" : "",
    "wiki_url" : "https://github.com/gienaz/",
    "category" : "AddMaterial",
}




import bpy
import os




    

class MainPanel(bpy.types.Panel):
    bl_label = "EasyMat by fckngienaz"
    bl_idname = "PT_MatPanel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "EasyMat"
    
    
    def draw(self, context):
        
        layout = self.layout
        row = layout.row()
        layout.prop(context.scene, 'dir_')
        row.label(text = "Select textures directory", icon = "NEWFOLDER")
        row = layout.row()
        row = layout.row()
        row.label(text = "Enter material name")

        row= layout.row()
        layout.prop(context.scene, "materialName", icon_only = True)
        
        row = layout.row()
        row.operator("easymat.addbasic_operator")
        
def showPath(self, context):
    print("filepath: ", bpy.context.scene.file_)# return only //x_bot.json 
    print("self.filepath", self.filepath)
        
        

class EASYMAT_OT_add_basic(bpy.types.Operator):
    """Creates material"""
    
    bl_label = "Create Material"
    bl_idname = "easymat.addbasic_operator"
    bl_icon = "MATERIAL"    

    def execute(self, context):  
        
        #check for textures with suffix
        
        #baseColor
        if os.path.isdir(context.scene.dir_):
            files = os.listdir(context.scene.dir_)
            for file in files:
                if file.endswith(context.scene.baseColor + context.scene.textureType):
                    baseColorImported = True
                    baseColor_path = context.scene.dir_ + os.path.basename(file)
                    break
                else:
                    baseColorImported = False                    
                
            #roughness
            if(context.scene.useComplexTextures == False):
                for file in files:
                    if file.endswith(context.scene.roughness + context.scene.textureType):
                        roughnessImported = True
                        roughness_path = context.scene.dir_ + os.path.basename(file)
                        break
                    else:
                        roughnessImported = False                                  
            #metallic
                for file in files:
                    if file.endswith(context.scene.metallic + context.scene.textureType):
                        metallicImported = True
                        metallic_path = context.scene.dir_ + os.path.basename(file)
                        break
                    else:
                        metallicImported = False  
                  
            #ambientOcclusion
            
                for file in files:
                    if file.endswith(context.scene.ao + context.scene.textureType):
                        aoImported = True
                        ao_path = context.scene.dir_ + os.path.basename(file)
                        break
                    else:
                        aoImported = False  
            
            #complex
            elif(context.scene.useComplexTextures == True):
                for file in files:
                    if file.endswith(context.scene.complex + context.scene.textureType):
                        complexImported = True
                        complex_path = context.scene.dir_ + os.path.basename(file)
                        break
                    else:
                        complexImported = False     
                        
        #normalMap
        
            for file in files:
                if file.endswith(context.scene.normalMap + context.scene.textureType):
                    normalMapImported = True
                    normalMap_path = context.scene.dir_ + os.path.basename(file)
                    break
                else:
                    normalMapImported = False
        #transparensy
        
            if(context.scene.useTransparency):
                if(context.scene.useAlphaInBaseColor == False):
                    for file in files:
                        if file.endswith(context.scene.alpha + context.scene.textureType):
                            alphaImported = True
                            alpha_path = context.scene.dir_ + os.path.basename(file)
                            break
                        else:
                            alphaImported = False
            
        
        
        
        #create material      
        material_basic = bpy.data.materials.new(name = context.scene.materialName)
        material_basic.use_nodes = True
        
        link = material_basic.node_tree.links.new
        
        bpy.context.object.active_material = material_basic
        
        principled_node = material_basic.node_tree.nodes.get('Principled BSDF')
        
        #principled_node.inputs[0].default_value = (1,0,0,1)
        
        #create baseColor
        baseColor_node = material_basic.node_tree.nodes.new('ShaderNodeTexImage')
        baseColor_node.location = (-750, 500)
        
        if(baseColorImported == True):
            baseColor_node.image = bpy.data.images.load(baseColor_path)
            
        if(context.scene.useComplexTextures == False):
            if(context.scene.useAmbientOcclusion):
                AO_node = material_basic.node_tree.nodes.new('ShaderNodeTexImage')
                AO_node.location = (-750, 250)
                
                mixAOcolor_node = material_basic.node_tree.nodes.new('ShaderNodeMix')
                
                mixAOcolor_node.data_type = 'RGBA'
                mixAOcolor_node.blend_type = 'MULTIPLY'
               # mixAOcolor_node.inputs[1].default_value = (1,0,0)
               # mixAOcolor_node.inputs[2].default_value = (1,1,1,1)
                mixAOcolor_node.location = (-400,500)
                
                link(baseColor_node.outputs[0], mixAOcolor_node.inputs[6])
                link(AO_node.outputs[0], mixAOcolor_node.inputs[7])
                link(mixAOcolor_node.outputs[2], principled_node.inputs[0])
                if(aoImported == True):
                    AO_node.image = bpy.data.images.load(ao_path)                
            else:
                link(baseColor_node.outputs[0], principled_node.inputs[0])
                
        
        else:
            complex_node = material_basic.node_tree.nodes.new('ShaderNodeTexImage')
            complex_node.location = (-1000, 250)
            if(complexImported == True):
                    complex_node.image = bpy.data.images.load(complex_path)
            
            separateComplex_node = material_basic.node_tree.nodes.new('ShaderNodeSeparateColor')
            separateComplex_node.location = (-650,175)
            
            mixAOcolor_node = material_basic.node_tree.nodes.new('ShaderNodeMix')
            mixAOcolor_node.data_type = 'RGBA'
            mixAOcolor_node.blend_type = 'MULTIPLY'

            mixAOcolor_node.location = (-400,500)
            
            link(baseColor_node.outputs[0], mixAOcolor_node.inputs[6])
            link(complex_node.outputs[0], separateComplex_node.inputs[0])
            
            link(mixAOcolor_node.outputs[2], principled_node.inputs[0])
            
            if(context.scene.aoChannel == "R"):
                link(separateComplex_node.outputs[0], mixAOcolor_node.inputs[7])
            elif(context.scene.aoChannel == "G"):
                link(separateComplex_node.outputs[1], mixAOcolor_node.inputs[7])
            elif(context.scene.aoChannel == "B"):
                link(separateComplex_node.outputs[2], mixAOcolor_node.inputs[7])
            
        #transparent
        if(context.scene.useTransparency):
            if(context.scene.useAlphaInBaseColor == False):    
                alpha_node = material_basic.node_tree.nodes.new('ShaderNodeTexImage')
                alpha_node.location = (-750, 0)
                link(alpha_node.outputs[0], principled_node.inputs[4])
            else:
                link(baseColor_node.outputs[1], principled_node.inputs[4])
                
        
        
        if(context.scene.useComplexTextures == False):
            #create roughness
            roughness_node = material_basic.node_tree.nodes.new('ShaderNodeTexImage')
            roughness_node.location = (-500, 0)
            link(roughness_node.outputs[0], principled_node.inputs[2])
            if(roughnessImported == True):
                roughness_node.image = bpy.data.images.load(roughness_path)
                
            #create metallic
            metallic_node = material_basic.node_tree.nodes.new('ShaderNodeTexImage')
            metallic_node.location = (-500, 250)
            link(metallic_node.outputs[0], principled_node.inputs[1])
            if(metallicImported == True):
                metallic_node.image = bpy.data.images.load(metallic_path)
        else:
            if(context.scene.roughnessChannel == "R"):
                link(separateComplex_node.outputs[0], principled_node.inputs[2])
            elif(context.scene.roughnessChannel == "G"):
                link(separateComplex_node.outputs[1], principled_node.inputs[2])
            elif(context.scene.roughnessChannel == "B"):
                link(separateComplex_node.outputs[2], principled_node.inputs[2])
                
            if(context.scene.metallicChannel == "R"):
                link(separateComplex_node.outputs[0], principled_node.inputs[1])
            elif(context.scene.metallicChannel == "G"):
                link(separateComplex_node.outputs[1], principled_node.inputs[1])
            elif(context.scene.metallicChannel == "B"):
                link(separateComplex_node.outputs[2], principled_node.inputs[1])
            
        #create normal
        normalMap_node = material_basic.node_tree.nodes.new('ShaderNodeTexImage')
        normalMap_node.location = (-1300, -250)        
        
        separateRGB_node = material_basic.node_tree.nodes.new('ShaderNodeSeparateColor')
        separateRGB_node.location = (-1000,-275)
        link(normalMap_node.outputs[0], separateRGB_node.inputs[0])
        
        invert_node = material_basic.node_tree.nodes.new('ShaderNodeInvert')
        invert_node.location = (-800,-300)
        link(separateRGB_node.outputs[1], invert_node.inputs[1])
        
        combineRGB_node = material_basic.node_tree.nodes.new('ShaderNodeCombineColor')
        combineRGB_node.location = (-600,-275)
        link(separateRGB_node.outputs[0], combineRGB_node.inputs[0])
        link(invert_node.outputs[0], combineRGB_node.inputs[1])
        link(separateRGB_node.outputs[2], combineRGB_node.inputs[2])
        
        shaderNormal_node = material_basic.node_tree.nodes.new('ShaderNodeNormalMap')
        shaderNormal_node.location = (-400,-275)
        link(combineRGB_node.outputs[0], shaderNormal_node.inputs[1])
        link(shaderNormal_node.outputs[0], principled_node.inputs[5])
        
        if(normalMapImported == True):
            normalMap_node.image = bpy.data.images.load(normalMap_path)
            
        if(context.scene.normal_enum == "DIRECTX"):
            invert_node.inputs[0].default_value = 0
        else:
            invert_node.inputs[0].default_value = 1
            
                
        
        
        return {'FINISHED'}

        
        
class PanelSuffix(bpy.types.Panel):
    bl_label = "Suffix settings"
    bl_idname = "PT_PanelSpecials"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "EasyObjectCreate"
    bl_parent_id = "PT_MatPanel"
    bl_options = {"DEFAULT_CLOSED"}
    
    def draw(self, context):
        layout = self.layout
        layout.scale_y = 0.8
        row = layout.row()
        row.label(text = "Base Color", icon = "COLORSET_02_VEC")
        layout.prop(context.scene, "baseColor", icon_only = True)
        if(context.scene.useTransparency == True):
            if(context.scene.useAlphaInBaseColor == False):
                row = layout.row()
                row.label(text = "Transparensy map", icon = "IMAGE_ALPHA")
                layout.prop(context.scene, "alpha", icon_only = True)
        row = layout.row()
        row.label(text = "NormalMap", icon = "COLORSET_04_VEC")
        layout.prop(context.scene, "normalMap", icon_only = True)
        row = layout.row()
        if(context.scene.useComplexTextures == False):
            row = layout.row()
            row.label(text = "Roughness", icon = "COLORSET_13_VEC")
            layout.prop(context.scene, "roughness", icon_only = True)
            row = layout.row()
            row.label(text = "Metallic", icon = "COLORSET_10_VEC")
            layout.prop(context.scene, "metallic", icon_only = True)
            
            if(context.scene.useAmbientOcclusion == True):
                row = layout.row()
                row.label(text = "AmbientOcclusion", icon = "COLORSET_10_VEC")
                layout.prop(context.scene, "ao", icon_only = True)
        else:
            row = layout.row()
            row.label(text = "Complex Texture", icon = "COLORSET_10_VEC")
            layout.prop(context.scene, "complex", icon_only = True)
        
        
        
        
class PanelSettings(bpy.types.Panel):
    bl_label = "Advanced settings"
    bl_idname = "PT_PanelAdvanced"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "EasyObjectCreate"
    bl_parent_id = "PT_MatPanel"
    bl_options = {"DEFAULT_CLOSED"}
    
    
    
    def draw(self, context):
        layout = self.layout
        layout.scale_y = 0.8
        row = layout.row()
        row.label(text="Normal Map Type:")
        row = layout.row()
        layout.prop(context.scene, "normal_enum")
        row = layout.row()
        row.label(text="Texture extension:")
        
        row.prop(context.scene, "textureType", icon_only = True)
        
        if(context.scene.useComplexTextures == False):
            row = layout.row()
            row.label(text="Use Ambient Occlusion")
            row.prop(context.scene, "useAmbientOcclusion"  , icon_only = True)
            
        row = layout.row()
        row.prop(context.scene, "useComplexTextures" , text = "Use Complex Textures")
        if(context.scene.useComplexTextures == True):
            row = layout.row()
            #AmbientOcclusion
            row.prop(context.scene, "aoChannel")
            row = layout.row()
            row.prop(context.scene, "roughnessChannel")
            row = layout.row()
            row.prop(context.scene, "metallicChannel")
            #Roughness
            #Metallic
            
        row = layout.row()
        row.prop(context.scene, "useTransparency", text="Use Transparenсy")
        if(context.scene.useTransparency == True):
            row = layout.row()
            row.prop(context.scene, "useAlphaInBaseColor", text="Use Base Color Alpha")
        
            
        
            
        
        
        
        
def register():
    bpy.utils.register_class(MainPanel)
    bpy.utils.register_class(EASYMAT_OT_add_basic)



    bpy.utils.register_class(PanelSuffix)
    bpy.utils.register_class(PanelSettings)
    
    
    bpy.types.Scene.useAmbientOcclusion = bpy.props.BoolProperty(
        default = True
    )
    bpy.types.Scene.useComplexTextures = bpy.props.BoolProperty(
        default = False
    )
    bpy.types.Scene.useTransparency = bpy.props.BoolProperty(
        default = False
    )
    bpy.types.Scene.useAlphaInBaseColor = bpy.props.BoolProperty(
        default = True
    )
    bpy.types.Scene.aoChannel = bpy.props.EnumProperty(
        name = "ambientOcclusion",
        description = "Select Ambient Occlusion channel",
        items = [
            ('R', "Red", "Assign to Red Channel"),
            ('G', "Green", "Assign to Green Channel"),
            ('B', "Blue", "Assign to Blue Channel")
        ],
        default = "R"
    
    ) 
    bpy.types.Scene.roughnessChannel = bpy.props.EnumProperty(
        name = "roughness",
        description = "Select Roughness channel",
        items = [
            ('R', "Red", "Assign to Red Channel"),
            ('G', "Green", "Assign to Green Channel"),
            ('B', "Blue", "Assign to Blue Channel")
        ],
        default = "G"
    
    ) 
    bpy.types.Scene.metallicChannel = bpy.props.EnumProperty(
        name = "metallic",
        description = "Select Metallic channel",
        items = [
            ('R', "Red", "Assign to Red Channel"),
            ('G', "Green", "Assign to Green Channel"),
            ('B', "Blue", "Assign to Blue Channel")
            
        ],
        default = "B"
    
    ) 
    
    bpy.types.Scene.dir_ = bpy.props.StringProperty(
        name= "", 
        subtype='DIR_PATH', 
        update=showPath,
        default="D:/"
    )   
    bpy.types.Scene.materialName = bpy.props.StringProperty(
        default = "defaultMaterial"
    )
    bpy.types.Scene.alpha = bpy.props.StringProperty(
        default = "_Transparensy"
    )
    bpy.types.Scene.baseColor = bpy.props.StringProperty(
        default = "_BaseColor"
    )
    bpy.types.Scene.roughness = bpy.props.StringProperty(
        default = "_Roughness"
    )
    bpy.types.Scene.metallic = bpy.props.StringProperty(
        default = "_Metallic"
    )
    bpy.types.Scene.normalMap = bpy.props.StringProperty(
        default = "_Normal"
    )
    bpy.types.Scene.ao = bpy.props.StringProperty(
        default = "_AmbientOcclusion"
    )
    bpy.types.Scene.complex = bpy.props.StringProperty(
        default = "_OcclusionRoughnessMetallic"
    )
    bpy.types.Scene.normalmaptype = bpy.props.BoolProperty(
        default = False
    )
    bpy.types.Scene.normal_enum = bpy.props.EnumProperty(
        name = "",
        description = "Select normal map type",
        items = [
            ('OPENGL', "OpenGl", "3DsMax, Unreal Engine"),
            ('DIRECTX', "DirectX", "Maya, Blender, Marmoset, Modo, Unity, Cryengine")
        ]
    
    ) 
    bpy.types.Scene.textureType = bpy.props.StringProperty(
        default = ".png"
    )
    
    
def unregister():
    bpy.utils.unregister_class(MainPanel)
    bpy.utils.unregister_class(EASYMAT_OT_add_basic)



    bpy.utils.unregister_class(PanelSuffix)
    bpy.utils.unregister_class(PanelSettings)
    
    
if __name__ == "__main__":
    register()
    
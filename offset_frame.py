bl_info = {
    "name": "offset_frame",
    "author": "Aite25",
    "version": (1, 0),
    "blender": (4, 1, 0),
    "location": "Operator search",
    "description": "Offset frames",
    "warning": "",
    "doc_url": "",
    "category": "Object",
}

import bpy

class offset_frame_OP(bpy.types.Operator):
    bl_idname = "object.offset_frame"
    bl_label = "offset_frame"
    bl_options = {'REGISTER','UNDO'}
    
    frame_num:bpy.props.IntProperty(
        name="Frame_num",
        description="Num of offset frames",
        default=1,
    )
    
    def execute(self, context):

        # 获取选择对象
        objarr = bpy.context.selected_objects
        s_objarr = []
        for i,obj in enumerate(objarr):
            # 排除不带关键帧的物体
            if(obj.animation_data != None):
                s_objarr.append(obj)

        def offset_key(single_obj,offset_frame):

            # 获取属性的动画曲线数据
            fcurves = single_obj.animation_data.action.fcurves

            # 遍历每个 fcurve
            for fcurve in fcurves:
                # 遍历该属性的所有关键帧
                for keyframe in fcurve.keyframe_points:
                    # 移动关键帧到新的帧位置
                    keyframe.co[0] += offset_frame
                    keyframe.handle_left[0] += offset_frame
                    keyframe.handle_right[0] += offset_frame

        for i,obj in enumerate(s_objarr):
            # offset_key(obj,i*1)
            offset_key(obj,i*self.frame_num)

        bpy.context.view_layer.update() 
        return{'FINISHED'}

class HT_drawUI(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "OffsetKF"
    bl_label = "Offset_KeyFrames"
        
    def draw(self, context):
        layout = self.layout
        col = layout.column(align=True)
        # numOfFrame = col.prop(context.scene.offset_frame,"frames_num")
        col.operator('object.offset_frame',
            text='Offset')
        props = col.operator('object.offset_frame',
            text='Offset 1 Frame')
        props.frames_num = 1

    #bpy.types.INFO_HT_header.prepend(draw)
    #bpy.types.INFO_HT_header.append(draw)

blender_classes = [
    offset_frame_OP,
    HT_drawUI
]

def register():
    # bpy.types.Scene.offset_frame.frame_num = bpy.props.IntProperty(
    #     name="Frame_num",
    #     description="Num of offset frames",
    #     default=1,
    # )
    for blender_class in blender_classes:
        bpy.utils.register_class(blender_class)

def unregister():
    # del bpy.types.Scene.offset_frame.frame_num
    for blender_class in blender_classes:
        bpy.utils.unregister_class(blender_class)
    
if __name__ == "__main__":
    register()
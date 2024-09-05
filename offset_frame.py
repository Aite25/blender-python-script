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
        if(s_objarr == []):
            return{'FINISHED'}
        if(len(objarr)>1 and len(s_objarr)>1):
            for i,obj in enumerate(s_objarr):
                # offset_key(obj,i*1)
                offset_key(obj,i*self.frame_num)
        elif(len(objarr)==1 and len(s_objarr)==1):
            offset_key(objarr[0],self.frame_num)
        bpy.context.view_layer.update() 
        return{'FINISHED'}
    
class align_frame_OP(bpy.types.Operator):
    bl_idname = "object.align_frame"
    bl_label = "align_frame"
    
    def execute(self, context):

        # 获取选择对象
        s_objarr = bpy.context.selected_objects

        # 排除没有动画的物体
        objarr = []
        for i,obj in enumerate(s_objarr):
            if(obj.animation_data != None):
                objarr.append(obj)

        obj_ff_arr = []

        def get_obj_fcurve(obj):
            if(obj.animation_data == None):
                return
            return obj.animation_data.action.fcurves

        def get_fcurve_ff(fcurve):
            return fcurve.keyframe_points[0].co[0]

        for i,obj in enumerate(objarr):
            if(obj.animation_data == None):
                continue
            # 找到曲线
            fcurve_arr = get_obj_fcurve(obj)
            ff_arr = []

            # 找到首个关键帧
            for j,fcurve in enumerate(fcurve_arr):
                ff_arr.append(get_fcurve_ff(fcurve))
                
            # 记录每个物体的首个关键帧
            obj_ff_arr.append(min(ff_arr))

        # 找到所有物体的首个关键帧作为锚点
        frame_anchor = min(obj_ff_arr)

        print(f"min frame = {frame_anchor}")
        print(f"obj_ff_arr = {obj_ff_arr}")

        # 位移物体关键帧对齐首个关键帧
        for i,obj in enumerate(objarr):
            if(obj.animation_data == None):
                continue 
            offset_key(obj,frame_anchor - obj_ff_arr[i])

        bpy.context.view_layer.update()
        return{'FINISHED'}

class curve_adjust_OP(bpy.types.Operator):
    bl_idname = "object.curve_adjust"
    bl_label = "curve_adjust"
    bl_options = {'REGISTER','UNDO'}
    
    curve_coef:bpy.props.FloatProperty(
        name="Curve_coef",
        description="Coefficient of Curves",
        default=0.05,
        min=0,max=1,
    )

    def execute(self, context):
        def lerp(a: float, b: float, t: float) -> float:
            return (1 - t) * a + t * b

        # 获取选择对象
        objarr = bpy.context.selected_objects
        obj = bpy.context.object

        coef = self.curve_coef

        def obj_keyframe_curves_adjust(obj,coef):
            if(obj.animation_data == None):
                return
            # 获取属性的动画曲线数据
            fcurves = obj.animation_data.action.fcurves

            # 遍历每个 fcurve
            for fcurve in fcurves:
                key_pts = fcurve.keyframe_points
                if len(key_pts)<2:
                    continue
                # 遍历该属性的所有关键帧
                for i,keyframe in enumerate(key_pts):
                    if(i == 0):
                        keyframe.handle_right[0] = lerp(keyframe.co[0],key_pts[i+1].co[0],coef)
                        continue
                    if(i == len(key_pts)-1):
                        keyframe.handle_left[0]  = lerp(key_pts[i-1].co[0],keyframe.co[0],coef)
                        continue
                    # 移动关键帧到新的帧位置
                    keyframe.handle_right[0] = lerp(keyframe.co[0],key_pts[i+1].co[0],coef)
                    keyframe.handle_left[0] = lerp(key_pts[i-1].co[0],keyframe.co[0],coef)
        
        for obj in objarr:
            obj_keyframe_curves_adjust(obj,coef)        
        
        bpy.context.view_layer.update() 
        return{'FINISHED'}
        
class curve_adjust_Select_OP(bpy.types.Operator):
    bl_idname = "object.curve_adjust_select"
    bl_label = "curve_adjust_select"
    bl_options = {'REGISTER','UNDO'}
    
    curve_coef:bpy.props.FloatProperty(
        name="Curve_coef",
        description="Coefficient of Curves",
        default=0.05,
        min=0,max=1,
    )

    def execute(self, context):
        def lerp(a: float, b: float, t: float) -> float:
            return (1 - t) * a + t * b

        # 获取选择对象
        objarr = bpy.context.selected_objects
        obj = bpy.context.object

        coef = self.curve_coef

        def obj_keyframe_curves_adjust(obj,coef):
            if(obj.animation_data == None):
                return
            # 获取属性的动画曲线数据
            fcurves = obj.animation_data.action.fcurves

            # 遍历每个 fcurve
            for fcurve in fcurves:
                key_pts = fcurve.keyframe_points
                if len(key_pts)<2:
                    continue
                # 遍历该属性的所有关键帧
                for i,keyframe in enumerate(key_pts):
                    if(keyframe.select_control_point==True):
                        if(i == 0):
                            keyframe.handle_right[0] = lerp(keyframe.co[0],key_pts[i+1].co[0],coef)
                            continue
                        if(i == len(key_pts)-1):
                            keyframe.handle_left[0]  = lerp(key_pts[i-1].co[0],keyframe.co[0],coef)
                            continue
                        # 移动关键帧到新的帧位置
                        keyframe.handle_right[0] = lerp(keyframe.co[0],key_pts[i+1].co[0],coef)
                        keyframe.handle_left[0] = lerp(key_pts[i-1].co[0],keyframe.co[0],coef)
        
        for obj in objarr:
            obj_keyframe_curves_adjust(obj,coef)        
        
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
        col.operator('object.align_frame',
            text='Align')
        col.operator('object.curve_adjust',
            text='Curve_Adjust')
        col.operator('object.curve_adjust_select',
            text='Curve_Adjust_Select')
        # props = col.operator('object.offset_frame',
        #     text='Offset 1 Frame')
        # props.frames_num = 1

    #bpy.types.INFO_HT_header.prepend(draw)
    #bpy.types.INFO_HT_header.append(draw)

blender_classes = [
    offset_frame_OP,
    align_frame_OP,
    curve_adjust_OP,
    curve_adjust_Select_OP,
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
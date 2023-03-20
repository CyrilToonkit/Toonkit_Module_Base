{    #Spine FK
                "Hips":(self.mocapPrefix + "Hips", True, True),
                "Spine_FK_2":(self.mocapPrefix + "Spine", True, True),
                "Spine_FK_3":(self.mocapPrefix + "Spine1", True, True),#RIG TO ADD
                "Spine_FK_4":(self.mocapPrefix + "Spine2", True, True),#RIG TO ADD
                "Spine_FK_5":(self.mocapPrefix + "Spine3", False, True),
                
                #Spine IK
                "Chest_IK":(self.mocapPrefix + "Spine3", True, True, False),
                "Spine_IK_StartHandle":(self.mocapPrefix + "Spine", True, True, False),
                "Spine_IK_Middle":(self.mocapPrefix + "Spine1", True, True, False),#RIG TO ADD
                "Spine_IK_EndHandle":(self.mocapPrefix + "Spine2", True, True, False),#RIG TO ADD

                #Neck FK
                "Neck_FK_1":(self.mocapPrefix + "Neck", True, True),#RIG TO ADD
                "Neck_FK_2":(self.mocapPrefix + "Neck1", True, True),#RIG TO ADD
                "Head_FK":(self.mocapPrefix + "Head", True, True),

                #Neck IK
                "Head_IK":(self.mocapPrefix + "Head", True, True, False),
                "Neck_IK_Start":(self.mocapPrefix + "Neck", True, True, False),#RIG TO ADD
                "Neck_IK_Middle":(self.mocapPrefix + "Neck1", True, True, False),#RIG TO ADD

                #Left Arm
                "Left_Shoulder":(self.mocapPrefix + "LeftShoulder", False, True),

                #Left Arm FK
                "Left_Arm_FK_1":(self.mocapPrefix + "LeftArm", False, True),
                "Left_Arm_FK_2":(self.mocapPrefix + "LeftForeArm", False, True),
                "Left_Hand":(self.mocapPrefix + "LeftHand", False, True),
                
                #Left Arm IK
                "Left_Arm_upV":(self.mocapPrefix + "LeftArmPoleVector", True, False, False, "poleMatcher", (self.mocapPrefix +"LeftArm", self.mocapPrefix +"LeftForeArm_poleHelper", self.mocapPrefix +"LeftHand")),
                "Left_Arm_IK":(self.mocapPrefix + "LeftHand", True, True, False),
                
                #Left Fingers
                "Left_Thumb_1":(self.mocapPrefix + "LeftHandThumb1", False, True),
                "Left_Thumb_2":(self.mocapPrefix + "LeftHandThumb2", False, True),
                "Left_Thumb_3":(self.mocapPrefix + "LeftHandThumb3", False, True),
                "TK_Left_HandRig_Thumb_Eff_Output":(self.mocapPrefix + "LeftHandThumb4",),

                "Left_Index_Mtc":(self.mocapPrefix + "LeftHandIndex0", False, True),
                "Left_Index_1":(self.mocapPrefix + "LeftHandIndex1", False, True),
                "Left_Index_2":(self.mocapPrefix + "LeftHandIndex2", False, True),
                "Left_Index_3":(self.mocapPrefix + "LeftHandIndex3", False, True),
                "TK_Left_HandRig_Index_Eff_Output":(self.mocapPrefix + "LeftHandIndex4",),
                
                "Left_Middle_Mtc":(self.mocapPrefix + "LeftHandMiddle0", False, True),
                "Left_Middle_1":(self.mocapPrefix + "LeftHandMiddle1", False, True),
                "Left_Middle_2":(self.mocapPrefix + "LeftHandMiddle2", False, True),
                "Left_Middle_3":(self.mocapPrefix + "LeftHandMiddle3", False, True),
                "TK_Left_HandRig_Middle_Eff_Output":(self.mocapPrefix + "LeftHandMiddle4",),
                
                "Left_Ring_Mtc":(self.mocapPrefix + "LeftHandRing0", False, True),
                "Left_Ring_1":(self.mocapPrefix + "LeftHandRing1", False, True),
                "Left_Ring_2":(self.mocapPrefix + "LeftHandRing2", False, True),
                "Left_Ring_3":(self.mocapPrefix + "LeftHandRing3", False, True),
                "TK_Left_HandRig_Ring_Eff_Output":(self.mocapPrefix + "LeftHandRing4",),
                
                "Left_Pinky_Mtc":(self.mocapPrefix + "LeftHandPinky0", False, True),
                "Left_Pinky_1":(self.mocapPrefix + "LeftHandPinky1", False, True),
                "Left_Pinky_2":(self.mocapPrefix + "LeftHandPinky2", False, True),
                "Left_Pinky_3":(self.mocapPrefix + "LeftHandPinky3", False, True),
                "TK_Left_HandRig_Pinky_Eff_Output":(self.mocapPrefix + "LeftHandPinky4",),
                
                #Left HandProp
                #"Left_HandProp":(self.mocapPrefix + "Lf_HandProp_MCP_0_JNT", True, True, False),

                #Left Leg IK
                "Left_Leg_upV":(self.mocapPrefix + "LeftLegPoleVector", True, False, False, "poleMatcher", (self.mocapPrefix +"LeftUpLeg", self.mocapPrefix +"LeftLeg_poleHelper", self.mocapPrefix +"LeftFoot")),
                "Left_Leg_IK":(self.mocapPrefix + "LeftFoot", True, True, False),
                "Left_IK_Tip":(self.mocapPrefix + "LeftToeBase", True, True),
                
                #Left Leg FK
                "Left_Leg_FK_1":(self.mocapPrefix + "LeftUpLeg", False, True),
                "Left_Leg_FK_2":(self.mocapPrefix + "LeftLeg", False, True),
                "Left_Foot_FK_1":(self.mocapPrefix + "LeftFoot", False, True),
                "Left_Foot_FK_2":(self.mocapPrefix + "LeftToeBase", False, True),
                
                #"Left_Tip":(self.mocapPrefix + "Lf_Foot_MCP_2_JNT",),

                #Right Arm
                "Right_Shoulder":(self.mocapPrefix + "RightShoulder", False, True),

                #Right Arm FK
                "Right_Arm_FK_1":(self.mocapPrefix + "RightArm", False, True),
                "Right_Arm_FK_2":(self.mocapPrefix + "RightForeArm", False, True),
                "Right_Hand":(self.mocapPrefix + "RightHand", False, True),
                
                #Right Arm IK
                "Right_Arm_upV":(self.mocapPrefix + "RightArmPoleVector", True, False, False, "poleMatcher", (self.mocapPrefix +"RightArm", self.mocapPrefix +"RightForeArm_poleHelper", self.mocapPrefix +"RightHand")),
                "Right_Arm_IK":(self.mocapPrefix + "RightHand", True, True, False),
                
                #Right Fingers
                "Right_Thumb_1":(self.mocapPrefix + "RightHandThumb1", False, True),
                "Right_Thumb_2":(self.mocapPrefix + "RightHandThumb2", False, True),
                "Right_Thumb_3":(self.mocapPrefix + "RightHandThumb3", False, True),
                "TK_Right_HandRig_Thumb_Eff_Output":(self.mocapPrefix + "RightHandThumb4",),

                "Right_Index_Mtc":(self.mocapPrefix + "RightHandIndex0", False, True),
                "Right_Index_1":(self.mocapPrefix + "RightHandIndex1", False, True),
                "Right_Index_2":(self.mocapPrefix + "RightHandIndex2", False, True),
                "Right_Index_3":(self.mocapPrefix + "RightHandIndex3", False, True),
                "TK_Right_HandRig_Index_Eff_Output":(self.mocapPrefix + "RightHandIndex4",),
                
                "Right_Middle_Mtc":(self.mocapPrefix + "RightHandMiddle0", False, True),
                "Right_Middle_1":(self.mocapPrefix + "RightHandMiddle1", False, True),
                "Right_Middle_2":(self.mocapPrefix + "RightHandMiddle2", False, True),
                "Right_Middle_3":(self.mocapPrefix + "RightHandMiddle3", False, True),
                "TK_Right_HandRig_Middle_Eff_Output":(self.mocapPrefix + "RightHandMiddle4",),
                
                "Right_Ring_Mtc":(self.mocapPrefix + "RightHandRing0", False, True),
                "Right_Ring_1":(self.mocapPrefix + "RightHandRing1", False, True),
                "Right_Ring_2":(self.mocapPrefix + "RightHandRing2", False, True),
                "Right_Ring_3":(self.mocapPrefix + "RightHandRing3", False, True),
                "TK_Right_HandRig_Ring_Eff_Output":(self.mocapPrefix + "RightHandRing4",),
                
                "Right_Pinky_Mtc":(self.mocapPrefix + "RightHandPinky0", False, True),
                "Right_Pinky_1":(self.mocapPrefix + "RightHandPinky1", False, True),
                "Right_Pinky_2":(self.mocapPrefix + "RightHandPinky2", False, True),
                "Right_Pinky_3":(self.mocapPrefix + "RightHandPinky3", False, True),
                "TK_Right_HandRig_Pinky_Eff_Output":(self.mocapPrefix + "RightHandPinky4",),
                
                #Right HandProp
                #"Right_HandProp":(self.mocapPrefix + "Lf_HandProp_MCP_0_JNT", True, True, False),

                #Right Leg IK
                "Right_Leg_upV":(self.mocapPrefix + "RightLegPoleVector", True, False, False, "poleMatcher", (self.mocapPrefix +"RightUpLeg", self.mocapPrefix +"RightLeg_poleHelper", self.mocapPrefix +"RightFoot")),
                "Right_Leg_IK":(self.mocapPrefix + "RightFoot", True, True, False),
                "Right_IK_Tip":(self.mocapPrefix + "RightToeBase", True, True),
                
                #Right Leg FK
                "Right_Leg_FK_1":(self.mocapPrefix + "RightUpLeg", False, True),
                "Right_Leg_FK_2":(self.mocapPrefix + "RightLeg", False, True),
                "Right_Foot_FK_1":(self.mocapPrefix + "RightFoot", False, True),
                "Right_Foot_FK_2":(self.mocapPrefix + "RightToeBase", False, True),
                
                #"Right_Tip":(self.mocapPrefix + "Lf_Foot_MCP_2_JNT",),
           }
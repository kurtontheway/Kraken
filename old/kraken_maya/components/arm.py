from kraken.kraken_maya.utils import *
from kraken.kraken_maya.maths import *
from kraken.kraken_maya.maths import mathUtils
from kraken.kraken_maya.objects import elements
from kraken.kraken_maya.components.base import BaseComponent

from kraken.core.components import arm


class ArmComponent(arm.ArmComponent, BaseComponent):
    """Arm Rig Component"""

    def __init__(self, name, side="M", parent=None):
        super(ArmComponent, self).__init__(name, side=side, parent=parent)


    # ===============
    # Init Functions
    # ===============
    def initDataFromGuide(self, inputGuide):
        """Initilizes component data from the input guide.

        Arguments:
        inputGuide -- Object, Scene object that is the parent of the guide.

        Return:
        True if successful.

        """

        bicepGdSrt = inputGuide.findChild("bicep_" + self.side + "_gdSrt").object3D
        forearmGdSrt = inputGuide.findChild("forearm_" + self.side + "_gdSrt").object3D
        wristGdSrt = inputGuide.findChild("wrist_" + self.side + "_gdSrt").object3D

        if bicepGdSrt is None or forearmGdSrt is None or wristGdSrt is None:
            raise ValueError("Could not locate all guide srt's!")


        self.positions[0] = Vec3(bicepGdSrt.getTranslation(space='world')[0],
                                 bicepGdSrt.getTranslation(space='world')[1],
                                 bicepGdSrt.getTranslation(space='world')[2])

        self.positions[1] = Vec3(forearmGdSrt.getTranslation(space='world')[0],
                                 forearmGdSrt.getTranslation(space='world')[1],
                                 forearmGdSrt.getTranslation(space='world')[2])

        self.positions[2] = Vec3(wristGdSrt.getTranslation(space='world')[0],
                                 wristGdSrt.getTranslation(space='world')[1],
                                 wristGdSrt.getTranslation(space='world')[2])

        return True


    # ======================
    # Guide Build Functions
    # ======================
    def _preBuildGuide(self):
        """Pre-build Guide operations.

        Return:
        True if successful.

        """

        super(ArmComponent, self)._preBuildGuide()

        return


    def _buildGuide(self):
        """Builds the component guide in the DCC.

        Return:
        True if successful.

        """

        self.guide = elements.Group(self.name.split("_")[0] + "_" + self.side + "_guide_hrc", parent=None)

        bicepGdSrt = elements.Null("bicep_" + self.side + "_gdSrt", parent=self.guide)

        if self.side == "L":
            bicepGdSrt.xfo.rot.set(Vec3(0.0, 0.0, -0.38268343236508984), 0.9238795325112867)
            bicepGdSrt.xfo.tr.set(5.0, 20.0, 0.0)
        elif self.side == "R":
            bicepGdSrt.xfo.rot.set(Vec3(0.9238795325112867, 0.38268343236508984, -3.313870358775352e-17), 8.000390764101651e-17)
            bicepGdSrt.xfo.tr.set(-5.0, 20.0, 0.0)

        forearmGdSrt = elements.Null("forearm_" + self.side + "_gdSrt", parent=bicepGdSrt)

        if self.side == "L":
            forearmGdSrt.xfo.rot.set(Vec3(0.0, 0.0, -0.38268343236508995), 0.9238795325112866)
            forearmGdSrt.xfo.tr.set(8.535533905932736, 16.46446609406726, -2.5)
        elif self.side == "R":
            forearmGdSrt.xfo.rot.set(Vec3(0.9238795325112867, 0.38268343236508984, 8.00039076410165e-17), 3.3138703587753523e-17)
            forearmGdSrt.xfo.tr.set(-8.535533905932736, 16.46446609406726, -2.5)

        wristGdSrt = elements.Null("wrist_" + self.side + "_gdSrt", parent=forearmGdSrt)

        if self.side == "L":
            wristGdSrt.xfo.rot.set(Vec3(0.0, 0.0, -0.38268343236508995), 0.9238795325112866)
            wristGdSrt.xfo.tr.set(12.071067811865474, 12.92893218813452, 0.0)
        elif self.side == "R":
            wristGdSrt.xfo.rot.set(Vec3(0.9238795325112867, 0.38268343236508984, 8.000390764101648e-17), 3.313870358775353e-17)
            wristGdSrt.xfo.tr.set(-12.071067811865474, 12.92893218813452, 0.0)

        self.guide.build()

        return


    def _postBuildGuide(self):
        """Post-build operations.

        Return:
        True if successful.

        """

        super(ArmComponent, self)._postBuildGuide()

        return


    # ==========================
    # Component Build Functions
    # ==========================
    def _build(self):
        """Internal build function for building the component in Softimage."""

        super(ArmComponent, self)._build()

        # ====================
        # Calculate positions
        # ====================
        self.getComponentXfo()
        self.getUpVXfo()
        self.getBoneData()

        # =================
        # Find Hierarchies
        # =================
        ioHrc = self.findChild("arm_io_hrc")
        ctrlHrc = self.findChild("arm_ctrl_hrc")
        armatureHrc = self.findChild("arm_armature_hrc")

        # ============
        # Setup Ctrls
        # ============

        # Setup Hierarchy
        ioHrc.addAttributeGroup("DisplayInfo_Arm_Settings")
        ioHrc.addAttribute("float", "bone1Len", self.boneData["bicep"]["length"], minValue=0.0, maxValue=100.0, group="DisplayInfo_Arm_Settings")
        ioHrc.addAttribute("float", "bone2Len", self.boneData["forearm"]["length"], minValue=0.0, maxValue=100.0, group="DisplayInfo_Arm_Settings")
        ioHrc.addAttribute("float", "fkik", 1.0, minValue=0.0, maxValue=1.0, group="DisplayInfo_Arm_Settings")
        ioHrc.addAttribute("float", "softDist", 0.5, minValue=0.0, maxValue=1.0, group="DisplayInfo_Arm_Settings")
        ioHrc.addAttribute("bool", "softIK", True, group="DisplayInfo_Arm_Settings")
        ioHrc.addAttribute("bool", "stretch", True, group="DisplayInfo_Arm_Settings")
        ioHrc.addAttribute("float", "stretchBlend", 1.0, minValue=0.0, maxValue=1.0, group="DisplayInfo_Arm_Settings")
        ioHrc.addAttribute("bool", "rightSide", self.side == "R", group="DisplayInfo_Arm_Settings")
        ioHrc.addAttribute("bool", "toggleDebugging", True, group="DisplayInfo_Arm_Settings")

        # Creat Inputs
        clavicleKineIn = elements.Null("arm_" + self.side + "_clavicle_kineIn", parent=ioHrc)
        clavicleKineIn.setGlobalTranslation(self.positions[0])

        # Create Controls
        ikHandleZero = elements.Group("arm_" + self.side + "_ikHandle_ctrl_zero", parent=ctrlHrc)
        ikHandleZero.setLocalTranslation(self.boneData["wrist"]["xfo"].tr)

        ikHandleCtrl = elements.Control("arm_" + self.side + "_ikHandle_ctrl", "pin", parent=ikHandleZero)
        ikHandleCtrl.setLocalTranslation(Vec3(0,0,0))
        ikHandleCtrl.color = self.ctrlColor
        ikHandleCtrl.rotOffset = [-90,0,0]
        ikHandleCtrl.sclOffset = [1.5,1.5,1.5]

        upVZero = elements.Group("arm_" + self.side + "_upV_ctrl_zero", parent=ctrlHrc)
        upVZero.setLocalTranslation(self.upVXfo.tr)

        upVCtrl = elements.Control("arm_" + self.side + "_upV_ctrl", "triangle", parent=upVZero)
        upVCtrl.setLocalTranslation(Vec3(0,0,0))
        upVCtrl.color = self.ctrlColor
        upVCtrl.rotOffset = [0,-90,0]
        upVCtrl.posOffset = [0,0,-1]

        bicepFKZero = elements.Group("arm_" + self.side + "_bicepFK_ctrl_zero", parent=ctrlHrc)
        bicepFKZero.setLocalTranslation(self.boneData["bicep"]["xfo"].tr)
        bicepFKZero.setGlobalRotation(self.boneData["bicep"]["xfo"].rot)

        bicepFKCtrl = elements.Control("arm_" + self.side + "_bicepFK_ctrl", "cubeXAligned", parent=bicepFKZero)
        bicepFKCtrl.setLocalTranslation(Vec3(0,0,0))
        bicepFKCtrl.color = self.ctrlColor
        bicepFKCtrl.sclOffset = [self.boneData["bicep"]["length"] * self.sideScale,1,1]

        forearmFKZero = elements.Group("arm_" + self.side + "_forearmFK_ctrl_zero", parent=bicepFKCtrl)
        forearmFKZero.setGlobalTranslation(self.boneData["forearm"]["xfo"].tr)
        forearmFKZero.setGlobalRotation(self.boneData["forearm"]["xfo"].rot)

        forearmFKCtrl = elements.Control("arm_" + self.side + "_forearmFK_ctrl", "cubeXAligned", parent=forearmFKZero)
        forearmFKCtrl.setLocalTranslation(Vec3(0,0,0))
        forearmFKCtrl.color = self.ctrlColor
        forearmFKCtrl.sclOffset = [self.boneData["forearm"]["length"] * self.sideScale,1,1]

        # Setup SRTs
        bicepKineOut = elements.Null("arm_" + self.side + "_bicep_kineOut", parent=ioHrc)
        bicepKineOut.setLocalTranslation(self.boneData["bicep"]["xfo"].tr)
        bicepKineOut.setGlobalRotation(self.boneData["bicep"]["xfo"].rot)

        forearmKineOut = elements.Null("arm_" + self.side + "_forearm_kineOut", parent=ioHrc)
        forearmKineOut.setLocalTranslation(self.boneData["forearm"]["xfo"].tr)
        forearmKineOut.setGlobalRotation(self.boneData["forearm"]["xfo"].rot)

        wristKineOut = elements.Null("arm_" + self.side + "_wrist_kineOut", parent=ioHrc)
        wristKineOut.setLocalTranslation(self.boneData["wrist"]["xfo"].tr)
        wristKineOut.setGlobalRotation(self.boneData["wrist"]["xfo"].rot)

        # ===============
        # Setup Armature
        # ===============

        # Setup Joints
        bicepJnt = elements.Joint("arm_" + self.side + "_bicep_jnt", parent=armatureHrc)
        bicepJnt.setLocalTranslation(Vec3(0,0,0))
        bicepJnt.setGlobalRotation(self.boneData["bicep"]["xfo"].rot)
        bicepJnt.addConstraint("bicepJntToKineOut", "pose", [bicepKineOut])

        forearmJnt = elements.Joint("arm_" + self.side + "_forearm_jnt", parent=armatureHrc)
        forearmJnt.setLocalTranslation(Vec3(4,0,-3))
        forearmJnt.setGlobalRotation(self.boneData["forearm"]["xfo"].rot)
        forearmJnt.addConstraint("forearmJntToKineOut", "pose", [forearmKineOut])

        wristJnt = elements.Joint("arm_" + self.side + "_wrist_jnt", parent=armatureHrc)
        wristJnt.setLocalTranslation(Vec3(8,0,0))
        wristJnt.setGlobalRotation(self.boneData["wrist"]["xfo"].rot)
        wristJnt.addConstraint("wristJntToKineOut", "pose", [wristKineOut])

        return


    def _postBuild(self):

        super(ArmComponent, self)._postBuild()
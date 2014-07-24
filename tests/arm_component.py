from kraken.core.maths import *

from kraken.core.objects.attributes.float_attribute import FloatAttribute
from kraken.core.objects.attributes.integer_attribute import IntegerAttribute
from kraken.core.objects.attributes.bool_attribute import BoolAttribute
from kraken.core.objects.attributes.string_attribute import StringAttribute

from kraken.core.objects.constraints.pose_constraint import PoseConstraint

from kraken.core.objects.components.base_component import BaseComponent

from kraken.core.objects.locator import Locator

from kraken.core.objects.controls.cube_control import CubeControl
from kraken.core.objects.controls.circle_control import CircleControl
from kraken.core.objects.controls.square_control import SquareControl
from kraken.core.objects.controls.null_control import NullControl

from kraken.core.objects.operators.splice_operator import SpliceOperator


class ArmComponent(BaseComponent):
    """Arm Component Test"""

    def __init__(self, name, parent=None, side='M'):
        super(ArmComponent, self).__init__(name, parent, side)

        # Setup component attributes
        defaultAttrGroup = self.getAttributeGroupByIndex(0)
        defaultAttrGroup.addAttribute(BoolAttribute("toggleDebugging", True))

        # Add Guide Controls
        bicepGuideCtrl = CubeControl('bicepGuideCtrl')
        bicepGuideCtrl.rotatePoints(45.0, 0, 0)
        bicepGuideCtrl.xfo.tr = Vec3(5.0, 20.0, 0.0)
        bicepGuideCtrl.setColor("greenBright")
        self.addChild(bicepGuideCtrl)

        forearmGuideCtrl = CubeControl('forearmGuideCtrl')
        forearmGuideCtrl.xfo.tr = Vec3(8.5, 16.4, -2.5)
        forearmGuideCtrl.setColor("greenBright")
        self.addChild(forearmGuideCtrl)

        wristGuideCtrl = CubeControl('wristGuideCtrl')
        wristGuideCtrl.xfo.tr = Vec3(12.0, 12.9, 0.0)
        wristGuideCtrl.setColor("greenBright")
        self.addChild(wristGuideCtrl)


        # Setup component Xfo I/O's
        clavicleEndInput = Locator('clavicleEnd')
        armEndOutput = Locator('armEnd')

        # Setup componnent Attribute I/O's
        armFollowBodyInputAttr = FloatAttribute('followBody', 0.0, 0.0, 1.0)

        # Constraint outputs
        armEndOutputConstraint = PoseConstraint('_'.join([armEndOutput.getName(), 'To', wristGuideCtrl.getName()]))
        armEndOutputConstraint.addConstrainer(wristGuideCtrl)
        armEndOutput.addConstraint(armEndOutputConstraint)

        # Add Xfo I/O's
        self.addInput(clavicleEndInput)
        self.addOutput(armEndOutput)

        # Add Attribute I/O's
        self.addInput(armFollowBodyInputAttr)


        # Add Splice Op
        spliceOp = SpliceOperator("armSpliceOp", "ArmSolver", "extension")
        spliceOp.setInput("armRoot_input", clavicleEndInput)
        spliceOp.setInput("followClav_input", armFollowBodyInputAttr)
        spliceOp.setInput("wrist_output", armEndOutput)
        self.addOperator(spliceOp)

        # Think about how to add multiple operators to the SpliceOp
        # armSolveKLOp = spliceOp.AddKLOp("armSolve")
        # armDebugKLOp = spliceOp.AddKLOp("armDebug")
        # klOp.appendInput


    def buildRig(self, parent):
        pass


if __name__ == "__main__":
    armLeft = ArmComponent("myArm", side='L')
    print armLeft.getNumChildren()
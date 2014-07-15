from kraken.core.maths import *

from kraken.core.objects.attributes.float_attribute import FloatAttribute
from kraken.core.objects.attributes.bool_attribute import BoolAttribute
from kraken.core.objects.attributes.string_attribute import StringAttribute

from kraken.core.objects.component import BaseComponent
from kraken.core.objects.component_input import ComponentInput
from kraken.core.objects.component_output import ComponentOutput

from kraken.core.objects.controls.cube_control  import CubeControl
from kraken.core.objects.controls.circle_control  import  CircleControl
from kraken.core.objects.controls.square_control  import  SquareControl
from kraken.core.objects.controls.null_control  import  NullControl


class ArmComponent(BaseComponent):
    """Arm Component Test"""

    def __init__(self, name, parent=None, side='M'):
        super(ArmComponent, self).__init__(name, parent, side)

        self.addInput(ComponentInput('armParent'))
        self.addOutput(ComponentInput('wrist'))


        defaultAttrGroup = self.getAttributeGroupByName("")

        # Setup component attributes
        defaultAttrGroup.addAttribute(BoolAttribute("toggleDebugging", True))

        # Add Guide Controls
        bicepGuideCtrl = NullControl('bicepGuideCtrl')
        bicepGuideCtrl.xfo.tr = Vec3(5.0, 20.0, 0.0)
        self.addChild(bicepGuideCtrl)

        forearmGuideCtrl = NullControl('forearmGuideCtrl')
        forearmGuideCtrl.xfo.tr = Vec3(8.5, 16.4, -2.5)
        self.addChild(forearmGuideCtrl)

        wristGuideCtrl = NullControl('wristGuideCtrl')
        wristGuideCtrl.xfo.tr = Vec3(12.0, 12.9, 0.0)
        self.addChild(wristGuideCtrl)

        # Guide Splice Op Code
        guideSpliceOps = []

        guideSpliceCode = """
          drawLine(bicep.tr, forearm.tr, Color(1.0, 0.0, 0.0));
          drawLine(forearm.tr, wrist.tr, Color(1.0, 0.0, 0.0));

        """

    def buildRig(self, parent):

        # component = super(ArmComponent, self).buildRig()
        component = BaseComponent(self.getName(), parent, self.getSide())

        # Setup component attributes
        component.addAttribute(FloatAttribute("bone1Len", 1.0, minValue=0.0, maxValue=100.0))
        component.addAttribute(FloatAttribute("bone2Len", 1.0, minValue=0.0, maxValue=100.0))
        component.addAttribute(FloatAttribute("fkik", 1.0, minValue=0.0, maxValue=1.0))
        component.addAttribute(FloatAttribute("softDist", 0.5, minValue=0.0, maxValue=1.0))
        component.addAttribute(BoolAttribute("softIK", True))
        component.addAttribute(BoolAttribute("stretch", True))
        component.addAttribute(FloatAttribute("stretchBlend", 1.0, minValue=0.0, maxValue=1.0))
        component.addAttribute(StringAttribute("Side", self.side))
        component.addAttribute(BoolAttribute("toggleDebugging", True))


        bicepGuideCtrl = self.getChildByName('bicepGuideCtrl')
        forearmGuideCtrl = self.getChildByName('forearmGuideCtrl')
        wristGuideCtrl = self.getChildByName('wristGuideCtrl')


        # Math here...


        # Add Rig Controls
        bicepFKCtrl = SquareControl('bicepFKCtrl', parent=self)
        bicepFKCtrl.xfo = bicepGuideCtrl.xfo
        self.addChild(bicepFKCtrl)

        forearmFKCtrl = NullControl('forearmFKCtrl', parent=self)
        forearmFKCtrl.xfo = forearmGuideCtrl.xfo
        self.addChild(forearmFKCtrl)

        wristIKCtrl = CircleControl('wristIKCtrl', parent=self)
        wristIKCtrl.xfo = wristGuideCtrl.xfo
        self.addChild(wristIKCtrl)

        # componentSpliceCode = """require Math;"""

        return container


if __name__ == "__main__":
    armLeft = ArmComponent("myArm", side='L')
    print armLeft.getNumChildren()
import os
import sys
import optparse

from kraken import plugins
from kraken.core.kraken_system import KrakenSystem
from kraken.core.objects.locator import Locator
from kraken.core.objects.rig import Rig
from kraken.core.configs.config import Config

def argOpts():

    prog = os.path.basename(__file__)
    usage = "usage: %prog krg_file output_directory [options]"
    parser = optparse.OptionParser(usage, version="%prog 1.0")

    parser.add_option("-c", "--config", dest="config",
            help="Create the directory structure of a new asset locally.")

    description = optparse.OptionGroup(parser, "Description", "Generate a kl character from krg input")

    parser.add_option_group(description)


    options, args = parser.parse_args()

    options.name = None
    if len(args) != 2:
        print "\nPlease provide the rig file to convert and the target folder as command line arguments."
        exit(1)

    if options.config and not os.path.isfile(options.config):
        print "\nCannot read config file path [%s]" % options.config
        exit(1)

    return (options, args)


def main():

    os.environ['KRAKEN_DCC'] = 'KL'

    options, args  = argOpts()

    ks = KrakenSystem.getInstance()
    numConfigs = len(ks.registeredConfigs)

    if options.config:
        directory, file = os.path.split(options.config)
        filebase, ext = os.path.splitext(file)
        sys.path = [directory] + sys.path # prepend
        exec("import "+filebase)

        if len(ks.registeredConfigs) > numConfigs:
            configName = next(reversed(ks.registeredConfigs))
            print ("Using config %s from %s" % (configName, options.config))
            ks.getConfigClass(configName).makeCurrent()

        else:
            print ("Failed to use config in %s" % options.config)
            exit()

    guideRig = Rig()
    guideRig.loadRigDefinitionFile(args[0])

    rig = Rig()
    rig.loadRigDefinition(guideRig.getRigBuildData())

    builder = plugins.getBuilder()
    builder.setOutputFolder(args[1])

    config = builder.getConfig()

    config.setMetaData('RigTitle', os.path.split(args[0])[1].partition('.')[0])
    config.setMetaData('SetupDebugDrawing', True)
    config.setMetaData('CollapseComponents', False)
    config.setMetaData('AddCollectJointsNode', True)

    builder.build(rig)

if __name__ == "__main__":
    main()
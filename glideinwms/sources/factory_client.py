import argparse
import pprint
import pandas

from decisionengine_modules.htcondor.sources import source


PRODUCES = ['factoryclient_manifests']


class FactoryClientManifests(source.ResourceManifests):

    def __init__(self, config):
        super(FactoryClientManifests, self).__init__(config)
        self.constraint = '(%s)&&(glideinmytype=="glidefactoryclient")' % self.constraint
        self.subsystem_name = 'any'


    def produces(self):
        """
        Return list of items produced
        """
        return PRODUCES


    def acquire(self):
        return {PRODUCES[0]: self.load()}


def module_config_template():
    """
    Print template for this module configuration
    """

    template = {
        'factoryclient_manifests': {
            'module': 'modules.htcondor.s_factory_client',
            'name': 'StartdManifests',
            'parameters': {
                'collector_host': 'factory_collector.com',
                'condor_config': '/path/to/condor_config',
                'constraints': 'HTCondor collector query constraints',
                'classad_attrs': [],
            }
        }
    }
    print('Entry in channel configuration')
    pprint.pprint(template)


def module_config_info():
    """
    Print module information
    """
    print('produces %s' % PRODUCES)
    module_config_template()


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--configtemplate',
        action='store_true',
        help='prints the expected module configuration')

    parser.add_argument(
        '--configinfo',
        action='store_true',
        help='prints config template along with produces and consumes info')
    args = parser.parse_args()

    if args.configtemplate:
        module_config_template()
    elif args.configinfo:
        module_config_info()
    else:
        pass


if __name__ == '__main__':
    main()

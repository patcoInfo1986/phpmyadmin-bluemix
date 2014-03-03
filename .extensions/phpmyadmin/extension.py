"""PHPMyAdmin Extension

Downloads, installs and configures PHPMyAdmin
"""
import os
import os.path
import logging
from build_pack_utils import Downloader
from build_pack_utils import utils


_log = logging.getLogger('phpmyadmin')


DEFAULTS = utils.FormattedDict({
    'PHPMYADMIN_VERSION': '4.1.8',
    'PHPMYADMIN_URL': 'http://sourceforge.net/projects/phpmyadmin/'
                      'files/phpMyAdmin/{PHPMYADMIN_VERSION}/'
                      'phpMyAdmin-{PHPMYADMIN_VERSION}-english.tar.gz'
                      '/download#',
    'PHPMYADMIN_HASH': 'a2d00654347bcba2731e24f0358df069e57fc12b'
})

# Extension Methods
def preprocess_commands(ctx):
    return ()


def service_commands(ctx):
    return {}


def service_environment(ctx):
    return {}


def compile(install):
    print 'Installing PHPMyAdmin %s' % DEFAULTS['PHPMYADMIN_VERSION']
    ctx = install.builder._ctx
    inst = install._installer
    workDir = os.path.join(ctx['TMPDIR'], 'phpmyadmin')
    inst.install_binary_direct(
        DEFAULTS['PHPMYADMIN_URL'],
        DEFAULTS['PHPMYADMIN_HASH'],
        workDir, strip=True)
    (install.builder.
        .move()
        .everything()
        .under('{BUILD_DIR}/htdocs')
        .into(workDir)
        .done())
    (install.builder.
        .move()
        .everything()
        .under(workDir)
        .info('{BUILD_DIR}/htdocs')
        .done())
    os.rmdir(workDir) # make sure we moved everything
    return 0

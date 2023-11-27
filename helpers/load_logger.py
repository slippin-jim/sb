#!/Users/jim/anaconda3/envs/sb/bin/python
import sys
import time
import os
import logging

def main(arg):
    base_dir = os.path.abspath(os.path.pardir)
    log_path = os.path.join(base_dir,'logs')

    logging.basicConfig(filename=f"{log_path}/init_load.log",
                        format='%(asctime)s %(message)s',
                        filemode='a')
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    if arg == 'start':
        logger.debug('started')
    elif arg == 'completed':
        logger.debug('completed')
    else:
        logger.debug('hit error')

if __name__ == '__main__':
    main(sys.argv[1])
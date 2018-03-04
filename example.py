#!/usr/bin/python3

import logging
import distlog

logger = logging.getLogger()
handler = distlog.ZmqHandler('tcp://localhost:5010')
handler.setFormatter(distlog.JSONFormatter())
logger.addHandler(handler)
logger.setLevel(logging.INFO)

def main():
    with distlog.task('toplevel') as job:
        print('into task')
        logger.info('into task')
        with distlog.to('subtask') as job:
            print('into subtask')
            logger.info('into task')
            job.success('subtask done')
    print('all done')
    logger.info('all done')

if __name__ == '__main__':
    main()

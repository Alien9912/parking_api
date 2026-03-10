import sys
import logging
import logging.config
from dict_config import dict_config
from utils import string_to_operator
import logging_tree

logging.config.dictConfig(dict_config)
logger = logging.getLogger('app')

def calc(args):
    logger.info(f"Arguments: {args}")

    num_1 = args[0]
    operator = args[1]
    num_2 = args[2]

    try:
        num_1 = float(num_1)
    except ValueError as e:
        logger.error("Error while converting number 1")
        logger.exception(e)

    try:
        num_2 = float(num_2)
    except ValueError as e:
        logger.error("Error while converting number 2")
        logger.exception(e)

    operator_func = string_to_operator(operator)

    result = operator_func(num_1, num_2)

    logger.info(f"Result: {result}")
    logger.info(f"{num_1} {operator} {num_2} = {result}")

if __name__ == '__main__':
    with open('logging_tree.txt', 'w', encoding='utf-8') as f:
        f.write(logging_tree.format.build_description())

    # calc(sys.argv[1:])
    calc('2+3')
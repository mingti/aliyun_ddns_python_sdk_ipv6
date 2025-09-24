import logging

logger = logging.getLogger('ddns')

log_file_path = "./ddns.log"



logger.setLevel(logging.INFO)
# 处理器 - 输出目的地
consoleHandler = logging.StreamHandler()
consoleHandler.setLevel(logging.INFO)

fileHandler = logging.FileHandler(filename=log_file_path)  # 没有指定日志级别，将使用logger的级别

# formatter格式
formatter = logging.Formatter(fmt="%(asctime)s|%(levelname)s|%(filename)s:%(lineno)s|%(message)s")

# 给处理器设置格式
consoleHandler.setFormatter(formatter)
fileHandler.setFormatter(formatter)

# 记录器要设置处理器

logger.addHandler(consoleHandler)
logger.addHandler(fileHandler)


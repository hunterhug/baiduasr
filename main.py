# -*- coding:utf-8 -*-
from aip import AipSpeech
import json, os, csv, traceback, sys
import tool.log, logging
from tool.jfile import file
import concurrent.futures

APP_ID = ''
API_KEY = ''
SECRET_KEY = ''
ASR_DIR = './dir'
RESULT_DIR = './result'
RESULT_FILE = './result.csv'
PROCESS = 2
tool.log.setup_logging()
logger = logging.getLogger(__name__)


def init_config(filename):
    global APP_ID, API_KEY, SECRET_KEY, ASR_DIR, RESULT_DIR, RESULT_FILE, PROCESS
    try:
        doc = open(filename, 'rb')
        doc_content = doc.read().decode('utf-8', 'ignore')
        config = json.loads(doc_content)
        APP_ID = config['appId']
        API_KEY = config['appKey']
        SECRET_KEY = config['appSecret']
        ASR_DIR = config['asrDir']
        RESULT_DIR = config['resultDir']
        RESULT_FILE = config['resultFile']
        PROCESS = config['process']
        logger.info('Config: %s', config)
    except Exception as e:
        logger.error(traceback.print_exc())
        exit(1)


def new_baidu_asr_client(id, key, secret):
    client = AipSpeech(id, key, secret)
    client.setConnectionTimeoutInMillis(60.0 * 1000)
    client.setSocketTimeoutInMillis(60.0 * 1000)
    logger.info('Baidu ASR PythonSDK version: %s', client.getVersion())
    return client


def list_files(rootdir):
    files = []
    for parent, dirnames, filenames in os.walk(rootdir):
        if parent == rootdir:
            for filename in filenames:
                if filename.endswith('.wav') or filename.endswith('pcm'):
                    files.append(filename)
            return files
        else:
            pass


def list_result_files(rootdir):
    files = []
    for parent, dirnames, filenames in os.walk(rootdir):
        if parent == rootdir:
            for filename in filenames:
                if filename.endswith('txt'):
                    files.append(filename)
            return files
        else:
            pass


def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()


# 1536	普通话(支持简单的英文识别)	搜索模型	无标点	支持自定义词库
# 1537	普通话(纯中文识别)	输入法模型	有标点	不支持自定义词库
# 1737	英语		有标点	不支持自定义词库
# 1637	粤语		有标点	不支持自定义词库
# 1837	四川话		有标点	不支持自定义词库
# 1936
def deal_files(index, files, asr_dir, result_dir):
    client = new_baidu_asr_client(APP_ID, API_KEY, SECRET_KEY)
    len_files = len(files)
    logger.debug('%d=total: %d', index, len_files)

    i = 0
    for f in files:
        logger.info('%d=done:%d, remain:%d', index, i, len_files - i)
        i = i + 1

        origin = asr_dir + '/' + f
        txt = result_dir + '/' + f + '.txt'

        if os.path.exists(txt):
            logger.debug('%d=exist-%s,%s', index, origin, txt)
            continue

        result = {}

        try:
            if f.endswith('wav'):
                result = client.asr(get_file_content(origin), 'wav', 16000, {'dev_pid': 1536})
            elif f.endswith('pcm'):
                result = client.asr(get_file_content(origin), 'pcm', 16000, {'dev_pid': 1536})
            else:
                logger.error('%d=not support type: %s', index, f)
                continue
            if result['err_no'] != 0:
                logger.error('%d=err-%s,%s', index, origin, result)
            else:
                raw = '+'.join(result['result'])
                txt_f = open(txt, 'wb')
                txt_f.write(raw.encode('utf-8'))
                txt_f.close()

                logger.info('%d=success-%s,%s', index, origin, raw)
                logger.debug('%d=writein-%s,%s', index, origin, txt)
        except Exception as e:
            logger.error(traceback.print_exc())
            continue


def merge_csv(result_dir, result_file):
    files = list_result_files(result_dir)
    files.sort()
    csvFile = open(result_file, 'w')
    writer2 = csv.writer(csvFile)
    for f in files:
        try:
            origin = result_dir + '/' + f
            raw_file = open(origin, 'rb')
            txt = raw_file.read().decode('utf-8', 'ignore')
            raw_file.close()
            real_file = f.replace('.txt', '')
            logger.debug('%s write: %s', real_file, txt)
            writer2.writerow([real_file, txt])
        except Exception as e:
            logger.error(traceback.print_exc())
            continue
    csvFile.close()
    logger.info('csv in %s', result_file)


def main():
    files = list_files(ASR_DIR)
    devide_files = file.devidelist(files, PROCESS)
    futures = set()
    with concurrent.futures.ProcessPoolExecutor(PROCESS) as executor:
        for index in devide_files:
            future = executor.submit(deal_files, index, devide_files[index], ASR_DIR, RESULT_DIR)
            futures.add(future)
    try:
        for future in concurrent.futures.as_completed(futures):
            err = future.exception()
            if err is not None:
                raise err
    except KeyboardInterrupt:
        logger.error("stopped by hand")


if __name__ == '__main__':
    init_config('./config/config.json')
    os.makedirs(RESULT_DIR, 0o777, True)
    if len(sys.argv) > 1:
        if sys.argv[1] == 'csv':
            merge_csv(RESULT_DIR, RESULT_FILE)
            exit(1)
            logger.error('only csv can choose!')
        exit(1)

    logger.info('start!!!!!!!')
    main()
    merge_csv(RESULT_DIR, RESULT_FILE)

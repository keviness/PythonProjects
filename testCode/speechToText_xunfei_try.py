import base64
import hashlib
import hmac
import json
import os
import time
import requests

# 请求的接口名
api_prepare = '/prepare'
api_upload = '/upload'
api_merge = '/merge'
api_get_progress = '/getProgress'
api_get_result = '/getResult'
# 文件分片大小10M
file_piece_sice = 10485760
pre_slice_id = 'aaaaaaaaa`'

lfasr_host = 'http://raasr.xfyun.cn/api'
appid = '5f368b48'
secret_key = 'd60ab1681c013a265ee6858bef330d97'
upload_file_path = r"cold.wav"

def getNextSliceId():
    global pre_slice_id
    ch = pre_slice_id
    j = len(ch) - 1
    while j >= 0:
        cj = ch[j]
        if cj != 'z':
            ch = ch[:j] + chr(ord(cj) + 1) + ch[j + 1:]
            break
        else:
            ch = ch[:j] + 'a' + ch[j + 1:]
            j = j - 1
    pre_slice_id = ch;
    return pre_slice_id

# 根据不同的apiname生成不同的参数,本示例中未使用全部参数您可在官网(https://doc.xfyun.cn/rest_api/%E8%AF%AD%E9%9F%B3%E8%BD%AC%E5%86%99.html)查看后选择适合业务场景的进行更换
def gene_params(apiname, taskid=None, slice_id=None):
    ts = str(int(time.time()))
    m2 = hashlib.md5()
    m2.update((appid + ts).encode('utf-8'))
    md5 = m2.hexdigest()
    md5 = bytes(md5, encoding='utf-8')
    # 以secret_key为key, 上面的md5为msg， 使用hashlib.sha1加密结果为signa
    signa = hmac.new(secret_key.encode('utf-8'), md5, hashlib.sha1).digest()
    signa = base64.b64encode(signa)
    signa = str(signa, 'utf-8')
    file_len = os.path.getsize(upload_file_path)
    file_name = os.path.basename(upload_file_path)
    param_dict = {}

    if apiname == api_prepare:
        # slice_num是指分片数量，如果您使用的音频都是较短音频也可以不分片，直接将slice_num指定为1即可
        slice_num = int(file_len / file_piece_sice) + (0 if (file_len % file_piece_sice == 0) else 1)
        param_dict['app_id'] = appid
        param_dict['signa'] = signa
        param_dict['ts'] = ts
        param_dict['file_len'] = str(file_len)
        param_dict['file_name'] = file_name
        param_dict['slice_num'] = str(slice_num)
    elif apiname == api_upload:
        param_dict['app_id'] = appid
        param_dict['signa'] = signa
        param_dict['ts'] = ts
        param_dict['task_id'] = taskid
        param_dict['slice_id'] = slice_id
    elif apiname == api_merge:
        param_dict['app_id'] = appid
        param_dict['signa'] = signa
        param_dict['ts'] = ts
        param_dict['task_id'] = taskid
        param_dict['file_name'] = file_name
    elif apiname == api_get_progress or apiname == api_get_result:
        param_dict['app_id'] = appid
        param_dict['signa'] = signa
        param_dict['ts'] = ts
        param_dict['task_id'] = taskid
    return param_dict

# 请求和结果解析，结果中各个字段的含义可参考：https://doc.xfyun.cn/rest_api/%E8%AF%AD%E9%9F%B3%E8%BD%AC%E5%86%99.html
def gene_request(apiname, data, files=None, headers=None):
    response = requests.post(lfasr_host + apiname, data=data, files=files, headers=headers)
    result = json.loads(response.text)
    if result["ok"] == 0:
        #print("{} success:".format(apiname) + str(result))
        return result
    else:
        print("{} error:".format(apiname) + str(result))
        exit(0)
        return result

# 预处理
def prepare_request():
    data = gene_params(api_prepare)
    return gene_request(apiname=api_prepare, data=data)

# 上传
def upload_request(taskid, upload_file_path):
    file_object = open(upload_file_path, 'rb')
    try:
        index = 1
        while True:
            content = file_object.read(file_piece_sice)
            if not content or len(content) == 0:
                break
            files = {
                "filename": gene_params(api_upload).get("slice_id"),
                "content": content
            }
            data = gene_params(api_upload, taskid=taskid, slice_id=getNextSliceId())

            response = gene_request(api_upload, data=data, files=files)
            if response.get('ok') != 0:
                # 上传分片失败，退出
                print('upload slice fail, response: ' + str(response))
                return False
            print('upload slice ' + str(index) + ' success')
            index += 1

    finally:
        'file index:' + str(file_object.tell())
        file_object.close()
    return True

# 合并
def merge_request(taskid):
    data = gene_params(api_merge, taskid=taskid)
    return gene_request(api_merge, data=data)

# 获取进度
def get_progress_request(taskid):
    data = gene_params(api_get_progress, taskid=taskid)
    return gene_request(api_get_progress, data=data)

# 获取结果
def get_result_request(taskid):
    data = gene_params(api_get_result, taskid=taskid)

    response = gene_request(api_get_result, data=data)
    result_list_dict = eval(response['data'])
    #print(result_list_dict)
    result_list = []
    for element in result_list_dict:
        print(element)
        result_list.append(element['onebest'])
        print(element['onebest'])
    print(result_list)

def main():
    # 1. 预处理
    pre_result = prepare_request()
    taskid = pre_result["data"]
    # 2 . 分片上传
    upload_request(taskid=taskid, upload_file_path=upload_file_path)
    # 3 . 文件合并
    merge_request(taskid=taskid)
    # 4 . 获取任务进度
    while True:
        # 每隔20秒获取一次任务进度
        progress = get_progress_request(taskid)
        progress_dic = progress
        if progress_dic['err_no'] != 0 and progress_dic['err_no'] != 26605:
            print('task error: ' + progress_dic['failed'])
            return
        else:
            data = progress_dic['data']
            task_status = json.loads(data)
            if task_status['status'] == 9:
                print('task ' + taskid + ' finished')
                break
            print('The task ' + taskid + ' is in processing, task status: ' + str(data))

        # 每次获取进度间隔20S
        time.sleep(20)
    # 5 . 获取结果
    get_result_request(taskid=taskid)

# 输入讯飞开放平台的appid，secret_key和待转写的文件路径
if __name__ == '__main__':
    main()
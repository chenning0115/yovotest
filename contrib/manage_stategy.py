import os, sys
from contrib import taskdb



def check_pid_SCUEESE(self, pid):
    return True

def check_pid_FAILED(self, pid):
    return True

# 检查runnning状态的任务状态
def check_running_status():
    info_list = taskdb.task_db_handler.get_running_pids()
    for info in info_list:
        task_id, pid = info
        if check_pid_FAILED():
            taskdb.task_db_handler.modify_status(task_id, taskdb.TASK_STATUS.FAILED)
        if check_pid_SCUEESE():
            taskdb.task_db_handler.modify_status(task_id, taskdb.TASK_STATUS.SUCCESS)


# check if should run next
# 当前判断只要没有任务在跑 就认为可以启动一个新任务 以后策略可以修改 支持多任务同时跑
def check_if_should_run_next():
    running_list = taskdb.task_db_handler.get_running_pids()
    if len(running_list) == 0:
        # should run next
        next_info_list = taskdb.task_db_handler.get_wait_list()
        if len(next_info_list) == 0:
            print('no waiting task...')
            return False, None
        else:
            task_id, rank = next_info_list[0]
            print('should run task_id=%s, its rank is %s' % (task_id, rank))
            return True, task_id
    else:
        print('still have running task...')
        return False, None

def dump_data_yaml(path, task_id):
    js = taskdb.task_db_handler.get_data_info(task_id)
    print('dump datafile into yaml. %s -> %s' % (task_id, path))
    with open(path, 'w') as fout:
        fout.write("# Train/val/test sets as 1) dir: path/to/imgs, 2) file: path/to/imgs.txt, or 3) list: [path/to/imgs1, path/to/imgs2, ..] \n")
        fout.write("path: %s\n" % js['path'])
        fout.write("train: %s\n" % js['train'])
        fout.write("val: %s\n" % js['val'])
        fout.write("test: %s\n" % js['test'])

        fout.write("names:\n")
        for k, v in js['names'].items():
            fout.write("    %s: %s\n" % (k, v))
        fout.flush()
    return "--data %s" % path


def gen_params_str(task_id):
    js = taskdb.task_db_handler.get_param_info(task_id)
    ss = ""
    for k, v in js.items():
        ss = ss + " --%s %s" % (k, v)
    return ss


def get_weight_str(task_id):
    js = taskdb.task_db_handler.get_weight_info(task_id)
    ss = "--weights %s" % js['path']
    return ss


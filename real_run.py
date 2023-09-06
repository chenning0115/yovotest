import os, sys, subprocess
from contrib.taskdb import task_db_handler
from contrib.manage_stategy import check_running_status, check_if_should_run_next, dump_data_yaml, gen_params_str, get_weight_str

base_prefix = os.path.dirname(os.path.abspath(__file__))
path_prefix_data_yaml = '%s/data' % base_prefix
path_prefix_log_path = "%s/log" % base_prefix
path_prefix_res_path = "%s/runs/train/" % base_prefix



def real_run():
    # 1. 检查running的任务状态并进行修改
    print('start to check running status...')
    check_running_status()

    # 2. 检查是否需要进行下一个新任务
    print('start to check if should run next...')
    check, new_task_id = check_if_should_run_next()
    if not check:
        print('[real_run]: no need to run next...')
        return
    
    print('need to run next task. will run...')

    # 3. run one task
    path_data = '%s/%s.yaml' % (path_prefix_data_yaml, new_task_id) 
    data_str = dump_data_yaml(path_data, new_task_id)
    params_str = gen_params_str(new_task_id)
    weight_str = get_weight_str(new_task_id)

    path_log = '%s/%s.txt' % (path_prefix_log_path, new_task_id)
    path_res = '%s/%s' % (path_prefix_res_path, new_task_id)

    task_db_handler.set_log_path(new_task_id, path_log)
    task_db_handler.set_res_path(new_task_id, path_res)
    log_file = open(path_log, 'w')

    command_str = 'python train.py --taskid %s %s %s %s' % (new_task_id, params_str, data_str, weight_str)
    print('prepare to run task %s, run command is %s' % (new_task_id, command_str))
    process = subprocess.Popen(command_str, stdout=log_file, stderr=log_file)
    pid = process.pid
    task_db_handler.set_PID(new_task_id, pid)
    print('running task : task_id=%s, pid=%s, log_path=%s, res_path=%s' % (new_task_id, pid, path_log, path_res))
    

if __name__ == "__main__":
    real_run()
import os, sys

class TASK_STATUS:
    SUCCESS = 'SUCCESS'
    FAILED = 'FAILED'
    WAIT = 'WATI'
    RUNNING = 'RUNNING'
    READYFORRUN = 'READYFORRUN'

class TaskDBHandler(object):
    '''
    caution: 本类必须要是无状态的
    '''
    def __init__(self, conn) -> None:
        self.conn = conn

        self.temp_pid = None
        self.temp_log_path = None
        self.temp_res_path = None

    def modify_status(self, task_id, status):
        pass

    def get_data_info(self, task_id):
        '''
        return: json
        '''
        demo = {
            'path': '../datasets/test_data',   # dataset root dir
            'train': 'images/train',
            'val': 'images/train',
            'test': '',
            'names': {
                0: 'helmet'
            }
        }        
        return demo

    
    def get_param_info(self, task_id):
        return {} 
    
    def get_weight_info(self, task_id):
        
        demo = {
            'path' : 'yolov5s.pt'
        }
        return demo



    def set_PID(self, task_id, pid):
        self.temp_pid = pid

    def get_PID(self, task_id):
        return self.temp_pid

    def get_log_path(self, task_id):
        return self.temp_log_path

    def get_res_path(self, task_id):
        return "C:\charnix/codes/torchserve/yolov5/runs/train/%s" % task_id 

    def set_log_path(self, task_id, log_path):
        '''
        log_path: str
        '''
        self.temp_log_path = log_path

    def set_res_path(self, task_id, res_path):
        '''
        res_path : str
        '''
        self.temp_res_path = res_path

    # -------------------------- 
    # 针对全表扫描

    def get_running_pids(self):
        '''
        get pidlist of running tasks
        return : [[task_id, pid], [task_id, pid], ...]
        '''

        return []

    def get_wait_list(self, order_by_rank=True):
        '''
        获取等待列表 并按照rank从小到大排序
        返回pids
        return : [[task_id, rank], [task_id, rank ], ...]
        '''
        return [[1003, 0]]


task_db_handler = TaskDBHandler(conn=None)


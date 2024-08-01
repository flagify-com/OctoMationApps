import mysql.connector
from mysql.connector import Error
from datetime import datetime, timedelta
from hg_special import  get_mysql_params_from_sdk, get_mysql_params_for_app_from_env

class ActiveListManager:
    _prefix = '_al_'
    msg = "ActiveListManager:\n"
    def __init__(self, hg_client=None):
        self.db_connection = None
        self.hg_client = hg_client
    
    # 数据库连接
    def get_db_connection(self):
        db_conn = None
        # 获取数据库连接信息
        # mysql_params = get_mysql_params_from_env()
        # mysql_params = get_mysql_params_for_app_from_env()
        mysql_params = get_mysql_params_from_sdk(self.hg_client)
        # self.msg += str(mysql_params) + "\n"
        db_host = mysql_params['host']
        db_name = mysql_params['database']
        db_username = mysql_params['username']
        db_password = mysql_params['password']
        db_port = mysql_params['port']
        db_ssl = mysql_params['ssl']
        # self.msg += str(mysql_params) + "\n"
        try:
            connection = mysql.connector.connect(
                host=db_host,
                database=db_name,
                user=db_username,
                password=db_password,
                port=db_port
                # ,ssl_disabled=not db_ssl
            )
            db_conn = connection
        except Error as e:
            self.msg += f"get_db_connection() Error: {e}\n"
        return db_conn

    # 初始化活动列表表
    def initialize_active_list_table(self, table_name, key_name="_key", value_name="_value", remark_name="_remark"):
        ret = False
        table_name = f"_al_{table_name}"
        conn = None
        try:
            conn = self.get_db_connection()
            if not conn:
                self.msg +="Failed to connect to database\n"
                return ret
            cursor = conn.cursor()
            
            create_table_query = f"""
            CREATE TABLE IF NOT EXISTS {table_name} (
                {key_name} VARCHAR(512) NOT NULL,
                {value_name} TEXT,
                {remark_name} TEXT,
                _ext_01 TEXT,
                _ext_02 TEXT,
                _ext_03 TEXT,
                create_time DATETIME DEFAULT CURRENT_TIMESTAMP,
                update_time DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                expire_time DATETIME DEFAULT NULL,
                KEY `idx_{table_name}_{key_name}` (`{key_name}`(255)),
                KEY `idx_{table_name}_{value_name}` (`{value_name}`(255)),
                KEY `idx_{table_name}_create_time` (`create_time`),
                KEY `idx_{table_name}_update_time` (`update_time`)
            );
            """
            cursor.execute(create_table_query)
            
            # # 创建索引
            # cursor.execute(f"CREATE INDEX idx_{table_name}_{key_name} ON `{table_name}` ({key_name}(255));")
            # cursor.execute(f"CREATE INDEX idx_{table_name}_{value_name} ON `{table_name}` ({value_name}(255));")
            # cursor.execute(f"CREATE INDEX idx_{table_name}_create_time ON {table_name} (create_time);")
            # cursor.execute(f"CREATE INDEX idx_{table_name}_update_time ON {table_name} (update_time);")
            
            conn.commit()
            ret = True
        except Error as e:
            self.msg += f"Error: {e}\n"
        finally:
            if conn:
                cursor.close()
                conn.close()
        return ret

    # 添加记录到列表
    def add_record_to_active_list(self, table_name, item_key=None, item_value=None, item_remark="", replace_if_exists=False):
        ret = False
        table_name = f"_al_{table_name}"
        conn = None
        try:
            conn = self.get_db_connection()
            if not conn:
                self.msg +="Failed to connect to database\n"
                return ret
            cursor = conn.cursor()
            if replace_if_exists:
                # 先查询数据库，看是否有相同的key存在
                select_query = f"SELECT COUNT(*) FROM {table_name} WHERE _key = %s;"
                cursor.execute(select_query, (item_key,))
                result = cursor.fetchone()
                if result and result[0] > 0:
                    # 存在相同的key，则更新
                    self.msg += f"存在相同的key，更新\n"
                    update_query = f"""
                    UPDATE {table_name} SET _value = %s, _remark = %s, update_time = CURRENT_TIMESTAMP
                    WHERE _key = %s;
                    """
                    cursor.execute(update_query, (item_value, item_remark, item_key))
                    conn.commit()
                else:
                    # 不存在相同的key，则插入
                    self.msg += f"不存在相同的key，插入.\n"
                    insert_query = f"""
                    INSERT INTO {table_name} (_key, _value, _remark, create_time, update_time)
                    VALUES (%s, %s, %s, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);
                    """
                    cursor.execute(insert_query, (item_key, item_value, item_remark))
                    conn.commit()
            else:
                # 直接插入数据
                insert_query = f"""
                INSERT INTO {table_name} (_key, _value, _remark, create_time, update_time)
                VALUES (%s, %s, %s, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);
                """
                cursor.execute(insert_query, (item_key, item_value, item_remark))
                conn.commit()
            ret = True
        # except mysql.connector.IntegrityError as err:
        #     # Catch duplicate entry error
        #     if err.errno == mysql.connector.errorcode.ER_DUP_ENTRY:
        except Error as e:
            self.msg += f"add_record_to_active_list() Error: {e}\n"
        finally:
            if conn:
                cursor.close()
                conn.close()
        return ret

    # 在时间窗口内计数
    def count_records_within_time_window(self, table_name, item_key, end_time=None, time_delta="30m"):
        xcount = None
        
        if end_time is None:
            end_time = datetime.now()
        else:
            end_time = datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S")
        
        # 解析 time_delta
        delta_amount = int(time_delta[:-1]) # 30
        delta_unit = time_delta[-1] # m
        
        if delta_unit == 'm':
            delta = timedelta(minutes=delta_amount)
        elif delta_unit == 'h':
            delta = timedelta(hours=delta_amount)
        elif delta_unit == 'd':
            delta = timedelta(days=delta_amount)
        else:
            self.msg += f"Invalid time_delta format. Use 'm' for minutes, 'h' for hours, 'd' for days.\n"
            return xcount
        
        start_time = end_time - delta
        table_name = f"_al_{table_name}"
        conn = None
        try:
            conn = self.get_db_connection()
            if not conn:
                self.msg += f"DB connection error.\n"
                return xcount
            cursor = conn.cursor()
            if item_key == "*" or item_key == "":
                count_query = f"""
                SELECT COUNT(*) FROM {table_name}
                WHERE create_time BETWEEN %s AND %s;
                """
                cursor.execute(count_query, (start_time, end_time))
            else:
                count_query = f"""
                SELECT COUNT(*) FROM {table_name}
                WHERE _key = %s AND create_time BETWEEN %s AND %s;
                """
                cursor.execute(count_query, (item_key, start_time, end_time))
            count = cursor.fetchone()[0]
            xcount = count
        except Exception as e:
            self.msg += f"count_records_within_time_window() Error: {e}\n"
        finally:
            if conn:
                cursor.close()
                conn.close()
        return xcount

    # 列举出所有活动列表
    def list_all_active_lists(self):
        """
        列举出所有活动列表，以_al_开头的表名
        :return: 列表名称组成的list
        """
        lists = None
        conn = None
        try:
            conn = self.get_db_connection()
            if not conn:
                self.msg +="Failed to connect to database\n"
                return lists
            cursor = conn.cursor()
            count_query = f"""SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = DATABASE() 
                AND table_name LIKE '{self._prefix}%';
            """
            cursor.execute(count_query)
            result = cursor.fetchall()
            lists = [table_name.replace(self._prefix, "",1) for table_name, in result]
        except Exception as e:
            self.msg += f"list_all_active_lists() Error: {e}\n"
        finally:
            if conn:
                cursor.close()
                conn.close()
        return lists

    # 从列表中移除项
    def remove_record_from_active_list(self, table_name, item_key):
        ret = False
        table_name = f"_al_{table_name}"
        conn = None
        try:
            conn = self.get_db_connection()
            if not conn:
                return ret
            cursor = conn.cursor()
            
            delete_query = f"DELETE FROM {table_name} WHERE _key = %s;"
            cursor.execute(delete_query, (item_key,))
            conn.commit()
            ret = True
        except Error as e:
            self.msg += f"remove_record_from_active_list() Error: {e}\n"
        finally:
            if conn:
                cursor.close()
                conn.close()
        return ret
    
    # 从列表中移除项
    def clear_active_list(self, table_name):
        ret = False
        table_name = f"_al_{table_name}"
        conn = None
        try:
            conn = self.get_db_connection()
            if not conn:
                self.msg +="Failed to connect to database\n"
                return ret
            cursor = conn.cursor()
            truncate_command = f"TRUNCATE TABLE {table_name};"
            cursor.execute(truncate_command)
            conn.commit()
            ret = True
        except Error as e:
            self.msg += f"clear_active_list() Error: {e}\n"
        finally:
            if conn:
                cursor.close()
                conn.close()
        return ret
    
    # 删除活动列表
    def delete_active_list(self, table_name):
        ret = False
        table_name = f"_al_{table_name}"
        conn = None
        try:
            conn = self.get_db_connection()
            if not conn:
                self.msg +="Failed to connect to database\n"
                return ret
            cursor = conn.cursor()
            drop_command = f"DROP TABLE IF EXISTS {table_name};"
            cursor.execute(drop_command)
            conn.commit()
            ret = True
        except Error as e:
            self.msg += f"delete_active_list() Error: {e}\n"
        finally:
            if conn:
                cursor.close()
                conn.close()
        return ret

    # 按照创建时间的天、小时、分钟统计活动列表中的元素数量
    def count_records_by_time_unit(self, table_name, time_unit="day", unit_amount=None):
        ret = None
        table_name = f"_al_{table_name}"
        conn = None
        try:    
            conn = self.get_db_connection()
            if not conn:
                self.msg +="Failed to connect to database\n"
                return ret
            cursor = conn.cursor()
            if time_unit.lower() == "day":
                # 按天统计N天以内的元素记录，根据create_time字段分组
                if unit_amount is None:
                    unit_amount = 7
                count_query = f"""
                SELECT DATE(create_time) AS XTIME, COUNT(*) AS XCOUNT FROM {table_name}
                WHERE create_time >= DATE_SUB(NOW(), INTERVAL {unit_amount} DAY)
                GROUP BY XTIME; 
                """
            elif time_unit.lower() == "hour":
                # 按小时统计N小时以内的元素记录，对格式化之后的create_time字段XTIME进行分组，XTIME格式：MMDD_HH
                # MySQL语句中对create_time先做format，然后再进行分组
                if unit_amount is None:
                    unit_amount = 24
                count_query = f"""
                SELECT DATE_FORMAT(create_time, '%m%d_%H') AS XTIME, COUNT(*) AS XCOUNT FROM {table_name}
                WHERE create_time >= DATE_SUB(NOW(), INTERVAL {unit_amount} HOUR)
                GROUP BY XTIME;
                """
            elif time_unit.lower() == "minute":
                # 按分钟统计N分钟以内的元素记录，对格式化之后的create_time字段XTIME进行分组，XTIME格式：MMDD_HHMM
                # MySQL语句中对create_time先做format，然后再进行分组
                if unit_amount is None:
                    unit_amount = 60
                count_query = f"""
                SELECT DATE_FORMAT(create_time, '%m%d_%H%i') AS XTIME, COUNT(*) AS XCOUNT FROM {table_name}
                WHERE create_time >= DATE_SUB(NOW(), INTERVAL {unit_amount} MINUTE)
                GROUP BY XTIME;
                """
            else:
                self.msg += f"Invalid time_unit format. Use 'day', 'hour', or'minute'.\n"
                return ret
            cursor.execute(count_query)
            result = cursor.fetchall()
            ret = result
        except Error as e:
            self.msg += f"count_records_by_time_unit() Error: {e}\n"
        finally:
            if conn:
                cursor.close()
                conn.close()
        return ret

    def get_records_time_trend(self, table_name, item_key="",time_unit="day", unit_amount=None):
        """
        获取指定key的活动列表中的时间趋势数据，天/时/分
        """
        ret = None
        table_name = f"_al_{table_name}"
        conn = None
        try:    
            conn = self.get_db_connection()
            if not conn:
                self.msg +="Failed to connect to database\n"
                return ret
            cursor = conn.cursor()
            select_query = f"SELECT DATE(create_time) AS XTIME, COUNT(*) AS XCOUNT FROM {table_name} WHERE "
            
            if item_key:
                select_query += f"_key = '{item_key}' AND "
    
            if time_unit.lower() == "day":
                # 按天统计N天以内的元素记录，根据create_time字段分组
                if unit_amount is None:
                    unit_amount = 7
                select_query += f"create_time >= DATE_SUB(NOW(), INTERVAL {unit_amount} DAY) GROUP BY XTIME; "
            elif time_unit.lower() == "hour":
                # 按小时统计N小时以内的元素记录，对格式化之后的create_time字段XTIME进行分组，XTIME格式：MMDD_HH
                # MySQL语句中对create_time先做format，然后再进行分组
                if unit_amount is None:
                    unit_amount = 24
                select_query += f"create_time >= DATE_SUB(NOW(), INTERVAL {unit_amount} HOUR) GROUP BY XTIME;"
            elif time_unit.lower() == "minute":
                # 按分钟统计N分钟以内的元素记录，对格式化之后的create_time字段XTIME进行分组，XTIME格式：MMDD_HHMM
                # MySQL语句中对create_time先做format，然后再进行分组
                if unit_amount is None:
                    unit_amount = 60
                select_query += f"create_time >= DATE_SUB(NOW(), INTERVAL {unit_amount} MINUTE) GROUP BY XTIME;"
            else:
                self.msg += f"Invalid time_unit format. Use 'day', 'hour', or'minute'.\n"
                return ret
            cursor.execute(select_query)
            result = cursor.fetchall()
            ret = result
        except Error as e:
            self.msg += f"get_records_time_trend() Error: {e}\n"
        finally:
            if conn:
                cursor.close()
                conn.close()
        return ret

    # 快速查看活动列表，返回最新10条记录
    def quick_view_active_list(self, table_name, item_key="*"):
        ret = None
        table_name = f"_al_{table_name}"
        conn = None
        try:
            conn = self.get_db_connection()
            if not conn:
                self.msg +="Failed to connect to database\n"
                return ret
            cursor = conn.cursor()
            if item_key == "" or item_key == "*":
                quick_view_query = f"SELECT _key, _value, _remark, create_time, update_time FROM {table_name} ORDER BY create_time DESC LIMIT 10;"
            else:
                quick_view_query = f"SELECT _key, _value, _remark, create_time, update_time FROM {table_name} WHERE _key = '{item_key}' ORDER BY create_time DESC LIMIT 10;"
            cursor.execute(quick_view_query)
            result = cursor.fetchall()
            ret = result
        except Error as e:
            self.msg += f"quick_view_active_list() Error: {e}\n"
        finally:
            if conn:
                cursor.close()
                conn.close()
        return ret

if __name__ == '__main__':
    import time
    alm = ActiveListManager()
    print(alm.get_db_connection())
    current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    alm.initialize_active_list_table("test_activelist")
    alm.add_record_to_active_list("test_activelist", "key1", "value1-1", "remark1-1")
    alm.add_record_to_active_list("test_activelist", "key1", "value1-2", "remark1-2")
    alm.add_record_to_active_list("test_activelist", "key2", "value2", "remark2")
    alm.add_record_to_active_list("test_activelist", "key3", "value3", "remark3")
    alm.add_record_to_active_list("test_activelist", "key3", "value3", "remark3",True)
    print(alm.count_records_within_time_window("test_activelist", "key1"))
    print(alm.count_records_within_time_window("test_activelist", "key2"))
    print(alm.count_records_within_time_window("test_activelist", "key3"))
    alm.remove_record_from_active_list("test_activelist", "key2")
    print(alm.count_records_within_time_window("test_activelist", "key2", current_time, "30m"))
    print(alm.count_records_within_time_window("test_activelist", "key1", current_time))
    print(alm.count_records_within_time_window("test_activelist", "key4"))
    print(alm.list_all_active_lists())
    try:
        alm.is_key_in_active_list("key1", "test_activelist")
    except mysql.connector.Error as e:
        print(e)
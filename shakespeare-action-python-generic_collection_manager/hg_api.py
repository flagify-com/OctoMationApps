import requests
from action_sdk_for_cache.action_cache_sdk import HoneyGuide
from datetime import datetime, timedelta
requests.packages.urllib3.disable_warnings() 

class HoneyGuideAPI():
    __useragent = "HG-Python-SDK"
    def __init__(self, hg_server, hg_token, context_info={}, timeout_seconds=10):
        self._hg_server = hg_server
        self._hg_token = hg_token
        self._hg_sdk = HoneyGuide(context_info=context_info)
        self._api_timeout_seconds = timeout_seconds
        self.summary = {
            "statusCode": 0,
            "msg": "",
            "duplicated": False
        }

    def _clear_status(self):
        self.summary = {
            "statusCode": 0,
            "msg": "",
            "duplicated": False
        }

    def _request_api(self, method, url, headers=None, json_params=None,json_payload=None, retry_times=3):
        response = None
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "hg-token": self._hg_token,
            "User-Agent": self.__useragent
        }
        self._hg_sdk.actionLog.info(f"_request_api():请求地址：{url}")
        self._hg_sdk.actionLog.info(f"_request_api():请求参数：{json_params}")
        self._hg_sdk.actionLog.info(f"_request_api():请求体：{json_payload}")
        while retry_times > 0:
            try:
                if method.upper() == "GET":
                    response = requests.get(url, headers=headers, params=json_params, verify=False, timeout=self._api_timeout_seconds)
                elif method.upper() == "POST":
                    response = requests.post(url, headers=headers, params=json_params, json=json_payload, verify=False, timeout=self._api_timeout_seconds)
                if response and hasattr(response, "text"):
                    self._hg_sdk.actionLog.info(f"_request_api():请求成功，返回结果：{response.text}")
                break
            except Exception as e:
                self._hg_sdk.actionLog.info(f"_request_api():请求失败，错误信息：{e}")
                self.summary["statusCode"] = 500
                self.summary["msg"] = f"_request_api():请求失败，错误信息：{e}"
            retry_times -= 1
        return response
    # 集合操作
    def get_generic_collections(self, collection_name=None,page_start=1, batch_size=50, max_count=200):
        """
        获取所有（通用）集合信息，并返回集合字典组成的数组。本动作会逐页查询，直到所有集合都查询完毕。
        :param page_start: 起始页码，默认1。
        :param batch_size: 每页查询数量，默认50。
        :param max_count: 最多返回的集合数量，默认1000。
        :return: 集合字典组成的数组。
        """
        self._clear_status()
        json_payload = {}
        if collection_name and collection_name!= "":
            # 集合名称是模糊查询，需要在返回结果中再次确认
            json_payload["name"] = collection_name
        url = f"{self._hg_server}/api/collection/find"
        collections = []
        while True:
            json_params = {
                "page": page_start,
                "size": batch_size
            }
            response = self._request_api("POST", url, json_params=json_params, json_payload=json_payload)
            try:
                if response.status_code == 200:
                    json_result = response.json()
                    if json_result["code"] == 200 and 'result' in json_result.keys() \
                        and 'empty' in json_result['result'].keys() and 'content' in json_result['result'].keys():
                        if json_result['result']['empty'] == False:
                            for content in json_result["result"]["content"]:
                                collections.append(content)
                                if len(collections) >= max_count:
                                    break
                            if len(collections) >= max_count:
                                # 已经获取到足够数量的集合，break
                                break
                            # 继续翻页查询
                            if  'numberOfElements' in json_result['result'].keys():
                                if json_result['result']['numberOfElements'] < batch_size:
                                    # 已经没有下一页
                                    break
                                else:
                                    # 还可能有下一页
                                    page_start += 1
                        else:
                            break
                    else:
                        self.summary["statusCode"] = 500
                        self.summary["msg"] = f"请求失败，返回结果不符合预期，返回结果：{json_result}"
                        break
                else:
                    self.summary["statusCode"] = response.status_code
                    self.summary["msg"] = f"请求失败，状态码：{response.status_code}"
                    break
            except Exception as e:
                self.summary["statusCode"] = 500
                self.summary["msg"] = f"请求失败，错误信息：{e}"
                break
        if len(collections) > 0:
            self.summary["statusCode"] = 0
            self.summary["msg"] = f"获取成功，共获取到{len(collections)}个集合。"
        return collections

    def create_generic_collection(self, collection_name, collection_name_cn, collection_description=""):
        """
        创建通用集合。
        :param collection_name: 集合名称。
        :param collection_name_cn: 集合名称中文。
        :param collection_description: 集合描述。
        :return: 创建成功返回True，失败返回False。
        """
        self._clear_status()
        generic_collection_id = 0
        json_payload = {
            "name": collection_name,
            "cnName": collection_name_cn,
            "description": collection_description,
            "ttl": 315360000
        }
        url = f"{self._hg_server}/api/collection"
        try:
            response = self._request_api("POST", url, json_payload=json_payload)
            self._hg_sdk.actionLog.info(f"create_generic_collection():请求结果：{response.text}")
            self.summary["statusCode"] = response.status_code
            self.summary["msg"] = f"请求失败，服务器返回：{response.text}"
            json_result = response.json()
            if response.status_code == 200:
                if 'code' in json_result.keys() and json_result['code'] == 200 and \
                    'result' in json_result.keys() :
                    generic_collection_id = json_result['result']
                    self.summary["statusCode"] = 0
                    self.summary["msg"] = f"请求成功，集合{collection_name}创建成功。"
            else:
                #{"code": 400,"msg": "集合名称(unitest_collection_name_1)在通用集合,或者ip名单中已存在"}
                if 'msg' in json_result.keys():
                    self.summary["msg"] = json_result['msg']
                    if 'code' in json_result.keys() and json_result['code'] == 400:
                        # 要创建的集合已经存在了，查一下collection_id，返回给用户
                        if collection_name in json_result['msg'] and '已存在' in json_result['msg'].replace(collection_name, ""):
                            self.summary["statusCode"] = 0
                            self.summary["msg"] = f"请求成功，集合名称{collection_name}已存在。"
                            self.summary["duplicated"] = True
                            generic_collection_id = self.get_generic_collection_id_by_name(collection_name=collection_name)
                            self.summary["duplicated"] = True
        except Exception as e:
            self.summary["statusCode"] = 500
            self.summary["msg"] = f"请求失败，错误信息：{e}"
        return generic_collection_id
   
    def get_generic_collection_id_by_name(self, collection_name=None):
        """
        根据集合名称获取集合ID。
        :param collection_name: 集合名称。
        :return: 集合ID。
        """
        self._clear_status()
        collection_id = 0
        if collection_name and collection_name != "":
            collections = self.get_generic_collections(collection_name=collection_name, batch_size=30, max_count=200)
            for collection in collections:
                # 集合名称是模糊查询，需要在返回结果中再次确认
                if collection["name"] == collection_name:
                    collection_id = collection["id"]
                    break
            if not collection_id > 0:
                self.summary["statusCode"] = 500
                self.summary["msg"] = f"请求失败，{collection_name}对应的collection_id不存在。"
        else:
            self.summary["statusCode"] = 400
            self.summary["msg"] = f"请求失败，collection_name不能为空。"
        return collection_id

    def delete_generic_collection_by_name(self, collection_name=None):
        """
        根据集合名称删除通用集合。
        :param collection_name: 集合名称。
        :return: 删除成功返回True，失败返回False。
        """
        self._clear_status()
        delete_collection_result = False
        collection_id = self.get_generic_collection_id_by_name(collection_name=collection_name)
        self._hg_sdk.actionLog.info(f"{collection_id} collection_id: {collection_name}")
        if collection_id > 0:
            delete_collection_result = self.delete_generic_collection_by_id(collection_id=collection_id)
        elif self.summary["statusCode"] == 500 and self.summary["msg"].endswith("collection_id不存在。"):
            self.summary["msg"] = f"请求失败，集合{collection_name}对应的collection_id不存在，无需删除"
            self.summary["statusCode"] = 0
            delete_collection_result = True
        return delete_collection_result
        
    def delete_generic_collection_by_id(self, collection_id=0):
        """
        根据集合ID删除通用集合。
        :param collection_id: 集合ID。
        :return: 删除成功返回True，失败返回False。        
        """
        self._clear_status()
        delete_collection_result = False
        url = f"{self._hg_server}/api/collection/del/{collection_id}"
        try:
            response = self._request_api("GET", url)
            # should be POST, will fix later
            #response = self._request_api("POST", url)
            self._hg_sdk.actionLog.info(f"delete_generic_collection_by_id():请求结果：{response.text}")
            self.summary["statusCode"] = response.status_code
            self.summary["msg"] = f"请求失败，服务器返回：{response.text}"
            json_result = response.json()
            if response.status_code == 200:
                if 'code' in json_result.keys() and json_result['code'] == 200:
                    self.summary["statusCode"] = 0
                    delete_collection_result = True
                    if 'result' in json_result.keys() and json_result['result'] > 0:
                        self.summary["msg"] = f"集合删除成功。"
                    else:
                        self.summary["msg"] = f"集合删除成功，集合ID原本不存在"
        except Exception as e:
            self.summary["statusCode"] = 500
            self.summary["msg"] = f"请求失败，错误信息：{e}"
        return delete_collection_result
    # 元素操作
    def get_generic_collection_elements(self, collection_name=None, collection_id=None, element_value=None,page_start=1, batch_size=50, max_count=200):
        """
        获取指定集合（通用）中的所有元素信息，并返回元素字典组成的数组。本动作会逐页查询，直到所有元素都查询完毕。collection_id和collection_name不能同时为空。
        :param collection_id: 集合ID。
        :param collection_name: 集合名称。
        :param page_start: 起始页码，默认1。
        :param batch_size: 每页查询数量，默认50。
        :param max_count: 最多返回的元素数量，默认1000。
        :return: 元素字典组成的数组。
        """
        self._clear_status()
        elements = []
        json_payload = {}
        if collection_id and collection_id != "":
            json_payload["collectionId"] = collection_id
        elif collection_name and collection_name != "":
            json_payload["collectionName"] = collection_name
        if element_value and element_value != "":
            json_payload["value"] = element_value
        url = f"{self._hg_server}/api/collectionElement/find"
        while True:
            json_params = {
                "page": page_start,
                "size": batch_size
            }
            response = self._request_api("POST", url, json_params=json_params, json_payload=json_payload)
            try:
                if response.status_code == 200:
                    json_result = response.json()
                    if json_result["code"] == 200 and 'result' in json_result.keys() \
                        and 'empty' in json_result['result'].keys() and 'content' in json_result['result'].keys():
                        if json_result['result']['empty'] == False:
                            for content in json_result["result"]["content"]:
                                elements.append(content)
                                if len(elements) >= max_count:
                                    break
                            if len(elements) >= max_count:
                                # 已经获取到足够数量的元素，break
                                break
                            # 继续翻页查询
                            if  'numberOfElements' in json_result['result'].keys():
                                if json_result['result']['numberOfElements'] < batch_size:
                                    # 已经没有下一页
                                    break
                                else:
                                    # 还可能有下一页
                                    page_start += 1
                        else:
                            break
                    else:
                        self.summary["statusCode"] = 500
                        self.summary["msg"] = f"请求失败，返回结果不符合预期，返回结果：{json_result}"
                        break
                else:
                    self.summary["statusCode"] = response.status_code
                    self.summary["msg"] = f"请求失败，状态码：{response.status_code}"
                    break
            except Exception as e:
                self.summary["statusCode"] = 500
                self.summary["msg"] = f"请求失败，错误信息：{e}"
                break
        if len(elements) > 0:
            self.summary["statusCode"] = 0
            self.summary["msg"] = f"执行成功，共获取到{len(elements)}个元素。"
        return elements

    def add_generic_collection_element(self, collection_name=None, collection_id=None, element_value=None, element_remark="", update_if_exist=False, effective_time_str=None, expire_time_str=None):
        """
        添加集合元素。collection_id和collection_name不能同时为空。
        :param collection_id: 集合ID。
        :param collection_name: 集合名称。
        :param element_value: 元素值。
        :param element_remark: 元素备注。
        :param effective_time_str: 生效时间，格式为“YYYY-MM-DD HH:MM:SS”。
        :param expire_time_str: 失效时间，格式为“YYYY-MM-DD HH:MM:SS”。
        :return: 添加成功返回True，失败返回False。
        """
        self._clear_status()
        add_element_result = False
        json_payload = {}
        # 集合参数
        if collection_id and collection_id != "":
            json_payload["collectionId"] = int(collection_id)
        if collection_name and collection_name != "":
            json_payload["collectionName"] = collection_name
        # 元素信息
        if element_value and element_value != "":
            json_payload["value"] = element_value
        else:
            self.summary["statusCode"] = 400
            self.summary["msg"] = f"请求失败，element_value不能为空。"
            return add_element_result
        if element_remark and element_remark != "":
            json_payload["remark"] = element_remark
        # 时间信息，将来可能使用
        if effective_time_str and effective_time_str != "":
            json_payload["effectiveTime"] = effective_time_str
        if expire_time_str and expire_time_str != "":
            json_payload["expireTime"] = expire_time_str
        else:
            json_payload["expireTime"] = (datetime.now() + timedelta(days=365 * 10)).strftime("%Y-%m-%d %H:%M:%S")
        self._hg_sdk.actionLog.info(f"add_collection_element():请求参数：{json_payload}")
        url = f"{self._hg_server}/api/collectionElement"
        try:
            response = self._request_api("POST", url, json_payload=json_payload)
            self._hg_sdk.actionLog.info(f"add_collection_element():请求结果：{response.text}")
            self.summary["statusCode"] = response.status_code
            self.summary["msg"] = f"请求失败，服务器返回：{response.text}"
            json_result = response.json()
            if response.status_code == 200:
                if 'code' in json_result.keys():
                    self.summary["statusCode"] = json_result["code"]
                    if json_result["code"] == 200:
                        self.summary["msg"] = f"请求成功，元素添加成功。"
                        add_element_result = True
                    else:
                        self.summary["msg"] = f"请求失败，元素添加失败:{json_result}"
                else:
                    self.summary["statusCode"] = 500
                    self.summary["msg"] = f"API请求失败，返回结果不符合预期，返回结果：{json_result}"
            elif response.status_code == 400:
                # {"code": 400, "msg": "元素(XXX)重复"}
                if 'code' in json_result.keys() and json_result['code'] == 400 and 'msg' in json_result.keys() \
                    and json_result['msg'].startswith("元素(") and json_result['msg'].endswith(")重复"):
                    # 创建了一个已经存在的元素，默认不更新，如果设置了update_if_exist=True，则尝试更新
                    self.summary['duplicated'] = True
                    if not update_if_exist:
                        self.summary["statusCode"] = json_result['code']
                        self.summary["msg"] = f"请求成功，元素已存在。"
                        add_element_result = True
                    else:
                        # 尝试更新元素
                        element_id = self.get_generic_collection_element_id_by_value(collection_id=collection_id, collection_name=collection_name, element_value=element_value)
                        update_result = self.update_generic_collection_element_by_id(collection_id=collection_id, collection_name=collection_name, element_id=element_id,element_remark=element_remark)
                        self.summary['duplicated'] = True # 防止被其他动作覆盖，再次设置
                        if update_result:
                            self.summary["statusCode"] = 0
                            self.summary["msg"] = f"请求成功，元素已存在，已更新。"
                            add_element_result = True
                        else:
                            self.summary["statusCode"] = 500
                            self.summary["msg"] = f"请求失败，元素已存在，但更新失败。"
                    
        except Exception as e:
            self.summary["statusCode"] = 500
            self.summary["msg"] = f"请求失败，错误信息：{e}"
        return add_element_result

    def update_generic_collection_element_by_id(self, collection_id=None,collection_name=None, element_id=0, element_remark=""):
        """
        根据元素ID，更新集合元素。
        :param collection_name: 集合名称。
        :param element_id: 元素ID（整数，不能为空）
        :param element_remark: 元素备注。
        :return: 更新成功返回True，失败返回False。statusCode:0表示成功，其他表示失败。
        """
        self._clear_status()
        update_element_result = False
        json_payload = {}
        # 集合参数
        if collection_id and collection_id != "":
            json_payload["collectionId"] = int(collection_id)
        if collection_name and collection_name != "":
            json_payload["collectionName"] = collection_name
        # 元素参数
        json_payload["id"] = int(element_id)
        json_payload["remark"] = element_remark
        self._hg_sdk.actionLog.info(f"update_collection_element():请求参数：{json_payload}")
        url = f"{self._hg_server}/api/collectionElement/modify"
        try:
            response = self._request_api("POST", url, json_payload=json_payload)
            self._hg_sdk.actionLog.info(f"update_collection_element():请求结果：{response.text}")
            self.summary["statusCode"] = response.status_code
            self.summary["msg"] = f"请求失败，服务器返回：{response.text}"
            json_result = response.json()
            if response.status_code == 200:
                if 'code' in json_result.keys():
                    self.summary["statusCode"] = json_result["code"]
                    if json_result["code"] == 200:
                        self.summary["msg"] = f"请求成功，元素更新成功。"
                        update_element_result = True
                    else:
                        self.summary["msg"] = f"请求失败，元素更新失败:{json_result}"
                else:
                    self.summary["statusCode"] = 500
                    self.summary["msg"] = f"API请求失败，返回结果不符合预期，返回结果：{json_result}"
        except Exception as e:
            self.summary["statusCode"] = 500
            self.summary["msg"] = f"请求失败，错误信息：{e}"
        return update_element_result
    
    def update_generic_collection_element_by_value(self, collection_id=None,collection_name=None, element_value=None, element_remark=""):
        """
        根据元素ID，更新集合元素。
        :param collection_name: 集合名称。
        :param element_value: 元素值
        :param element_remark: 元素备注。
        :return: 更新成功返回True，失败返回False。statusCode:0表示成功，其他表示失败。
        """
        self._clear_status()
        update_element_result = False
        json_payload = {}
        # 集合参数
        if collection_id and collection_id != "":
            json_payload["collectionId"] = int(collection_id)
        if collection_name and collection_name != "":
            json_payload["collectionName"] = collection_name
        # 元素参数
        element_id = self.get_generic_collection_element_id_by_value(collection_id=collection_id, collection_name=collection_name, element_value=element_value)
        if not element_id > 0:
            self.summary["statusCode"] = 404
            self.summary["msg"] = f"请求失败，元素{element_value}不存在。"
            return update_element_result
        json_payload["id"] = element_id
        json_payload["remark"] = element_remark
        self._hg_sdk.actionLog.info(f"update_collection_element():请求参数：{json_payload}")
        url = f"{self._hg_server}/api/collectionElement/modify"
        try:
            response = self._request_api("POST", url, json_payload=json_payload)
            self._hg_sdk.actionLog.info(f"update_collection_element():请求结果：{response.text}")
            self.summary["statusCode"] = response.status_code
            self.summary["msg"] = f"请求失败，服务器返回：{response.text}"
            json_result = response.json()
            if response.status_code == 200:
                if 'code' in json_result.keys():
                    self.summary["statusCode"] = json_result["code"]
                    if json_result["code"] == 200:
                        self.summary["msg"] = f"请求成功，元素更新成功。"
                        update_element_result = True
                    else:
                        self.summary["msg"] = f"请求失败，元素更新失败:{json_result}"
                else:
                    self.summary["statusCode"] = 500
                    self.summary["msg"] = f"API请求失败，返回结果不符合预期，返回结果：{json_result}"
        except Exception as e:
            self.summary["statusCode"] = 500
            self.summary["msg"] = f"请求失败，错误信息：{e}"
        return update_element_result
    
    def get_generic_collection_element_info_by_value(self, collection_id=None,collection_name=None, element_value=None):
        """
        根据集合名称和元素名称获取通用集合中的元素信息。
        :param collection_name: 集合名称。
        :param element_value: 元素值。
        :return: 元素信息字典。
        """
        json_element_info =  {
            "createdBy": "",
            "modifiedBy": "",
            "createdNickName": "",
            "modifiedNickName": "",
            "createTime": "",
            "updateTime": "",
            "id": 0,
            "value": "",
            "collectionId": 0,
            "collectionName": "",
            "remark": "",
            "expireTime": "",
            "expireTimeStr": "",
            "effectiveTime": None,
            "effectiveTimeStr": None
        }
        elements = self.get_generic_collection_elements(collection_id=collection_id, collection_name=collection_name, element_value=element_value)
        if elements and len(elements) == 1:
            json_element_info = elements[0]
        return json_element_info
    
    def get_generic_collection_element_id_by_name(self, collection_id=None,collection_name=None, element_value=None):
        return self.get_generic_collection_element_id_by_value(collection_id, collection_name, element_value)
    
    def get_generic_collection_element_id_by_value(self, collection_id=None,collection_name=None, element_value=None):
        """
        根据集合名称和元素名称获取通用集合中的元素ID。
        :param collection_name: 集合名称。
        :param element_name: 元素名称。
        :return: 元素ID。
        """
        self._clear_status()
        element_id = 0
        json_element_info = self.get_generic_collection_element_info_by_value(collection_id=collection_id, collection_name=collection_name, element_value=element_value)
        if 'id' in json_element_info.keys() and 'value' in json_element_info.keys() and json_element_info['value'] == element_value:
            element_id = json_element_info['id']
            self.summary["statusCode"] = 0
            self.summary["msg"] = f"查询成功，元素ID为：{element_id}"
        return element_id

    def delete_generic_collection_element_by_name(self, collection_name, element_value):
        return self.delete_generic_collection_element_by_value(self, collection_name, element_value)

    def delete_generic_collection_element_by_value(self, collection_name, element_value):
        """
        根据集合名称和元素名称删除通用集合中的元素。
        :param collection_name: 集合名称。
        :param element_name: 元素名称。
        :return: 删除成功返回True，失败返回False。
        """
        self._clear_status()
        delete_element_result = False
        element_id = self.get_generic_collection_element_id_by_name(collection_name=collection_name, element_value=element_value)
        if element_id > 0:
            delete_result = self.delete_generic_collection_element_by_id(element_id)
            if delete_result:
                self.summary["statusCode"] = 0
                self.summary["msg"] = f"删除成功"
                delete_element_result = True
        else:
            if self.summary["statusCode"] == 0:
                self.summary["statusCode"] = 0
                self.summary["msg"] = f"删除成功，元素{element_value}本来就不存在"
                delete_element_result = True
            else:
                self.summary["statusCode"] = 500
                self.summary["msg"] = f"删除失败，元素{element_value}查询失败"
        return delete_element_result

    def delete_generic_collection_element_by_id(self, element_id):
        """
        根据元素ID删除通用集合中的元素。
        :param element_id: 元素ID。ID不存在，服务器也会返回删除成功
        :return: 删除成功返回True，失败返回False。
        """
        self._clear_status()
        delete_element_result = False
        url = f"{self._hg_server}/api/collectionElement/delete/{element_id}"
        try:
            response = self._request_api("POST", url)
            self._hg_sdk.actionLog.info(f"delete_generic_collection_element_by_id():请求结果：{response.text}")
            # 先锁定一个状态码
            self.summary["statusCode"] = response.status_code
            self.summary["msg"] = f"删除元素失败，服务器返回：{response.text}"
            json_result = response.json()
            if response.status_code == 200 and 'code' in json_result.keys() and json_result['code'] == 200:
                # API接口返回的应用状态码为200，表示删除成功
                self.summary["statusCode"] = 0
                self.summary["msg"] = "删除元素成功。"
                delete_element_result = True
            else:
                if 'code' in json_result.keys():
                    self.summary["statusCode"] = json_result["code"]
        except Exception as e:
            self.summary["statusCode"] = 500
            self.summary["msg"] = f"HTTP请求失败，错误信息：{e}"

        return delete_element_result

    def check_generic_collection_element_exists(self, collection_id=None, collection_name=None, element_value=None):
        """
        检查集合元素是否存在。集合ID和集合名称不能同时为空。
        :param collection_id: 集合ID。
        :param collection_name: 集合名称。
        :param element_name: 元素名称。
        :return: 存在返回True，不存在返回False。
        """
        self._clear_status()
        element_exists = False
        elements = self.get_generic_collection_elements(collection_id=collection_id, collection_name=collection_name, element_value=element_value)
        if elements and len(elements) > 0:
            element_exists = True
        return element_exists

    def health_check(self):
            """
            健康检查。
            :return: 
            """
            self._clear_status()
            json_payload = {}
            url = f"{self._hg_server}/api/collection/find"
            json_params = {
                "page": 1,
                "size": 1
            }
            response = self._request_api("POST", url, json_params=json_params, json_payload=json_payload)
            try:
                self.summary["msg"] = f"服务器返回：{response.text}"
                # self._hg_sdk.actionLog.info(f"health_check():请求结果：{response.text}")
                if response.status_code == 200:
                    json_result = response.json()
                    self.summary["statusCode"]  = json_result["code"] 
                    if self.summary["statusCode"] == 200:
                        self.summary["msg"] = "健康检查成功"
                        return True
                else:
                    self.summary["statusCode"] = response.status_code
            except Exception as e:
                self.summary["statusCode"] = 500
                self.summary["msg"] = f"健康检查失败，错误信息：{e}"
            return False

if __name__ == '__main__':
    hg_server = "https://hg.wuzhi-ai.com"
    hg_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.***.y7voPwo3qeuVqfLuFGIL3xmmPzkgU_Rd4fBFeX41fiE"
    hgapi = HoneyGuideAPI(hg_server, hg_token, context_info={}, timeout_seconds=10)
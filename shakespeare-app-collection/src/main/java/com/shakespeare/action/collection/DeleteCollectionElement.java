package com.shakespeare.action.collection;

import com.alibaba.fastjson.JSONArray;
import com.alibaba.fastjson.JSONObject;
import com.shakespeare.action.Result;
import com.shakespeare.action.sdk.api.HoneyGuide;
import com.shakespeare.action.sdk.api.oparetor.SdkLogger;
import org.apache.commons.lang3.StringUtils;
import org.apache.http.HttpStatus;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.util.List;
import java.util.Map;

/**
 * 删除集合元素v1.0,  先根据集合名称和集合的元素查询当前元素的id,在根据id删除
 * @author hongrongxu
 */
public class DeleteCollectionElement extends AbstractDeleteElementAction{

    private static final SdkLogger logger = HoneyGuide.actionLog;

    @Override
    protected Result bussinessInvoke(JSONObject paramsJson, Map<String, Object> assetSettingJson) {
        CollectionElementParam param = validateParam(paramsJson);
        AppConfig config = validateConfig(assetSettingJson);

        String json = JSONObject.toJSONString(param);
        String url = config.getServerAddress() + Constant.API_DELETE_COLLECTION_ELEMENT_BY_ID;
        try {
            String queryUrl = config.getServerAddress() + Constant.API_QUERY_COLLECTION_ELEMENT;
            String pageDataStr = HttpClientUtils.doPostJson(queryUrl, json, config.getAppToken());
            String message = "集合("+param.getCollectionName()+")不存在元素("+param.getValue()+")";
            if (StringUtils.isBlank(pageDataStr)) {
                JSONObject data = new JSONObject();
                data.put("code", HttpStatus.SC_BAD_REQUEST);
                data.put("msg", "删除失败,原因查询元素失败");
                Result result = new Result(paramsJson, null, data);
                return result;
            } else {
                ResponseEntity<JSONObject> pageData = JSONObject.parseObject(pageDataStr, ResponseEntity.class);
                if (pageData.getCode() == HttpStatus.SC_OK) {
                    int totalElements = pageData.getResult().getIntValue("totalElements");
                    if (totalElements > 0) {
                        JSONArray jsonArray = pageData.getResult().getJSONArray("content");
                        long id = getElementId(jsonArray, param);
                        String requestResult = HttpClientUtils.doPostJson(String.format(url, id), json, config.getAppToken());
                        logger.info("delete collection element request result = " + requestResult);
                        if (StringUtils.isBlank(requestResult)) {
                            JSONObject data = new JSONObject();
                            data.put("code", HttpStatus.SC_BAD_REQUEST);
                            data.put("msg", "集合元素删除失败");
                            Result result = new Result(paramsJson, null, data);
                            return result;
                        } else {
                            ResponseEntity<Integer> response = JSONObject.parseObject(requestResult, ResponseEntity.class);
                            Result result = new Result(paramsJson, null, response);
                            result.setCode(response.getCode());
                            if (response.getCode() == HttpStatus.SC_OK) {
                                if (response.getResult() == 1) {
                                    result.setMsg("集合元素删除成功");
                                } else {
                                    JSONObject data = new JSONObject();
                                    data.put("code", HttpStatus.SC_BAD_REQUEST);
                                    data.put("msg", "集合元素删除失败,元素不存在");
                                }
                            }
                            return result;
                        }
                    } else {
                        JSONObject data = new JSONObject();
                        data.put("code", HttpStatus.SC_BAD_REQUEST);
                        data.put("msg", "删除失败," + message);
                        Result result = new Result(paramsJson, null, data);
                        return result;
                    }
                } else {
                    JSONObject data = new JSONObject();
                    data.put("code", HttpStatus.SC_BAD_REQUEST);
                    data.put("msg", "删除失败,原因查询元素失败");
                    Result result = new Result(paramsJson, null, data);
                    return result;
                }
            }

        } catch (Exception e) {
            logger.info("集合元素删除失败:" + e);
            Result result = new Result(HttpStatus.SC_BAD_REQUEST,"集合元素删除失败:("+e.getMessage()+")");
            result.setParam(paramsJson);
            return result;
        }
    }

    int getElementId(JSONArray pageList, CollectionElementParam param) {
        for (Object o: pageList) {
            JSONObject element = JSONObject.parseObject(JSONObject.toJSONString(o));
            if (param.getValue().equals(element.getString("value"))) {
                return element.getInteger("id");
            }
        }
        return 0;
    }
}

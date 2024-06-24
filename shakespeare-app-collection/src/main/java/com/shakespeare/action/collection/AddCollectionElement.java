package com.shakespeare.action.collection;

import com.alibaba.fastjson.JSONObject;
import com.shakespeare.action.Result;
import com.shakespeare.action.sdk.api.HoneyGuide;
import com.shakespeare.action.sdk.api.oparetor.SdkLogger;
import org.apache.commons.lang3.StringUtils;
import org.apache.http.HttpStatus;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.text.ParseException;
import java.util.Map;

/**
 * @author: hongrongxu
 * @date: 2021/5/7 上午10:59
 */
public class AddCollectionElement extends AbstractAddCollectionElementAction {

    private static final SdkLogger logger = HoneyGuide.actionLog;

    @Override
    protected Result bussinessInvoke(JSONObject paramsJson, Map<String, Object> assetSettingJson) {
        CollectionElementParam param = null;
        try {
            param = validateParam(paramsJson);
        } catch (ParseException e) {
            logger.info("parse string to date failed");
            Result result = new Result(HttpStatus.SC_BAD_REQUEST,"集合元素添加失败:("+e.getMessage()+")");
            result.setParam(paramsJson);
            return result;
        }
        AppConfig config = validateConfig(assetSettingJson);
        String json = JSONObject.toJSONString(param);
        String url = config.getServerAddress() + Constant.API_COLLECTION_ELEMENT;
        ResponseEntity<Integer> response;
        String requestResult;
        try {
            requestResult = HttpClientUtils.doPostJson(url, json, config.getAppToken());
            logger.info("add collection element request result = " + requestResult);
            if (StringUtils.isBlank(requestResult)) {
                Result result = new Result(HttpStatus.SC_BAD_REQUEST,"集合元素添加失败!");
                result.setParam(paramsJson);
                return result;
            } else {
                response = JSONObject.parseObject(requestResult, ResponseEntity.class);
                Result result = new Result(paramsJson, null, response);
                result.setCode(response.getCode());
                if (response.getCode() == HttpStatus.SC_OK) {
                    result.setMsg("集合元素添加成功");
                } else if (response.getCode() == HttpStatus.SC_BAD_REQUEST) {
                    if (StringUtils.isNotBlank(response.getMsg()) && response.getMsg().contains("重复")) {
                        result.setCodeMsg(HttpStatus.SC_OK, response.getMsg());
                    }
                }
                return result;
            }
        } catch (Exception e) {
            logger.info("集合元素添加失败:" + e);
            Result result = new Result(HttpStatus.SC_BAD_REQUEST,"集合元素添加失败:("+e.getMessage()+")");
            result.setParam(paramsJson);
            return result;
        }
    }
}

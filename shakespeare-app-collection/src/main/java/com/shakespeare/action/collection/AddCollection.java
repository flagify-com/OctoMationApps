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
 * 添加集合
 * @author: hongrongxu
 * @date: 2021/5/7 上午10:59
 */
public class AddCollection extends AbstractAddCollectionAction {

    private static final SdkLogger logger = HoneyGuide.actionLog;

    @Override
    protected Result bussinessInvoke(JSONObject paramsJson, Map<String, Object> assetSettingJson) {
        CollectionParam param = null;
        try {
            param = validateParam(paramsJson);
        } catch (ParseException e) {
            logger.info("parse string to date failed");
            Result result = new Result(HttpStatus.SC_BAD_REQUEST,"集合添加失败:("+e.getMessage()+")");
            result.setParam(paramsJson);
            return result;
        }
        AppConfig config = validateConfig(assetSettingJson);
        String json = JSONObject.toJSONString(param);
        String url = config.getServerAddress() + Constant.ADD_COLLECTION_API;
        ResponseEntity<Integer> response;
        try {
            String requestResult = HttpClientUtils.doPostJson(url, json, config.getAppToken());
            logger.info("add collection request result = " + requestResult);
            if (StringUtils.isBlank(requestResult)) {
                Result result = new Result(HttpStatus.SC_BAD_REQUEST,"集合添加失败!");
                result.setParam(paramsJson);
                return result;
            } else {
                response = JSONObject.parseObject(requestResult, ResponseEntity.class);
                Result result = new Result(paramsJson, null, response);
                result.setCode(response.getCode());
                if (response.getCode() == HttpStatus.SC_OK) {
                    result.setMsg("集合添加成功");
                }
                return result;
            }
        } catch (Exception e) {
            logger.info("集合添加失败:" + e);
            Result result = new Result(HttpStatus.SC_BAD_REQUEST,"集合添加失败:("+e.getMessage()+")");
            result.setParam(paramsJson);
            return result;
        }
    }
}

package com.shakespeare.action.collection;

import com.alibaba.fastjson.JSONObject;
import com.shakespeare.action.Result;
import com.shakespeare.action.sdk.api.HoneyGuide;
import com.shakespeare.action.sdk.api.oparetor.SdkLogger;
import org.apache.commons.lang3.StringUtils;
import org.apache.http.HttpStatus;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.util.Map;

/**
 * 删除集合元素v2.0,直接调用条件删除接口,删除元素
 * @author hongrongxu
 */
public class DeleteCollectionElementV2 extends AbstractDeleteElementAction{

    private static final SdkLogger logger = HoneyGuide.actionLog;

    @Override
    protected Result bussinessInvoke(JSONObject paramsJson, Map<String, Object> assetSettingJson) {
        CollectionElementParam param = validateParam(paramsJson);
        AppConfig config = validateConfig(assetSettingJson);
        String json = JSONObject.toJSONString(param);
        String url = config.getServerAddress() + Constant.API_DELETE_COLLECTION_ELEMENT;
        try {
            String requestResult = HttpClientUtils.doPostJson(url, json, config.getAppToken());
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
                //所有的参照都返回code为200。具体错误通过response来展示
                result.setCode(HttpStatus.SC_OK);
                return result;
            }
        } catch (Exception e) {
            logger.info("集合元素删除失败:" + e);
            Result result = new Result(HttpStatus.SC_BAD_REQUEST,"集合元素删除失败:("+e.getMessage()+")");
            result.setParam(paramsJson);
            return result;
        }
    }
}

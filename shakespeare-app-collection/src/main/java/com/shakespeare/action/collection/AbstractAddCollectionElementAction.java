package com.shakespeare.action.collection;

import com.shakespeare.action.sdk.api.HoneyGuide;
import com.shakespeare.action.utils.Verifier;
import org.apache.commons.lang3.StringUtils;

import java.text.ParseException;
import java.util.Date;
import java.util.Map;

/**
 * @author: hongrongxu
 * @date: 2021/5/7 上午11:00
 */
public abstract class AbstractAddCollectionElementAction extends AbstractValidateAssertAction {

    protected CollectionElementParam validateParam(Map<String, Object> params) throws ParseException {
        Verifier verifier = Verifier.create();
        verifier.isNotNull(params, ErrorCode.NULL_ERROR.getMsg(), "params").throwIfError();
        verifier.isNotNull(params.get("collectionName"), ErrorCode.NULL_ERROR.getMsg(), "集合英文名").throwIfError();
        verifier.isNotNull(params.get("value"), ErrorCode.NULL_ERROR.getMsg(), "集合元素").throwIfError();
        String remark = params.get("remark") == null ? "" : params.get("remark").toString();
        String createdBy = HoneyGuide.context.executor();

        String effectiveTimeStr = params.get("effectiveTime") == null ? null : params.get("effectiveTime").toString();
        Date effectiveTime = DateUtils.str2date(effectiveTimeStr);
        String expireTimeStr = params.get("expireTime") == null ? null : params.get("expireTime").toString();
        Date expireTime = DateUtils.str2date(expireTimeStr);

        if (StringUtils.isBlank(createdBy)) {
            createdBy = Constant.ROBOT;
        }
        CollectionElementParam collectionElementParam = new CollectionElementParam((String) params.get("collectionName"),
                (String) params.get("value"), remark, createdBy, effectiveTime, expireTime);

        if (StringUtils.isBlank(collectionElementParam.getCollectionName())) {
            throw new IllegalArgumentException("集合英文名不能为空");
        }
        if (StringUtils.isBlank(collectionElementParam.getValue())) {
            throw new IllegalArgumentException("元素值不能为空");
        }
        return collectionElementParam;
    }
}

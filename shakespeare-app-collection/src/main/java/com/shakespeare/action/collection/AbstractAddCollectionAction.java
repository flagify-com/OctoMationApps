package com.shakespeare.action.collection;

import com.shakespeare.action.AbstractActionComponent;
import com.shakespeare.action.sdk.api.HoneyGuide;
import com.shakespeare.action.utils.Verifier;
import org.apache.commons.lang3.StringUtils;

import java.text.DateFormat;
import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.Map;

/**
 *  添加集合
 * @author: hongrongxu
 * @date: 2021/5/7 上午11:00
 */
public abstract class AbstractAddCollectionAction extends AbstractValidateAssertAction {

    protected CollectionParam validateParam(Map<String, Object> params) throws ParseException {
        Verifier verifier = Verifier.create();
        verifier.isNotNull(params, ErrorCode.NULL_ERROR.getMsg(), "params").throwIfError();
        verifier.isNotNull(params.get("name"), ErrorCode.NULL_ERROR.getMsg(), "集合名").throwIfError();
        verifier.isNotNull(params.get("cnName"), ErrorCode.NULL_ERROR.getMsg(), "集合中文名").throwIfError();
        Integer ttl = params.get("ttl") == null ? 315360000 : (Integer) params.get("ttl");
        String description = params.get("description") == null ? "" : params.get("description").toString();
        String effectiveTimeStr = params.get("effectiveTime") == null ? null : params.get("effectiveTime").toString();
        Date effectiveTime = DateUtils.str2date(effectiveTimeStr);
        CollectionParam collectionParam = new CollectionParam(params.get("name").toString(), (String) params.get("cnName"), description, ttl, effectiveTime);
        String createdBy = HoneyGuide.context.executor();
        if (StringUtils.isBlank(createdBy)) {
            createdBy = Constant.ROBOT;
        }
        collectionParam.setCreatedBy(createdBy);
        return collectionParam;
    }
}

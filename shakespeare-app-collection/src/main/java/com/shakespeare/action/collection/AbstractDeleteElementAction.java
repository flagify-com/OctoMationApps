package com.shakespeare.action.collection;

import com.shakespeare.action.utils.Verifier;
import org.apache.commons.lang3.StringUtils;

import java.util.Map;

/**
 * @author: hongrongxu
 * @date: 2021/5/7 上午11:00
 */
public abstract class AbstractDeleteElementAction extends AbstractValidateAssertAction {

    protected CollectionElementParam validateParam(Map<String, Object> params) {
        Verifier verifier = Verifier.create();
        verifier.isNotNull(params, ErrorCode.NULL_ERROR.getMsg(), "params").throwIfError();
        verifier.isNotNull(params.get("collectionName"), ErrorCode.NULL_ERROR.getMsg(), "集合名称").throwIfError();
        verifier.isNotNull(params.get("value"), ErrorCode.NULL_ERROR.getMsg(), "集合元素").throwIfError();
        CollectionElementParam collectionElementParam = new CollectionElementParam((String) params.get("collectionName"), (String) params.get("value"));
        if (StringUtils.isBlank(collectionElementParam.getCollectionName())) {
            throw new IllegalArgumentException("集合名称不能为空");
        }
        if (StringUtils.isBlank(collectionElementParam.getValue())) {
            throw new IllegalArgumentException("集合元素不能为空");
        }
        return collectionElementParam;
    }
}

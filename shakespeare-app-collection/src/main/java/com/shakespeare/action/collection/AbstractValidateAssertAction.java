package com.shakespeare.action.collection;

import com.shakespeare.action.AbstractActionComponent;
import com.shakespeare.action.utils.Verifier;

import java.util.Map;

/**
 * 资源校验，校验请求的资源token和serverAddress
 * @author: hongrongxu
 * @date: 2021/9/2 上午10:28
 */
public abstract class AbstractValidateAssertAction extends AbstractActionComponent {

    protected AppConfig validateConfig(Map<String, Object> assetConfigMap) {
        Verifier verifier = Verifier.create();
        verifier.isNotNull(assetConfigMap.get("appToken"), ErrorCode.NULL_ERROR.getMsg(), "appToken").throwIfError();
        verifier.isNotNull(assetConfigMap.get("serverAddress"), ErrorCode.NULL_ERROR.getMsg(), "server").throwIfError();
        AppConfig appConfig = new AppConfig(String.valueOf(assetConfigMap.get("appToken")), String.valueOf(assetConfigMap.get("serverAddress")));
        return appConfig;
    }
}

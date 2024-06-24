package com.shakespeare.action.collection;

/**
 * @author tracy01.wu
 * @create 2019/3/25
 */
public enum ErrorCode {
    NULL_ERROR("%s为空"),SYSTEM_ERROR("system error"),LOGON_ERROR("login fail");
    private String msg;
    private ErrorCode(String msg){
        this.msg = msg;
    }

    public String getMsg() {
        return msg;
    }
}

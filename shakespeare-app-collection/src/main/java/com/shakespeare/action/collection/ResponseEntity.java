package com.shakespeare.action.collection;

/**
 * @author: hongrongxu
 * @date: 2021/5/7 上午11:56
 */
public class ResponseEntity<T> {
    private T result;
    private Integer code;
    private String msg;

    public ResponseEntity() {
    }

    public ResponseEntity(T result, Integer code, String msg) {
        this.result = result;
        this.code = code;
        this.msg = msg;
    }

    public T getResult() {
        return result;
    }

    public void setResult(T result) {
        this.result = result;
    }

    public Integer getCode() {
        return code;
    }

    public void setCode(Integer code) {
        this.code = code;
    }

    public String getMsg() {
        return msg;
    }

    public void setMsg(String msg) {
        this.msg = msg;
    }
}

package com.shakespeare.action.collection;

/**
 * @author: hongrongxu
 * @date: 2021/5/7 下午4:58
 */
public class AppConfig {
    private String appToken;
    private String serverAddress;

    public AppConfig() {
    }

    public AppConfig(String appToken, String serverAddress) {
        this.appToken = appToken;
        this.serverAddress = serverAddress;
    }

    public String getAppToken() {
        return appToken;
    }

    public void setAppToken(String appToken) {
        this.appToken = appToken;
    }

    public String getServerAddress() {
        return serverAddress;
    }

    public void setServerAddress(String serverAddress) {
        this.serverAddress = serverAddress;
    }
}

package com.shakespeare.action.collection;

import com.fasterxml.jackson.annotation.JsonFormat;

import java.util.Date;

/**
 * 集合属性
 * @author: hongrongxu
 * @date: 2021/5/7 上午11:08
 */
public class CollectionParam {
    private String name;

    private String cnName;

    private String description;

    private Integer ttl;

    private String createdBy;

    @JsonFormat(pattern = "yyyy-MM-dd HH:mm:ss",timezone = "GMT+8")
    private Date effectiveTime;

    public CollectionParam() {
    }

    public CollectionParam(String name, String cnName, String description, Integer ttl) {
        this.name = name;
        this.cnName = cnName;
        this.description = description;
        this.ttl = ttl;
    }

    public CollectionParam(String name, String cnName, String description, Integer ttl, Date effectiveTime) {
        this.name = name;
        this.cnName = cnName;
        this.description = description;
        this.ttl = ttl;
        this.effectiveTime = effectiveTime;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public String getCnName() {
        return cnName;
    }

    public void setCnName(String cnName) {
        this.cnName = cnName;
    }

    public String getDescription() {
        return description;
    }

    public void setDescription(String description) {
        this.description = description;
    }

    public Integer getTtl() {
        return ttl;
    }

    public void setTtl(Integer ttl) {
        this.ttl = ttl;
    }

    public String getCreatedBy() {
        return createdBy;
    }

    public void setCreatedBy(String createdBy) {
        this.createdBy = createdBy;
    }

    public Date getEffectiveTime() {
        return effectiveTime;
    }

    public void setEffectiveTime(Date effectiveTime) {
        this.effectiveTime = effectiveTime;
    }
}

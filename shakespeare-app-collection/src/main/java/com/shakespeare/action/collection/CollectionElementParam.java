package com.shakespeare.action.collection;

import com.fasterxml.jackson.annotation.JsonFormat;

import java.util.Date;

/**
 * @author: hongrongxu
 * @date: 2021/5/7 上午11:08
 */
public class CollectionElementParam {
    private Long collectionId;
    private String collectionName;
    private String value;
    private String remark;
    private String createdBy;
    @JsonFormat(pattern = "yyyy-MM-dd HH:mm:ss",timezone = "GMT+8")
    private Date effectiveTime;
    @JsonFormat(pattern = "yyyy-MM-dd HH:mm:ss",timezone = "GMT+8")
    private Date expireTime;

    public CollectionElementParam() {
    }

    public String getCollectionName() {
        return collectionName;
    }

    public void setCollectionName(String collectionName) {
        this.collectionName = collectionName;
    }

    public String getValue() {
        return value;
    }

    public void setValue(String value) {
        this.value = value;
    }

    public String getRemark() {
        return remark;
    }

    public void setRemark(String remark) {
        this.remark = remark;
    }

    public CollectionElementParam(String collectionName, String value, String remark, String createdBy, Date effectiveTime, Date expireTime) {
        this.collectionName = collectionName;
        this.value = value;
        this.remark = remark;
        this.createdBy = createdBy;
        this.effectiveTime = effectiveTime;
        this.expireTime = expireTime;
    }

    public CollectionElementParam(Long collectionId, String value, String remark, String createdBy, Date effectiveTime, Date expireTime) {
        this.collectionId = collectionId;
        this.value = value;
        this.remark = remark;
        this.createdBy = createdBy;
        this.effectiveTime = effectiveTime;
        this.expireTime = expireTime;
    }

    public CollectionElementParam(String collectionName, String value) {
        this.collectionName = collectionName;
        this.value = value;
    }

    public CollectionElementParam(Long collectionId, String value) {
        this.collectionId = collectionId;
        this.value = value;
    }

    public String getCreatedBy() {
        return createdBy;
    }

    public void setCreatedBy(String createdBy) {
        this.createdBy = createdBy;
    }

    public Long getCollectionId() {
        return collectionId;
    }

    public void setCollectionId(Long collectionId) {
        this.collectionId = collectionId;
    }

    public Date getEffectiveTime() {
        return effectiveTime;
    }

    public void setEffectiveTime(Date effectiveTime) {
        this.effectiveTime = effectiveTime;
    }

    public Date getExpireTime() {
        return expireTime;
    }

    public void setExpireTime(Date expireTime) {
        this.expireTime = expireTime;
    }
}
